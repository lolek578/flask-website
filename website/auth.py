import self as self
from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
import flask_bcrypt

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@auth.route('/logout')
def logout():
    return '<p>logout</p>'


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if '@' not in email:
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
            flash('Account created!', category="success")
            return redirect(url_for('views.home'))

    return render_template('sign_up.html')





