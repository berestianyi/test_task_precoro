from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, Email


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=128)])
    password2 = PasswordField("Repeat password", validators=[DataRequired(), EqualTo("password")])


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
