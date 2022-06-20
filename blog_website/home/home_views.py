from flask import Blueprint, render_template, redirect
from ..models import BlogPost

home_pages = Blueprint(
    "home_pages",
    __name__,
    template_folder="../templates",
    static_folder="../static"
)


@home_pages.route('/')
def get_all_posts():
    """Home page."""
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@home_pages.route("/about")
def about():
    """About page."""
    return render_template("about.html")


@home_pages.route("/contact")
def contact():
    """Contact page."""
    return render_template("contact.html")
