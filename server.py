import os
import pymongo
import time
from flask import Flask, render_template, send_from_directory, url_for
import cv2
import face_recognition
import numpy as np
from forms import RegForm, AuthForm, MultimodeForm
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
    return [None,None]

def findPersonByFace(encoding):
    print(encoding.shape)
    for item in collection.find():
        encoding2 = np.asarray(item['encoding'],dtype=np.float64)
        if face_recognition.compare_faces([encoding],encoding2)[0]:
            return [0.0, item]
    return [None, None]



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


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        error = False
        filename = photos.save(form.photo.data)
        profile_url = url_for('get_file',filename=filename)

        try:
            img = cv2.imread('./'+profile_url)
            face = extractFace(img,600)
            cv2.imwrite('./'+profile_url,face)
            img = cv2.cvtColor(face,cv2.COLOR_BGR2RGB)
            encoding = face_recognition.face_encodings(img)[0]
            print(encoding)
        except:
            error = True 
            form.photo.errors.append("Face is not visible properly")

        filename = photos.save(form.earphoto.data)
        ear_url = url_for('get_file',filename=filename)
        name = form.name.data
        fathername = form.fathername.data
        regno = form.regno.data
        dob = form.dob.data
        bloodgroup = form.bloodgroup.data
        
        try:
            start = time.time()
            ear = getFvAndShape('./'+ear_url)
            end = time.time()
            timetook = round((end-start)/4,3)
            info = getEarCannyAndGaussImg('./'+ear_url,600,9)
            earimg = cv2.imread('./'+ear_url)
            os.remove('./'+ear_url)
            cv2.imwrite('static/images/ear.jpg',earimg)
            cv2.imwrite('static/images/canny.jpg',info['canny'])
            cv2.imwrite('static/images/gauss.jpg',info['gaussian'])
            print(ear)
            if not error:
                profile = {
                    'name':name,
                    'id':regno,
                    'profileImg': profile_url,
                    'fatherName':fathername,
                    'dob': dob.strftime("%d/%m/%Y"),
                    'bloodGroup':bloodgroup,
                    'fv': ear['fv'],
                    'shape':ear['shape'],
                    'encoding':encoding.tolist()
                }
            
                collection.insert_one(profile)
                prompt = "Registration Successfull"
                print(prompt)
                # return render_template('registration.html',form=form, profile_url=profile_url, ear_url=ear_url,isRegister=True)
                return render_template('profile.html', profile=profile, images=['static/images/ear.jpg','static/images/gauss.jpg','static/images/canny.jpg'], ear=ear, prompt=prompt, values = [None,timetook], databasetype="0")
            else:
                pass
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
            
            earimg = cv2.imread('uploads/'+filename)
            cv2.imwrite('static/images/ear.jpg',earimg)
            cv2.imwrite('static/images/canny.jpg',info['canny'])
            cv2.imwrite('static/images/gauss.jpg',info['gaussian'])
            os.remove('uploads/'+filename)
            
            accuracy, profile = findPerson(ear['fv'])
            
            prompt = ""
            if(profile):
                prompt = "Match Found"
            else:
                prompt = "Match Not Found"
            return render_template('profile.html', profile=profile, images=['static/images/ear.jpg','static/images/gauss.jpg','static/images/canny.jpg'], ear=ear, prompt=prompt, values=[accuracy, timetook], databasetype=databasetype)
        except:
            print("Anonymous Ear Image")
            form.earphoto.errors.append("Not able to scan ear properly. Try again with other image.")

    return render_template('auth.html',form=form)

@app.route('/multimode', methods=['GET','POST'])
def multimode():
    form = MultimodeForm()
    if form.validate_on_submit():
        # Time taken calculation
        # accuracy
        databasetype = form.databasetype.data
        timetook = 0
        if form.earphoto.data:
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
                earimg = cv2.imread('uploads/'+filename)
                cv2.imwrite('static/images/ear.jpg',earimg)
                cv2.imwrite('static/images/canny.jpg',info['canny'])
                cv2.imwrite('static/images/gauss.jpg',info['gaussian'])
                os.remove('uploads/'+filename)
                # print("-----------------------reached ------------------------")
                # print(ear)
                accuracy, profile = findPerson(ear['fv'])
                print("accuracy: ",accuracy)
                # print("profile", profile) 
                prompt = ""
                if(profile):
                    prompt = "Match Found"
                else:
                    prompt = "Match Not Found"
                return render_template('profile.html', profile=profile, images=['static/images/ear.jpg','static/images/gauss.jpg','static/images/canny.jpg'], ear=ear, prompt=prompt, values=[accuracy, timetook], databasetype=databasetype)
            except:
                print("Anonymous Ear Image")
                form.earphoto.errors.append("Not able to scan ear properly. Try again with other image.")

        elif form.photo.data:
            print("Face Photo recieved")
            filename = photos.save(form.photo.data)
            face = cv2.imread('uploads/'+filename)
            face = extractFace(face,600)
            # cv2.imwrite('uploads/'+filename,face)
            os.remove('uploads/'+filename)
            face = cv2.cvtColor(face,cv2.COLOR_BGR2RGB)
            try:
                encoding = face_recognition.face_encodings(face)[0]
                accuracy, profile = findPersonByFace(encoding)
                if profile:
                    prompt = "Face Matched"
                return render_template('profile.html', profile=profile, images=None, ear=None, prompt=prompt, values=[accuracy, timetook], databasetype=databasetype)         
            except:
                form.photo.errors.append("Face is not visible properly")    
        else:
            form.earphoto.errors.append("Neither ear nor face image is uploaded")
            print("Neither ear nor face image is uploaded")
        

    return render_template('multimode.html',form=form)



if __name__ == '__main__':
    # collection.insert_one({'name':'prasant','marks':100})
    app.run(port=3000, debug=True)