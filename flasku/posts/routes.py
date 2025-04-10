from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flasku import db
from flasku.models import Post
from flasku.posts.forms import PostForm

posts=Blueprint('posts',__name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('your post has been created','success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html',title ='New post',form=form,legend='new_post')
@posts.route("/post/<int:post_id>")#for each post specific id will be provided in int
def post(post_id):
    post=Post.query.get_or_404(post_id)#
    return render_template('post.html',title=post.title,post=post)

@posts.route("/post/<int:post_id>/update",methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!= current_user:#if current user loged in did not make the blog he cannot update it 
        abort(403)#it will throw error
    form=PostForm()
    if form.validate_on_submit():#if it validates then then entered data will be saved in post title and content and in db
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your post has been successfully updated','success')
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method=='GET':
        form.title.data=post.title # to add current data to title and content page when user try to update
        form.content.data=post.content
    return render_template('create_post.html',title='Update Post',form=form,legend='Update Post')

@posts.route("/post/<int:post_id>/delete",methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!= current_user:#if current user loged in did not make the blog he cannot update it 
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been successfully deleted','success')
    return redirect(url_for('main.home'))