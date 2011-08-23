import hashlib

class CheckSum:
    
    def __init__(self,options):
        self.options = options

    def headers(self):
        return ['Hash SHA1']

    def process(self,request):
        return [hashlib.sha1(request.HTML).hexdigest()]
