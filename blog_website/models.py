from blog_website import db, manager
from flask_login import UserMixin


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


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

    def __repr__(self):
        return f"{self.title}"


class User(UserMixin, db.Model):
    __tablename__ = "users_data"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    posts = db.relationship("BlogPost", back_populates="user")
    comments = db.relationship("Comment", back_populates="user")

    def __repr__(self):
        return f"{self.name}"


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users_data.id"))
    user = db.relationship("User", back_populates="comments")
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    post = db.relationship("BlogPost", back_populates="comments")

    def __repr__(self):
        return f"post: {self.post} -> user_comment: {self.user}"
