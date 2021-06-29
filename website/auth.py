import self as self
from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
import flask_bcrypt
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            #first is password from db, second from form
            if flask_bcrypt.check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Try again!', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category="error")
        elif '@' not in email:
            flash('Wrong email', category="error")
        elif len(firstName) < 2:
            flash('Wrong first name', category="error")
        elif password1 != password2:
            flash('Wrong password', category="error")
        elif len(password1) < 10:
            flash('Wrong password', category="error")
        else:
            new_user = User(email=email, firstName=firstName, password=flask_bcrypt.generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created!', category="success")
            return redirect(url_for('views.home'))

    return render_template('sign_up.html')





