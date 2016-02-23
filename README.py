# example_code
# This code was shared with me as an example of how to write in Python.

#!/usr/bin/env python

# import something called "glob" and something called "sys", presumably these are seismology things...no "glob" is a python code for matching filenames.  I don't know what this means.  "sys" is a python code for "system specific parameters," but I don't know what this means either.
import glob
import sys

# import something called "numpy" - turns out this is a python code package for scientific computing. "np" is what numpy will be called.
import numpy as np

# ok. this is the seismology data
from obspy.signal.spectral_estimation import get_NLNM

# this is a package that allows you to plot something, just like in matlab
import matplotlib.pyplot as plt

# a multiprocessing tool allows you to use multiple processors to do a function
from multiprocessing import Pool

# this is something for when the program is debugged (maybe it's the output if there is a bug??)
debug = True

# Grab the NLNM and get power and per in the microseism band
minper = 5.
maxper = 10.

# I don't know what "per" is, but NLNM is the seismology data -- Maybe this is creating a matrix of the data.  
per, NLNM = get_NLNM()

# These are codes to create subsets of data from the seismology data.
micNLNM = NLNM[(minper <= per) & (per <= maxper)]
micper = per[(minper <= per) & (per <= maxper)]

# Creating a new variable called "fDead"
fDead = open('DeadChannelsAGAIN','w')

# defining a new function called "checkifdead", but what is "curfile"? current file
# look up try and except in google -- has to do with errors
# look up open
# look up brackets []
# look up line, strip, and split
# look up minper and maxper - minimum period and maximum period
# look up staper 
def checkifdead(curfile):
    try:
        with open(curfile,'r') as f:
            staper=[]
            stapow=[]
            for line in f:    
                line = (line.strip()).split(',')
                if (1./float(line[1]) >= minper) and (1./float(line[1]) <= maxper):
                    staper.append(1./float(line[1]))
                    stapow.append(float(line[0]))
        staper = np.asarray(staper)
        stapow = np.asarray(stapow)
        NLNMinterp = np.interp(1./staper,1./micper,micNLNM)
        #plt.figure()
        #p1=plt.semilogx(micper,micNLNM)
        #p2=plt.semilogx(staper,stapow,'k')
        #p3=plt.semilogx(staper,NLNMinterp,'r')
        #plt.show()
        dbdiff = 1./float(len(NLNMinterp))*sum(stapow-NLNMinterp)
        if dbdiff <= 0.:
            result = curfile + ' is dead with dB difference ' + str(dbdiff) + '\n'
        else:
            result = ''
    except:
        print curfile + ' is bad'
        result = curfile + ' is bad\n'
    return result

# this is where the code actually starts
# pool: from a multiprocessing package, we import something called pool -- look this up in google
# glob.glob pulls everything that is from test archive with a certain name
pool = Pool(10)
for year in range(1989,2016):
    for days in range(1,367):
        print 'On ' + str(year) + ' ' + str(days).zfill(3)
        files = glob.glob('/TEST_ARCHIVE/PSDS/*/' + str(year) + '/PSD*' + str(days).zfill(3)) 
        p = pool.map(checkifdead,files)
        for res in p:
            if len(res) > 1:
                fDead.write(res)

# closing of the script??
fDead.close()
