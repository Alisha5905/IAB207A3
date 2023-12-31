from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
# new imports:
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User, Event
from . import db

# create a blueprint
authbp = Blueprint('auth', __name__)


@authbp.route('/register', methods=['GET', 'POST'])
def register():
    genres = db.session.scalars(db.select(Event.genre.distinct())).all()
    register = RegisterForm()
    # the validation of form is fine, HTTP request is POST
    if (register.validate_on_submit() == True):
        # get username, password and email from the form
        uname = register.user_name.data
        pwd = register.password.data
        email = register.email_id.data
        contact_number = register.contact_number.data
        address = register.address.data
        # check if a user exists
        user = db.session.scalar(db.select(User).where(User.name == uname))
        if user:  # this returns true when user is not None
            flash('Username already exists, please try another')
            return redirect(url_for('auth.register', **request.args))
        # don't store the password in plaintext!
        pwd_hash = generate_password_hash(pwd)
        # create a new User model object
        new_user = User(name=uname, password_hash=pwd_hash, email=email,
                        contact_number=contact_number, address=address)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        # commit to the database and redirect to HTML page
        if 'next' in request.args:
            if request.args['next'] is not '':
                return redirect(request.args['next'])
        return redirect(url_for('main.index'))
    # the else is called when the HTTP request calling this page is a GET
    else:
        return render_template('user.html', form=register, heading='Register', genres=genres, selected_genre='Select')


@authbp.route('/login', methods=['GET', 'POST'])
def login():
    genres = db.session.scalars(db.select(Event.genre.distinct())).all()
    login_form = LoginForm()
    error = None
    if (login_form.validate_on_submit() == True):
        # get the username and password from the database
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.name == user_name))
        # if there is no user with that name
        if user is None:
            error = 'Incorrect username'  # could be a security risk to give this much info away
        # check the password - notice password hash function
        # takes the hash and password
        elif not check_password_hash(user.password_hash, password):
            error = 'Incorrect password'
        if error is None:
            # all good, set the login_user of flask_login to manage the user
            login_user(user)
            if 'next' in request.args:
                if request.args['next'] is not '':
                    return redirect(request.args['next'])
            return redirect(url_for('main.index'))
        else:
            flash(error,'error')
    return render_template('user.html', form=login_form, heading='Login', genres=genres, selected_genre='Select')


@authbp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
