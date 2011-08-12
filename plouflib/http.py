import httplib
import socket
import urllib2
from urlparse import urlparse
from datetime import datetime

class HTTPRequest:
    
    def __init__(self, url):
        self.url = url
        self.HTML = ''
        self.status_code = 0
        self.fetched = None
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-agent','Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13')]

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
        if 'http://' in self.url:
            try:
                self.HTML = self.opener.open(self.url).read()
            except urllib2.HTTPError:
                print 'Error'
        else:
            try:
                self.HTML = open(self.url).read()
            except IOError:
                print 'File does not exist'
