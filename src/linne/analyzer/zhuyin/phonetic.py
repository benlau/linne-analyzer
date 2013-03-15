

class Phonetic:
    """Zhu Yin Phonetic
    
    It is a class to hold the phonetic of a Chinese Character
    in zhu yin system. 
    """
   
    def __init__(self,symbol):
        """
        @type phonetics: list
        @param phonetics: list of zhu yin symbol 
        """
        self.consonant = symbol[0]
        self.vowel = symbol[1:len(symbol)]
        self.points = []
        
    def __unicode__(self):
        return self.consonant + u''.join(self.vowel)
        
    def __str__(self):
        return unicode(self).encode("utf-8")

    def breakdown(self):
        """ Break down into a list of consonant and/or vowel symbols
        
        @rtype: list
        """
        ret = [self.consonant]
        if len(self.vowel) > 0:
            ret.append(self.vowel[0])
        return ret
        
    def toLabel(self):
        """Convert to Audacity label format"""
        ret = []
        if len(self.vowel) == 0:
            ret.append([self.points[0],self.points[1],self.consonant] )
        else:
            ret.append([self.points[0],self.points[1],"[" + self.consonant + "]"] )
            ret.append([self.points[1],self.points[2],"[" + u''.join(self.vowel)+ "]"] )
            ret.append([self.points[0],self.points[2],unicode(self)] )
            
        return ret
