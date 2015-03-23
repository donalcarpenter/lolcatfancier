from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import  DataRequired, Length, ValidationError
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed

__author__ = 'Donal_Carpenter'

class LolCatUploadForm(Form):
    id = HiddenField("_id")
    title = StringField("Title", validators=[DataRequired(), Length(min=4, max=20)])
    blurb = TextAreaField("Blurb", validators=[DataRequired(), Length(max=200)])
    source = StringField("Source")
    image_data = FileField("Image", validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg', 'please only upload images'])])

    def validate_image(self, field):
        if(len(self.id.data)==0 and len(field.data) == 0):
            raise ValidationError('image must be provided for new lolcat uploads')

class CommentForm(Form):
    author = StringField("your name")
    comment = TextAreaField("comment", validators=[DataRequired()])