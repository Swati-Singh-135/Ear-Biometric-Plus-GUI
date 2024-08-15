import os
import pymongo
import time
from flask import Flask, render_template, send_from_directory, url_for
import cv2
from forms import RegForm, AuthForm
from flask_uploads import UploadSet, IMAGES, configure_uploads
import sys
sys.path.append('D:\\Project\\BE project\\BE Project Code\\Main\\projectMainDirectory')
from quickRun import getFvAndShape, getEarCannyAndGaussImg
from facedetect import extractFace
from earCompare import compareEar
def findPerson(fv):
    for item in collection.find():
        accuracy = compareEar(fv,item['fv'],a=0.1)
        if accuracy>85:
            return [accuracy, item]
    return None



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

        img = cv2.imread('./'+profile_url)
        print(img.shape)
        face = extractFace(img,600)
        cv2.imwrite('./'+profile_url,face)

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
            start = time.time()
            ear = getFvAndShape('./'+ear_url)
            end = time.time()
            timetook = round((end-start)/4,3)
            info = getEarCannyAndGaussImg('./'+ear_url,600,9)
            cv2.imwrite('uploads/canny.jpg',info['canny'])
            cv2.imwrite('uploads/gauss.jpg',info['gaussian'])
            print(ear)
            profile = {
                'name':name,
                'id':regno,
                'profileImg': profile_url,
                'fatherName':fathername,
                'dob': dob.strftime("%d/%m/%Y"),
                'bloodGroup':bloodgroup,
                'fv': ear['fv'],
                'shape':ear['shape']
            }
            collection.insert_one(profile)
            prompt = "Registration Successfull"
            print(prompt)
            # return render_template('registration.html',form=form, profile_url=profile_url, ear_url=ear_url,isRegister=True)
            return render_template('profile.html', profile=profile, images=['uploads/'+filename,'uploads/gauss.jpg','uploads/canny.jpg'], ear=ear, prompt=prompt, values = [None,timetook], databasetype="0")
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
    if form.validate_on_submit():
        filename = photos.save(form.earphoto.data)
        databasetype = form.databasetype.data
        print(databasetype,type(databasetype))
        # print('upload/'+filename)
        
        try:
            start = time.time()
            ear = getFvAndShape('uploads/'+filename)
            end = time.time()
            timetook = round((end-start)/4,3)
            print("Time took:",end-start)
            info = getEarCannyAndGaussImg('uploads/'+filename,600,9)
            cv2.imwrite('uploads/canny.jpg',info['canny'])
            cv2.imwrite('uploads/gauss.jpg',info['gaussian'])
            # print(ear)
            accuracy, profile = findPerson(ear['fv'])
            print("accuracy: ",accuracy)
            # print("profile", profile) 
            prompt = ""
            if(profile):
                prompt = "Match Found"
            else:
                prompt = "Match Not Found"
            return render_template('profile.html', profile=profile, images=['uploads/'+filename,'uploads/gauss.jpg','uploads/canny.jpg'], ear=ear, prompt=prompt, values=[accuracy, timetook], databasetype=databasetype)
        except:
            print("Anonymous Ear Image")
            form.earphoto.errors.append("Not able to scan ear properly. Try again with other image.")

    return render_template('auth.html',form=form)

if __name__ == '__main__':
    # collection.insert_one({'name':'prasant','marks':100})
    app.run(port=3000, debug=True)