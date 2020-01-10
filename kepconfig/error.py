"""Exception classes raised by Kepconfig

KepURLError - Inherits responses from the urllib URLError exceptions.

KepHTTPError - Inherits responses from the urllib HTTPError exceptions.
This exception class is also a valid HTTP response instance.  It behaves 
this way because HTTP protocol errors are validresponses, with a status 
code, headers, and a body.  In some contexts,an application may want to 
handle an exception like a regular response.
"""

__all__ = ['KepURLError', 'KepHTTPError']

class KepURLError(Exception):

    def __init__(self, reason, url):
        self.reason = reason
        self.url = url

    def __str__(self):
        return '<urlopen error %s>' % self.reason

class KepHTTPError(Exception):
    
    def __init__(self, url, code, msg, hdrs, payload):
        self.url = url
        self.code = code
        self.msg = msg
        self.hdrs = hdrs
        self.payload = payload
    
    @property
    def reason(self):
        return self.msg

    def __str__(self):
        return 'HTTP Error %s: %s' % (self.code, self.msg)