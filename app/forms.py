from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    username = StringField("Username or Email", 
        validators=[DataRequired()
    ])

    password = PasswordField("Password", 
        validators=[DataRequired()
    ])

    submit = SubmitField("Go")


class SignupForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=3, max=20, message="Username must be between 3 and 20 characters long!")
    ])

    email = EmailField("Email", validators=[
        DataRequired(),
        Email(message="Email must be valid!")
    ])

    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long!")
    ])

    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(),
        EqualTo("password", message="Passwords must match!")
    ])

    submit = SubmitField("Create Account")