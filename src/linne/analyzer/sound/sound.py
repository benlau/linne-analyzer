# Sound Data Type

class Sound:
    def __init__(self,phonetic = None,ipa = None , filter = None,threshold = None,remarks = None):
        self.phonetic = phonetic
        self.ipa = ipa
        self.filter = filter
        self.threshold = threshold
        self.remarks = remarks

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
