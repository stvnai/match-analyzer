from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):

    username= StringField(
        "username",
        validators= [
            InputRequired(),
            Length(max=75)
        ]
    )

    password= PasswordField(
        "password",
        validators= [
            InputRequired(),
            Length(max=75)
        ]
    )

    submit_user= SubmitField("Sign In")

class LogOutForm(FlaskForm):
    submit= SubmitField("Log Out")

