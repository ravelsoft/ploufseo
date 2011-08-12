import csv
import sys
import string
from urllib2 import urlopen
from lxml.html.soupparser import fromstring

class URLList:
    
    def __init__(self):
        self.urls = []

    def load_from_csv(self, filename):
        csv_file = open(filename,'rU')
        url_reader = csv.reader(csv_file)
        for lines in url_reader:
            self.urls.append(lines[0])
        csv_file.close()

    def load_from_sitemap(self, url):
        try:
            res = urlopen(url)
        except ValueError:
            print 'Sitemap URL is not valid'
            sys.exit()
        content = fromstring(res.read())
        self.urls = content.xpath('//loc/text()')


    def load_from_urls(self, urls):
        print urls
        self.urls = string.split(urls,',')



