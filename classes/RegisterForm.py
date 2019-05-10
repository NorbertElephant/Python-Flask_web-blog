from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

class RegisterForm(FlaskForm):
    name = StringField('Name', validators= [Length(min=1, max=50)] )
    username = StringField('Username',validators =[Length(min=1, max=25)] )
    email = StringField('Email', validators=[Length(min=1,max=50)] )
    password = PasswordField('Password',
        validators= [
            DataRequired(),
            EqualTo('confirm', message="Passwords do not match ")
    ])
    confirm = PasswordField('Confirm Password')
