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
from scipy import stats
from matplotlib.colors import LogNorm
import mpmath
'''
Instead of averaging, I'm going to bin the LEND data by the LPNS data.
These are the raw data I was sent by Sanin and Lawrence.
'''
LENDfilepath = 'C:\\Users\\engin\\LENDSouth.csv'
#LPNSfilepath = 'C:\\Users\\engin\\PolarfilteredLunarProspector.csv'
#Using more recent LPNS modelling
LPNSfilepath = 'C:\\Users\\engin\\Downloads\\LPNS2018\\LPNS2018.csv'
def openCSVasFloatArray(filepath):
    array = np.asarray(pd.read_csv(filepath, header=0, names=None, index_col=False))
    array = array.astype(np.float)
    #for column in range(array.shape[1]):
    #    array[:,column] = array[:,column].astype(np.float)
    return array
LENDarray = openCSVasFloatArray(LENDfilepath)
LPNSarray = openCSVasFloatArray(LPNSfilepath)
print(LPNSarray)
print(LENDarray)
print(LPNSarray.shape[1])
LPNSarray = LPNSarray[0:28800,:]
#only leaves the south pole
LENDlonglat = LENDarray[:,0:2]
LPNSlonglat = LPNSarray[:,1:3]
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
LENDbinnedArray = [0]*28800
#I'll do one LPNS at a time
'''
The outermost loop is the number of LPNS bands. (40)
'''
added, zeros, addedCounts, unbinnedZero = 0,0,0,0
for iteration in range(int(LPNSarray.shape[0]/(720))): #get the entire south pole
    for initial in range(720): #get a full LEND band
        for row in range(8): #group 8 LEND bands to correspond to a LPNS band
            itAddOn = iteration*720*8
            inAddOn = initial*8
            if (itAddOn+inAddOn+row < 230399):
                if (not LENDarray[itAddOn+inAddOn+row,2]==0):
                    added = added+1
                    LENDbinnedArray[int((itAddOn+inAddOn)/8)] = LENDbinnedArray[int((itAddOn+inAddOn)/8)] + LENDarray[itAddOn+inAddOn+row,2]
                else:
                    unbinnedZero = unbinnedZero+1
        if(not added==0):
            addedCounts = addedCounts+1
            LENDbinnedArray[int((itAddOn+inAddOn)/8)] = LENDbinnedArray[int((itAddOn+inAddOn)/8)]/added
            added=0
combinedArray = [[0]*28800, [0]*28800]
combinedArray [0] = LENDbinnedArray
combinedArray [1] = LPNSarray[:,0]
for a in range(len(LENDbinnedArray)):
    if LENDbinnedArray[a]==0:
        zeros = zeros+1
#now to filter out the 0s
combinedArray = np.array(combinedArray)
LENDbinnedArray = np.array(LENDbinnedArray)
zeroIndices = np.where(LENDbinnedArray==0)[0]
combinedArray = np.delete(combinedArray, zeroIndices, 1)
#now to convert the ppm to wt%. 1wt% = 1111.11111ppm.
#Thus we need to divide the LPNS data by this number
conversion = 1/(50/.045)
print(combinedArray)
print(type(combinedArray[1]) is np.ndarray)
print(combinedArray[1].shape)
combinedArray[1] = np.array(combinedArray[1])
combinedArray[0] = np.array(combinedArray[0])
print(combinedArray[1][0].dtype)
combinedArray[1] = np.multiply(combinedArray[1],conversion)
print(combinedArray)
