from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL1", 'sqlite:///blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate = Migrate(app, db, render_as_batch=True)
gravatar = Gravatar(app, size=100)

# CONNECT TO AUTHORIZATION FUNCTIONALITY
manager = LoginManager()
manager.init_app(app)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.id == 1:
            return func(*args, **kwargs)
        else:
            return abort(403)

    return wrapper


# CONFIGURE TABLES

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users_data.id"))
    user = db.relationship("User", back_populates="posts")
    comments = db.relationship("Comment", back_populates="post")


class User(UserMixin, db.Model):
    __tablename__ = "users_data"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    posts = db.relationship("BlogPost", back_populates="user")
    comments = db.relationship("Comment", back_populates="user")


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users_data.id"))
    user = db.relationship("User", back_populates="comments")
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    post = db.relationship("BlogPost", back_populates="comments")


# db.create_all()

## CONFIGURE FORMS


@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        passed_email = form.email.data
        email_exists = User.query.filter_by(email=passed_email).first()
        if email_exists:
            flash("This email is already registered, try to log in.")
            return redirect(url_for('login'))

        passed_name = form.name.data
        name_exists = User.query.filter_by(name=passed_name).first()
        if name_exists:
            flash("This name is already taken. Try another one.")
            return redirect(url_for('register'))

        password = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8)

        new_entry = User(email=passed_email, name=passed_name, password=password)
        db.session.add(new_entry)
        db.session.commit()

        login_user(new_entry)

        return redirect(url_for("get_all_posts"))

    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        passed_email = form.email.data
        required_account = User.query.filter_by(email=passed_email).first()
        if required_account is not None:
            passed_password = form.password.data
            if check_password_hash(required_account.password, passed_password):
                login_user(required_account)
                return redirect(url_for("get_all_posts"))
            else:
                flash("Invalid Password. Try again.")
        else:
            flash("We couldn't find the email you've entered. Please try again.")

    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    form = CommentForm()
    requested_post = BlogPost.query.get(post_id)
    if form.validate_on_submit():
        if current_user.is_authenticated:
            written_comment = form.comment.data
            new_comment = Comment(text=written_comment, post_id=requested_post.id, user_id=current_user.id)
            db.session.add(new_comment)
            db.session.commit()
        else:
            flash("To post your comment, you need to log in or register.")
            return redirect(url_for("login"))
    return render_template("post.html", post=requested_post, form=form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        if current_user.is_authenticated and current_user.id == 1:
            new_post = BlogPost(
                title=form.title.data,
                subtitle=form.subtitle.data,
                body=form.body.data,
                img_url=form.img_url.data,
                user_id=current_user.id,
                date=date.today().strftime("%B %d, %Y")
            )
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for("get_all_posts"))
        else:
            flash("To post something you need to have a permission.")
            return redirect(url_for("login"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["POST", "GET"])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    if current_user.is_authenticated:
        if current_user.id == 1:
            edit_form = CreatePostForm(
                title=post.title,
                subtitle=post.subtitle,
                img_url=post.img_url,
                body=post.body
            )
            if edit_form.validate_on_submit():
                post.title = edit_form.title.data
                post.subtitle = edit_form.subtitle.data
                post.img_url = edit_form.img_url.data
                post.body = edit_form.body.data
                db.session.commit()
                return redirect(url_for("show_post", post_id=post_id))
        else:
            flash("You don't have a permission for that.")
            return redirect(url_for("show_post", post_id=post_id))
    else:
        flash("To edit this post, you need to log in into the related account.")
        return redirect(url_for("login"))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(debug=True)
