"""
Take the sampling data from input audio and save the result in 
csv format
"""

from pymir import AudioFile
import math
import csv
import sys
import os

from linne.analyzer.utils import slidingWindow,frange

def writeCsv(sampling,frames,output):

    csvfile = open(output, 'wb');

    writer = csv.writer(csvfile, delimiter=',',
                    quotechar='"', quoting=csv.QUOTE_MINIMAL);

    writer.writerow(["Timestamp",
                       "ZCR",
                       "Spectrum Variance",
                       "RMS"]);

    for i  in xrange(0,len(frames)):
        timestamp = "%0.3f" % (sampling[i] / float(freq))
        row = [timestamp,
               frames[i].zcr(),
               frames[i].spectrum().variance(),
               frames[i].rms()];
        writer.writerow(row);

    print "The result is written on %s" % output

try:
	target = sys.argv[1]
except:
	print "Usage: %s [wav file] " % sys.argv[0]
	exit(0)

#TODO read from configuration file
frameSize = 882 # 20ms
freq = 44100

token = os.path.basename(target).split(".")
filename = ".".join(token[0:len(token)-1])

wav = AudioFile.open(target)

# Data set 2 - Using sliding Window

sampling = [s for s in frange(frameSize/4.0,len(wav),frameSize/4.0)]
frames = slidingWindow(wav,sampling,frameSize)
output = '%s-sampling.csv' % filename
writeCsv(sampling,frames,output)




