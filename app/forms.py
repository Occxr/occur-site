from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Optional


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    email = StringField('Email (optional)', validators=[Optional(), Email()])
    submit = SubmitField('Sign Up')


class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add Product')