import os
import re
import codecs

from linne.analyzer.audacity import LabelFile
from linne.analyzer.zhuyin import Phonetic

class Label:
    def __init__(self):
        pass

class Record:
    # A helper class to process a record in oto.ini by reading the 
    # data from label file
    def __init__(self,phonetic):
    
        self.label = Label()
        self.label.consonant = None
        self.label.vowel = None
        self.label.phonetic = None
        self.phonetic = phonetic
        self.items = []
        self.finished = False
        self.data = []
        
    def append(self,data):
        """ Append a label record.
        """
        def adjust(p):
            # Convert to ms
            return [float(p[0]) * 1000  , float(p[1])  * 1000 , p[2] ]

        data = adjust(data)
        symbol = re.sub("[\[\]]","",data[2])
        if unicode(self.phonetic) == symbol:
            self.label.phonetic = data
        elif self.phonetic.isConsonant(symbol):
            self.label.consonant = data
        elif self.phonetic.isVowel(symbol):
            self.label.vowel = data
        else:
            raise RuntimeError('A symbol is not existed. Corrupted data?')
            
        self.items.append(data)
        if ( self.phonetic.isMono() 
            or len(self.items) == 3 ):
            self._setup()
            (ret , msg) = self.validate()
            if not ret:
                print "[Warning] " + msg
            self.finished = True

    def validate(self):
        ret = True
        msg = ""
        if len(self.items) == 3:
            if ((self.label.consonant[0] != self.label.phonetic[0]) or 
                (self.label.vowel[1] != self.label.phonetic[1])  or 
                (self.label.consonant[1] != self.label.vowel[0])):
                msg = "Record of %s is not aligned!" % self.label.phonetic[2]
                ret = False
        elif len(self.items) != 1:
            msg = "Invalid input size. Data : %s" % self.items 
            ret = False
        
        return (ret,msg)

    def _setup(self):
    
        if len(self.items) == 3:
            self.data = [self.label.phonetic[2] , 
                          self.label.phonetic[0], 
                          self.label.consonant[1] - self.label.phonetic[0] , 
                          -(self.label.phonetic[1] - self.label.phonetic[0]) ,
                          0,0] 
        else:
            # Mono
            if self.phonetic.hasConsonant():
                consonant = self.label.phonetic[1] - self.label.phonetic[0]
                vowel = 0
            else:
                consonant = 0
                vowel = -(self.label.phonetic[1] - self.label.phonetic[0])
            
            self.data = [self.label.phonetic[2] , 
                          self.label.phonetic[0], 
                          consonant , 
                          vowel,
                          0,0] 

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
            record = Record(p)
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
