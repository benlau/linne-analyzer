

class Phonetic:
    """Zhu Yin Phonetic
    
    It is a class to hold the phonetic of a Chinese Character
    in zhu yin system. 
    """
   
    def __init__(self,symbol):
        """
        @type symbol: string
        @param symbol: The phonetic of a Chinese character formed by zhu yin symbol 
        """
        if len(symbol) == 1:
            self.consonant = u''
            self.vowel = symbol[0] # Mandarin don't have pronounce with only consonant
        else:
            self.consonant = symbol[0]
            self.vowel = symbol[1:len(symbol)]

        self.points = [] # The starting and end point of the symbol in audio track
        
    def __unicode__(self):
        ret = u''
        if len(self.consonant) > 0:
            ret = ret + self.consonant
        ret = ret + u''.join(self.vowel)
        return ret
        
    def __str__(self):
        return unicode(self).encode("utf-8")

    def isMono(self):
        """TRUE if the phonetic only contains consonant or vowel"""
        return self.consonant == u''        
    
    def hasConsonant(self):
        return len(self.consonant) > 0
        
    def isConsonant(self,symbol):
        """TRUE if the symbol is a consonant of this phonetic"""
        return self.consonant == symbol

    def isVowel(self,symbol):
        """TRUE if the symbol is a consonant of this phonetic"""
        return u''.join(self.vowel) == symbol
        
    def last(self):
        """ Return the last symbol of this phonetic.
        (experimental API)
        """
        ret = u''
        if self.vowel:
            ret = self.vowel[len(self.vowel) - 1]
        elif self.consonant:
            ret = self.consonant

        return ret

    def breakdown(self):
        """ Break down into a list of consonant and/or vowel symbols
        
        @rtype: list
        """
        ret = []
        if len(self.consonant) > 0:
            ret.append(self.consonant)
        if len(self.vowel) > 0:
            ret.append(self.vowel[0])
        return ret
        
    def toLabel(self):
        """Convert to Audacity label format"""
        ret = []
        if len(self.consonant) == 0:
            ret.append([self.points[0],self.points[1],self.vowel] )
        else:
            ret.append([self.points[0],self.points[1],"[" + self.consonant + "]"] )
            ret.append([self.points[1],self.points[2],"[" + u''.join(self.vowel)+ "]"] )
            ret.append([self.points[0],self.points[2],unicode(self)] )
            
        return ret
