from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import login_required, current_user
from ..forms import CommentForm
from ..models import BlogPost, Comment
from blog_website import db

posts_pages = Blueprint("posts_pages",
                        __name__,
                        static_folder="../static",
                        template_folder="../templates")


@posts_pages.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def show_post(post_id):
    """ Page to show clicked post's inners. """
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
            return redirect(url_for("authentication_pages.login"))
    return render_template("post.html", post=requested_post, form=form)
