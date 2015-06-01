#!/bin/python
#
#   Bing Image extractor
#
import urllib,urllib2,json
import os,sys

keyBing = 'wJYkWxwJfKoCUfh5L7xGeC6Q8YqIKHwKvKsvQ5Sfn/k='        
# get Bing key from:https://datamarket.azure.com/account/keys
credentialBing = 'Basic ' + (':%s' % keyBing).encode('base64')[:]

#searchString = '%27Xbox+One%27'
#top = 20
#offset = 0

def bing_search(searchString,top=10,offset=0):
    url = 'https://api.datamarket.azure.com/Bing/Search/Image?'+\
      'Query=%s&$top=%d&$skip=%d&$format=json'%(searchString,top,offset)

    request = urllib2.Request(url)
    request.add_header('Authorization', credentialBing)
    requestOpener = urllib2.build_opener()
    response = requestOpener.open(request) 

    results = json.load(response)
    # process results
    #print "#Results:",len(results['d']['results'])
    #print results['d']['results'][0]['MediaUrl']
    urls = []
    for i in xrange(0,len(results['d']['results'])):
        urls.append(results['d']['results'][i]['MediaUrl'])
    return urls

def download_images(searchTerm,urls):
    DIR = os.getcwd()+'/'+searchTerm.replace(' ','_')+'/'

    try: os.stat(DIR)
    except: os.mkdir(DIR)
    
    urlList = open(searchTerm.replace(' ','_')+"_urllist.txt","w")
    counter = 0
    for imageUrl in urls:
        img_file = str(counter).zfill(6)
        counter += 1    
        f = open(DIR+img_file+'.jpg','wb')
        print "Downloading:",imageUrl
        f.write(urllib.urlopen(imageUrl).read())
        f.close()
        urlList.write(imageUrl+"\n")
    urlList.close()
    return

if __name__ == "__main__":
    if len(sys.argv) > 1:
        number = int(sys.argv[1])
        offset = int(sys.argv[2])
        tags = ""
        searchTerm = ""
        if len(sys.argv) > 4:
            for i in xrange(3,len(sys.argv)): searchTerm+=sys.argv[i]+" "
            for i in xrange(3,len(sys.argv)): tags+=sys.argv[i]+"+"
            tags = tags[:-1]
            searchTerm = searchTerm[:-1]
        else:
            tags = sys.argv[3]
        tags = '%27'+tags+'%27'
        print "Max Images to download:",number,"offset=",offset,",Tags =",tags
        
        urls = bing_search(tags,number,offset)
        download_images(searchTerm,urls)
    print "Finished"
