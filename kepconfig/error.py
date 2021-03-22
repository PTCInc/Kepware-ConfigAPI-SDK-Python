# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


r"""`error` Exception classes raised by Kepconfig.
Includes KepURLError and KepHTTPError
"""

__all__ = ['KepError', 'KepURLError', 'KepHTTPError']


class KepError(Exception):
    '''General Exception class for Kepconfig.
    '''
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
            return 'KepError Error: %s' % (self.msg)

class KepURLError(KepError):
    '''Exception class raised by Kepconfig that inherits responses from the urllib URLError exceptions.
    '''
    def __init__(self, reason, url):
        KepError.__init__(self)
        self.reason = reason
        self.url = url

    def __str__(self):
        return '<urlopen error %s>' % self.reason

class KepHTTPError(KepError):
    '''Exception class raised by Kepconfig that inherits responses from the urllib HTTPError 
    exceptions. This exception class is also a valid HTTP response instance.  It behaves 
    this way because HTTP protocol errors are valid responses, with a status 
    code, headers, and a body.  In some contexts,an application may want to 
    handle an exception like a regular response.
    '''
    def __init__(self, url, code, msg, hdrs, payload):
        KepError.__init__(self, msg)
        self.url = url
        self.code = code
        self.hdrs = hdrs
        self.payload = payload
    
    @property
    def reason(self):
        return self.msg

    def __str__(self):
        return 'HTTP Error %s: %s' % (self.code, self.msg)