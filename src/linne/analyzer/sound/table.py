# Sound Table Management

import csv
import codecs
from sound import Sound


class Iterator:
    def __init__(self,table):
        self._table = table
        self._keys = [k for k in table._data]
        self._index = 0
        
    def next(self):
        try:
            key = self._keys[self._index]
            ret = self._table._data[key]
            self._index = self._index + 1
        except IndexError:
            raise  StopIteration
        return ret

class Table:
    def __init__(self):
        self._data = {}
        self._header = None

    def __iter__(self):
        return Iterator(self)

    def __len__(self):
        return len(self._data)
        
    def __getitem__(self,key):
        return self._data[key]
        
    def __setitem__(self,key,value):
        self._data[key] = value
    
    def open(self,filename):
        f = open(filename,"rw")
        reader = csv.reader(f,delimiter=",")
        self._data = {}
        for row in reader:
            if self._header == None:
                self._header = row
                continue
            urow = []
            for cell in row:
                urow.append(unicode(cell,"utf-8"))
            s = Sound()
            s.phonetic = urow[0]
            s.ipa = urow[1]
            s.filter = urow[2]
            s.threshold = float(urow[3])
            s.remarks = urow[4]
            self._data[s.phonetic] = s
        return self._data

    def save(self,filename):
        f = open(filename,"wb")
        
        writer = csv.writer(f,csv.excel)
        writer.writerow(self._header)
        for key in self._data:
            s = self._data[key]
            row = [s.phonetic,
                               s.ipa,
                               s.filter,
                               s.threshold,
                               s.remarks];
            row = [ unicode(x).encode("utf-8") for x in row]
            writer.writerow(row)
