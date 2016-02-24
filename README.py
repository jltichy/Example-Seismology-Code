# example_code
# This code was shared with me as an example of how to write in Python.

# look up a python dot operator -- a dot is a connection between attributes, ex. dog.color = "black"
# read about modules, classes, and objects -- Modules are python files that contain functions and variables.  You can access the contents of a module with dot operators.  Once you define a function in a module, you can access it like this: Module = Example, function = TestFunction, Example.TestFunction.  Classes are mini modules.  You can only have one module per program, but you can have multiple classes.  Objects are unique instances of data that include numbers and the method to get those numbers.

# this is the "shebang" line -- it defines the document to be python code -- This is only required in the Linux Environment, not if using Microsoft.
#!/usr/bin/env python

# import something called "glob" and something called "sys".  "glob" is a python code for matching filenames.  "sys" is a python code for "system specific parameters."
import glob
import sys

# import something called "numpy" - turns out this is a python code package for scientific computing. "np" is what numpy will be called.  This is pronounced NUM-PYE.
import numpy as np

# ok. this is the seismology data.  ObsPY is a Python package for observing seismology data.  It looks like you can use "import module" or "from module import foo" interchangeably.  get_NLNM is a function that returns periods and psd values for the New Low Noise Model (seismology data)
from obspy.signal.spectral_estimation import get_NLNM

# this is a package that allows you to plot something, just like in matlab
import matplotlib.pyplot as plt

# a multiprocessing tool allows you to use multiple processors to do a function.  The pool class represents a pool of worker processes.  I think this allows you to choose which processors are used to do the function (CONFIRM WITH ADAM!)
from multiprocessing import Pool

# this is something for when the program is debugged (maybe it's the output if there is a bug??).  "debug" is the variable name
debug = True

# Grab the NLNM and get power and per in the microseism band.  The minimum period is 5 and the maximum period is 10.
minper = 5.
maxper = 10.

# I don't know what "per" is, but NLNM is the seismology data -- Maybe this is creating a matrix of the data.  
per, NLNM = get_NLNM()

# These are codes to create subsets of data from the seismology data.
micNLNM = NLNM[(minper <= per) & (per <= maxper)]
micper = per[(minper <= per) & (per <= maxper)]

# Creating a new variable called "fDead" -- What is 'DeadChannelsAGAIN' or 'w'?? -- Ask Adam!
fDead = open('DeadChannelsAGAIN','w')

# defining a new function called "checkifdead", but what is "curfile"? current file
# look up try and except in google -- has to do with errors - Try is like a loop, except is for exceptions
# look up open - opens something
# look up brackets [] - The [] is called a list and {} is called a dictionary.  Use [] to add elements and {} to name specific things. 
# look up line, strip, and split -- A split will divide up a line (splits are like commas or spaces); a strip will remove excessive white space.
# look up minper and maxper - minimum period and maximum period
# look up staper 
def checkifdead(curfile):
    try:
        with open(curfile,'r') as f:
            staper=[] #station period??
            stapow=[] #station power?
            for line in f:    # this reads every line of the file into an array
                line = (line.strip()).split(',')
                if (1./float(line[1]) >= minper) and (1./float(line[1]) <= maxper): #float is a python class that allows for NaN, Inf, and -Inf when doing arithmetic
                    staper.append(1./float(line[1])) #append adds an item to the end of a list (the list in this case is staper)
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
