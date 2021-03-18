# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


r"""`names` exposes an API to allow modifications (add, delete, modify) to 
name resolution objects for EGD devices within the Kepware Configuration API
"""

import kepconfig
from typing import Union
from .. import channel, device

NAMES_ROOT = '/name_resolution_groups/Name Resolutions/name_resolutions'

def _create_url(device_path, name = None):
    '''Creates url object for the "name resolution" branch of Kepware's project 
    tree. Used to build a part of Kepware Configuration API URL structure

    Returns the name resolution specific url when a value is passed.
    '''
    path_obj = kepconfig.path_split(device_path)
    device_root = channel._create_url(path_obj['channel']) + device._create_url(path_obj['device'])

    if name == None:
        return '{}/{}'.format(device_root, NAMES_ROOT)
    else:
        return '{}/{}/{}'.format(device_root, NAMES_ROOT, name)

def add_name_resolution(server, device_path, DATA) -> Union[bool, list]:
    '''Add a "name resolution" or multiple "name resolution" objects to Kepware. This allows you to 
    create a name resolution or multiple name resolutions all in one function, if desired.

    INPUTS:

    "server" - instance of the "server" class

    "device_path" - path to name resolutions. Standard Kepware address decimal 
    notation string such as "channel1.device1"

    "DATA" - properly JSON object (dict) of the range or ranges

    RETURNS:

    True - If a "HTTP 201 - Created" is received from Kepware
    
    List - If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    name resolutions added that failed.

    False - If a non-expected "2xx successful" code is returned

    EXCEPTIONS:

    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_add(server.url + _create_url(device_path), DATA)
    if r.code == 201: return True
    elif r.code == 207:
        errors = [] 
        for item in r.payload:
            if item['code'] != 201:
                errors.append(item)
        return errors
    else: return False

def del_name_resolution(server, device_path, name) -> bool:
    '''Delete a "name resolution" object in Kepware.
    
    INPUTS:

    "server" - instance of the "server" class

    "device_path" - path to exchanges and their ranges. Standard Kepware address decimal 
    notation string such as "channel1.device1"

    "name resolution" - name of name resolution
    
    RETURNS:

    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:

    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_del(server.url + _create_url(device_path, name))
    if r.code == 200: return True 
    else: return False

def modify_name_resolution(server, device_path, DATA, name = None, force = False) -> bool:
    '''Modify a name resolution object and it's properties in Kepware. If a "name" is not provided as an input,
    you need to identify the name resolution in the 'common.ALLTYPES_NAME' property field in the "DATA". It will 
    assume that is the name resolution that is to be modified.

    INPUTS:

    "server" - instance of the "server" class

    "device_path" - path to exchanges and their ranges. Standard Kepware address decimal 
    notation string such as "channel1.device1"

    "DATA" - properly JSON object (dict) of the range properties to be modified.

    "name" (optional) - name of name resolution to modify. Only needed if not existing in  "DATA"

    "force" (optional) - if True, will force the configuration update to the Kepware server
    
    RETURNS:
    
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    
    name_data = server._force_update_check(force, DATA)
    if name == None:
        try:
            r = server._config_update(server.url + _create_url(device_path, name_data['common.ALLTYPES_NAME']), name_data)
            if r.code == 200: return True 
            else: return False
        except KeyError as err:
            print('Error: No name resolution identified in DATA | Key Error: {}'.format(err))
            return False
        # except Exception as e:
        #     return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    else:
        r = server._config_update(server.url + _create_url(device_path, name), name_data)
        if r.code == 200: return True 
        else: return False

def get_name_resolution(server, device_path, name = None) -> Union[dict, list]:
    '''Returns the properties of the name resolution object or a list of all name resolutions.
    Returned object is JSON.
    
    INPUTS:

    "server" - instance of the "server" class

    "device_path" - path to exchanges and their ranges. Standard Kepware address decimal 
    notation string such as "channel1.device1"

    "name" - name of name resolution
    
    RETURNS:

    JSON - data for the name resolution requested or a list of name resolutions and their properties

    EXCEPTIONS:

    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    if name == None:
        r = server._config_get(server.url + _create_url(device_path))
    else:
        r = server._config_get(server.url + _create_url(device_path, name))
    return r.payload