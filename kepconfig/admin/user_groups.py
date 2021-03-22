# -------------------------------------------------------------------------
# Copyright (c), PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`user_groups` exposes an API to allow modifications (add, delete, modify) to 
user_groups within the Kepware Administration User Manager through the Kepware Configuration API
"""
from typing import Union
from ..error import KepHTTPError, KepError


USERGROUPS_ROOT = '/admin/server_usergroups'
ENABLE_PROPERTY = 'libadminsettings.USERMANAGER_GROUP_ENABLED'

def _create_url(user_group = None):
    '''Creates url object for the "server_usergroups" branch of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure

    Returns the user_group specific url when a value is passed as the user_group name.
    '''
    
    if user_group == None:
        return USERGROUPS_ROOT
    else:
        return '{}/{}'.format(USERGROUPS_ROOT,user_group)

def add_user_group(server, DATA) -> Union[bool, list]:
    '''Add a "user_group" or multiple "user_group" objects to Kepware User Manager by passing a 
    list of user groups to be added all at once.

    INPUTS:
    "server" - instance of the "server" class

    "DATA" - properly JSON object (dict) of the user_group
    expected by Kepware Configuration API

    RETURNS:
    True - If a "HTTP 201 - Created" is received from Kepware

    List - If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    user groups added that failed.

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

def del_user_group(server, user_group) -> bool:
    '''Delete a "user_group" object in Kepware User Manager
    
    INPUTS:
    "server" - instance of the "server" class

    "user_group" - name of user_group
    
    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_del(server.url + _create_url(user_group))
    if r.code == 200: return True 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_user_group(server, DATA, user_group = None) -> bool:
    '''Modify a user_group object and it's properties in Kepware User Manager. If a "user_group" is not provided as an input,
    you need to identify the user_group in the 'common.ALLTYPES_NAME' property field in the "DATA". It will 
    assume that is the user_group that is to be modified.

    INPUTS:
    "server" - instance of the "server" class

    "DATA" - properly JSON object (dict) of the user_group properties to be modified.

    "user_group" (optional) - name of user_group to modify. Only needed if not existing in  "DATA"
    
    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    
    # channel_data = server._force_update_check(force, DATA)
    if user_group == None:
        try:
            r = server._config_update(server.url + _create_url(DATA['common.ALLTYPES_NAME']), DATA)
            if r.code == 200: return True 
            else: return False
        except KeyError as err:
            err_msg = 'Error: No User Group identified in DATA | Key Error: {}'.format(err)
            raise KepError(err_msg)
        # except Exception as e:
        #     return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    else:
        r = server._config_update(server.url + _create_url(user_group), DATA)
        if r.code == 200: return True 
        else: return False

def get_user_group(server, user_group) -> dict:
    '''Returns the properties of the user_group object. Returned object is JSON.
    
    INPUTS:
    "server" - instance of the "server" class

    "user_group" - name of user_group
    
    RETURNS:
    dict - data for the user_group requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_get(server.url + _create_url(user_group))
    return r.payload

def get_all_user_groups(server) -> list:
    '''Returns list of all user_group objects and their properties. Returned object is JSON list.
    
    INPUTS:
    "server" - instance of the "server" class
    
    RETURNS:
    list - data for all user_groups requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_get(server.url + _create_url())
    return r.payload

def enable_user_group(server, user_group) -> bool:
    '''Enable the user group. Returned object is JSON.
    
    INPUTS:
    "server" - instance of the "server" class

    "user_group" - name of user group

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    DATA = {ENABLE_PROPERTY: True}
    return modify_user_group(server, DATA, user_group)

def disable_user_group(server, user_group) -> bool:
    '''Disable the user group. Returned object is JSON.
    
    INPUTS:
    "server" - instance of the "server" class

    "user_group" - name of user group

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    DATA = {ENABLE_PROPERTY: False}
    return modify_user_group(server, DATA, user_group)