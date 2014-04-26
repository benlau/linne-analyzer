import csv
from linne.analyzer.audacity import LabelFile
from linne.analyzer.sampling import SamplingFile
from linne.analyzer.phonetic import Ipa

class Sample:
    def __init__(self):
        self.phonetic = None
        self.timestamp = None
        self.zcr = None
        self.rms = None
        self.variance = None

class Dataset:
    # Dataset is a set of files associated with an audio file.
    # The name of a dataset is same as the audio file.
    
    # This class is an utility to manage this set of files
    
    def __init__(self,name):
        self.name = name
        
        # A list of word(formed by phonetic)
        self.charList = []
        self._phoneticList = []
        
        self._labelFile = None
        
    def open(self):
        charFile = open(self.name+".txt","r")
        line = charFile.readline()
        self.charList = [unicode(item,"utf-8") for item in line.split(" ")]
        
        self._labelFile = LabelFile()
        self._labelFile.open(self.name + "-label.txt")
        
        self._samplingFile = SamplingFile()
        self._samplingFile.open(self.name + "-sampling.csv")
        
        self._createPhoneticList()
        
    def phoneticList(self):
        return self._phoneticList
                        
    def _createPhoneticList(self):
        for row in self._labelFile:
            sample = Sample()
            sample.timestamp = row[0]
            sample.phonetic = Ipa.simplifySymbol(row[2])
            
            record = self._samplingFile.search(float(row[0]));
            sample.zcr = float(record["ZCR"])
            sample.variance = float(record["Spectrum Variance"])
            sample.rms = float(record["RMS"])
            sample.str = float(record["STE"])
            
            self._phoneticList.append(sample)
            
        

        
        
