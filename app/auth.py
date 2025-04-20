from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user
from .forms import SignupForm, LoginForm
from .models import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose another one.')
            return redirect(url_for('auth.register'))
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('✅ Account created. Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f"Welcome back, {user.username}!")
            return redirect(url_for('main.dashboard' if user.is_admin else 'main.home'))
        else:
            flash('❌ Invalid username or password.')
    return render_template('login.html', form=form)