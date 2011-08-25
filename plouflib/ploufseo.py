import csv
import sys
import os
import hashlib

from plouflib.http import HTTPRequest
from plouflib.urllist import URLList
from plouflib.mapcount import wc_lines
from plouflib.check_status import StatusCheck
from plouflib.check_xpath import XpathCheck
from plouflib.checksum import CheckSum
from plouflib.unicodecsv import UnicodeWriter

class PloufSeo:

    def __init__(self, options):
        self.home = os.path.join(os.getenv('HOME'),'.ploufseo')
        if not os.path.exists(self.home):
            os.mkdir(self.home)
        self.options = options
        self.filters = []
        self.headers = ['URL']
        self.output = []
        if self.options.status_code:
            self.status = StatusCheck(self.options)
        if self.options.xpath_expression:
            self.xpath = XpathCheck(self.options)
        if self.options.checksum:
            self.checksum = CheckSum(self.options)
    
    def __make_headers(self):
        if self.options.status_code:
            self.headers.extend(self.status.headers())
        if self.options.checksum:
            self.headers.extend(self.checksum.headers())
        if self.options.xpath_expression:
            self.headers.extend(self.xpath.headers())

    def get_request_from_shelf(self, url):
        if self.url_list.shelf.has_key(url):
            return self.url_list.shelf[url]
        else:
            return HTTPRequest(url)

    def run(self):
        self.url_list = URLList()
    
        if self.options.empty_cache:
            self.url_list.empty_shelf(self.home)

        self.url_list.open_shelf(self.home)

        if self.options.csv:
            self.url_list.load_from_csv(self.options.csv)
        if self.options.sitemap:
            self.url_list.load_from_sitemap(self.options.sitemap)
        if self.options.url:
            self.url_list.load_from_urls(self.options.url)

        if self.options.uniqify:
            self.url_list.uniqify()

        self.__make_headers()

        if self.options.progress:
            progress = ProgressBar(widgets=widgets,maxval=len(self.url_list.urls)).start()
        
        count = 0
        for url in self.url_list.urls:
            if len(url) >= 1:
                request = self.get_request_from_shelf(url.strip())
                current_line = [request.url]
                if request.url != "URL":
                    if self.options.status_code: 
                        request.get_headers()
                        current_line.extend(self.status.process(request))
                    if self.options.checksum:
                        request.get_content()
                        current_line.extend(self.checksum.process(request))
                    if self.options.xpath_expression:
                        request.get_content()
                        res_xpath = self.xpath.process(request)

                        if self.options.multiple:
                            for line in res_xpath:
                                tmp_line = current_line[:]
                                tmp_line.extend(list(reversed(line)))
                                self.output.append(tmp_line)
                        else:
                            current_line.extend(res_xpath)
                            self.output.append(current_line)

                    elif self.options.status_code or self.options.checksum:
                        self.output.append(current_line)
                self.url_list.shelf[request.url] = request
            count += 1
            if self.options.progress:
                progress.update(count)

        if self.options.progress:
            progress.finish()

        if self.options.output:
            if self.options.append:
                mode = 'a'
            else:
                mode = 'w'
            output_file = open(self.options.output,mode)
        else:
            output_file = sys.stdout
            

        url_writer = UnicodeWriter(output_file)
        url_writer.writerow(self.headers)
        url_writer.writerows(self.output)
