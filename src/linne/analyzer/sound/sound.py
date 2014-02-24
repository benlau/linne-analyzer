# Sound Data Type

class Sound:
    def __init__(self):
        self.phonetic = None
        self.ipa = None
        self.filter = None
        self.threshold = None
        self.remarks = None 

    def passThreshold(self,frame):
        ret = False
        if self.filter == "RMS":
            ret = frame["RMS"] > self.threshold
        elif self.filter == "SV":
            ret = frame["Spectrum Variance"] > self.threshold
        elif self.filter == "ZCR":
            ret = frame["ZCR"] > self.threshold
        elif self.filter == "STE":
            ret = frame["STE"] > self.threshold
        
        return ret
