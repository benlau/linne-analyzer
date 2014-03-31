import os
import re
import codecs

from linne.analyzer.audacity import LabelFile
from linne.analyzer.phonetic import Ipa

class Label:
    def __init__(self):
        pass

class LabelFinder:
    """ Perform a column based string matching from label list"
    """
    def __init__(self,pattern):
        self.pattern = pattern
        self.target = ""
        
    def match(self,record):
        self.target = self.target + record[2]
        if not self.pattern.startswith(self.target):
            raise RuntimeError('The symbol do not match. Corrupted data?')
        if self.pattern == self.target:
            return True
        return False

    def find(self,data,start):
        i = start
        while True:
            self.target = self.target + data[i][2]
            if not self.pattern.startswith(self.target):
                msg = u'Searching for %s but it found %s. Corrupted data?' % (self.pattern,self.target)
                raise RuntimeError(msg)
            if self.pattern == self.target:
                return (start,i+1)
            i = i + 1

class Record:
    """ A helper class to process a record in oto.ini by reading the 
     data from label file.
    
     Since a record in oto.ini require multiple line information 
     from label file. It will keep reading from the label file ,
     once the information is enough , the "finished" flag 
     will be set.
     
     Args:
        phonetic: A Phonetic class instance
        lastSymbol: The last symbol in previous record

     
     """
    def __init__(self,phonetic,lastSymbol):
    
        self.label = Label()
        self.label.consonant = None
        self.label.vowel = None
        self.label.phonetic = None
        self.phonetic = phonetic
        self.lastSymbol = lastSymbol
        #self.items = []
        #self.finished = False
        self.data = []
        
    def read(self,labels,index):
        """ Read from label file to complete the record
        @param labels: List of label record
        """
        phonetic = u""
        data = []
        
        finder = LabelFinder(unicode(self.phonetic))
        (s,e) = finder.find(labels,index)
        data = labels[0:e]

        if not self.validateInputLabels(data):
            raise RuntimeError("Invalid data")

        self.label.phonetic = (data[0][0] , data[len(data) - 1][1], phonetic) 
            
        p = range(0,len(data))
        vowel = 0
        if self.phonetic.hasConsonant():
            finder = LabelFinder(self.phonetic.consonant)
            (s,e) = finder.find(data,0)
            self.label.consonant = (data[s][0] , data[e-1][1],self.phonetic.consonant)
            vowel = e
        
        finder = LabelFinder(self.phonetic.vowel)
        (s,e) = finder.find(data,vowel)
        self.label.vowel = (data[s][0] , data[e-1][1],self.phonetic.vowel)
        self._process()
                
        
    def validateInputLabels(self,data):
        """
        Validate the label
        """
        
        phonetic = u''.join([row[2] for row in data])
        if phonetic != unicode(self.phonetic):
            return False
        
        for i in range(0,len(data) - 1):
            if data[i][0] >= data[i][1]:
                print "Invalid record : ", data
                return False
            if data[i][1] != data[i+1][0]:
                print "Invalid record : ", data
                return False
        
        return True
        
        
    def append(self,data):
        """ Append a label record
        @deprecated
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
            self._process()
            (ret , msg) = self.validate()
            if not ret:
                print "[Warning] " + msg
            self.finished = True

    def validate(self):
        """
        @deprecated
        """
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

    def _name(self,name):
        """ Re-format the "name" of the record. 
        """
        ret = name
        if self.lastSymbol != u"":
            ret = "%s %s" % (self.lastSymbol , name)
        return ret

    def _process(self):
        """
        Process the input items and write the result to "data"
        """
        #if len(self.items) == 3:
        if self.label.consonant != None and self.label.vowel != None:
            self.data = [self._name(self.label.phonetic[2]) , 
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
            
            self.data = [self._name(self.label.phonetic[2]) , 
                          self.label.phonetic[0], 
                          consonant , 
                          vowel,
                          0,0] 

def adjustLabel(p):
    # Convert label record to be based on ms
    return [float(p[0]) * 1000  , float(p[1])  * 1000 , p[2] ]


def process(phoneticFile,labelFile):
        format="%s=%s,%d,%d,%d,%d,%d\n"
        wav = labelFile.replace("-label.txt",".wav")

        print "Reading %s..." % phoneticFile
        f = codecs.open(phoneticFile,"r","utf-8")
        line = f.readline()
        phonetics = [ Ipa(item.strip()) for item in line.split(" ") ]       

        print "Reading %s..." % labelFile
        f = LabelFile()
        f.open(labelFile)
        
        labels = [adjustLabel(l) for l in f] 
        i = 0
        lastSymbol = u""

        for p in phonetics:
            print "Processing %s..." % unicode(p)
            record = Record(p,lastSymbol)
            record.read(labels,i)
            i = i + len(p)
#            while not record.finished:
#                row = iterator.next()
#                record.append(row)
            t = [wav,] + record.data
            
            lastSymbol = p.last()
            oto.write(format % tuple(t))
         

oto = codecs.open("oto.ini","w","utf-16")


cwd = os.getcwd()
files = os.listdir(cwd)

try:
    for f in files:
        filename , ext = os.path.splitext(f)
        if re.match(".*-label\.txt$",f):
            input = f.replace("-label.txt",".txt")
            process(input,f)
            
    print "Result is written to oto.ini"
except RuntimeError,e:
    print unicode(e.message).encode('utf-8')
