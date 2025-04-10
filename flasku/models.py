from flasku import db,login_manager
from flask import current_app
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))





class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
   
    def get_reset_token(self):# were passing the instance through self and expire sec which is 1800 or 30 minutes
        s =Serializer(current_app.config['SECRET_KEY']) # Serializer uses a secret key and expiration time to securely sign data (in this case, the user_id) and turn it into a token string.
        return s.dumps({'user_id':self.id})# now we will dump the s which has secret key to decode the user_id which is self 
    @staticmethod # No need to create an instance
    def verify_reset_token(token,expires_sec=1800):
        s =Serializer(current_app.config['SECRET_KEY'])
        try:  
            user_id= s.loads(token,max_age=expires_sec)['user_id']# if userid load token then we will return the user.query 
        except:
            None# if time fails or any toher issue none will be retrurned
        return User.query.get(user_id)

            
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"