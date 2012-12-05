import csv
import sys
import string
import logging
import shelve
import os
from urllib2 import urlopen, HTTPError
from lxml.html.soupparser import fromstring

class URLList:
    
    def __init__(self):
        self.urls = []
    
    def open_shelf(self, path, name='database'):
        self.shelf = shelve.open(os.path.join(path, name))

    def close_shelf(self):
        self.shelf.close()

    def empty_shelf(self, path, name='database'):
        os.remove(os.path.join(path, name))

    def load_from_csv(self, filename):
        csv_file = open(filename,'rU')
        url_reader = csv.reader(csv_file)
        for lines in url_reader:
            if len(lines) > 0:
                self.urls.append(lines[0])
        csv_file.close()

    def load_from_sitemap(self, url):
        try:
            res = urlopen(url)
        except ValueError:
            logging.warning('Sitemap URL is not valid')
        except HTTPError, e:
            logging.error('sitemap: %s' % e)
            sys.exit(127)
        except Exception, e:
            logging.error('Unexpected Error : %s' % e)
            sys.exit(127)
        content = fromstring(res.read())
        self.urls.extend(content.xpath('//loc/text()'))


    def load_from_urls(self, urls):
        self.urls.extend(string.split(urls,','))


    def uniqify(self,idfun = None):
        # order preserving 
        if idfun is None: 
            def idfun(x): return x 
        seen = {} 
        result = [] 
        for item in self.urls: 
            marker = idfun(item) 
            # in old Python versions: 
            # if seen.has_key(marker) 
            # but in new ones: 
            if marker in seen: continue 
            seen[marker] = 1 
            result.append(item) 
        self.urls = result


