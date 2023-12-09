from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = StringField('Text', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    submit = StringField('Submit')