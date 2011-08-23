import string
import types
import sys
from lxml import etree
from lxml.html.soupparser import fromstring

class XpathCheck:

    def rotation(self, array):
        return zip(*array[::-1])
             

    def __init__(self, options):
        self.options = options
        self.expressions = string.split(options.xpath_expression,',')

    def headers(self):
        return self.expressions

    def process(self,request):
        root = fromstring(request.HTML)
        res = []
        max_res = 0
        for xpath in self.expressions:
            try:
                value = root.xpath(xpath)
                if value:
                    if self.options.multiple:
                        res.append(value)
                        if len(value) > max_res:
                            max_res = len(value)
                    else:
                        if isinstance(value,types.ListType):
                            res.append(value[0])
                        else:
                            res.append(unicode(value))
                else:
                    if self.options.multiple:                
                        res.append([''])
                    else:
                        res.append('')
            except etree.XPathEvalError:
                res.append('ERROR')
       
        if self.options.multiple and isinstance(res,types.ListType):
            for values in res:
                values.extend(['' for i in range(max_res - len(values))])
            res = self.rotation(res)
        
        return res

