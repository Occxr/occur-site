from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Optional
from wtforms import EmailField


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = EmailField('Email (optional)', validators=[Optional()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Sign Up')


class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add Product')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')