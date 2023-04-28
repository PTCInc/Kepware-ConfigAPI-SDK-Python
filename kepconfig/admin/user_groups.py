# -------------------------------------------------------------------------
# Copyright (c), PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`user_groups` exposes an API to allow modifications (add, delete, modify) to 
user groups within the Kepware Administration User Manager through the Kepware Configuration API
"""
from typing import Union
from ..error import KepHTTPError, KepError
from ..connection import server
from ..utils import _url_parse_object


USERGROUPS_ROOT = '/admin/server_usergroups'
ENABLE_PROPERTY = 'libadminsettings.USERMANAGER_GROUP_ENABLED'

def _create_url(user_group = None):
    '''Creates url object for the "server_usergroups" branch of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure

    Returns the user group specific url when a value is passed as the user_group name.
    '''
    
    if user_group == None:
        return USERGROUPS_ROOT
    else:
        return '{}/{}'.format(USERGROUPS_ROOT, _url_parse_object(user_group))

def add_user_group(server: server, DATA: Union[dict, list]) -> Union[bool, list]:
    '''Add a `"user group"` or multiple `"user group"` objects to Kepware User Manager by passing a 
    list of user groups to be added all at once.

    :param server: instance of the `server` class
    :param DATA: Dict or List of Dicts of the user groups to add

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

def del_user_group(server: server, user_group: str) -> bool:
    '''Delete a `"user group"` object in Kepware User Manager
    
    :param server: instance of the `server` class
    :param user_group: name of user group to delete
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_del(server.url + _create_url(user_group))
    if r.code == 200: return True 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_user_group(server: server, DATA: dict, *, user_group: str = None) -> bool:
    '''Modify a `"user group"` object and it's properties in Kepware User Manager. If a `"user group"` is not provided as an input,
    you need to identify the user group in the *'common.ALLTYPES_NAME'* property field in the `"DATA"`. It will 
    assume that is the user group that is to be modified.

    :param server: instance of the `server` class
    :param DATA: Dict of the user group properties to be modified.
    :param user_group: *(optional)* name of user group to modify. Only needed if not existing in `"DATA"`
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    
    if user_group == None:
        try:
            r = server._config_update(server.url + _create_url(DATA['common.ALLTYPES_NAME']), DATA)
            if r.code == 200: return True 
            else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
        except KeyError as err:
            err_msg = 'Error: No User Group identified in DATA | Key Error: {}'.format(err)
            raise KepError(err_msg)
    else:
        r = server._config_update(server.url + _create_url(user_group), DATA)
        if r.code == 200: return True 
        else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def get_user_group(server: server, user_group: str) -> dict:
    '''Returns the properties of the `"user group"` object.
    
    :param server: instance of the `server` class
    :param user_group: name of user group to retrieve
    
    :return: Dict of properties for the user group requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_get(server.url + _create_url(user_group))
    return r.payload

def get_all_user_groups(server: server, *, options: dict = None) -> list:
    '''Returns list of all `"user group"` objects and their properties.
    
    :param server: instance of the `server` class
    :param options: *(optional)* Dict of parameters to filter, sort or pagenate the list of user groups. Options are 'filter', 
    'sortOrder', 'sortProperty', 'pageNumber', and 'pageSize.

    :return: List of properties for all user groups

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_get(f'{server.url}{_create_url()}', params= options)
    return r.payload

def enable_user_group(server: server, user_group: str) -> bool:
    '''Enable the `"user group"`.
    
    :param server: instance of the `server` class
    :param user_group: name of user group

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    DATA = {ENABLE_PROPERTY: True}
    return modify_user_group(server, DATA, user_group= user_group)

def disable_user_group(server: server, user_group: str) -> bool:
    '''Disable the `"user group"`.
    
    :param server: instance of the `server` class
    :param user_group: name of user group

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    DATA = {ENABLE_PROPERTY: False}
    return modify_user_group(server, DATA, user_group= user_group)