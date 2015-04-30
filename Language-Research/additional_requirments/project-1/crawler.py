#/usr/bin/env python

############################################################
###  Website crawler

import urllib2
from bs4 import BeautifulSoup
from collections import deque

#WEBSITE = "http://www.bhojpuria.com" ;
#seed_URL = [ WEBSITE + "/v2/" ]
#ROOT = "WebPages/bhojpuria/";
#BASENAME = "bhojpuria";

#WEBSITE = "http://www.bhojpurimedia.com" ;
#seed_URL = [ WEBSITE  ]
#ROOT = "WebPages/bhojpurimedia/";
#BASENAME = "bhojpurimedia";

#WEBSITE = "http://tatkakhabar.com/" ;
#seed_URL = [ WEBSITE ]
#ROOT = "WebPages/tatkakhabar/";
#BASENAME = "tatkakhabar";

#WEBSITE = "http://khabarlahariya.org/?cat=66"
#seed_URL = [ WEBSITE  ]
#ROOT = "WebPages/khabarlahariya/";
#BASENAME = "khabarlahariya";

#WEBSITE = "http://www.anjoria.com"
#seed_URL = [ WEBSITE  ]
#ROOT = "WebPages/anjoria/";
#BASENAME = "anjoria";

#WEBSITE = "http://bhojpurika.com"
#seed_URL = [ WEBSITE  ]
#ROOT = "WebPages/bhojpurika/";
#BASENAME = "bhojpurika";

WEBSITE = "http://www.thebhojpuri.com/"
seed_URL = [ WEBSITE  ]
ROOT = "WebPages/thebhojpuri/";
BASENAME = "thebhojpuri";

URL_queue = deque( seed_URL );
URLs_tovisit = [ ]

def filter_links( url ) :
    if url==None or len(url) <= 1 :
        return ''
    if "http" in url and WEBSITE not in url :
        return '';
    if url.endswith('.jpg') or url.endswith('.png') or url.endswith('.pdf'):
        return ''     
    if "wp-admin" in url or "share" in url or "reply" in url :
        return '';

    url = url.split('#')[0].strip();
    if url.startswith('/') :
        url = WEBSITE + url

    if "http" not in url :
        url = WEBSITE + "/" + url

       
    return url;

    
count = 0;
while len(URL_queue) > 0 :
     
    url = URL_queue.popleft() 
    try : 
        response = urllib2.urlopen( url )
    except :
        print "Error while downloading the file"
        continue

 
    print "Downloaded URL (%d) : %s " %(count,url) 
    if count%50 == 0 :
        print "Length of URL queue : %d"%(len(URL_queue))

    try : 
        html = response.read()
        soup = BeautifulSoup(html)
    	fp = open( ROOT + BASENAME + str(count)+".html", "w" )
        fp.write( url + u"\n" )
    	fp.write(html)
    	fp.close()
        count = count + 1;
    except : 
        print "Error while parsing the html file"
        continue

 
    for link in soup.find_all('a'):
        l = filter_links(link.get('href'))
        # tatkakhabar
        # if len(l) > 0 and l not in URLs_tovisit and "?p=" not in l and "?tag" not in l and "?author" not in l :
        if len(l) > 0 and l not in URLs_tovisit :
            URL_queue.append(l)
            URLs_tovisit.append(l)
    
