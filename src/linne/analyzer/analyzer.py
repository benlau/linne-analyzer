import os
import re
import csv
import sys
import codecs
import traceback

import numpy
from linne.analyzer.sound import Table as SoundTable
from linne.analyzer.sound import Sound
from linne.analyzer.sampling import SamplingFile
from linne.analyzer.audacity import LabelFile
from linne.analyzer.zhuyin import Phonetic as Word

class Filter:
    def __init__(self):
        self._index = 0
      
    def process(self,soundTable,sampling,words):
        self._index = 0
        self._soundTable = soundTable
        self._sampling = sampling
        
        try:
            for word in words:
                points = [] 
                #phonetics = [word.consonant , word.vowel[0] ]
                phonetics = word.toKeyList()
                for phonetic in phonetics:
                    try:
                        res = self.search(phonetic)["Timestamp"]
                        points.append(res)
                    except KeyError:
                        print "[Error] %s is not existed in sound table(sound.csv)" %  phonetic
                    
                points.append(self.lowPass()["Timestamp"])
                word.points = points
        except IndexError:
            print "[Error] Unexpected termination. Not all phonetic is found."
            #exc_type, exc_value, exc_traceback = sys.exc_info()
            #traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
		

    def search(self,phonetic):
        print "Searching %s..." % phonetic
        s = self._soundTable[phonetic]
        while not s.passThreshold(self._sampling[self._index]):
            self._index = self._index+1
        frame = self._sampling[self._index]
        self._index = self._index + 1
        return frame
        
    def lowPass(self):
        # A low pass filter on RMS. A dirty hack for right-endpoint searching
        while self._sampling[self._index]["RMS"] > 0.03:
            self._index = self._index+1
        frame = self._sampling[self._index]
        self._index = self._index + 1
        return frame

try:
	target = sys.argv[1]
except:
	print "Usage: %s name_of_sample " % sys.argv[0]
	exit(0)

table = SoundTable()
print "Reading sound.csv..."
table.open("sound.csv")

samplingFile = SamplingFile()

filename = target + "-sampling.csv"
print "Reading %s..." % filename
samplingFile.open(filename)

filename = target + ".txt"
print "Reading %s..." % filename

f = codecs.open(filename,"r","utf-8")
line = f.readline()
words = [ Word(item.strip()) for item in line.split(" ") ]

filter = Filter()
filter.process(table,samplingFile,words)

labelFile = LabelFile()

for word in words:
    for row in word.toLabel():
        labelFile.append(row)

filename = target + "-label.txt"
print "Writing to %s..." % filename
    
labelFile.save(filename)

