import cv2
import numpy as np
import math
import warnings
from earShapeFinder import *
warnings.filterwarnings("ignore", category=DeprecationWarning) 


def getSlope(point1, point2):
    '''
    point1 = [x1,y1] \n
    point2 = [x2,y2] \n
    This funtion will return slope of line joining these two points.
    '''
    x1 , y1 = point1
    x2 , y2 = point2
    m = (y2-y1)/((x2-x1) if (x2-x1)!=0 else 1)
    return m

def isSafe(img,visited, i, j):
    '''
    A supporting funtion for BFS for backtracking.
    '''
    if(i<0 or i>=len(visited) or j<0 or j>=len(visited[0]) or visited[i][j]==1 or img[i][j]<100):
        return False
    else:
        return True

def bfs(img,visited,i,j):
    '''
    Find all the connected pixles to pixle(i,j) having white color using BFS(Breadth First Search).\n
    It will return a list of pixles included in line and pixle will be in the format[x,y]. 
    '''
    line_pixels = []
    queue = []
    visited[i][j] = 1
    queue.append([i,j])

    while queue:
        m = queue.pop(0)
        I, J = m
        line_pixels.append([J,I])
        if(isSafe(img,visited, I, J+1)):
            visited[I][J+1] = 1
            queue.append([I,J+1])
        if(isSafe(img,visited, I, J-1)):
            visited[I][J-1] = 1
            queue.append([I,J-1])
        if(isSafe(img,visited, I+1, J)):
            visited[I+1][J] = 1
            queue.append([I+1,J])
        if(isSafe(img,visited, I-1, J)):
            visited[I-1][J] = 1
            queue.append([I-1,J])
    return line_pixels

def find_lines(img):
    '''
    Find all the lines of white color in the image using BFS function.\n
    It Will return a list of lines and lines will be the list of pixle and pixle will be in format[x,y].
    '''
    visited = np.zeros((img.shape[0],img.shape[1]), dtype=bool)
    lines = list()
    for i in range(len(img)):
        for j in range(len(img[0])):
            if(img[i][j]>100 and visited[i][j]==0):
                lines.append(bfs(img, visited,i,j))
    return lines

def furthestPoint(points):
    '''
    It will find out the futhest two point on a given line.\n
    It will return tuple of two pixle (pixle1,pixle2). Pixle will be in the format[x,y].
    '''
    maxx = 0
    pair = tuple()
    for i in range(len(points)):
        for j in range (i+1,len(points)):
            dis = math.dist(points[i],points[j])
            if(dis>maxx):
                maxx = dis
                pair = (points[i],points[j])
    return pair

def getsign(point1, point2):
    '''
    This funtion will tell in which direction we should proceed(+ or -) to go from point1 to point2.\n
    '''
    m = getSlope(point1,point2)
    prev = math.dist(point1,point2)
    x1, y1 = point1
    x2, y2 = point2
    x3 = int(((1/math.sqrt(1+m**2))*1*10 + x1))
    y3 = int(((m/math.sqrt(1+m**2))*1*10 + y1))
    curr = math.dist([x3,y3],point2)
    if(curr<prev):
        return 1
    else:
        return -1

def getPoints(points, n):
    '''
    It will generate n number of points between points[0] and points[1]. \n
    All the points will be equally spaced and evenly spread. \n
    This function will return list of n pixles. Pixle format[x,y].
    '''
    if n%2==0:
        raise Exception("Odd value for n is required")
    ans = list()
    d = math.dist(points[0],points[1])/(n+1)
    x1, y1 = points[1]
    # use getsign() function to decide wheather to go in positive or in negative direction
    sign = int(getsign(points[1],points[0]))
    m = getSlope(points[0],points[1])
    c = y1 - m*x1
    for i in range(n):
        X1 = int(((1/math.sqrt(1+m**2))*(i+1)*sign*d + x1))
        Y1 = int(((m/math.sqrt(1+m**2))*(i+1)*sign*d + y1))
        ans.append([X1,Y1])
    if(not len(ans)==n):
        return getPoints(points,n,-1)
    return ans
    
def findIntersection(point1, m, outerEdge, sign):
    '''
    This function will find the intersection of line(passing from point1 with slope m) and outeredge.\n
    Sign will be provided by the user, which will determine the direction of searching for the function.
    '''
    x1 , y1 = point1
    for d in range(4,300):
        x2 = int(((1/math.sqrt(1+m**2))*sign*d + x1))
        y2 = int(((m/math.sqrt(1+m**2))*sign*d + y1))
        if([x2,y2] in outerEdge):
            return [x2,y2]
    return []

def createNormals(outerEdge, points):
    '''
    This function will return pair of points [points[i],point_of_intersection]. Point format[x,y].
    '''
    m = getSlope(points[1],points[2])
    if not m==0:
        m = -1/m
    # first we will find intersections in positive direction
    sign = 1
    ans = list()
    for point1 in points:
        point2 = findIntersection(point1, m, outerEdge, sign)
        if not len(point2)==0:
            ans.append([point1,point2])
    if(len(ans)==len(points)):
        return ans
    # if above condition is not true
    # we will fidn intersections in negative direction
    sign = -1
    ans = list()
    for point1 in points:
        point2 = findIntersection(point1, m, outerEdge, sign)
        if not len(point2)==0:
            ans.append([point1,point2])
    if(len(ans)!=len(points)):
        raise Exception("Ambigous Ear. Problem in drawing normals.")
    return ans

def middlePoint(points):
    '''
    returns center point of the line joining points[0] and points[1]
    '''
    x1 , y1 = points[0]
    x2 , y2 = points[1]
    x3 = int((x2+x1)/2)
    y3 = int((y1+y2)/2)
    return [x3,y3]

def getLMax2(umax,midPoint,outerEdge):
    '''
    return LMax2 
    '''
    m = getSlope(umax,midPoint)
    lmax2 = findIntersection(midPoint,m,outerEdge,-1)
    if(lmax2[1]>midPoint[1]):
        return lmax2
    else:
        return findIntersection(midPoint,m,outerEdge,1)

def extractFeature(ref,normalpoints,precision=2):
    '''
    return feature vector in the form of 1D list.
    '''
    fv = list()
    m1 = getSlope(ref, normalpoints[int(len(normalpoints)/2)][1])
    # cv2.circle(img, normalpoints[int(len(normalpoints)/2)][1],5,(255,255,0),6);
    for point in normalpoints:
        m2 = getSlope(ref, point[1])
        tan = abs((m1-m2)/(1+m1*m2))
        angle = math.degrees(math.atan(tan))
        fv.append(round(angle,precision))
    return fv

def getEarInfo(canny,drawShape=1,drawFeature=1):
    '''
    This funtion accept image of canny of ear in BGR format and provide feature vector. \n
    return [image_with_drawing, featureVector1, featureVector2]
    '''
    canny1 = canny.copy()
    canny2 = canny.copy()
    # importing canny image as 
    # img(in grayscale for processing) 
    # and canny(in RGB for drawing colorfull lines on it)
    grey = cv2.cvtColor(canny, cv2.COLOR_BGR2GRAY)
    # Dilate the image to avoid error beacause of thin disjoints
    kernel = np.ones((2, 2), np.uint8)
    grey = cv2.dilate(grey, kernel, iterations=1)
    canny = cv2.dilate(canny, kernel, iterations=1)


    # Finding all connected line of white color in image
    # lines variable will have list of pixles(coordinates [x,y]) of all the lines present in the img
    lines = find_lines(grey)

    # Out of all the lines we need only the outer edge for further calculation
    # OuterEdge variable will consisit all the pixles of outer edge
    outerEdge = sorted(lines,key=len,reverse=True)[0]

    # Find furthest point on outer edge
    # umax - uppermost point
    # lmax - lowermost point 
    umax, lmax = furthestPoint(outerEdge)

    # Generating 19 points in between umax and lmax
    points = getPoints([umax, lmax],19)

    # Finding the intersection of normal drawn with outer edge
    normalpoints = createNormals(outerEdge, points)

    # Finding the reference point for feature vector 1
    # reference point is middle point
    refPoint = points[int(len(points)/2)]  

    # Finding feature vector 1
    fv1 = extractFeature(refPoint,normalpoints)

    # shape of the ear
    shape = findShape(canny,outerEdge,umax,lmax,normalpoints,draw=drawShape)




    # midline start and end point
    midLine = normalpoints[int(len(normalpoints)/2)]

    # finding middlePoint from start and end point of midline
    midPoint = middlePoint(midLine)

    # finding lmax2 by extanding line from 
    # umax to midpoint and find where it intersect on outeredge
    lmax2 = getLMax2(umax,midPoint,outerEdge)

    # Finding 9 points in between umax and lmax2
    points2 = getPoints([umax, lmax2],9)

    # Finding normal intersection point
    normalpoints2 = createNormals(outerEdge, points2)

    # Finding reference point for feature vector 2
    refPoint2 = points2[int(len(points2)/2)]

    # Finding the feature vector 2
    fv2 = extractFeature(refPoint2,normalpoints2)

    # midline start and end point
    midLine2 = normalpoints2[int(len(normalpoints2)/2)]

       

    #------------Drawings---------------------------------------
    if drawFeature:
        cv2.circle(canny, umax, 2, (0,0,255), 2)
        cv2.circle(canny, lmax, 2, (0,0,255), 2)
        cv2.line(canny,umax,lmax,(0,0,255), 1)
        for x in points:
            cv2.circle(canny, x, 2, (0,255,0), 2)
        for point in normalpoints:
            cv2.line(canny,point[0],point[1],(255,0,0), 1)

        cv2.circle(canny, refPoint, 2, (255,0,128), 2)
        cv2.line(canny,midLine[0],midLine[1],(255,0,128), 1)
        cv2.line(canny,umax,lmax2,(0,0,255), 1)
        cv2.circle(canny, lmax2, 2, (0,255,255), 2)
        for x in points2:
            cv2.circle(canny, x, 2, (0,255,0), 2)

        for point in normalpoints2:
            cv2.line(canny,point[0],point[1],(255,255,0), 1)
        cv2.circle(canny, refPoint2, 2, (255,0,128), 2)
        cv2.line(canny,midLine2[0],midLine2[1],(255,0,128), 1)
        cv2.imshow('fvimage', canny)
    #------------------------------------------------------------

    #------------------------------------------------------------
    if drawFeature:
        cv2.circle(canny1, umax, 2, (0,0,255), 2)
        cv2.circle(canny1, lmax, 2, (0,0,255), 2)
        cv2.line(canny1,umax,lmax,(0,0,255), 1)
        cv2.circle(canny1, refPoint, 2, (255,0,128), 2)
        
        for point in normalpoints:
            cv2.line(canny1,refPoint,point[1],(255,0,0), 1)
        cv2.line(canny1,midLine[0],midLine[1],(255,0,128), 1)
        cv2.imshow("Feature 1", canny1)
    #-----------------------------------------------------------


    #------------------------------------------------------------
    if drawFeature:
        cv2.circle(canny2, umax, 2, (0,0,255), 2)
        cv2.circle(canny2, lmax2, 2, (0,0,255), 2)
        cv2.line(canny2,umax,lmax2,(0,0,255), 1)
        cv2.circle(canny2, refPoint2, 2, (255,0,128), 2)
        
        for point in normalpoints2:
            cv2.line(canny2,refPoint2,point[1],(255,0,0), 1)
        
        cv2.line(canny2,midLine2[0],midLine2[1],(255,0,128), 1)

        cv2.imshow("Feature 2", canny2)
    
    #-----------------------------------------------------------

    return {"fv":[fv1,fv2],"shape":shape}


if __name__=='__main__':
    path = 'canny/img/195_.jpg'
    canny = cv2.imread(path)
    if canny is None:
        raise Exception("Image not Found")
    ear = getEarInfo(canny)
    # print(ear["fv"])
    print("Feature Vector 1: (angle between reference_Line_1 joining reference point and normal intersection point on the outer edge)")
    print(len(ear['fv'][0]),"->",ear['fv'][0])
    print("Feature Vector 2: (angle between reference_line_2 joining reference point and normal intersection point on the outer edge)")
    print(len(ear['fv'][1]),"->",ear['fv'][1])
    print("Category:",ear['shape']+1)
    print("Free Lobe:",bool(4&ear['shape']))
    print("Round:",bool(2&ear['shape']))
    print("Narrow:",bool(1&ear['shape']))
    # cv2.imshow('Orignal Ear', )
    cv2.imshow('Canny', canny)
    
    cv2.waitKey(0)
