# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


r"""`names` exposes an API to allow modifications (add, delete, modify) to 
name resolution objects for EGD devices within the Kepware Configuration API
"""

from ... import path_split
from ...connection import server
from ...error import KepHTTPError, KepError
from typing import Union
from .. import channel, device

NAMES_ROOT = '/name_resolution_groups/Name Resolutions/name_resolutions'

def _create_url(device_path, name = None):
    '''Creates url object for the "name resolution" branch of Kepware's project 
    tree. Used to build a part of Kepware Configuration API URL structure

    Returns the name resolution specific url when a value is passed.
    '''
    path_obj = path_split(device_path)
    device_root = channel._create_url(path_obj['channel']) + device._create_url(path_obj['device'])

    if name == None:
        return '{}/{}'.format(device_root, NAMES_ROOT)
    else:
        return '{}/{}/{}'.format(device_root, NAMES_ROOT, name)

def add_name_resolution(server: server, device_path: str, DATA: dict | list) -> Union[bool, list]:
    '''Add a `"name resolution"` or multiple `"name resolution"` objects to Kepware. This allows you to 
    create a name resolution or multiple name resolutions all in one function, if desired.

    :param server: instance of the `server` class
    :param device_path: path to EGD device. Standard Kepware address decimal 
    notation string such as `"channel1.device1"`
    :param DATA: Dict or List of Dicts of name resolutions
    expected by Kepware Configuration API

    :return: True - If a "HTTP 201 - Created" is received from Kepware server
    :return: If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    name resolutions added that failed.

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_add(server.url + _create_url(device_path), DATA)
    if r.code == 201: return True
    elif r.code == 207:
        errors = [] 
        for item in r.payload:
            if item['code'] != 201:
                errors.append(item)
        return errors
    else: 
        raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def del_name_resolution(server: server, device_path: str, name: str) -> bool:
    '''Delete a `"name resolution"` object in Kepware.
    
    :param server: instance of the `server` class
    :param device_path: path to EGD device. Standard Kepware address decimal 
    notation string such as `"channel1.device1"`
    :param name: name of name resolution to delete
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_del(server.url + _create_url(device_path, name))
    if r.code == 200: return True 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_name_resolution(server: server, device_path: str, DATA: dict, *, name: str = None, force: bool = False) -> bool:
    '''Modify a `"name resolution"` object and it's properties in Kepware. If a `"name"` is not provided as an input,
    you need to identify the name resolution in the *'common.ALLTYPES_NAME'* property field in the `"DATA"`. It will 
    assume that is the name resolution that is to be modified.

    :param server: instance of the `server` class
    :param device_path: path to EGD device. Standard Kepware address decimal 
    notation string such as `"channel1.device1"`
    :param DATA: Dict of name resolution properties to be modified
    :param name: *(optional)* name of name resolution to modify. Only needed if not existing in `"DATA"`
    :param force: *(optional)* if True, will force the configuration update to the Kepware server
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    
    name_data = server._force_update_check(force, DATA)
    if name == None:
        try:
            r = server._config_update(server.url + _create_url(device_path, name_data['common.ALLTYPES_NAME']), name_data)
            if r.code == 200: return True 
            else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
        except KeyError as err:
            err_msg = f'Error: No name resolution identified in DATA | Key Error: {type(DATA)}'
            raise KepError(err_msg) 
    else:
        r = server._config_update(server.url + _create_url(device_path, name), name_data)
        if r.code == 200: return True 
        else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def get_name_resolution(server: server, device_path: str, name: str = None, *, options: dict = None) -> Union[dict, list]:
    '''Returns the properties of the `"name resolution"` object or a list of all name resolutions.
    
    :param server: instance of the `server` class
    :param device_path: path to EGD device. Standard Kepware address decimal 
    notation string such as `"channel1.device1"`
    :param DATA: Dict of name resolution properties to be modified
    :param name: *(optional)* name of name resolution to retrieve. If not defined, will get all name resolutions
    :param options: *(optional)* Dict of parameters to filter, sort or pagenate when getting a list of profiles. Options are `filter`, 
        `sortOrder`, `sortProperty`, `pageNumber`, and `pageSize`. Only used when `"name"` is not defined.
    
    :return: Dict of the name resolution properties or List of Dicts for all name resolutions and their properties 
    
    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    if name == None:
        r = server._config_get(f'{server.url}{_create_url(device_path)}', params= options)
    else:
        r = server._config_get(f'{server.url}{_create_url(device_path, name)}')
    return r.payload