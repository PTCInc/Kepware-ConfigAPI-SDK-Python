# -------------------------------------------------------------------------
# Copyright (c), PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r""":mod:`users` exposes an API to allow modifications (add, delete, modify) to 
users within the Kepware Administration User Management through the Kepware Configuration API
"""
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
        return '{}/{}'.format(USERS_ROOT,user)

def add_user(server, DATA):
    '''Add a "user" or multiple "user" objects to Kepware User Manager by passing a 
    list of users to be added all at once.

    INPUTS:
    "server" - instance of the "server" class

    "DATA" - properly JSON object (dict) of the user
    expected by Kepware Configuration API

    RETURNS:
    True - If a "HTTP 201 - Created" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_add(server.url + _create_url(), DATA)
    if r.code == 201: return True 
    else: return False

def del_user(server, user):
    '''Delete a "user" object in Kepware User Manager
    
    INPUTS:
    "server" - instance of the "server" class

    "user" - name of user
    
    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_del(server.url + _create_url(user))
    if r.code == 200: return True 
    else: return False

def modify_user(server, DATA, user = None):
    '''Modify a user object and it's properties in Kepware User Manager. If a "user" is not provided as an input,
    you need to identify the user in the 'common.ALLTYPES_NAME' property field in the "DATA". It will 
    assume that is the user that is to be modified.

    INPUTS:
    "server" - instance of the "server" class

    "DATA" - properly JSON object (dict) of the user properties to be modified.

    "user" (optional) - name of user to modify. Only needed if not existing in  "DATA"
    
    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    
    # channel_data = server._force_update_check(force, DATA)
    if user == None:
        try:
            r = server._config_update(server.url + _create_url(DATA['common.ALLTYPES_NAME']), DATA)
            if r.code == 200: return True 
            else: return False
        except KeyError as err:
            print('Error: No User identified in DATA | Key Error: {}'.format(err))
            return False
        # except Exception as e:
        #     return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    else:
        r = server._config_update(server.url + _create_url(user), DATA)
        if r.code == 200: return True 
        else: return False

def get_user(server, user):
    '''Returns the properties of the user object. Returned object is JSON.
    
    INPUTS:
    "server" - instance of the "server" class

    "user" - name of user
    
    RETURNS:
    JSON - data for the user requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_get(server.url + _create_url(user))
    return r.payload

def get_all_users(server):
    '''Returns list of all user objects and their properties. Returned object is JSON list.
    
    INPUTS:
    "server" - instance of the "server" class
    
    RETURNS:
    JSON - data for all users requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_get(server.url + _create_url())
    return r.payload

def enable_user(server, user):
    '''Enable the user. Returned object is JSON.
    
    INPUTS:
    "server" - instance of the "server" class

    "user" - name of user

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    DATA = {ENABLE_PROPERTY: True}
    return modify_user(server, DATA, user)

def disable_user(server, user):
    '''Disable the user. Returned object is JSON.
    
    INPUTS:
    "server" - instance of the "server" class

    "user" - name of user

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    DATA = {ENABLE_PROPERTY: False}
    return modify_user(server, DATA, user)