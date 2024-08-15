import os
from flask import Flask, render_template, send_from_directory, url_for
# from forms import Register
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, IntegerField, validators, DateField, RadioField, SelectField
from flask_wtf.file import FileRequired, FileAllowed

app = Flask(__name__)
app.config['SECRET_KEY'] = 'B3NzaC1ycDAQABAAABAQCkPsx7jEchCJDX'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet('photos',IMAGES)
configure_uploads(app,photos)

class UploadForm(FlaskForm):
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

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'],filename)


@app.route('/register', methods=['GET','POST'])
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        profile_url = url_for('get_file',filename=filename)
        filename = photos.save(form.earphoto.data)
        ear_url = url_for('get_file',filename=filename)
        name = form.name.data
        fathername = form.fathername.data
        regno = form.regno.data
        dob = form.dob.data
        bloodgroup = form.bloodgroup.data
        print(fathername,name,regno,dob,bloodgroup)
    else:
        profile_url = None
        ear_url = None

    return render_template('signup.html',form=form, profile_url=profile_url, ear_url=ear_url)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
    