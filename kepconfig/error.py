# -------------------------------------------------------------------------
# Copyright (c) 2020, PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

""":mod:`error` defines exception classes raised by Kepconfig

KepURLError - Inherits responses from the urllib URLError exceptions.

KepHTTPError - Inherits responses from the urllib HTTPError exceptions.
This exception class is also a valid HTTP response instance.  It behaves 
this way because HTTP protocol errors are validresponses, with a status 
code, headers, and a body.  In some contexts,an application may want to 
handle an exception like a regular response.
"""

__all__ = ['KepURLError', 'KepHTTPError']

class KepURLError(Exception):
    """Exception class raised by Kepconfig that inherits responses from 
    the urllib URLError exceptions.
    """

    def __init__(self, reason, url):
        self.reason = reason
        self.url = url

    def __str__(self):
        return '<urlopen error %s>' % self.reason

class KepHTTPError(Exception):
    """Exception class raised by Kepconfig that inherits responses from 
    the urllib HTTPError exceptions. This exception class is also a valid 
    HTTP response instance.  It behaves this way because HTTP protocol 
    errors are validresponses, with a status code, headers, and a body.  
    In some contexts,an application may want to handle an exception like 
    a regular response.
    """
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