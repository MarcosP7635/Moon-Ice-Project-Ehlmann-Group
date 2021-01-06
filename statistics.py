import scipy as sp
import numpy as np
import rasterio as rio
import rasterio.features
import rasterio.warp
import os
import matplotlib.pyplot as plt
import pandas as pd
#first I need to get the WEH raster as an array, since it's a tif
path = 'C:\\WEH Raster.tif'
with rasterio.open(path) as dataset:
    # Read the dataset's valid data mask as a ndarray.
    mask = dataset.dataset_mask()
    # Extract feature shapes and values from the array.
    for geom, val in rasterio.features.shapes(
            mask, transform=dataset.transform):
'''wehsrc = rio.open(path)
print(wehsrc.shape)
print(wehsrc)
wehArray = np.asarray(wehsrc)
print(wehArray.shape)
#checking the data is clean
array_sum = np.sum(wehArray)
array_has_nan = np.isnan(array_sum)
print("Are the Nans? ", array_has_nan) #The data is clean, this returns False'''
#print(wehArray.dtype) #float64
#print(len(wehArray[0])) #250
#print(wehArray[0,0,0])
print(wehArray)
#wehArray = np.asarray(wehArray[0:,:,])
print(wehArray.shape)
#print(wehArray)
plt.hist(wehArray)
plt.title("histogram")
plt.show()
print(pd.DataFrame(wehArray))
