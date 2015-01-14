# coding: utf-8
import sys

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

def sanitize(theStr):
    return theStr.replace(u'’', u"'")

class MyHTMLParser(HTMLParser):
    classSpell = False
    def handle_starttag(self, tag, attrs):
        if tag == "a" :
            for attr in attrs:
                if attr == ('class', 'spell') :
                    self.classSpell = True
    def handle_endtag(self, tag):
        if tag =='a' : self.classSpell = False
    def handle_data(self, data):
        if self.classSpell : print "\""+sanitize(data)+"\""

def main(argv):
    import urllib
    usock = urllib.urlopen("http://www.d20srd.org/srd/spellLists/druidSpells.htm")
    parser = MyHTMLParser()
    print "Spell"
    parser.feed(usock.read().decode('utf-8'))
    usock.close()
    parser.close()

if __name__ == "__main__":
    main(sys.argv)
