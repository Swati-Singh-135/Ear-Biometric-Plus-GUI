from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField

class Register(FlaskForm):
    faceImage = FileField(
        validators=[
            FileAllowed()
        ]
    )
    earImage = PasswordField('Ear Image')
    name = StringField('Name')
    submit = SubmitField('Sign up')