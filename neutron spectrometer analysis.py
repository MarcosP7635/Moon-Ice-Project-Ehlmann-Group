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
import rasterio
from rasterio.plot import show
import struct
'''
cannonArray = np.asarray(pd.read_csv(filename))
#cannonArray = pd.read_csv('C:\\Users\\engin\Downloads\\NP_IFI (1).tif')
print(cannonArray.columns)
cannonArray.drop(cannonArray.columns[0], axis=1, inplace=True)
cannonArray.drop(cannonArray.columns[0], axis=1, inplace=True)
imagetif = Image.open(filename)
imagetif.show()'''
#filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
#print(filename)
'''LENDraster = gdal.Open('C:/Users/engin/Downloads/LEND.tif')
print(type(LENDraster))
print(LENDraster.GetMetadata())
LENDband = LENDraster.GetRasterBand(1)
print("Band Type={}".format(gdal.GetDataTypeName(LENDband.DataType)))
LENDmin = LENDband.GetMinimum()
LENDmax = LENDband.GetMaximum()
print("this is the band", LENDband, "this is the min", LENDmin, "this is the max", LENDmax)
if LENDband.GetRasterColorTable():
    print("Band has a color table with {} entries".format(LENDband.GetRasterColorTable().GetCount()))
LENDscanline = LENDband.ReadRaster(xoff=0, yoff=0,xsize=LENDband.XSize, ysize=1,
buf_xsize=LENDband.XSize, buf_ysize=1, buf_type=gdal.GDT_Float32)
tuple_of_floats = struct.unpack('f' * LENDband.XSize, LENDscanline)
print("LENDscanline ", LENDscanline, " tuple of floats ", tuple_of_floats)
LPNSraster = gdal.Open('C:/Users/engin/Downloads/LPNS.tif')
print(type(LPNSraster))
print(LPNSraster.GetMetadata())
#print(saninraster.GetRast)'''
LENDpath = r'C:\Users\engin\Downloads\LEND.tif'
LENDarray = np.array(plt.imread(LENDpath))
print(LENDarray)
print("LENDarray shaep ", LENDarray.shape)
'''LENDarray = np.asarray(pd.read_csv('C:\\Users\\engin\\LEND.csv'))

print(wehArray[:,0])
print(wehArray[200,0])
print(wehArray)'''
#print(cannonArray.shape, "should be 671, 11")
#print(cannonArray.columns)
#def openTIF (filename):
#    outArray = pd.read_csv(filename)

#let's graph area vs counts and see what we get.
