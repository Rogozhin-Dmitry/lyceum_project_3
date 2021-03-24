from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, IntegerField, BooleanField, RadioField, \
    SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class TestForm(FlaskForm):
    languages = SelectField('Язык',
                         validators=[DataRequired()])
    submit = SubmitField('Submit')
