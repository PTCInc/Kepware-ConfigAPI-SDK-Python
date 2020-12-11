# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


# r""":mod:`exchange` exposes an API to allow modifications (add, delete, modify) to 
# exchange objects for EGD devices within the Kepware Configuration API
# """

import kepconfig
from typing import Union
from .. import egd as EGD, channel, device

CONSUMER_ROOT = '/consumer_exchange_groups/consumer exchanges/consumer_exchanges'
PRODUCER_ROOT = '/producer_exchange_groups/producer exchanges/producer_exchanges'

def _create_url(device_path, ex_type, exchange_name = None):
    '''Creates url object for the "exchange" branch of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure

    Returns the exchange specific url when a value is passed as the exchange name.
    '''
    path_obj = kepconfig.path_split(device_path)
    device_root = channel._create_url(path_obj['channel']) + device._create_url(path_obj['device'])

    if exchange_name == None:
        if ex_type == EGD.CONSUMER_EXCHANGE:
            return device_root + CONSUMER_ROOT
        else:
            return device_root + PRODUCER_ROOT
    else:
        if ex_type == EGD.CONSUMER_EXCHANGE:
            return '{}{}/{}'.format(device_root,CONSUMER_ROOT,exchange_name)
        else:
            return '{}{}/{}'.format(device_root,PRODUCER_ROOT,exchange_name)

def add_exchange(server, device_path, ex_type, DATA) -> Union[bool, list]:
    '''Add a "exchange" or multiple "exchange" objects to Kepware. Can be used to pass children of a exchange object 
    such as ranges. This allows you to create a exchange and ranges for the exchange all in one function, if desired.

    Additionally it can be used to pass a list of exchanges and it's children to be added all at once.

    INPUTS:

    "server" - instance of the "server" class

    "device_path" - path to exchanges. Standard Kepware address decimal 
    notation string such as "channel1.device1"

    "type" - type of exchange either consumer or producer

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

    r = server._config_add(server.url + _create_url(device_path, ex_type), DATA)
    if r.code == 201: return True
    elif r.code == 207:
        errors = [] 
        for item in r.payload:
            if item['code'] != 201:
                errors.append(item)
        return errors
    else: return False

def del_exchange(server, device_path, ex_type, exchange_name) -> bool:
    '''Delete a "exchange" object in Kepware. This will delete all children as well
    
    INPUTS:

    "server" - instance of the "server" class

    "device_path" - path to exchanges. Standard Kepware address decimal 
    notation string such as "channel1.device1"

    "ex_type" - type of exchange either consumer or producer

    "exchange_name" - name of exchange
    
    RETURNS:

    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:

    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_del(server.url + _create_url(device_path, ex_type, exchange_name))
    if r.code == 200: return True 
    else: return False

def modify_exchange(server, device_path, ex_type, DATA, exchange_name = None, force = False) -> bool:
    '''Modify a exchange object and it's properties in Kepware. If a "exchange_name" is not provided as an input,
    you need to identify the exchange in the 'common.ALLTYPES_NAME' property field in the "DATA". It will 
    assume that is the exchange that is to be modified.

    INPUTS:

    "server" - instance of the "server" class

    "device_path" - path to exchanges. Standard Kepware address decimal 
    notation string such as "channel1.device1"

    "ex_type" - type of exchange either consumer or producer

    "DATA" - properly JSON object (dict) of the exchange properties to be modified.

    "exchange_name" (optional) - name of exchange to modify. Only needed if not existing in  "DATA"

    "force" (optional) - if True, will force the configuration update to the Kepware server
    
    RETURNS:
    
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    
    exchange_data = server._force_update_check(force, DATA)
    if exchange_name == None:
        try:
            r = server._config_update(server.url + _create_url(device_path, ex_type, exchange_data['common.ALLTYPES_NAME']), exchange_data)
            if r.code == 200: return True 
            else: return False
        except KeyError as err:
            print('Error: No exchange identified in DATA | Key Error: {}'.format(err))
            return False
        # except Exception as e:
        #     return 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, str(e))
    else:
        r = server._config_update(server.url + _create_url(device_path, ex_type, exchange_name), exchange_data)
        if r.code == 200: return True 
        else: return False

def get_exchange(server, device_path, ex_type, exchange_name = None) -> Union[dict, list]:
    '''Returns the properties of the exchange object or a list of all exchanges and their 
    properties for the type input. Returned object is JSON.
    
    INPUTS:

    "server" - instance of the "server" class

    "device_path" - path to exchanges. Standard Kepware address decimal 
    notation string such as "channel1.device1"

    "ex_type" - type of exchange either consumer or producer

    "exchange_name" - name of exchange
    
    RETURNS:

    JSON - data for the exchange requested or a list of exchanges and their properties

    EXCEPTIONS:

    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    if exchange_name == None:
        r = server._config_get(server.url + _create_url(device_path, ex_type))
    else:
        r = server._config_get(server.url + _create_url(device_path, ex_type, exchange_name))
    return r.payload

def get_all_exchanges(server, device_path):
    '''Returns list of all exchange objects and their properties. Returned object is JSON list.
    
    INPUTS:

    "server" - instance of the "server" class

    "device_path" - path to exchanges. Standard Kepware address decimal 
    notation string such as "channel1.device1"
    
    RETURNS:

    List - [list of consumer exchanges, list of producer exchanges] - list of lists for all 
    exchanges for the device

    EXCEPTIONS:

    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    exchange_list = []
    exchange_list.append(get_exchange(server, device_path, EGD.CONSUMER_EXCHANGE))
    exchange_list.append(get_exchange(server, device_path, EGD.PRODUCER_EXCHANGE))
    return exchange_list