

class Phonetic:
    """Zhu Yin Phonetic"""
   
    def __init__(self,phonetics):
        self.consonant = phonetics[0]
        self.vowel = phonetics[1:len(phonetics)]
        self.points = []
        
    def __unicode__(self):
        return self.consonant + u''.join(self.vowel)
        
    def __str__(self):
        return unicode(self).encode("utf-8")

    def toKeyList(self):
        # Convert to a list of key phonetics of this word
        ret = [self.consonant]
        if len(self.vowel) > 0:
            ret.append(self.vowel[0])
        return ret
        
    def toLabel(self):
        ret = []
        if len(self.vowel) == 0:
            ret.append([self.points[0],self.points[1],self.consonant] )
        else:
            ret.append([self.points[0],self.points[1],"[" + self.consonant + "]"] )
            ret.append([self.points[1],self.points[2],"[" + u''.join(self.vowel)+ "]"] )
            ret.append([self.points[0],self.points[2],unicode(self)] )
            
        return ret
