# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


r"""`error` Exception classes raised by Kepconfig.
Includes KepError, KepURLError and KepHTTPError
"""

__all__ = ['KepError', 'KepURLError', 'KepHTTPError']


class KepError(Exception):
    '''General Exception class for Kepconfig.
    
    :param msg: General error message returned in string format.
    '''
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
            return 'KepError Error: %s' % (self.msg)

class KepURLError(KepError):
    '''Exception class raised by Kepconfig that derives responses from the urllib URLError exceptions.

    :param url: full url path of the request that flagged a URLError exception
    :param msg: reason parameter in URLError exception
    '''
    def __init__(self, url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url
    
    @property
    def reason(self):
        return self.msg

    def __str__(self):
        return '<urlopen error %s>' % self.reason

class KepHTTPError(KepError):
    '''Exception class raised by Kepconfig that derives responses from the urllib HTTPError 
    exceptions. This exception class is also a valid HTTP response instance.  It behaves 
    this way because HTTP protocol errors are valid responses, with a status 
    code, headers, and a body.  In some contexts, an application may want to 
    handle an exception like a regular response.

    :param url: url parameter in HTTPError exception
    :param code: HTTP response code parameter in HTTPError exception
    :param hdrs: hdrs parameter in HTTPError exception
    :param payload: string of HTTP response payload that flagged HTTPError exception 
    :param msg: msg parameter in HTTPError exception
    '''
    def __init__(self, url=None, code=None, hdrs=None, payload=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url
        self.code = code
        self.hdrs = hdrs
        self.payload = payload
    
    @property
    def reason(self):
        return self.msg

    def __str__(self):
        return 'HTTP Error %s: %s' % (self.code, self.msg)