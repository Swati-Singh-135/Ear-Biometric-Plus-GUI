import os
from flask import Flask, render_template, send_from_directory, url_for
from forms import RegForm
from flask_uploads import UploadSet, IMAGES, configure_uploads



app = Flask(__name__)
app.config['SECRET_KEY'] = 'B3NzaC1ycDAQABAAABAQCkPsx7jEchCJDX'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet('photos',IMAGES)
configure_uploads(app,photos)


@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'],filename)


@app.route('/register', methods=['GET','POST'])
def upload_image():
    form = RegForm()
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
        print(name,regno,fathername,dob,bloodgroup)
    else:
        profile_url = None
        ear_url = None

    return render_template('registration.html',form=form, profile_url=profile_url, ear_url=ear_url)

if __name__ == '__main__':
    app.run(port=3000, debug=True)