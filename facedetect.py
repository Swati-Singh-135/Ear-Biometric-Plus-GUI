import cv2

def resizeImage(img,size):
    '''
    This funtion will resize the image while maintaining the proportionality of the image.\n
    After applying this funtion \n
    \t max(img.width,img.height)=size \n
    '''
    w = int(img.shape[1])
    h = int(img.shape[0])
    if w>h:
        h = int(min(h,size*h/w))
        w = int(min(size,w))
    else:
        w = int(min(w,size*w/h))
        h = int(min(size,h))
    img = cv2.resize(img,(w,h))
    return img

def extractFace(img,size=600):
    img = resizeImage(img,size)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Load the cascade
    face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_alt2.xml')
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Define the margin around the detected area
    xmargin = 0.2
    ymargin = 0.2

    # Draw rectangle around the faces and crop the faces
    if len(faces):
        x, y, w, h = faces[0]
        face = img[int(y-ymargin*h):int(y+h+ymargin*h), int(x-xmargin*w):int(x+w+xmargin*w)]
        return face
    return None

def extractEar(img, size=600):
    img = resizeImage(img,size)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    left_ear_cascade = cv2.CascadeClassifier('models/haarcascade_mcs_leftear.xml')
    right_ear_cascade = cv2.CascadeClassifier('models/haarcascade_mcs_rightear.xml')
    offset = 0.1

    Lears= left_ear_cascade.detectMultiScale(gray, 1.3, 5)
    if len(Lears):
        Lear = Lears[0]
        x,y,w,h = Lear
        Lcrop = img[int(y-offset*h):int(y+h+offset*h), int(x-offset*w):int(x+w+offset*w)]
        return Lcrop

    Rears= right_ear_cascade.detectMultiScale(gray, 1.3, 5)
    if len(Rears):
        Rear = Rears[0]
        x,y,w,h = Rear
        Rcrop = img[int(y-offset*h):int(y+h+offset*h), int(x-offset*w):int(x+w+offset*w)]
        return Rcrop
    return None
        


if __name__=='__main__':
    img_path = 'img\\register\\jawale\\jawale.jpg'
    img_path = 'img\\register\\prasant\\4.jpeg'
    img = cv2.imread(img_path)
    img = resizeImage(img,600)
    face = extractFace(img,600)
    cv2.imshow('img', img)
    cv2.imshow('face', face)
    cv2.waitKey(0)
    