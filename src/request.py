import urllib.request
import urllib.parse
import json

class Request:
    def __init__(self,url,method='GET',headers={},data=None,timeout=5):

        self._response = None

        if method == 'GET':
            self.url = url+("?{}".format("&".join(["{}={}".format(urllib.parse.quote(k),urllib.parse.quote(v)) for k,v in data.items()])) if data != {} else "")
            data = None
        else:
            self.url = url
            data =  urllib.parse.urlencode(data).encode('utf-8') if type(data) == dict else None

        req = urllib.request.Request(url=self.url, headers=headers,data=data, method=method)

        for k,v in headers.items():
            req.add_header(k, v)

        try:
            self._res = urllib.request.urlopen(req, timeout=timeout)
            self._response = self._res.read()
        except Exception as e:
            self.error = str(e)

    def Json(self,encoding = 'utf-8'):
        return jszon.loads(self._response.decode(encoding))

    def Text(self, encoding = None):
        return (self._response.decode(self._res.headers.get_content_charset()) if self._response != None else self.error) if self._res.headers.get_content_charset() is not None else self._response.decode("ascii")

    def Bytes(self):
        return self._response
