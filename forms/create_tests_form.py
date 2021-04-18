from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, IntegerField, BooleanField, RadioField, \
    SelectField, FileField, FieldList, FormField
from wtforms.validators import DataRequired


class PictureSlot(FlaskForm):
    slot = FileField()


class WordSlot(FlaskForm):
    slot = StringField()


class FirstTestCreateForm(FlaskForm):
    right_image_choosing = RadioField()
    question = StringField()
    images = FieldList(FormField(PictureSlot), min_entries=2)
    right = SubmitField('Right')
    left = SubmitField('Left')
    submit = SubmitField('Submit')


class SecondTestCreateForm(FlaskForm):
    first_sentence = StringField()
    second_sentence = StringField()
    right_word_choosing = RadioField(validators=[DataRequired()])
    words = FieldList(FormField(WordSlot), min_entries=2)
    right = SubmitField('Right')
    left = SubmitField('Left')
    submit = SubmitField('Submit')


class TestCreateForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    title_picture = FileField('Картинка')
    description = TextAreaField('Description')
    submit = SubmitField('Submit')


class NewTestForm(FlaskForm):
    right_image_choosing = RadioField()
    question = StringField()
    images = FieldList(FormField(PictureSlot), min_entries=2)
    right = SubmitField('Right')
    left = SubmitField('Left')
    submit = SubmitField('Submit')
