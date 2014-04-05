# -*- coding: utf-8 -*-

class Ipa:
    """IPA Phonetic
   """
   
    def __init__(self,symbol):
        """
        @type symbol: string
        @param symbol: The phonetic of a Chinese character formed by zhu yin symbol 
        
        >>> sys.getdefaultencoding()
        'utf-8'
        >>> len("ʂɑʊ".decode('utf-8'))
        3
        >>> p = Ipa('ʂɑʊ'.decode('utf-8'))
        >>> unicode(p)
        u'\u0282\u0251\u028a'
        >>> len(p.consonant) # Based on the assumption from the discussion on 2014-03-15
        2
        >>> len(p.vowel)
        1
        >>> len(p.symbols)
        3
        >>> p.points  # The points for each phonetic symbol on the audio track
        []
        
        """
        if len(symbol) == 1:
            self.consonant = u''
            self.vowel = symbol[0] # Dirty hack for Mandarin as it don't have pronounce with only consonant
        else:
            self.consonant = symbol[0:len(symbol)-1]
            self.vowel = symbol[len(symbol)-1]
        self.symbols = [s for s in symbol]

        self.points = [] # The starting of the symbol in audio track. The last record should be the end point
        
    def __unicode__(self):
        ret = u''
        if len(self.consonant) > 0:
            ret = ret + self.consonant
        ret = ret + u''.join(self.vowel)
        return ret
        
    def __str__(self):
        return unicode(self).encode("utf-8")
        
    def __len__(self):
        return len(self.symbols)

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
        
        For oto generation
        """
        ret = u''
        if self.vowel:
            ret = self.vowel[len(self.vowel) - 1]
        elif self.consonant:
            ret = self.consonant

        return ret

    def breakdown(self):
        """ Break down into a list of consonant and/or vowel symbols for analysis
        
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
        symbols = self.breakdown()
        for i in range(0,len(symbols)):
            print i
            record = [self.points[i],self.points[i+1],symbols[i] ]
            ret.append(record)
        return ret

if __name__ == '__main__':
    import sys
    reload(sys)  # Reload does the trick!
    sys.setdefaultencoding('utf-8')    
    import doctest
    doctest.testmod()
    

