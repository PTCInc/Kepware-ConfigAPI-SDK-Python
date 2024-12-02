# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`structures` provides general data structures to help manage 
various objects for Kepware's configuration
"""
class KepServiceResponse:
    '''A class to represent a return object when calling a "service" API of Kepware. This is
    used to return the responses when a "service" is executed appropriately

    :param code: HTTP code returned

    :param message: return from the "service" call

    :param href: URL reference to the JOB that is created by the service API
    '''

    def __init__(self, code: str = '', message: str = '', href: str = ''):
        self.code = code
        self.message = message
        self.href = href
    
    def __str__(self):
        return '{"code": %s, "message": %s, "href": %s}' % (self.code, self.message, self.href)

class KepServiceStatus:
    '''A class to represent a status object when checking on a "service" API job state in Kepware. This is
    used to return the status of a "service" job

    :param complete: Boolean of service job completion status

    :param status: Status code of job

    :param message: Error message if service job fails
    
    '''
    def __init__(self, complete: bool = False, status: str = '', message: str = ''):
        self.status = status
        self.message = message
        self.complete = complete
    
    def __str__(self):
        return '{"complete": %s, "status": %s, "message": %s}' % (self.complete, self.status, self.message)

class _HttpDataAbstract:
    def __init__(self):
        self.payload = ''
        self.code = ''
        self.reason = ''