# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


# r""":mod:`ranges` exposes an API to allow modifications (add, delete, modify) to 
# range objects in exchanges for EGD devices within the Kepware Configuration API
# """

from typing import Union
from .. import egd as EGD

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

def add_range(server, device_path, ex_type, exchange_name, DATA) -> Union[bool, list]:
    '''Add a "range" or multiple "range" objects to Kepware. This allows you to 
    create a range or multiple ranges all in one function, if desired.

    When passing multiple ranges, they will be populated in the same order
    in the list sent. Ensure you provide the list in the order desired.

    INPUTS:

    "server" - instance of the "server" class

    "device_path" - path to exchanges and their ranges. Standard Kepware address decimal 
    notation string such as "channel1.device1"

    "ex_type" - type of exchange either consumer or producer

    "exchange_name" - name of exchange to add range to

    "DATA" - properly JSON object (dict) of the range or ranges

    RETURNS:

    True - If a "HTTP 201 - Created" is received from Kepware
    
    List - If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    ranges added that failed.

    False - If a non-expected "2xx successful" code is returned

    EXCEPTIONS:

    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_add(server.url + _create_url(device_path, ex_type, exchange_name), DATA)
    if r.code == 201: return True
    elif r.code == 207:
        errors = [] 
        for item in r.payload:
            if item['code'] != 201:
                errors.append(item)
        return errors
    else: return False

def del_range(server, device_path, ex_type, exchange_name, range_name) -> bool:
    '''Delete a "range" object in Kepware.
    
    INPUTS:

    "server" - instance of the "server" class

    "device_path" - path to exchanges and their ranges. Standard Kepware address decimal 
    notation string such as "channel1.device1"

    "ex_type" - type of exchange either consumer or producer

    "exchange_name" - name of exchange that range is located

    "range_name" - name of range
    
    RETURNS:

    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:

    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_del(server.url + _create_url(device_path, ex_type, exchange_name, range_name))
    if r.code == 200: return True 
    else: return False

def modify_range(server, device_path, ex_type, exchange_name, DATA, range_name = None, force = False) -> bool:
    '''Modify a range object and it's properties in Kepware. If a "range_name" is not provided as an input,
    you need to identify the range in the 'common.ALLTYPES_NAME' property field in the "DATA". It will 
    assume that is the range that is to be modified.

    INPUTS:

    "server" - instance of the "server" class

    "device_path" - path to exchanges and their ranges. Standard Kepware address decimal 
    notation string such as "channel1.device1"

    "ex_type" - type of exchange either consumer or producer

    "exchange_name" - name of exchange that range is located

    "DATA" - properly JSON object (dict) of the range properties to be modified.

    "range_name" (optional) - name of range to modify. Only needed if not existing in  "DATA"

    "force" (optional) - if True, will force the configuration update to the Kepware server
    
    RETURNS:
    
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    
    range_data = server._force_update_check(force, DATA)
    if range_name == None:
        try:
            r = server._config_update(server.url + _create_url(device_path, ex_type, exchange_name, range_data['common.ALLTYPES_NAME']), range_data)
            if r.code == 200: return True 
            else: return False
        except KeyError as err:
            print('Error: No range identified in DATA | Key Error: {}'.format(err))
            return False
        # except Exception as e:
        #     return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    else:
        r = server._config_update(server.url + _create_url(device_path, ex_type, exchange_name, range_name), range_data)
        if r.code == 200: return True 
        else: return False

def get_range(server, device_path, ex_type, exchange_name, range_name = None) -> Union[dict, list]:
    '''Returns the properties of the range object or a list of all ranges. Returned object is JSON.
    
    INPUTS:

    "server" - instance of the "server" class

    "device_path" - path to exchanges and their ranges. Standard Kepware address decimal 
    notation string such as "channel1.device1"

    "ex_type" - type of exchange either consumer or producer

    "exchange_name" - name of exchange that range is located

    "range_name" - name of range
    
    RETURNS:

    JSON - data for the range requested or a list of ranges and their properties

    EXCEPTIONS:

    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    if range_name == None:
        r = server._config_get(server.url + _create_url(device_path, ex_type, exchange_name))
    else:
        r = server._config_get(server.url + _create_url(device_path, ex_type, exchange_name, range_name))
    return r.payload