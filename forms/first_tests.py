from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField


class FirstTestForm(FlaskForm):
    images = RadioField('style image')
    submit = SubmitField('Submit')