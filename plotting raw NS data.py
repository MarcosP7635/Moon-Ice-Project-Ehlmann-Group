import geopandas
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image
from osgeo import gdal
import rasterio
from rasterio.plot import show
import struct
'''
Instead of averaging, I'm going to bin the LEND data by the LPNS data.
These are the raw data I was sent by Sanin and Lawrence.
'''
LENDarray = np.asarray(pd.read_csv('C:\\Users\\engin\\LEND South.csv'))
LPNSarray = np.asarray(pd.read_csv('C:\\Users\\engin\\Polar filtered Lunar Prospector.csv'))
'''print(LENDarray.dtype)#float64
print(LPNSarray.dtype)#float64 '''
#print(LPNSarray[28800,])
LPNSarray = LPNSarray[0:28800,:]
#only leaves the south pole
#print(LENDarray[0][2]) #wt%
#print(LPNSarray[0][0]) #WEH ppm
LENDlonglat = LENDarray[:,0:2]
print(LENDlonglat)
LPNSlonglat = LPNSarray[:,1:3]
print(LPNSlonglat)
LENDaverageArray = [0]*28800
group1,group2,group3,group4,group5,group6,group7,group8 = [0]*28800, [0]*28800, [0]*28800, [0]*28800,  [0]*28800, [0]*28800, [0]*28800, [0]*28800
for i in range(28799):
    group1[i] = group1[i]+LENDarray[i*8+1,2]
    group2[i] = group2[i]+LENDarray[i*8+2,2]
    group3[i] = group3[i]+LENDarray[i*8+3,2]
    group4[i] = group4[i]+LENDarray[i*8+4,2]
    group5[i] = group5[i]+LENDarray[i*8+5,2]
    group6[i] = group6[i]+LENDarray[i*8+6,2]
    group7[i] = group7[i]+LENDarray[i*8+7,2]
    group8[i] = group8[i]+LENDarray[i*8+8,2]
    for smalli in range(8):
        LENDaverageArray[i] = LENDaverageArray[i]+LENDarray[i*8+smalli,2]
    LENDaverageArray[i] = LENDaverageArray[i]/8
print(LENDlonglat.shape) #(230399, 2)
print(LPNSlonglat.shape) #(230399, 2)
#plt.scatter(LPNSarray[:,0], LENDaverageArray)
'''plt.scatter(LPNSarray[:,0], group1)
plt.scatter(LPNSarray[:,0], group1)
plt.scatter(LPNSarray[:,0], group3)
plt.scatter(LPNSarray[:,0], group4)
plt.scatter(LPNSarray[:,0], group5)
plt.scatter(LPNSarray[:,0], group6)
plt.scatter(LPNSarray[:,0], group7)
plt.scatter(LPNSarray[:,0], group8)
plt.title("Lunar Prospector Hydrogen Abundance vs LEND")
plt.xlabel('Lunar Prospector WEH in ppm')
plt.ylabel(r'LEND Hydrogen Wt percent')
#plt.show()'''
'''
To confirm that my hypothesis about the long and lat is right I can just take
every 8th latitude of the LEND data and see if that's the latitude of the LPNS
data
'''
'''Every8thlong, longDifference, Every20thlat, latDifference = [0]*28800, [0]*28800, [0]*11520, [0]*28800
for i in range(11519):
    Every20thlong[i] = LENDlonglat[i*8,0]
    Every8thlat[i] = LENDlonglat[i*8,1]
    latDifference[i] = LPNSlonglat[i,0]-Every8thlat[i]
    longDifference[i] = LPNSarray[i,1]-Every8thlong[i]
Every8thlat[28799] = -70
Every8thlong[28799] = -150
#print(Every8thlat)
#print(LPNSarray[:,1])
#plt.scatter(LPNSarray[:,1],LPNSarray[:,1])
#print(len(LENDarray[:,0])/len(LPNSarray[:,1]))
#Let's plot the differences in longtiude for at each index
#I think the problem is that I'm currently binning by long and not lat.'''
'''plt.scatter(latDifference,longDifference)
plt.title("Lunar Prospector Hydrogen Abundance vs LEND")
plt.xlabel('Lunar Prospector and LEND latitude difference in degrees')
plt.ylabel(r'Lunar Prospector and LEND longitude difference in degrees')'''
#plt.show()
#I need to find the closest lat long pairs
'''print(LENDlonglat)
print(LPNSlonglat)
plt.scatter(Every8thlong, LPNSlonglat[:,0])
plt.xlabel('First 1/8th of LEND longitude')
plt.ylabel(r'Lunar Prospector longitude')
plt.show()
plt.scatter(Every8thlat, LPNSlonglat[:,1])
plt.xlabel('LEND latitude')
plt.ylabel(r'Lunar Prospector latitude')
plt.show()'''
'''plt.scatter(LENDlonglat[:,1],LENDlonglat[:,0])
plt.xlabel('LEND latitude')
plt.ylabel(r'LEND longitude')
plt.show()
plt.scatter(LPNSlonglat[:,1],LPNSlonglat[:,0])
plt.xlabel('LPNS latitude')
plt.ylabel(r'Lunar Prospector longitude')
plt.show()
for row in range(28800*8-7):
    if not LENDlonglat[row,1]==-89.9688:
        print(row, LENDlonglat[row,1])
        row = 10^8
print("LEND latitude step size I think is ", 20/(28800*8-7))
#LEND latitude changes on row 1438 -89.9063 deg to 1439 row -89.8438 deg
#Thus the average step size is .0625 and step has 720 rows.
#LPNS has step size .5 degrees.
#Thus LPNS must also have a step every 720 rows
'''
'''
Every 720 rows the LPNS data will have the same longitude.
So it's not every 8 I want to average, it's 8 bands 720 apart.
So I'll add rows 720 apart, until there are 8, then average them into a band.
This should work. This is confirmed by the nested for loop in the next docustring
'''
print(LENDarray)
print(LPNSarray)
#row 0 from LPNS, row 2 from LEND.
''''
for initial in range(720):
    for row in range(int(LPNSarray.shape[0]/720)):
        long = LPNSarray[initial,1]
        if not LPNSarray[initial+row*720,1] == long:
            print("Doesn't work", initial, row)
            break
    else:
        continue  # only executed if the inner loop did NOT break
    break  # only executed if the inner loop DID break
'''
LENDbinnedArray = [0]*28800
#I'll do one longitude at a time
for iteration in range(int(LPNSarray.shape[0]/(720*8))): #get the entire south pole
    for initial in range(720): #get a full LEND band
        for row in range(8): #group 8 LEND bands to correspond to a LEND band
            if not LEND[,2]==0:
                added = added+1
                LENDbinnedArray[(iteration*720)+(initial)] = LENDbinnedArray[(iteration*720)+(initial)] + LEND[(iteration*720)+(720*row)+initial,2]
        added=0
        LENDbinnedArray[(iteration*720*8)+(initial)] = LENDbinnedArray[(iteration*720*8)+(initial)]/8
