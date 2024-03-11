from flask import Blueprint, render_template, request, redirect, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user
from exotic_builds_garage.models import User, db
from exotic_builds_garage.forms import RegisterForm, LoginForm

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    registerform = RegisterForm()

    if request.method == 'POST' and registerform.validate_on_submit():
        first_name = registerform.first_name.data
        last_name = registerform.last_name.data
        username = registerform.username.data
        email = registerform.email.data
        password = registerform.password.data

        if User.query.filter(User.username == username).first():
            flash(f"Username {username} already exists. Please Try Again!", category='warning')
            return redirect('/signup')
        if User.query.filter(User.email == email).first():
            flash(f"Email {email} already exists. Please Try Again!", category='warning')
            return redirect('/signup')

        user = User(username, email, password, first_name, last_name)

        db.session.add(user)
        db.session.commit()

        flash(f"You have successfully registered user {username}", category='success')
        return redirect('/signin')

    return render_template('sign_up.html', form=registerform)

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    loginform = LoginForm()

    if request.method == 'POST' and loginform.validate_on_submit():
        email = loginform.email.data
        password = loginform.password.data

        user = User.query.filter(User.email == email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f"{email} Signed In", category='success')
            return redirect('/')
        else:
            flash("Invalid Email and/or Password, Please Try Again!", category='warning')
            return redirect('/signin')

    return render_template('sign_in.html', form=loginform)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/')
