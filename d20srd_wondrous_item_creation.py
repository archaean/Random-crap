# coding: utf-8
import sys

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

def sanitize(theStr):
    return theStr.replace(u'’', u"'")

class MyHTMLParser(HTMLParser):
    inh5 = False
    classSpell = False
    afterCraftWond = False
    item = "Item"
    reqSpell = "Spell"
    def handle_starttag(self, tag, attrs):
        if tag == "h5" : self.inh5 = True; self.afterCraftWond = False
        if tag == "a" :
            for attr in attrs:
                #print attr
                if attr == ('class', 'spell') :
                    self.classSpell = True
                if attr == ('href', '/srd/feats.htm#craftWondrousItem') :
                    self.afterCraftWond = True
    def handle_endtag(self, tag):
        if tag == "h5" : self.inh5 = False
        if tag =='a' : 
            if self.reqSpell != "" :
                pStuff = "\""+sanitize(self.item)+"\""+",\""+sanitize(self.reqSpell)+"\""
                print pStuff
                self.reqSpell = ""
            self.classSpell = False
    def handle_data(self, data):
        if self.inh5 :
            self.item = data 
        if self.classSpell and self.afterCraftWond:
            self.reqSpell = data

def main(argv):
    import urllib
    usock = urllib.urlopen("http://www.d20srd.org/srd/magicItems/wondrousItems.htm")
    parser = MyHTMLParser() #URLLister()
    parser.feed(usock.read().decode('utf-8'))
    usock.close()
    parser.close()

if __name__ == "__main__":
    main(sys.argv)
