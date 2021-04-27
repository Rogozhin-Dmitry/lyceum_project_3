from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired


class TestCreateForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    title_picture = FileField('Картинка')
    description = TextAreaField('Description')
    submit = SubmitField('Submit')
