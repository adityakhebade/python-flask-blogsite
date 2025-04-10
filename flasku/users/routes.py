from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flasku import db, bcrypt
from flasku.models import User, Post
from flasku.users.forms import (Registration, Loginform, UpdateAccountform,RequestResetform, ResetPasswordform)
from flasku.users.utils import save_pictures, send_reset_email

users=Blueprint('users',__name__)

@users.route("/register",methods=['GET','POST'])  
def register():  
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=Registration()  
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')#we have to decode the password
        new_user=User(username=form.username.data,email=form.email.data,password=hashed_password)#we have to create a new user and pass the data to the database 
        db.session.add(new_user)#we have to add the new user to the database
        db.session.commit()#we have to commit the changes to the database
        flash(f"your account has been created succesfully ",'success')
        return redirect(url_for('users.login'))
    return render_template('register.html',title='register',form=form)      


@users.route("/login",methods=['GET','POST'])  
def login():  
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=Loginform()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Unsuccesful login",'danger')
    return render_template('login.html',title='Login',form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form=UpdateAccountform()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_pictures(form.picture.data)
            current_user.image_file = picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('your account has succesfully updated','success')
        return redirect(url_for('users.account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email 
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Account', image_file=image_file,form=form)

#route for particular user in link
@users.route("/user/<string:username>")    
def user_posts(username):  
    page =request.args.get('page',1,type=int) #request.args.get('page'): fetches the value of page from the query string.1:default value,if no page is specified.type=int: ensures the page number is converted to an integer
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)#filter_by(author=user): filters the Post table to only posts where the author is the selected user
    return render_template('user_post.html',posts=posts,user=user)

@users.route('/reset_password',methods=['GET','POST']) #this is route for requesting to reset  password
def reset_request():
        if current_user.is_authenticated:# if user is authenticated  
            return redirect(url_for('main.home'))# return to home
        form =RequestResetform()
        if form.validate_on_submit(): #If the request is a POST AND the form passed all validations (e.g., email is required and valid format
            user =User.query.filter_by(email=form.email.data).first()#This looks in the database for a user with the submitted email.
            send_reset_email(user)
            flash('an email has sent with instruction to reset the password','info')
            return redirect(url_for('users.login'))
        return render_template('reset_request.html',title = 'Reset password',form =form)

@users.route('/reset_password/<token>',methods=['GET','POST']) #this is route for resting password
def reset_token(token):
        if current_user.is_authenticated:# if user is authenticated  
            return redirect(url_for('main.home'))# return to home
        user =User.verify_reset_token(token) #.verify_reset_token(token)-This is a class method defined inside the User class that:Takes in a token (usually a time-sensitive token sent via email).
        if user is None:
            flash('this is an inavlid or expired token','warning')
            return redirect(url_for('users.reset_request'))
        form= ResetPasswordform()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password=hashed_password
            db.session.commit()#we have to commit the changes to the database
            flash(f"your password has been update.You are now able to login ",'success')
            return redirect(url_for('users.login'))
        return render_template('reset_token.html',title = 'Reset password',form =form)
