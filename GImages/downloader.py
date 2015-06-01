#!/bin/python
#
#   Google Image extractor
#
import urllib, urllib2
import simplejson
import cStringIO
import os, sys

fetcher = urllib2.build_opener()
numberOfPages = int(sys.argv[1])
searchTerm = ""
for i in xrange(2,len(sys.argv)):
    searchTerm += sys.argv[i]+"+"
searchTerm = searchTerm[:-1]
startIndex = 0
counter = 0
DIR = os.getcwd()+'/'+searchTerm.replace('+','_')+'/'

try: os.stat(DIR)
except: os.mkdir(DIR)

urlList = open(searchTerm.replace('+','_')+"_urllist.txt","w")
for i in xrange(0,numberOfPages):
    searchUrl = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + searchTerm + "&start=" + str(i)
    searchUrl = searchUrl.replace(' ','+')

    f = fetcher.open(searchUrl)
    deserialized_output = simplejson.load(f)

    #print len(deserialized_output)
    
    for i in xrange(0,len(deserialized_output['responseData']['results'])):
        imageUrl = deserialized_output['responseData']['results'][i]['unescapedUrl']
        print imageUrl

        img_file = str(counter).zfill(6)
        counter += 1    
        f = open(DIR+img_file+'.jpg','wb')
        f.write(urllib.urlopen(imageUrl).read())
        f.close()
        urlList.write(imageUrl+"\n")
urlList.close()
