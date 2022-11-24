from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from ..forms import RegisterForm, LoginForm
from ..models import User
from blog_website import db

authentication_pages = Blueprint("authentication_pages",
                                 __name__,
                                 static_folder="../static",
                                 template_folder="../templates")


@authentication_pages.route('/register', methods=["GET", "POST"])
def register():
    """ Registration form. """
    form = RegisterForm()
    if form.validate_on_submit():
        passed_email = form.email.data
        email_exists = User.query.filter_by(email=passed_email).first()
        if email_exists:
            flash("This email is already registered, try to log in.")
            return redirect(url_for('authentication_pages.login'))

        passed_name = form.name.data
        name_exists = User.query.filter_by(name=passed_name).first()
        if name_exists:
            flash("This name is already taken. Try another one.")
            return redirect(url_for('authentication_pages.register'))

        password = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8)

        new_entry = User(email=passed_email, name=passed_name, password=password)
        db.session.add(new_entry)
        db.session.commit()

        login_user(new_entry)

        return redirect(url_for("home_pages.get_all_posts"))

    return render_template("register.html", form=form)


@authentication_pages.route('/login', methods=["GET", "POST"])
def login():
    """ Login form. """
    form = LoginForm()
    if form.validate_on_submit():
        passed_email = form.email.data
        required_account = User.query.filter_by(email=passed_email).first()
        if required_account is not None:
            passed_password = form.password.data
            if check_password_hash(required_account.password, passed_password):
                remember_me = True if form.remember_me.data else False
                login_user(required_account, remember=remember_me)
                if "next" in request.url:
                    return redirect(request.args.get("next"))
                else:
                    return redirect(url_for("home_pages.get_all_posts"))
            else:
                flash("Invalid Password. Try again.")
        else:
            flash("We couldn't find the email you've entered. Please try again.")

    return render_template("login.html", form=form)


@authentication_pages.route('/logout')
def logout():
    """ Logout. """
    logout_user()
    return redirect(url_for('home_pages.get_all_posts'))
