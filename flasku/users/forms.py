from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flasku.models import User



class Registration(FlaskForm):
    username= StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Signup')
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('that username already exists','danger')
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('that email already exists','danger')

class Loginform(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired()])
    remember =BooleanField('Remember me')
    submit=SubmitField('Login')
class UpdateAccountform(FlaskForm):
    username= StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    picture= FileField('Update profile picture',validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('update')
    def validate_username(self,username):
        if username.data!=current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('that username already exists','danger')
    def validate_email(self,email):
        if email.data!=current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('that email already exists','danger')

class RequestResetform(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('request password reset')
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with this email.please make a new one")
class ResetPasswordform(FlaskForm):
    password = PasswordField('password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField(' reset password')
