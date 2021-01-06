import numpy as np
import matplotlib.pyplot as plt
'''
We will use an array named timeArray that will consist of the values of t we
will use to compute each trigonometric sequence. We use the makeTimes function
to compute the array of time intervals, then compute arrays for the coefficient
and multiply them using the numpy multiply function.
'''
def useInterval(fx,fy,phi, Ax, Ay,deltaT, N):
    timeArray = makeTimes(deltaT, N)
    #calculate the array for t
    x, y, z = list(range(N+1)), list(range(N+1)), list(range(N+1))
        #compute the sinusoids and multiply by the coefficients
    for i in  list(range(N+1)):
        x[i] = np.round(Ax*np.cos(2*np.pi*fx*timeArray[i]),6)
        y[i] = np.round(Ay*np.sin(2*np.pi*fy*timeArray[i]+phi),6)
        z[i] = x[i]+y[i]
    #output the sinusoids to a .txt file
    outX = open('x of t.txt',"w+")
    outX.write(str(x))
    outY = open('y of t.txt',"w+")
    outY.write(str(y))
    outZ = open('z of t.txt',"w+")
    outZ.write(str(z))
    return x, y, z
'''
deltaT is the size of each interval in the time sequence we will use to compute
the trigonometric functions, and N is the number of those intervals. times is
the array containing the time sequence we will use to computer the trigonometric
functions, and we do this by making times and deltaT into lists, then use
multiply to get an array containing the product of each of their elements.
'''
def makeTimes(deltaT, N):
    times = list(range(N+1))
    deltaT = [deltaT]*(N+1)
    for i in range(N+1):
        times[i] = deltaT[i]*times[i]
    return times
'''
Plot t versus z(t) using the function useInterval
'''
def makeZtPlot(fx,fy,phi, Ax, Ay,deltaT, N):
    x, y, z = useInterval(fx,fy,phi, Ax, Ay,deltaT, N)
    t = makeTimes(deltaT, N)
    plt.ylabel('z(t)')
    plt.xlabel('t')
    title =  'fx = ' + str(fx) + ' fy = ' + str(fy) + ' phi = ' + str(phi)
    title =  title + " Ax = " + str(Ax) + " Ay = " + str(Ay)+  " deltaT =  "
    title = title + str(deltaT) +" N = " + str(N)
    plt.title(title)
    plt.plot(t,z)
    plt.show()
'''
Plot x(t) versus y(t) using the function useInterval
'''
def makeXYPlot(fx,fy,phi, Ax, Ay,deltaT, N):
    x, y, z = useInterval(fx,fy,phi, Ax, Ay,deltaT, N)
    plt.ylabel('y(t)')
    plt.xlabel('x(t)')
    title =  'fx = ' + str(fx) + ' fy = ' + str(fy) + ' phi = ' + str(phi)
    title =  title + " Ax = " + str(Ax) + " Ay = " + str(Ay)+  " deltaT =  "
    title = title + str(deltaT) +" N = " + str(N)
    plt.title(title)
    plt.plot(x,y)
    plt.show()
'''
This function will make the XY plots requested by the assignment to determine
the relationship between fx and fy
'''
def makeXYPlots(resolution, length):
    makeXYPlot(np.pi, 1, 0, 1, 1, resolution, int(length/2))
    makeXYPlot(1, np.pi, 0, 1, 1, resolution, int(length/2))
    makeXYPlot(10, 1, 0, 1, 1, int(resolution/2), length*2)
    makeXYPlot(1, 1, 0, 1, 1, resolution, length)
    makeXYPlot(1, 10, 0, 1, 1, resolution, length)
#makeXYPlots(2**-16, 2**19)
#the resolution and length that will allow for high resolution graphs
'''
This call to Zt will show the phenomenon of beats where
w1 = 2pifx and w2 = 2pify
We will make an array of nearby but distinct values of fx and fy then plot
t vs z. Then we will plot many cycles at the frequency (w1+w2)/2 and
a few cycles at the frequency (w1-w2)/2.
'''
makeZtPlot(1, 1+2**-3, np.pi/2, 1, 1, 2**-10, 2**15)
makeZtPlot(2, 0, 0, 1, 1, 2**-10, 2**15)
makeZtPlot(2+2**-2, 0, 0, 1, 1, 2**-10, 2**13)
