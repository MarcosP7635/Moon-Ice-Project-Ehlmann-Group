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
'''
Instead of averaging, I'm going to bin the LEND data by the LPNS data.
These are the raw data I was sent by Sanin and Lawrence.
'''
LENDfilepath = 'C:\\Users\\engin\\LENDSouth.csv'
LPNSfilepath = 'C:\\Users\\engin\\PolarfilteredLunarProspector.csv'
#Using more recent LPNS modelling
#LPNSfilepath = 'C:\\Users\\engin\\Downloads\\LPNS2018\\LPNS2018.csv'
def openCSVasFloatArray(filepath):
    array = np.asarray(pd.read_csv(filepath))
#    for column in range(array.shape[1]):
#        array[column] = array[column].astype(np.float)
    return array
LENDarray = openCSVasFloatArray(LENDfilepath)
LPNSarray = openCSVasFloatArray(LPNSfilepath)
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
print(combinedArray[0])
print(combinedArray[1])
print("hello")
conversion = 9/(1*(10**4))
combinedArray[1] = combinedArray[1]*conversion
'''
the next step would instead change the reference area in Sanin et al 2017
to the average of the LPNS data rather than the average of the Apollo samples
#combinedArray[1] = combinedArray[1]*87.30911597036007/50
'''
m, b = np.polyfit(combinedArray[0], combinedArray[1], 1)
print(m,b)
correlationMatrix = np.corrcoef(combinedArray[1], combinedArray[0])
print(correlationMatrix)
regressionLabel = "Least Squares Linear regression. y = "+ str(np.around(m, 4))+"x+"+ str(np.around(b, 4)) + ". r^2 = " + str(np.around(correlationMatrix[0,1]**2, 4))
secondLine = np.array(range(28800))
secondLine = secondLine+1
secondLine = secondLine*np.max(combinedArray[1])/28800
secondLine = secondLine
#this is just to move the y=x line into the right part of the graph
def plotRawDataRegression(combinedArray):
    plt.scatter(combinedArray[0], combinedArray[1],
    label = "Binned Data from LEND and Lunar Prospector")
    plt.scatter(combinedArray[0], m*combinedArray[0] + b, label = regressionLabel)
    plt.scatter(secondLine, secondLine, label = "Reference Line y=x in wt%")
    plt.title("Comparing Spatially Coregistered Lunar Prospector and LEND Hydrogen Abundance")
    plt.xlabel('Averaged LEND Enriched Hydrogen in wt%(zeros omitted)')
    plt.ylabel(r'Lunar Prospector Enriched Hydrogen wt%')
    plt.legend()
    #plt.show()
def makeScatterPlot(arrayX, arrayY, xAxis, yAxis, lineArray, labelArray, colorArray):
    plt.scatter(arrayX,arrayY)
    if(lineArray,labelArray):
        for i in range(len(lineArray)):
            plt.scatter(arrayX, lineArray[i], label = labelArray[i], color = colorArray[i])
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.legend()
    plt.show()
def makeDensityPlots(combinedArray):
    fig, ax = plt.subplots()
    h = ax.hist2d(combinedArray[0],  combinedArray[1], bins = 50)
    print(combinedArray[0])
    print(combinedArray[1])
    m1 = .047/.15
    b1 = .06-.0047/.15
    plt.scatter(secondLine, secondLine, label = "Reference Line y=x in wt%", color = 'r')
    plt.scatter(combinedArray[0], m*combinedArray[0] + b, label = regressionLabel, color = 'w')
    #plt.scatter(combinedArray[0],m1*combinedArray[0] +b1, label = "Connecting points of maximum density. y = "+ str(np.around(m1, 4)) +"x+ " + str(np.around(b1, 4)), color = 'black')
    fig.colorbar(h[3], ax=ax)
    plt.title("Density plot of LEND and Lunar Prospector Hydrogen Abundance")
    plt.xlabel('Averaged LEND Enriched Hydrogen in wt%(zeros omitted)')
    plt.ylabel(r'Lunar Prospector Enriched Hydrogen wt%')
    plt.legend()
    plt.show()
def makeDensityPlot(arrayX, arrayY, xAxis, yAxis, lineArray, labelArray, colorArray):
    fig, ax = plt.subplots()
    h = ax.hist2d(arrayX,  arrayY, bins = 50)
    if(lineArray,labelArray):
        for i in range(len(lineArray)):
            plt.scatter(arrayX, lineArray[i], label = labelArray[i], color = colorArray[i])
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.legend()
    plt.show()
'''
the two highest density spots are near (.10,.06) and (.25,.11). m=.05/.15.
b=.06-.005/.15
'''
residualLeastsquare = combinedArray[1]-(m*combinedArray[0] + b)
plt.scatter(combinedArray[0], residualLeastsquare)
plt.title("Comparing Spatially Coregistered Lunar Prospector and LEND Hydrogen Abundance")
plt.ylabel('Residual of ' + regressionLabel)
plt.xlabel('Averaged LEND Enriched Hydrogen in wt%(zeros omitted)')
fig, ax = plt.subplots()
h = ax.hist2d(combinedArray[0], residualLeastsquare, bins = 50)
fig.colorbar(h[3], ax=ax)
plt.legend()
plt.show()
plt.title("Comparing Spatially Coregistered Lunar Prospector and LEND Hydrogen Abundance")
plt.ylabel('Residual of Least Squares Linear Regression')
plt.xlabel('Averaged LEND Enriched Hydrogen in wt%(zeros omitted)')
plotRawDataRegression(combinedArray)
makeDensityPlots(combinedArray)
def calculateRSquared():
    return
