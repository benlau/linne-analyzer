import os
import re

from linne.analyzer.sound import Table as SoundTable
from linne.analyzer.sound import Sound
from linne.analyzer.dataset import Dataset
from linne.analyzer.phonetic import Ipa
import numpy

class Stat:
    def __init__(self):
        self.sound = None
        self.data = []
        self.threshold = None       
        
    def read(self,sample):
        # Read from sample
        filter = self.sound.filter
        if  filter == "RMS":
            self.data.append(sample.rms)
        elif filter == "SV":
            self.data.append(sample.variance)
        elif filter == "ZCR":
            self.data.append(sample.zcr)
        elif filter == "STE":
            self.data.append(sample.ste)
        else:
            print "Unknown filter type : %s" % filter
            
    def calc(self):
        # Calculate the new threshold value
        if len(self.data) > 0:
            self.threshold = numpy.average(numpy.array(self.data))
        return self.threshold

changed = False # It will set to True if the result should be saved.

table = SoundTable()

# For collect the phonetic data from sampling file
stat = {}

print "Reading sound.csv..."
try:
    table.open("sound.csv")
except IOError,e:
    print "Warn: Fail to open %s. " % ("sound.csv")   
    changed = True
    
print "%d of record(s) read." % len(table)

for sound in table:
    item = Stat()
    item.sound = sound
    item.threshold = sound.threshold
    stat[sound.phonetic] = item

datasetList = []

cwd = os.getcwd()
files = os.listdir(cwd)

for f in files:
    filename , ext = os.path.splitext(f)
    if ext == ".wav":
        print "Reading %s dataset..." % filename
        dataset = Dataset(filename)
        try:
            dataset.open()
            datasetList.append(dataset)
        except IOError,e:
            print e

# Collecting threshold value from dataset
for dataset in datasetList:
    sampleList = dataset.phoneticList()
    for sample in sampleList:
        phonetic = Ipa.simplifySymbol(sample.phonetic)
        if not stat.has_key(phonetic):
            print "Warning! Phonetic not found in sound.csv: %s" % sample.phonetic
            print "It will be added to sound.csv"
            item = Stat()
            item.sound = Sound(
                phonetic = phonetic,
                ipa = phonetic,
                filter = "RMS", # Just the default value. It should not be used.
                threshold = 0,
                remarks = "Added by linne-tuner. Please update the filter type"
            )
            item.threshold = item.sound.threshold
            stat[phonetic] = item
            table[phonetic] = item.sound
            changed = True
        stat[phonetic].read(sample)

print "Calculate the new threshold value..."

for key in stat:
    s = stat[key]
    old = s.threshold
    new = s.calc()

    if str(old) != str(new):
        print "%s : %f -> %f" % (key , old,new)
        s.sound.threshold = s.threshold
        changed = True
        
if changed:
    print "Saving to sound.csv..."
    table.save("sound.csv")
else:
    print "Nothing Changed. Skip saving"
print "Done"
