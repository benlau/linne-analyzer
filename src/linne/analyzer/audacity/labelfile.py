import csv
import sys
import os

class Iterator:
    def __init__(self,labelfile):
        self._labelfile = labelfile
        self._index = 0
        
    def next(self):
        try:
            ret = self._labelfile[self._index]
            self._index = self._index + 1
        except IndexError:
            raise  StopIteration
        return ret

class LabelFile:
    
    def __init__(self):
        self._data = []
        self._file = None
        pass
        
    def __iter__(self):
        return Iterator(self)
        
    def __len__(self):
        return len(self._data)
        
    def __getitem__(self,idx):
        return self._data[idx]
        
    def __setitem__(self,key,value):
        self._data[key] = value
        
    def open(self,file):
        self._file = open(file,"rw")
        reader = csv.reader(self._file,delimiter="\t")
        self._data = []
        for row in reader:
            tmp = []
            for cell in row:
                tmp.append(unicode(cell,"utf-8"))
            self._data.append(tmp)
        return self._data
        
    def save(self,filename):
        f = open(filename,"wb")
        
        writer = csv.writer(f,delimiter="\t")
        for row in self._data:
            row = [ unicode(x).encode("utf-8") for x in row]
            writer.writerow(row)
        
    def append(self,data):
        self._data.append(data)

