import os
import re
import codecs

from linne.analyzer.audacity import LabelFile

class Record:
    # A helper to process a record in oto.ini by reading the 
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


def processLabelFile(filename):
    file = LabelFile()
    file.open(filename)
    wav = filename.replace("-label.txt",".wav")
    format="%s=%s,%d,%d,%d,%d,%d\n"
    record = Record()
    for row in file:
        record.append(row)
        if record.finished:
            t = [wav,] + record.data
            record = Record()
            oto.write(format % tuple(t))

oto = codecs.open("oto.ini","w","utf-8")


cwd = os.getcwd()
files = os.listdir(cwd)



for f in files:
    filename , ext = os.path.splitext(f)
    if re.match(".*-label\.txt$",f):
        print "Reading %s..." % filename
        processLabelFile(f)
        
print "Result is written to oto.ini"
