
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
from flasku.config import Config

load_dotenv()  # This loads variables from .env into environment






db = SQLAlchemy()
bcrypt=Bcrypt()
login_manager=LoginManager()
login_manager.login_view='users.login'
login_manager.login_message_category='info'


mail =Mail()
from flasku.users.routes import users
from flasku.posts.routes import posts
from flasku.main.routes import main

def create_app(config_class=Config):
    app = Flask(__name__) #creating the Flask class object   
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    from flasku.users.routes import users
    from flasku.posts.routes import posts
    from flasku.main.routes import main
    from flasku.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
