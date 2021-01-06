## TODO: Measure correlation between Ice Detection counts per km^2 and WEH
'''
TODO: First I need to add a column of ones to all of the M3 Data then get it
back into ArcGIS to convert it to raster, export the raster as a TIF
Then correlate all of the corresponding columns on the TIF. I just need to
make the raster for M^3 as coarse as the raster for NS.
'''
#now to borrow lots of lines from weh analysis from lawrence.py
import geopandas
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter.filedialog import askopenfilename
#filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
#print(filename)
#m3Array = np.asarray(pd.read_csv(filename))
m3Array = pd.read_csv('C:\\Users\\engin\\Downloads\\M3_Ice_Detections_in_PSRs_as_CSV_and_xls\\M3 ice detections in PSRs South Pole Li et al 2018, Mazarico et al 2011.csv')
print(m3Array.columns)
m3Array.drop(m3Array.columns[0], axis=1, inplace=True)
m3Array.drop(m3Array.columns[0], axis=1, inplace=True)
print(m3Array.shape, "should be 671, 11")
print(m3Array.columns)
m3Array = np.asarray(m3Array)
print("first five rows of m3Array ", m3Array[:3,:])

wehArray = np.asarray(pd.read_csv('C:\\Users\\engin\\myweharray.csv'))
#so now the weh data is arrays :)
#print(wehArray[:,0])
#print(wehArray)
#print("I printed")
#let's graph area vs counts and see what we get.
'''
Graphs to make, listed by priority. First of all, after speaking with Bethany,
there isn't enough information in the M3 data to make it a raster. It did only
orbit for less than a year.

'''
