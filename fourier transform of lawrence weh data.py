import scipy
from scipy import stats as stats
from scipy import stats as optimize
import geopandas
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
filteredWehArray = pd.read_csv('C:\\Users\\engin\\myweharray.csv')
''''
Filtered to be more poleward than 70 degrees from Lawrence's 2006 WEH data.
'''
#wehArray = np.array(wehArray[:,]).astype(float)
for thing in filteredWehArray.columns:
    print(thing)
#print(wehArray.columns)
print(filteredWehArray.head(), "I just printed")
filteredWehArray.drop(filteredWehArray.columns[0], axis=1, inplace=True)
print(filteredWehArray.head(), "I printed too")
print(filteredWehArray.iloc[0], "meee")
print(filteredWehArray.dtypes, "me too" )
filteredWehArray = np.array([])
'''
This fuction is to filter out the regions where Lawrence's assumed thorium
concentration doesn't apply
'''
print(filteredWehArray.shape,filteredWehArray.shape)
doublefilter = filter(filteredWehArray)
print(filteredWehArray.shape, doublefilter.shape) #it works :)
filteredWehArray.to_csv('C:\\Users\\engin\\myweharray.csv')
'''
This exports the array. I'll just use this from now on and skip the whole
filtering process everytime.
'''
#make separate 1 row arrays of the latitude and weh.
latitude = filteredWehArray['LATITUDE']
latitude = np.asarray(latitude)
latitude = latitude.astype(np.float)
length = latitude.shape[0]
half = int(length/2 - 1)
latitude1 = latitude[0:half]
latitude2 = latitude[half+1:length]
#separate the poles for the correlation
print(latitude[0:20])
weh = filteredWehArray['WEH']
weh = np.asarray(weh)
weh = weh.astype(np.float)
print(weh.shape)
weh1 = weh[0:half]
weh2 = weh[half+1:length]
print(weh1[-1])
print(weh2[-1])
#separate the poles for the correlation
#keeps trying to be a string array for some reason and not having this line is bad
