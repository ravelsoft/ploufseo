import httplib
import socket
import urllib2
import sys
import logging
import shelve

from urlparse import urlparse, urljoin
from datetime import datetime

class HTTPRequest:
    
    def __init__(self, url):
        self.url = url
        self.urlparsed = None
        self.HTML = ''
        self.headers = {} 
        self.status = 0
        self.fetched = None
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-agent','Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13')]

    def __parse_headers(self,headers):
        output = {}
        for h in headers:
            output[h[0]] = h[1]

        self.headers = output

    def get_location(self):
        if not 'location' in self.headers:
            location = '';
        else:
            if 'http://' in output['location']:
                location = output['location']
            else:
                location = urljoin(self.url,output['location'])
        return location


    def get_headers(self):
        if not self.status:
            self.urlparsed = urlparse(self.url)
            self.date = datetime.today() 
            h = httplib.HTTPConnection(self.urlparsed.netloc)
            try :
                if self.urlparsed.query != '':
                    uri = ''.join([self.urlparsed.path,'?',self.urlparsed.query])
                else:
                    uri = self.urlparsed.path
                h.request('GET',uri)
                res = h.getresponse()
                self.__parse_headers(res.getheaders())
                self.status = res.status
            except socket.gaierror:
                logging.warning('No response from server : %s', self.urlparsed.netloc)
            except httplib.InvalidURL:
                logging.waring('Invalid URL : %s', self.url)
            except:
                logging.warning('Unexpected error')
                raise

    def get_content(self):
        if self.HTML == '':
            if 'http://' in self.url:
                try:
                    self.HTML = self.opener.open(self.url).read()
                except urllib2.HTTPError:
                    logging.warning('Error')
                except urllib2.URLError:
                    logging.warning('No response from server')
            else:
                try:
                    self.HTML = open(self.url).read()
                except IOError:
                    logging.warning('File does not exist')
