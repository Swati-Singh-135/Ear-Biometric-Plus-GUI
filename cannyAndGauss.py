import cv2
import numpy as np

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

def getCanny(img,blur=9,tmin=60,tmax=120):
    '''
    Accept image in BGR format and returns gussian(BGR) and canny(Gray) 
    '''    
    # applying gaussian blur to reduce noise
    gaussian = cv2.GaussianBlur(img,(blur,blur),0) # odd size matrix is used
    # applying canny edge detection
    canny = cv2.Canny(gaussian,tmin,tmax)
    return [gaussian, canny]


if __name__=='__main__':
    img_path = "img/065_.jpg"
    img = cv2.imread(img_path)
    img = resizeImage(img,300)
    gaussian, canny = getCanny(img)
    # saving the canny image
    # cv2.imwrite('canny/'+img_path, canny)
    cv2.imshow("Original", img)
    cv2.imshow("Gaussian Blur", gaussian)
    cv2.imshow("canny", canny)
    cv2.waitKey(0)