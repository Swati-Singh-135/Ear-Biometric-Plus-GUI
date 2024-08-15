import math
import numpy as np
import cv2

def middlePoint(points):
    '''
    returns center point of the line joining points[0] and points[1]
    '''
    x1 , y1 = points[0]
    x2 , y2 = points[1]
    x3 = int((x2+x1)/2)
    y3 = int((y1+y2)/2)
    return [x3,y3]

def getOuterEdgeImg(canny,outeredge):
    outerEdgeImg = np.zeros((canny.shape[0],canny.shape[1]), np.uint8)
    for point in outeredge:
        j , i = point
        outerEdgeImg[i][j]=255
    return outerEdgeImg

def getOverlapPercentage(img1,img2,edgeSize):
    ans = cv2.bitwise_and(img1,img2,mask=None)
    return cv2.countNonZero(ans)/edgeSize

def isFree(canny, lmax,refPoint, outerEdgeImg, edgeSize, draw=1):
    lobeMask = np.zeros((canny.shape[0],canny.shape[1]), np.uint8)
    x1,y1 = middlePoint([lmax,refPoint])
    x2,y2 = lmax
    for i in range(y1,y2):
        for j in range(x2):
            lobeMask[i][j] = 255
    # cv2.imshow('lobe',lobeMask)
    if(draw==1):
        cv2.rectangle(canny,[0,int((refPoint[1]+lmax[1])/2)],lmax,(0,255,255),1)

    if(getOverlapPercentage(lobeMask,outerEdgeImg,edgeSize)>0.03):
        return True
    else:
        return False
    
def isRound(canny, umax,refPoint,outerEdgeImg,edgeSize, draw=1):
    circleCenter = middlePoint([refPoint,umax])
    radius = int(math.dist(refPoint,umax)/2)
    circleMask = np.zeros((canny.shape[0],canny.shape[1]), np.uint8)
    cv2.circle(circleMask,circleCenter,radius,(255),2)
    # cv2.imshow('circle',circleMask)
    if(draw==1):
        cv2.circle(canny,circleCenter,radius,(255,0,255),1)
    
    if(getOverlapPercentage(circleMask,outerEdgeImg,edgeSize)>0.1):
        return True
    else:
        return False

def isNarrow(normalpoints, edgeSize):
    refLine = normalpoints[int(len(normalpoints)/2)]
    dist = math.dist(refLine[0],refLine[1])
    normalizeDist = dist/edgeSize
    if(normalizeDist<0.06):
        return True
    else:
        return False

def findShape(img,outerEdge,umax,lmax,normalpoints,draw=1):
    canny = img.copy()
    refLine = normalpoints[int(len(normalpoints)/2)]
    refPoint = refLine[0]

    outerEdgeImg = getOuterEdgeImg(canny,outerEdge)
    edgeSize = len(outerEdge)
    round = isRound(canny, umax,refPoint,outerEdgeImg,edgeSize)
    free = isFree(canny, lmax, refPoint, outerEdgeImg, edgeSize)
    narrow = isNarrow(normalpoints, edgeSize) 
    
    # ---------------------Drawings------------------------------------------
    if(draw==1):
        cv2.circle(canny, umax, 2, (0,0,255), 2)
        cv2.circle(canny, lmax, 2, (0,0,255), 2)
        cv2.line(canny, umax,lmax,(0,0,255), 1)
        cv2.imshow("Find Shape", canny)
    
    # print(free,round,narrow)

    return 4*free + 2*round + 1*narrow
   

if __name__=="__main__":
    pass
    