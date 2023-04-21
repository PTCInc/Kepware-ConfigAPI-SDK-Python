# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


r"""`ranges` exposes an API to allow modifications (add, delete, modify) to 
range objects in exchanges for EGD devices within the Kepware Configuration API
"""

from typing import Union
from .. import egd as EGD
from ...connection import server
from ...error import KepError, KepHTTPError

RANGES_ROOT = '/ranges'

def _create_url(device_path, ex_type, exchange_name, range = None):
    '''Creates url object for the "range" branch of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure

    Returns the range specific url when a value is passed as the range name.
    '''
    exchange_root = EGD.exchange._create_url(device_path, ex_type, exchange_name)

    if range == None:
        return '{}{}'.format(exchange_root, RANGES_ROOT)
    else:
        return '{}{}/{}'.format(exchange_root, RANGES_ROOT, range)

def add_range(server: server, device_path: str, ex_type: str, exchange_name: str, DATA: dict | list) -> Union[bool, list]:
    '''Add a `"range"` or multiple `"range"` objects to Kepware. This allows you to 
    create a range or multiple ranges all in one function, if desired.

    When passing multiple ranges, they will be populated in the same order
    in the list sent. Ensure you provide the list in the order desired.

    :param server: instance of the `server` class
    :param device_path: path to EGD device. Standard Kepware address decimal 
    notation string such as `"channel1.device1"`
    :param ex_type: type of exchange, either `CONSUMER` or `PRODUCER`
    :param exchange_name: name of exchange that range is located
    :param DATA: Dict or List of Dicts of the range(s) to add

    :return: True - If a "HTTP 201 - Created" is received from Kepware server
    :return: If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    ranges added that failed.
        
    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_add(server.url + _create_url(device_path, ex_type, exchange_name), DATA)
    if r.code == 201: return True
    elif r.code == 207:
        errors = [] 
        for item in r.payload:
            if item['code'] != 201:
                errors.append(item)
        return errors
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def del_range(server: server, device_path: str, ex_type: str, exchange_name: str, range_name: str) -> bool:
    '''Delete a `"range"` object in Kepware.
    
    :param server: instance of the `server` class
    :param device_path: path to EGD device. Standard Kepware address decimal 
    notation string such as `"channel1.device1"`
    :param ex_type: type of exchange, either `CONSUMER` or `PRODUCER`
    :param exchange_name: name of exchange that range is located
    :param range_name: name of range to delete
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_del(server.url + _create_url(device_path, ex_type, exchange_name, range_name))
    if r.code == 200: return True 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_range(server: server, device_path: str, ex_type: str, exchange_name: str, DATA: dict, *, range_name: str = None, force: bool = False) -> bool:
    '''Modify a `"range"` object and it's properties in Kepware. If a `"range_name"` is not provided as an input,
    you need to identify the range in the *'common.ALLTYPES_NAME'* property field in the `"DATA"`. It will 
    assume that is the range that is to be modified.

    :param server: instance of the `server` class
    :param device_path: path to EGD device. Standard Kepware address decimal 
    notation string such as `"channel1.device1"`
    :param ex_type: type of exchange, either `CONSUMER` or `PRODUCER`
    :param exchange_name: name of exchange that range is located
    :param DATA: Dict of the range properties to be modified.
    :param range_name: *(optional)* name of range to to modify. Only needed if not existing in `"DATA"`
    :param force: *(optional)* if True, will force the configuration update to the Kepware server
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    
    range_data = server._force_update_check(force, DATA)
    if range_name == None:
        try:
            r = server._config_update(server.url + _create_url(device_path, ex_type, exchange_name, range_data['common.ALLTYPES_NAME']), range_data)
            if r.code == 200: return True 
            else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
        except KeyError as err:
            err_msg = 'Error: No range identified in DATA | Key Error: {}'.format(err)
            raise KepError(err_msg)
    else:
        r = server._config_update(server.url + _create_url(device_path, ex_type, exchange_name, range_name), range_data)
        if r.code == 200: return True 
        else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def get_range(server: server, device_path: str, ex_type: str, exchange_name: str, range_name: str = None, *, options: dict = None) -> Union[dict, list]:
    '''Returns the properties of the `"range"` object or a list of all ranges.
    
    :param server: instance of the `server` class
    :param device_path: path to EGD device. Standard Kepware address decimal 
    notation string such as `"channel1.device1"`
    :param ex_type: type of exchange, either `CONSUMER` or `PRODUCER`
    :param exchange_name: name of exchange that range is located
    :param DATA: Dict of the range properties to be modified.
    :param range_name: *(optional)* name of range to retrieve. If not defined, get all ranges
    :param options: *(optional)* Dict of parameters to filter, sort or pagenate the list of exchanges. Options are 'filter', 
    'sortOrder', 'sortProperty', 'pageNumber', and 'pageSize'. Only used when range_name is not defined.
    
    :return: Dict of properties for the range requested or a List of ranges and their properties

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    if range_name == None:
        r = server._config_get(f'{server.url}{_create_url(device_path, ex_type, exchange_name)}', params= options)
    else:
        r = server._config_get(f'{server.url}{_create_url(device_path, ex_type, exchange_name, range_name)}')
    return r.payload