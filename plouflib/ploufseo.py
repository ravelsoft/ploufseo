import csv
import sys

from plouflib.http import HTTPRequest
from plouflib.sitemap import URLList
from plouflib.mapcount import wc_lines
from plouflib.check_status import StatusCheck
from plouflib.check_xpath import XpathCheck
from plouflib.unicodecsv import UnicodeWriter

class PloufSeo:

    def __init__(self, options):
        self.options = options
        self.filters = []
        self.headers = ['URL']
        self.output = []
        if self.options.status_code:
            self.status = StatusCheck(self.options)
        if self.options.xpath_expression:
            self.xpath = XpathCheck(self.options)
    
    def __make_headers(self):
        if self.options.status_code:
            self.headers.extend(self.status.headers())
        if self.options.xpath_expression:
            self.headers.extend(self.xpath.headers())

    def run(self):
        url_list = URLList()

        if self.options.csv:
            url_list.load_from_csv(self.options.csv)
        elif self.options.sitemap:
            url_list.load_from_sitemap(self.options.sitemap)
        elif self.options.url:
            url_list.load_from_urls(self.options.url)

        self.__make_headers()

        if self.options.progress:
            progress = ProgressBar(widgets=widgets,maxval=len(url_list.urls)).start()
        
        count = 0
        for url in url_list.urls:
            if len(url) >= 1:
                request = HTTPRequest(url.strip())
                current_line = [request.url]
                if request.url != "URL":
                    if self.options.status_code: 
                        request.get_headers()
                        current_line.extend( self.status.process(request))
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

            count += 1
            if self.options.progress:
                progress.update(count)

        if self.options.progress:
            progress.finish()

        if self.options.output:
            output_file = open(self.options.output,'w')
        else:
            output_file = sys.stdout
            

        url_writer = UnicodeWriter(output_file)
        url_writer.writerow(self.headers)
        url_writer.writerows(self.output)
