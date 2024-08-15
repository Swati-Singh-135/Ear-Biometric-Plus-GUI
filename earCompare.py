from math import exp as e
import numpy as np

def compareEar(ear1, ear2, a=0.1):
    '''
        accuracy = 100 - Σ (e^a(fv₁[i]-fv₂[i]) - 1)
        a : senstivity of comparison function
    '''
    diff = 0
    for i in range(len(ear1[0])):
        diff+= abs(ear1[0][i] - ear2[0][i])
    for i in range(len(ear1[1])):
        diff+= abs(ear1[1][i] - ear2[1][i])
    matchPercentage = 100 - (e(diff*a) - 1)
    if matchPercentage<0:
        matchPercentage=0.00
    return round(matchPercentage,2)

def compareEar2(ear1, ear2, a=0.5):
    '''
        accuracy = 100 - Σ (e^a(fv₁[i]-fv₂[i]) - 1)
        a : senstivity of comparison function
    '''
    accuracy = 100
    for i in range(len(ear1[0])):
        accuracy-= (e(abs(ear1[0][i] - ear2[0][i])*a)-1)
    for i in range(len(ear1[1])):
        accuracy-= (e(abs(ear1[1][i] - ear2[1][i])*a)-1)
    if(accuracy<0):
        accuracy = 0.00
    return round(accuracy,2)
    
def compareEar3(ear1,ear2,atol=1):
    feature_vector1 = np.array(ear1,dtype=object)
    feature_vector2 = np.array(ear2,dtype=object)
    print(feature_vector1)
    print(feature_vector2)
    # Compare the first lists of the feature_vector lists
    matching_percentage1 = np.mean(np.isclose(feature_vector1[0], feature_vector2[0], atol=atol)) * 100
    return round(matching_percentage1, 2) 
