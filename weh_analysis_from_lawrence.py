import scipy
from scipy import stats as stats
from scipy import stats as optimize
import geopandas
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
wehArray = pd.read_csv('C:\\Users\\engin\\Downloads\\LP_WaterEquivalentHydrogen_Lawrence_etal_2006 (1).csv')
''''
with open('C:\\Users\\engin\\Downloads\\LP_WaterEquivalentHydrogen_Lawrence_etal_2006 (1).csv') as csvfile:
    reader = csv.reader(csvfile, quoting = csv.QUOTE_NONNUMERIC)
    for row in reader:
        wehArray.append(row)
Meant to import the CSV of Lawrence's data as an array.
This is based off of https://stackoverflow.com/questions/37173892/convert-from-csv-to-array-in-python
'''
#wehArray = np.array(wehArray[:,]).astype(float)
for thing in wehArray.columns:
    print(thing)
#print(wehArray.columns)
print(wehArray.head(), "I just printed")
wehArray.drop(wehArray.columns[0], axis=1, inplace=True)
print(wehArray.head(), "I printed too")
print(wehArray.iloc[0], "meee")
filteredWehArray = np.array([])
print(wehArray.dtypes, "me too" )
def filter(inputArray):
    outputArray = inputArray[(inputArray['LATITUDE'] > 70.0) | (inputArray['LATITUDE'] < -70.0)]
    return outputArray
''' counter = 0
    for row in inputArray.columns[2].tolist():
        if (row**2 > 4900.0):
            outputArray = np.vstack(outputArray, inputArray.iloc[counter])
        counter = counter+1 '''
    #outputArray = np.vstack(outputArray, inputArray[inputArray[:,3] < -70])
filteredWehArray = filter(wehArray)
        ## TODO: np.vstack rows
print(filteredWehArray.shape, wehArray.shape)
doublefilter = filter(filteredWehArray)
print(filteredWehArray.shape, doublefilter.shape) #it works :)
filteredWehArray.to_csv('C:\\Users\\engin\\myweharray.csv')
#now to make a best fit line.
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
#separate the poles for the correlation
#keeps trying to be a string array for some reason and not having this line is bad
print(weh[0:20])
print(np.shape(latitude), np.shape(weh))
m, b = np.polyfit(latitude1, weh1, 1)
otherfit1 = stats.linregress(latitude1, weh1)
print("slope: ", otherfit1[0], " intercept: ", otherfit1[1], " r-value: ", otherfit1[2], " p-value: ", otherfit1[3], " stderror: ", otherfit1[4])
print(m, b)
plt.plot(latitude1, weh1, 'o')
plt.plot(latitude1, m*latitude1 + b, label = ('Least Squares Linear regression, WEH = -3.15(latitude) - 172'))
plt.xlabel('Latitude in degrees')
plt.ylabel('Water Equivalent Hydrogen in ppm')
plt.title('Lunar Prospector Neutron Spectrometer South Pole Results')
plt.legend()
plt.show()
m, b = np.polyfit(latitude2, weh2, 1)
otherfit2 = stats.linregress(latitude2, weh2)
print("slope: ", otherfit2[0], " intercept: ", otherfit2[1], " r-value: ", otherfit2[2], " p-value: ", otherfit2[3], " stderror: ", otherfit2[4])
print(m, b)
plt.plot(latitude2, weh2, 'o')
plt.plot(latitude2, m*latitude2 + b, label = ('Least Squares Linear regression, WEH = 3.60(latitude) + 212'))
plt.xlabel('Latitude in degrees')
plt.ylabel('Water Equivalent Hydrogen in ppm')
plt.title('Lunar Prospector Neutron Spectrometer North Pole Results')
plt.legend()
plt.show()
#I bet if I average each latitude there will be a really good correlation.
#wehDf = pd.DataFrame(data = wehArray)
#woohoo this works!! :)
'''# TODO: calculate the average weh at each latitude and get iiiit.
First I need rows where latitude changes. I was mispelling the variable names all last night :/
'''
#rowlatChange1 = np.array([0])
def findlatchanges(latitude):
    rowlatChange = np.array([])
    #making this array not include the 0 index makes the next function easier to write
    counter = 0
    previous = latitude[0]
        #making this array not include the 0 index makes the next function easier to write
    for row in latitude:
        if(not row == previous):
            rowlatChange = np.append(rowlatChange, counter)
            #the counters keep replacing each other. weird.
            print(counter, rowlatChange)
            print("different latitude detected")
        counter = counter+1
        previous = row
    return rowlatChange
rowlatChange1 = findlatchanges(latitude1)
print(rowlatChange1, "I am the first", len(rowlatChange1))
rowlatChange2 = findlatchanges(latitude2)
print(rowlatChange2, "I am the second", len(rowlatChange2))
#now to find the average WEH at each latitude then do the regression using that. Or do I want total? Hmm. Definitely mean.
def findAverageWEH(rowlatChange, weh):
    wehAverage= np.array([])
    previous = 0
    for index in rowlatChange:
        index = int(index)
        average = sum(weh[previous:index-1])/(index+1-previous)
        wehAverage = np.append(wehAverage, average)
        previous = index
    return wehAverage
def findNewLats(rowlatChange, latitude):
    NewLats = np.array([])
    for index in rowlatChange:
        index = int(index)
        NewLats = np.append(NewLats, latitude[index])
    return NewLats
wehAverage1 = findAverageWEH(rowlatChange1, weh1)
NewLats1 = findNewLats(rowlatChange1, latitude1)
print(wehAverage1, len(NewLats1), " length of wehAverages: ", len(wehAverage1))
wehAverage2 = findAverageWEH(rowlatChange2, weh2)
NewLats2 = findNewLats(rowlatChange2, latitude2)
print(wehAverage2, len(NewLats2), " length of wehAverages: ", len(wehAverage2))
def makeGraph(wehAverage, NewLats):
    fit = np.polyfit(NewLats, wehAverage, 4)
    #otherfit1 = stats.linregress(NewLats, wehAverage)
    #print("slope: ", otherfit1[0], " intercept: ", otherfit1[1], " r-value: ", otherfit1[2], " p-value: ", otherfit1[3], " stderror: ", otherfit1[4])
    print(fit)
    plt.plot(NewLats, wehAverage, 'o')
    plt.plot(NewLats, (fit[0]*(NewLats**4))+(fit[1]*(NewLats**3))+(fit[2]*(NewLats**2))+(fit[3]*(NewLats))+(fit[4]), label = ('Quartic fit of Average WEH as a function of latitude'))
    print((100*fit[0])/100, 'L^4 + ', int(100*fit[1])/100, 'L^3 + ', int(100*fit[2])/100, 'L^2', 'L^3 + ', int(100*fit[3])/100, 'L + ' 'L^3 + ', int(100*fit[4])/100)
    plt.xlabel('Latitude in degrees')
    plt.ylabel('Average Water Equivalent Hydrogen in ppm')
    plt.title('Lunar Prospector Neutron Spectrometer North Pole Results')
    plt.legend()
    plt.show()
makeGraph(wehAverage1, NewLats1)
makeGraph(wehAverage2, NewLats2)
'''
#I can't remember what this is but I presumably commented it out because it doesn't work
m, b = np.polyfit(NewLats1, wehAverage1, 1)
otherfit1 = stats.linregress(NewLats1, wehAverage1)
print("slope: ", otherfit1[0], " intercept: ", otherfit1[1], " r-value: ", otherfit1[2], " p-value: ", otherfit1[3], " stderror: ", otherfit1[4])
print(m, b)
plt.plot(NewLats1, wehAverage1, 'o')
plt.plot(NewLats1, m*NewLats1 + b, label = ('Least Squares Linear regression, WEH = (latitude) - '))
plt.xlabel('Latitude in degrees')
plt.ylabel('Average Water Equivalent Hydrogen in ppm')
plt.title('Lunar Prospector Neutron Spectrometer South Pole Results')
plt.legend()
plt.show()
m, b = np.polyfit(NewLats2, wehAverage2, 1)
otherfit2 = stats.linregress(NewLats2, wehAverage2)
print("slope: ", otherfit1[0], " intercept: ", otherfit1[1], " r-value: ", otherfit1[2], " p-value: ", otherfit1[3], " stderror: ", otherfit1[4])
print(m, b)
plt.plot(NewLats2, wehAverage2, 'o')
plt.plot(NewLats2, m*NewLats2 + b, label = ('Least Squares Linear regression, WEH = (latitude) -'))
plt.xlabel('Latitude in degrees')
plt.ylabel('Average Water Equivalent Hydrogen in ppm')
plt.title('Lunar Prospector Neutron Spectrometer South Pole Results')
plt.legend()
plt.show()'''
'''
rowlatChange2 = np.array([0])
counter = 0
previous = 0
for row in latitude2:
    if(not row == previous):
        rowlatChange2 = np.append(rowlatChange2, counter)
        print(counter, rowlatChange2)
        print("different latitude detected")
    counter = counter+1
    previous = row
'''
