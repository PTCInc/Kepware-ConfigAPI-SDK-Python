# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


r"""`profile` exposes an API to allow modifications (add, delete, modify) to 
profile objects for the UDD Profile Library plug-in within the Kepware Configuration API
"""

from ...connection import server
from ...error import KepHTTPError, KepError
from typing import Union

PROFILE_ROOT = '/project/_profile_library/profiles'

def add_profile(server: server, DATA: dict | list) -> Union[bool, list]:
    '''Add a `"profile"` or a list of `"profile"` objects to the UDD Profile Library plug-in for Kepware. 

    :param server: instance of the `server` class
    :param DATA: Dict or List of Dicts of the profiles to add to the Profile Library 
    through Kepware Configuration API

    :return: True - If a "HTTP 201 - Created" is received from Kepware server
    :return: If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    profiles added that failed.

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_add(f'{server.url}{PROFILE_ROOT}', DATA)
    if r.code == 201: return True
    elif r.code == 207:
        errors = [] 
        for item in r.payload:
            if item['code'] != 201:
                errors.append(item)
        return errors
    else: 
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def del_profile(server: server, profile_name: str) -> bool:
    '''Delete a `"profile"` object in UDD Profile Library plug-in for Kepware.
    
    :param server: instance of the `server` class
    :param profile_name: name of profile
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_del(f'{server.url}{PROFILE_ROOT}/{profile_name}')
    if r.code == 200: return True 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_profile(server: server, DATA: dict, profile_name: str = None, force: bool = False) -> bool:
    '''Modify a `"profile"` object and it's properties in Kepware. If a `"profile_name"` is not provided as an input,
    you need to identify the profile in the *'common.ALLTYPES_NAME'* property field in the `"DATA"`. It will 
    assume that is the profile that is to be modified.

    :param server: instance of the `server` class
    :param DATA: Dict or List of Dicts of the profile properties to be modified.
    :param profile_name: *(optional)* name of profile to modify. Only needed if not existing in `"DATA"`
    :param force: *(optional)* if True, will force the configuration update to the Kepware server
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    
    profile_data = server._force_update_check(force, DATA)
    if profile_name == None:
        try:
            r = server._config_update(f"{server.url}{PROFILE_ROOT}/{profile_data['common.ALLTYPES_NAME']}", profile_data)
            if r.code == 200: return True 
            else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
        except KeyError as err:
            err_msg = 'Error: No profile identified in DATA | Key Error: {}'.format(err)
            raise KepError(err_msg)
    else:
        r = server._config_update(f'{server.url}{PROFILE_ROOT}/{profile_name}', profile_data)
        if r.code == 200: return True 
        else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def get_profile(server: server, profile_name: str = None, *, options: dict = None) -> Union[dict, list]:
    '''Returns the properties of the profile object or a list of all profiles and their 
    properties. Will return a list if `"profile_name"` is not provided.
    
    INPUTS:

    :param server: instance of the `server` class
    :param profile_name: *(optional)* name of profile. If not defined, will get all profiles
    :param options: *(optional)* Dict of parameters to filter, sort or pagenate when getting a list of profiles. Options are `filter`, 
        `sortOrder`, `sortProperty`, `pageNumber`, and `pageSize`. Only used when profile_name is not defined.
    
    :return: Dict of the profile properties or List of Dicts for all profiles and their properties in the Profile Library

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    if profile_name == None:
        r = server._config_get(f'{server.url}{PROFILE_ROOT}', params= options)
    else:
        r = server._config_get(f'{server.url}{PROFILE_ROOT}/{profile_name}')
    return r.payload

def get_all_profiles(server: server, *, options: dict = None):
    '''Returns list of all profile objects and their properties. Returned object is JSON list.
    
    :param server: instance of the `server` class
    :param options: *(optional)* Dict of parameters to filter, sort or pagenate when getting a list of profiles. Options are `filter`, 
        `sortOrder`, `sortProperty`, `pageNumber`, and `pageSize`. Only used when profile_name is not defined.
    
    :return: List of data for all profiles and their properties in the Profile Library

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    return get_profile(server, options= options)