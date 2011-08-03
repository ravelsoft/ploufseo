import httplib
import socket
from urlparse import urlparse
from urllib2 import urlopen
from datetime import datetime

class HTTPRequest:
    
    def __init__(self, url):
        self.url = url
        self.HTML = ''
        self.status_code = 0
        self.fetched = None

    def __parse_headers(self,res):
        output = {}
        for h in res:
            output[h[0]] = h[1]
        if not 'location' in output:
            self.location = '';
            self.comment = '';
        else:
            self.location = output['location']
            self.comment = output['location']

    def fetch(self):
        get_headers()
        get_content()

    def get_headers(self):
        o = urlparse(self.url)
        self.date = datetime.today() 
        try:
            h = httplib.HTTPConnection(o.netloc)
        except httplib.InvalidURL:
            print 'URL ERROR'
            print url
        try :
            if o.query != '':
                uri = ''.join([o.path,'?',o.query])
            else:
                uri = o.path
            h.request('GET',uri)
            res = h.getresponse()
            self.__parse_headers(res.getheaders())
            self.status = res.status
        except socket.gaierror:
            print 'No response from server'
        except httplib.InvalidURL:
            print "Mechante URL"
            print uri

    def get_content(self):
        res = urlopen(self.url)
        self.HTML = res.read()
