## TODO: Measure correlation between Ice Detection counts per km^2 and WEH
'''
TODO: First I need to add a column of ones to all of the M3 Data then get it
back into ArcGIS to convert it to raster, export the raster as a TIF
Then correlate all of the corresponding columns on the TIF. I just need to
make the raster for M^3 as coarse as the raster for NS.
'''
#now to borrow lots of lines from weh analysis from lawrence.py
#I may want to open this TIF using rasterio like in
import geopandas
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image
from osgeo import gdal
from osgeo import gdal_array
#cannonArray = np.asarray(pd.read_csv(filename))
cannonArray = gdal_array.LoadFile('C:\\Users\\engin\Downloads\\NP_IFI (1).tif')
print(cannonArray.shape)
print(cannonArray)
cannonraster = gdal.Open('C:/Users/engin/Downloads/SP_IFI (1).tif')
print(type(cannonraster))
print(cannonraster.GetMetadata())
#print(cannonraster.GetRast)
wehArray = np.asarray(pd.read_csv('C:\\Users\\engin\\myweharray.csv'))
#LPNSarray = gdal_array.LoadFile('C:/Users/engin/Downloads/LP Neutron Spectra WEH in ppm [Lawrence et al 2006]1.tif')
LPNSarray = gdal_array.LoadFile('C:/Users/engin/Downloads/LPNS.tif')
LPNSraster = gdal.Open('C:/Users/engin/Downloads/LPNS.tif')
LENDarray = gdal_array.LoadFile('C:/Users/engin/Downloads/LEND zeroes resized.tif')
LENDraster = gdal.Open('C:/Users/engin/Downloads/LEND zeroes resized.tif')
print("LENDraster type is ", type(LENDraster))
print("LENDraster metadata is ", LENDraster.GetMetadata())
print("LENDraster is ",LENDraster)
print(type(LPNSraster))
print(LPNSraster.GetMetadata())
print("LPNSraster is ", LPNSraster)
print("LENDarray is a ", LENDarray.shape, " ", type(LENDarray))
print("LPNSarray is a ", LPNSarray.shape, " ", type(LENDarray))

#now to write the LENDarray to a csv file!
np.savetxt("LENDarray.csv", LENDarray, delimiter=",")
np.savetxt("LPNSarray.csv", LPNSarray, delimiter=",")
OneDLENDarray = LENDarray.flatten()
OneDLPNSarray = LPNSarray.flatten()
OneDcannonArray = cannonArray.flatten()
nonzero = 0
zero = 0
for a in list(OneDLENDarray):
    if a>0:
        nonzero = nonzero+1
        if a>1:
            print("large value")
    else:
        zero = zero+1
print("Number of zeros in OneLENDarray",  zero, "Number of nonzeros in OneLENDarray", nonzero, nonzero+zero)
nonzero = 0
zero = 0
for index in list(range(len(OneDLPNSarray))):
    if OneDLPNSarray[index]<0:
        OneDLPNSarray[index] = 0
for a in list(OneDLPNSarray):
    if a>0:
        nonzero = nonzero+1
        if a>1000:
            print("large value")
    else:
        if a<0:
            print("negative value of ", a)
        else:
            zero = zero+1
print("Number of zeros in OneDLPNSarray",  zero, "Number of nonzeros in OneDLPNSarray", nonzero, nonzero+zero)
#print("LPNSarray is a ", LPNSarray.shape, " ", type(LPNSarray))
#print("This is LPNSarray", LPNSarray)
#print("This is LENDarray", LENDarray)
#print("OneDLPNSarray is a ", OneDLPNSarray.shape, " ", type(LPNSarray))
#print(OneDLPNSarray)
#print(OneDLENDarray)
binLPNS, binLEND = [0]*12500, [0]*12500
for i in range(12500):
    for smalli in range(10):
        binLEND[i] = binLEND[i]+OneDLENDarray[i*10+smalli]
        binLPNS[i] = binLPNS[i]+OneDLPNSarray[i*10+smalli]
    binLEND[i] = binLEND[i]/10
    binLPNS[i] = binLPNS[i]/10
size = int((nonzero+zero))
plt.scatter(OneDLPNSarray, OneDLENDarray)
plt.title("Lunar Prospector Hydrogen Abundance vs LEND")
plt.xlabel('Lunar Prospector WEH in ppm')
plt.ylabel(r'LEND Hydrogen Wt percent')
#plt.show()
'''
plt.plot( np.array(range(0,10000)),OneDLPNSarray[0:10000])
plt.title("Array Index vs Lunar Prospector Hydrogen Abundance")
plt.plot( np.array(range(0,size)),OneDLENDarray[0:size])
plt.title("Array Index vs LPNS")
plt.show()'''
print("This is the OneDLENDarray ",  OneDLENDarray)
print("This is the OneDLPNSarray ", OneDLPNSarray)
print("This is the average of OneDLENDarray ", np.average(OneDLENDarray))
print("This is the average of OneDLPNSarray", np.average(OneDLPNSarray))
print("OneDLPNSarray.dtype", OneDLPNSarray.dtype)
#Now I'm going to divide each array by their for
LPNSaverage = np.average(OneDLPNSarray)
LENDaverage = np.average(OneDLENDarray)
LPNSaveragedArray, LENDaveragedArray = [0]*125000, [0]*125000
for index in list(range(125000)):
    LENDaveragedArray[index] = OneDLENDarray[index]/LENDaverage
    LPNSaveragedArray[index] = OneDLPNSarray[index]/LPNSaverage
plt.scatter(LPNSaveragedArray, LENDaveragedArray)
plt.title("Lunar Prospector Hydrogen Abundance vs LEND")
plt.xlabel('Lunar Prospector WEH in ppm')
plt.ylabel(r'LEND Hydrogen Wt percent')
plt.show()
#plt.show()
#np.savetxt("OneDLPNSarray.csv", OneDLPNSarray , delimiter=",")
#print("OneDLPNSarray is ", OneDLPNSarray.shape, " ", OneDLPNSarray)
#print(LENDarray[:,100])
#print(LPNSarray[:,100])
'''print(wehArray[:,0])
print(wehArray[200,0])
print(wehArray)'''
#print(cannonArray.shape, "should be 671, 11")
#print(cannonArray.columns)
#def openTIF (filename):
#    outArray = pd.read_csv(filename)
#let's graph area vs counts and see what we get.
