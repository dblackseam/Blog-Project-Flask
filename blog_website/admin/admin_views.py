from flask import Blueprint, redirect, url_for, flash, render_template
from ..models import BlogPost
from ..forms import CreatePostForm
from ..decorators import admin_only
from flask_login import current_user
from datetime import date
from blog_website import db

admin_functionality = Blueprint(
    "admin_functionality",
    __name__,
    template_folder="../templates",
    static_folder="../static"
)


@admin_functionality.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    """ Add new post functionality. """
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
            return redirect(url_for("home_pages.get_all_posts"))
        else:
            flash("To post something you need to have a permission.")
            return redirect(url_for("authentication_functionality.login"))
    return render_template("make-post.html", form=form)


@admin_functionality.route("/edit-post/<int:post_id>", methods=["POST", "GET"])
@admin_only
def edit_post(post_id):
    """ Edit post functionality. """
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
                return redirect(url_for("posts_pages.show_post", post_id=post_id))
        else:
            flash("You don't have a permission for that.")
            return redirect(url_for("posts_pages.show_post", post_id=post_id))
    else:
        flash("To edit this post, you need to log in into the related account.")
        return redirect(url_for("authentication_functionality.login"))

    return render_template("make-post.html", form=edit_form)


@admin_functionality.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    """ Delete post functionality. """
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home_pages.get_all_posts'))
