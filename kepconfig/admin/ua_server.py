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
from ..connection import server


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

def add_endpoint(server: server, DATA: Union[dict, list]) -> Union[bool, list]:
    '''Add an `"endpoint"` or multiple `"endpoint"` objects to Kepware UA Server by passing a 
    list of endpoints to be added all at once.

    :param server: instance of the `server` class
    :param DATA: Dict or List of Dicts of the UA Endpoints to add

    :return: True - If a "HTTP 201 - Created" is received from Kepware server
    :return: If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    endpoints added that failed.

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
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

def del_endpoint(server: server, endpoint: str) -> bool:
    '''Delete an `"endpoint"` object in Kepware UA Server
    
    :param server: instance of the `server` class
    :param endpoint: name of endpoint to delete
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_del(server.url + _create_url(endpoint))
    if r.code == 200: return True 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_endpoint(server: server, DATA: dict, endpoint: str = None) -> bool:
    '''Modify a `"endpoint"` object and it's properties in Kepware UA Server. If a `"endpoint"` is not provided as an input,
    you need to identify the endpoint in the *'common.ALLTYPES_NAME'* property field in the `"DATA"`. It will 
    assume that is the endpoint that is to be modified.

    :param server: instance of the `server` class
    :param DATA: Dict of the UA endpoint properties to be modified.
    :param endpoint: *(optional)* name of endpoint to modify. Only needed if not existing in `"DATA"`
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    if endpoint == None:
        try:
            r = server._config_update(server.url + _create_url(DATA['common.ALLTYPES_NAME']), DATA)
            if r.code == 200: return True 
            else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
        except KeyError as err:
            err_msg = 'Error: No UA Endpoint identified in DATA | Key Error: {}'.format(err)
            raise KepError(err_msg)
    else:
        r = server._config_update(server.url + _create_url(endpoint), DATA)
        if r.code == 200: return True 
        else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def get_endpoint(server: server, endpoint: str) -> dict:
    '''Returns the properties of the `"endpoint"` object.
    
    :param server: instance of the `server` class
    :param endpoint: name of endpoint to retrieve
    
    :return: Dict of properties for the UA endpoint requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_get(server.url + _create_url(endpoint))
    return r.payload

def get_all_endpoints(server: server, *, options: dict = None) -> list:
    '''Returns list of all `"endpoint"` objects and their properties.
    
    :param server: instance of the `server` class
    :param options: *(optional)* Dict of parameters to filter, sort or pagenate the list of UA endpoints. Options are 'filter', 
    'sortOrder', 'sortProperty', 'pageNumber', and 'pageSize.
    
    :return: List of properties for all UA endpoints requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_get(f'{server.url}{_create_url()}', params= options)
    return r.payload