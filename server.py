import os
import pymongo
from flask import Flask, render_template, send_from_directory, url_for
from forms import RegForm, AuthForm
from flask_uploads import UploadSet, IMAGES, configure_uploads
import sys
sys.path.append('D:\\Project\\BE project\\BE Project Code\\Main\\projectMainDirectory')
from quickRun import getFvAndShape
from earCompare import compareEar
def findPerson(fv):
    for item in collection.find():
        if compareEar(fv,item['fv'],a=0.1)>85:
            return item
    return -1



app = Flask(__name__)
app.config['SECRET_KEY'] = 'B3NzaC1ycDAQABAAABAQCkPsx7jEchCJDX'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet('photos',IMAGES)
configure_uploads(app,photos)

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client['earBiometricDatabase']
collection = db['earCollection']

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'],filename)


@app.route('/register', methods=['GET','POST'])
def register():
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
        print(type(dob))
        print(ear_url)
        try:
            ear = getFvAndShape('./'+ear_url)
            print(ear)
            collection.insert_one({
                'name':name,
                'id':regno,
                'profileImg': profile_url,
                'fatherName':fathername,
                'dob': dob.strftime("%d/%m/%Y"),
                'bloodgroup':bloodgroup,
                'fv': ear['fv']
            })
            return render_template('registration.html',form=form, profile_url=profile_url, ear_url=ear_url,isRegister=True)
        except:
            print("Anonymous Ear Image")
            form.earphoto.errors.append("Not able to scan ear properly. Try again with other image.")
    else:
        profile_url = None
        ear_url = None

    return render_template('registration.html',form=form, profile_url=profile_url, ear_url=ear_url,isRegister=False)

@app.route('/authenticate', methods=['GET','POST'])
def authenticate():
    form = AuthForm()
    ear=None
    if form.validate_on_submit():
        filename = photos.save(form.earphoto.data)
        # print('upload/'+filename)
        
        try:
            ear = getFvAndShape('uploads/'+filename)    
            return render_template('auth.html',form=form, ear=ear)
        except:
            print("Anonymous Ear Image")
            form.earphoto.errors.append("Not able to scan ear properly. Try again with other image.")

    return render_template('auth.html',form=form, ear=ear)

if __name__ == '__main__':
    # collection.insert_one({'name':'prasant','marks':100})
    app.run(port=3000, debug=True)