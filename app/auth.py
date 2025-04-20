from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from .forms import LoginForm
from .models import User
from . import login_manager

auth_bp = Blueprint('auth', __name__, url_prefix='/admin')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))  # ⛳️ Make sure this route exists!
        flash('Invalid credentials')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))