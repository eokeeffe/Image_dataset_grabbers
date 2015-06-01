#!/bin/python

import flickr
import urllib, urlparse
import os
import sys

if len(sys.argv)>1: 
    args = sys.argv[2:]
    tags = ""
    for arg in args:
        tags+=arg+" "
else:
    print 'no tag specified'

DIR = os.getcwd()+'/'+tags.replace(' ','_')+'/'

try: os.stat(DIR)
except: os.mkdir(DIR)

try: number = sys.argv[1]
except: number = 1

print 'Max number of images to download',number,':',tags

# downloading image data
f = flickr.photos_search(tags=tags,tag_mode='all', per_page=number)
urllist = [] #store a list of what was downloaded
counter = 0
# downloading images
for k in f:
    url = k.getURL(size='Medium', urlType='source')
    urllist.append(url)
    image = urllib.URLopener()
    img_file = str(counter).zfill(6)
    counter += 1
    image.retrieve(url, DIR+img_file+'.jpg')
    print 'downloading:', url

# write the list of urls to file       
fl = open(DIR+tags.replace(' ','_')+'urllist.txt', 'w')
for url in urllist: fl.write(url+'\n')
fl.close()
