import csv

class SamplingFile:
    # Utility to read sampling file
    def __init__(self):
        pass
        
    def __len__(self):
        return len(self._data)
        
    def __getitem__(self,idx):
        # It will return a dict object with field equal to the 
        # header of the CSV file
        return self._data[idx]
        
    def open(self,filename):
        file = open(filename,"rw")
        reader = csv.reader(file,delimiter=",")
        self._data = []
        self._header = []
        firstRow = True
        for row in reader:
            if firstRow:
                firstRow = False
                self._header = row
                continue
            item = {}
            for i in range(0 , len(row)):
                item[self._header[i]] = float(row[i])
            
            self._data.append(item)
        return self._data
        
    def search(self,time):
        start = 0
        end = len(self._data)
        item = self._data[start]
        
        while start <= end:
            middle = (end - start) / 2 + start
            item = self._data[middle]
            index = float(self._data[middle]["Timestamp"])

            if index == time:
                break
            elif index < time:
                start = middle + 1
            else:
                end = middle - 1
                
       
        return item
