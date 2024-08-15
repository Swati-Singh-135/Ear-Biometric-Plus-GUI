import cv2
import time
from cannyAndGauss import *
from earFeatureExtarction import *
from earShapeFinder import *
from earCompare import *

def getFvAndShape(img_path,size=600,blur=9):
    img = cv2.imread(img_path)
    resizeimg = resizeImage(img,size)
    _, canny = getCanny(resizeimg,blur=blur)
    canny = cv2.cvtColor(canny,cv2.COLOR_GRAY2BGR)
    ear1 = getEarInfo(canny,drawShape=0,drawFeature=0)
    return ear1

def compareImg(img1_path,img2_path,size=600,blur=9):
    ear1 = getFvAndShape(img1_path,size,blur=blur)
    ear2 = getFvAndShape(img2_path,size,blur=blur)
    print(ear1)
    print(ear2)
    # return 0
    return compareEar(ear1['fv'],ear2['fv'])

def getEarCannyAndGaussImg(img_path,size=600,blur=9):
    img = cv2.imread(img_path)
    resizeimg = resizeImage(img,size)
    gaussian , canny = getCanny(resizeimg,blur=blur)
    return {'gaussian':gaussian,'canny':canny}

if __name__=='__main__':
    # start = time.time()
    # info = getEarCannyAndGaussImg("img/my/4.jpg",600,3)
    # end = time.time()
    # print("Time took:",end-start)
    # cv2.imshow("Gaussian Blur", info['gaussian'])
    # cv2.imshow('Canny', info['canny'])
    # cv2.waitKey(0)
    print(compareImg('img//register//prasant//1.jpeg','img//register//prasant//2.jpeg'),"%")

