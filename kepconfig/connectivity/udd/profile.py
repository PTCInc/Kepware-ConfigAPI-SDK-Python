# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


r"""`profile` exposes an API to allow modifications (add, delete, modify) to 
profile objects for the UDD Profile Library plug-in within the Kepware Configuration API
"""

from kepconfig import connection
from typing import Union

PROFILE_ROOT = '/project/_profile_library/profiles'

def add_profile(server: connection.server, DATA: Union[dict, list]) -> Union[bool, list]:
    '''Add a "profile" or a list of "profile" objects to the UDD Profile Library plug-in for Kepware. 

    Additionally it can be used to pass a list of exchanges and it's children to be added all at once.

    INPUTS:

    "server" - instance of the "server" class

    "DATA" - properly JSON object (dict) of the exchange and it's children
    expected by Kepware Configuration API

    RETURNS:

    True - If a "HTTP 201 - Created" is received from Kepware
    
    List - If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    exchanges added that failed.

    False - If a non-expected "2xx successful" code is returned
        

    EXCEPTIONS:

    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_add(f'{server.url}{PROFILE_ROOT}', DATA)
    if r.code == 201: return True
    elif r.code == 207:
        errors = [] 
        for item in r.payload:
            if item['code'] != 201:
                errors.append(item)
        return errors
    else: return False

def del_profile(server: connection.server, profile_name: str) -> bool:
    '''Delete a "profile" object in UDD Profile Library plug-in for Kepware.
    
    INPUTS:

    "server" - instance of the "server" class

    "profile_name" - name of profile
    
    RETURNS:

    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:

    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_del(f'{server.url}{PROFILE_ROOT}/{profile_name}')
    if r.code == 200: return True 
    else: return False

def modify_profile(server: connection.server, DATA: dict, profile_name: str = None, force: bool = False) -> bool:
    '''Modify a profile object and it's properties in Kepware. If a "profile_name" is not provided as an input,
    you need to identify the profile in the 'common.ALLTYPES_NAME' property field in the "DATA". It will 
    assume that is the profile that is to be modified.

    INPUTS:

    "server" - instance of the "server" class

    "DATA" - properly JSON object (dict) of the exchange properties to be modified.

    "profile_name" (optional) - name of exchange to modify. Only needed if not existing in  "DATA"

    "force" (optional) - if True, will force the configuration update to the Kepware server
    
    RETURNS:
    
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    
    profile_data = server._force_update_check(force, DATA)
    if profile_name == None:
        try:
            r = server._config_update(f"{server.url}{PROFILE_ROOT}/{profile_data['common.ALLTYPES_NAME']}", profile_data)
            if r.code == 200: return True 
            else: return False
        except KeyError as err:
            print('Error: No profile identified in DATA | Key Error: {}'.format(err))
            return False
        # except Exception as e:
        #     return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    else:
        r = server._config_update(f'{server.url}{PROFILE_ROOT}/{profile_name}', profile_data)
        if r.code == 200: return True 
        else: return False

def get_profile(server: connection.server, profile_name: str = None) -> Union[dict, list]:
    '''Returns the properties of the profile object or a list of all profiles and their 
    properties. Returned object is JSON.
    
    INPUTS:

    "server" - instance of the "server" class

    "profile_name" - (optional) name of exchange. If not defined, get all profiles
    
    RETURNS:

    JSON - data for the exchange requested or a list of exchanges and their properties

    EXCEPTIONS:

    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    if profile_name == None:
        r = server._config_get(f'{server.url}{PROFILE_ROOT}')
    else:
        r = server._config_get(f'{server.url}{PROFILE_ROOT}/{profile_name}')
    return r.payload

def get_all_profiles(server: connection.server):
    '''Returns list of all profile objects and their properties. Returned object is JSON list.
    
    INPUTS:

    "server" - instance of the "server" class
    
    RETURNS:

    List - list of all profiles in the Profile Library

    EXCEPTIONS:

    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    return get_profile(server)