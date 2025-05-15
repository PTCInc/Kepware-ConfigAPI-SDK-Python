# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`structures` provides general data structures to help manage 
various objects for Kepware's configuration
"""
from enum import Enum

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

class FilterModifierEnum(Enum):
    '''Enum class to represent the various filter types that can be used in the Kepware API'''
    EQUAL = "eq"
    NOTEQUAL = "neq"
    GREATERTHAN = "gt"
    LESSTTHAN = "lt"
    GREATERTHANEQUAL = "gte"
    LESSTHANEQUAL = "lte"
    CONTAINS = "contains"
    NOTCONTAINS = "ncontains"
    STARTSWITH = "starts_with"
    NOTSTARTSWITH = "nstarts_with"
    ENDSWITH = "ends_with"
    NOTENDSWITH = "nends_with"

class FilterFieldEnum(Enum):
    ID = "id"
    TIMESTAMP = "timestamp"
    ACTION = "action"
    USER = "user"
    INTERFACE = "interface"
    DETAILS = "details"
    DATA = "data"

class Filter:
    '''A class to represent a filter object when calling the Kepware API. This is used to
    filter the results of a GET request for Audit Logs.

    :param name: Name of the object to filter on

    :param type: Type of filter to apply

    :param value: Value to filter on
    '''
    def __init__(self, field: FilterFieldEnum = FilterFieldEnum.ID, modifier: FilterModifierEnum = FilterModifierEnum.EQUAL, value: str = ''):
        self.field = field
        self.modifier = modifier
        self.value = value
    
    def __str__(self):
        return '{"field": %s, "modifier": %s, "value": %s}' % (self.field, self.modifier, self.value)
