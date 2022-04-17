from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, length, EqualTo
from flask_ckeditor import CKEditorField
from wtforms.fields.html5 import EmailField


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class RegisterForm(FlaskForm):
    email = EmailField("Your Email", validators=[DataRequired()])
    name = StringField("Your Name", validators=[DataRequired()])
    password = PasswordField("Your Password", validators=[DataRequired(),
                                                          length(6, 20),
                                                          EqualTo('password_check', message="Passwords must match")])
    password_check = PasswordField("Repeat Your Password", validators=[DataRequired(), length(6, 20)])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    email = EmailField("Your Email", validators=[DataRequired()])
    password = PasswordField("Your Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CommentForm(FlaskForm):
    comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit comment")
