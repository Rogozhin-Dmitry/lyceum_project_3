from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, IntegerField, BooleanField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class FirstTestForm(FlaskForm):
    images = RadioField('style image.',
                        choices=[('value1', 'label1'), ('value2', 'label2')])
    submit = SubmitField('Submit')