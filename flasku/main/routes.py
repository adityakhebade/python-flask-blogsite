from flask import render_template, request, Blueprint
from flasku.models import Post

main=Blueprint('main',__name__)

@main.route('/') 
@main.route('/home') #decorator drfines the   
def home():  
    page =request.args.get('page',1,type=int)#user can only request page with int type and default will be 1
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)#we will paginate the page in which only 2 blogs per page and query is order by dated posted in descending order
    return render_template('home.html',posts=posts)
  
@main.route("/about")  
def about():  
    return render_template('about.html')  



    
