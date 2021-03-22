# -------------------------------------------------------------------------
# Copyright (c), PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`ua_server` exposes an API to allow modifications (add, delete, modify) to 
OPC UA Server endpoints within the Kepware Administration through the Kepware Configuration API
"""
from typing import Union
from ..error import KepHTTPError, KepError


UA_ROOT = '/admin/ua_endpoints'

def _create_url(endpoint = None):
    '''Creates url object for the "server_users" branch of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure

    Returns the user specific url when a value is passed as the user name.
    '''
    
    if endpoint == None:
        return UA_ROOT
    else:
        return '{}/{}'.format(UA_ROOT,endpoint)

def add_endpoint(server, DATA) -> Union[bool, list]:
    '''Add an "endpoint" or multiple "endpoint" objects to Kepware UA Server by passing a 
    list of endpoints to be added all at once.

    INPUTS:
    "server" - instance of the "server" class

    "DATA" - properly JSON object (dict) of the endpoint
    expected by Kepware Configuration API

    RETURNS:
    True - If a "HTTP 201 - Created" is received from Kepware

    List - If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    endpoints added that failed.

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_add(server.url + _create_url(), DATA)
    if r.code == 201: return True
    elif r.code == 207:
        errors = [] 
        for item in r.payload:
            if item['code'] != 201:
                errors.append(item)
        return errors
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def del_endpoint(server, endpoint) -> bool:
    '''Delete a "endpoint" object in Kepware UA Server
    
    INPUTS:
    "server" - instance of the "server" class

    "endpoint" - name of endpoint
    
    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_del(server.url + _create_url(endpoint))
    if r.code == 200: return True 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_endpoint(server, DATA, endpoint = None) -> bool:
    '''Modify a endpoint object and it's properties in Kepware UA Server. If a "endpoint" is not provided as an input,
    you need to identify the endpoint in the 'common.ALLTYPES_NAME' property field in the "DATA". It will 
    assume that is the endpoint that is to be modified.

    INPUTS:
    "server" - instance of the "server" class

    "DATA" - properly JSON object (dict) of the endpoint properties to be modified.

    "endpoint" (optional) - name of endpoint to modify. Only needed if not existing in  "DATA"
    
    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    
    # channel_data = server._force_update_check(force, DATA)
    if endpoint == None:
        try:
            r = server._config_update(server.url + _create_url(DATA['common.ALLTYPES_NAME']), DATA)
            if r.code == 200: return True 
            else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
        except KeyError as err:
            err_msg = 'Error: No UA Endpoint identified in DATA | Key Error: {}'.format(err)
            raise KepError(err_msg)

        # except Exception as e:
        #     return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    else:
        r = server._config_update(server.url + _create_url(endpoint), DATA)
        if r.code == 200: return True 
        else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def get_endpoint(server, endpoint) -> dict:
    '''Returns the properties of the endpoint object. Returned object is JSON.
    
    INPUTS:
    "server" - instance of the "server" class

    "endpoint" - name of endpoint
    
    RETURNS:
    dict - data for the endpoint requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_get(server.url + _create_url(endpoint))
    return r.payload

def get_all_endpoints(server) -> list:
    '''Returns list of all endpoint objects and their properties. Returned object is JSON list.
    
    INPUTS:
    "server" - instance of the "server" class
    
    RETURNS:
    list - data for all endpoints requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_get(server.url + _create_url())
    return r.payload