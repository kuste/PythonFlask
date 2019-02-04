from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from myapp.models import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min = 2,  max = 20)])
    email = StringField('E-mail', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords do not match.')])
    submit = SubmitField('Register')

    def validate_username(self, username):
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('That username is allready taken.')
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is allready taken.')

class LoginForm(FlaskForm):
    email = TextField('E-mail', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class UpdateAccountForm(FlaskForm):
        username = StringField('Username', validators = [DataRequired(), Length(min = 2,  max = 20)])
        email = StringField('Email', validators = [DataRequired(), Email()])
        picture  = FileField('Update Profile Ficture', validators = [FileAllowed(['jpeg','jpg','png'])])
        submit = SubmitField('Update')

        def validate_username(self, username):
            if username.data != current_user.username:
                user = User.query.filter_by(username = username.data).first()
                if user:
                    raise ValidationError('That username is allready taken.')
        def validate_email(self, email):
            if email.data != current_user.email:
                user = User.query.filter_by(email = email.data).first()
                if user:
                    raise ValidationError('That email is allready taken.')
