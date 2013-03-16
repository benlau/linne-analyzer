import os
import re
import codecs

from linne.analyzer.audacity import LabelFile
from linne.analyzer.zhuyin import Phonetic

class Record:
    # A helper class to process a record in oto.ini by reading the 
    # data from label file
    def __init__(self):
    
        self.consonant = None
        self.vowel = None
        self.phonetic = None
        self.items = []
        self.finished = False
        self.data = []
        
    def append(self,data):
        self.items.append(data)
        if not re.match("\[.*\]",data[2]):
            self._setup()
            (ret , msg) = self.validate()
            if not ret:
                print "[Error] " + msg
            self.finished = True
                

    def validate(self):
        ret = True
        msg = ""
        if len(self.items) == 3:
            if (self.consonant[0] != self.phonetic[0]) or (self.vowel[1] != self.phonetic[1])  or (self.consonant[1] != self.vowel[0]):
                msg = "Record of %s is not aligned!" % self.phonetic[2]
                ret = False
        elif len(self.items) != 1:
            msg = "Invalid input size. Data : %s" % self.items 
            ret = False
        
        return (ret,msg)

    def _setup(self):
        def adjust(p):
            return [float(p[0]) * 1000  , float(p[1])  * 1000 , p[2] ]
    
        if len(self.items) == 3:
            (self.consonant ,self.vowel , self.phonetic)  = [adjust(item) for item in self.items ]           
            self.data = [self.phonetic[2] , self.phonetic[0], self.consonant[0] - self.phonetic[0] , -(self.phonetic[1] - self.phonetic[0]) ,0,0] 
        else:
            self.phonetic  = adjust(self.items[-1])
            self.data = [self.phonetic[2] , self.phonetic[0], 0 , self.phonetic[1] - self.phonetic[0],0,0] 

def process(phoneticFile,labelFile):
        format="%s=%s,%d,%d,%d,%d,%d\n"
        wav = labelFile.replace("-label.txt",".wav")

        print "Reading %s..." % phoneticFile
        f = codecs.open(phoneticFile,"r","utf-8")
        line = f.readline()
        phonetics = [ Phonetic(item.strip()) for item in line.split(" ") ]       
        
        f = LabelFile()
        f.open(labelFile)

        iterator = iter(f)
        
        for p in phonetics:
            record = Record()
            while not record.finished:
                row = iterator.next()
                record.append(row)
            t = [wav,] + record.data
            oto.write(format % tuple(t))
         

oto = codecs.open("oto.ini","w","utf-8")


cwd = os.getcwd()
files = os.listdir(cwd)

for f in files:
    filename , ext = os.path.splitext(f)
    if re.match(".*-label\.txt$",f):
        input = f.replace("-label.txt",".txt")
        process(input,f)
        
print "Result is written to oto.ini"
