import string
import types
import sys
from lxml import etree
from lxml.html import HtmlElement
from lxml.html.soupparser import fromstring

class XpathResult:

    def __init__(self,options):
        self.options = options
        self.max_res = 0
        self.value = []

    def rotate(self):
        return zip(*self.value[::-1])

    def get(self):
        if self.options.multiple:
            for result in self.value:
                result.extend(['' for i in range(self.max_res - len(result))])
            return self.rotate()
        else:
            res = []
            for result in self.value:
                res.append(result[0])
            return res


    def add(self,value):
        if isinstance(value,types.ListType):
            if self.max_res < len(value):
                self.max_res = len(value)
            self.value.append(map(self.__to_string, value))
        else:
            if self.max_res < 1:
                self.max_res = 1
            self.value.append([__to_string(value)])
        
    def __to_string(self,value):
        if isinstance(value,HtmlElement):
            return unicode(etree.tostring(value))
        else:
            return unicode(value)
        

class XpathCheck:

    def __init__(self, options):
        self.options = options
        self.expressions = string.split(options.xpath_expression,',')

    def headers(self):
        return self.expressions

    def process(self,request):
        root = fromstring(request.HTML)
        res = []
        max_res = 0
        xpath_result = XpathResult(self.options)
        for xpath in self.expressions:
            try:
                value = root.xpath(xpath)
                if value:
                    xpath_result.add(value)
                else:
                    xpath_result.add([''])
            except etree.XPathEvalError:
                res.append(['ERROR'])
         
        return xpath_result.get()

