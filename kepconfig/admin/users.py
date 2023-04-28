# -------------------------------------------------------------------------
# Copyright (c), PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`users` exposes an API to allow modifications (add, delete, modify) to 
users within the Kepware Administration User Management through the Kepware Configuration API
"""
from typing import Union
from ..error import KepError, KepHTTPError
from ..connection import server
from ..utils import _url_parse_object


USERS_ROOT = '/admin/server_users'
ENABLE_PROPERTY = 'libadminsettings.USERMANAGER_USER_ENABLED'

def _create_url(user = None):
    '''Creates url object for the "server_users" branch of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure

    Returns the user specific url when a value is passed as the user name.
    '''
    
    if user == None:
        return USERS_ROOT
    else:
        return '{}/{}'.format(USERS_ROOT, _url_parse_object(user))

def add_user(server: server, DATA: Union[dict, list]) -> Union[bool, list]:
    '''Add a `"user"` or multiple `"user"` objects to Kepware User Manager by passing a 
    list of users to be added all at once.

    :param server: instance of the `server` class
    :param DATA: Dict or List of Dicts of the users to add

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

def del_user(server: server, user: str) -> bool:
    '''Delete a `"user"` object in Kepware User Manager
    
    :param server: instance of the `server` class
    :param user: name of user to delete
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_del(server.url + _create_url(user))
    if r.code == 200: return True 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_user(server: server , DATA: dict, *, user: str = None) -> bool:
    '''Modify a `"user object"` and it's properties in Kepware User Manager. If a `"user"` is not provided as an input,
    you need to identify the user in the *'common.ALLTYPES_NAME'* property field in the `"DATA"`. It will 
    assume that is the user that is to be modified.

    :param server: instance of the `server` class
    :param DATA: Dict of the user properties to be modified.
    :param user: *(optional)* name of user to modify. Only needed if not existing in `"DATA"`
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    if user == None:
        try:
            r = server._config_update(server.url + _create_url(DATA['common.ALLTYPES_NAME']), DATA)
            if r.code == 200: return True 
            else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
        except KeyError as err:
            err_msg = 'Error: No User identified in DATA | Key Error: {}'.format(err)
            raise KepError(err_msg)
    else:
        r = server._config_update(server.url + _create_url(user), DATA)
        if r.code == 200: return True 
        else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def get_user(server: server, user: str) -> dict:
    '''Returns the properties of the `"user"` object.
    
    :param server: instance of the `server` class
    :param user: name of user to retrieve
    
    :return: Dict of properties for the user requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_get(server.url + _create_url(user))
    return r.payload

def get_all_users(server: server, *, options: dict = None) -> list:
    '''Returns list of all `"user"` objects and their properties.
    
    :param server: instance of the `server` class
    :param options: *(optional)* Dict of parameters to filter, sort or pagenate the list of users. Options are 'filter', 
    'sortOrder', 'sortProperty', 'pageNumber', and 'pageSize.

    :return: List of properties for all users

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_get(f'{server.url}{_create_url()}', params= options)
    return r.payload

def enable_user(server: server, user: str) -> bool:
    '''Enable the `"user"`.
    
    :param server: instance of the `server` class
    :param user: name of user

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    DATA = {ENABLE_PROPERTY: True}
    return modify_user(server, DATA, user= user)

def disable_user(server: server, user: str) -> bool:
    '''Disable the `"user"`.
    
    :param server: instance of the `server` class
    :param user: name of user

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    DATA = {ENABLE_PROPERTY: False}
    return modify_user(server, DATA, user= user)