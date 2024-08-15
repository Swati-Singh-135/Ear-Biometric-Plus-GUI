from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, IntegerField, validators, DateField, RadioField, SelectField
from flask_wtf.file import FileRequired, FileAllowed
from flask_uploads import UploadSet, IMAGES


photos = UploadSet('photos',IMAGES)


class RegForm(FlaskForm):
    photo = FileField(
        label="Profile Image",
        validators=[
            FileAllowed(photos,'Only images are allowed'),
            FileRequired('Profile Image Field should not be empty')
        ]
    )
    earphoto = FileField(
        label="Ear Image",
        validators=[
            FileAllowed(photos,'Only images are allowed'),
            FileRequired('Ear Image Field should not be empty')
        ]
    )
    name = StringField(
        label="Name",
        validators=[
            validators.InputRequired('Please enter the name')
        ]
    )
    regno = IntegerField(
        validators=[
            validators.InputRequired('Please enter the registration number')
        ]
    )
    fathername = StringField(
        label="Father Name",
        validators=[
            validators.InputRequired('Please enter the father\'s name')
        ]
    )
    dob = DateField(
        label="DOB",
        validators=[
            validators.InputRequired('Please enter the date of birth')
        ]
    )
    bloodgroup = StringField(
        label="Blood Group",
        validators=[
            validators.InputRequired('Please enter the blood group')
        ]
    )
    submit = SubmitField('Submit')

class AuthForm(FlaskForm):

    earphoto = FileField(
        label="Ear Image",
        validators=[
            FileAllowed(photos,'Only images are allowed'),
            FileRequired('Ear Image Field should not be empty')
        ]
    )

    databasetype = RadioField('database', choices = [(0,'Combined Database'), (1,'Distributed Database')], default=0)

    submit = SubmitField('Submit')

class MultimodeForm(FlaskForm):

    earphoto = FileField(
        label="Ear Image",
        validators=[
            FileAllowed(photos,'Only images are allowed'),
        ]
    )

    photo = FileField(
        label="Face Image",
        validators=[
            FileAllowed(photos,'Only images are allowed'),
        ]
    )

    databasetype = RadioField('database', choices = [(0,'Combined Database'), (1,'Distributed Database')], default=0)

    submit = SubmitField('Submit')
