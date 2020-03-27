from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import HiddenField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import validators

class addPostForm(FlaskForm):
    post = StringField('post', validators = [validators.DataRequired()])
    submit = SubmitField('submit', [validators.DataRequired()])

class editPostForm(FlaskForm):
    post = StringField('post', validators = [validators.DataRequired()])
    post_id = HiddenField('post_id')
    submit = SubmitField('submit', [validators.DataRequired()])

class loginForm(FlaskForm):
    username = StringField('username', validators = [validators.DataRequired()])
    password = PasswordField('password', validators =[validators.DataRequired()])
    submit = SubmitField('submit', [validators.DataRequired()])

class registrationForm(FlaskForm):
    username = StringField('username', validators = [validators.DataRequired()])
    password = PasswordField('password', validators = [validators.DataRequired()])
    password2 = PasswordField('password2', validators = [validators.DataRequired(),
            validators.EqualTo('password', message='Passwords must match')])
    submit = SubmitField('submit', [validators.DataRequired()])

