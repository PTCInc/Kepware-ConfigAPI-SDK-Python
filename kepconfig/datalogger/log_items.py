# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`log_items` exposes an API to allow modifications (add, delete, modify) to 
log item (tag) objects in a Datalogger log group within the Kepware Configuration API
"""
from typing import Union
from . import log_group as Log_Group
from ..error import KepError, KepHTTPError
from ..connection import server

LOG_ITEMS_ROOT = '/log_items'

def _create_url(log_item = None):
    '''Creates url object for the "log_item" branch of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure

    Returns the log_item specific url when a value is passed as the log_item name.
    '''

    if log_item == None:
        return '{}'.format(LOG_ITEMS_ROOT)
    else:
        return '{}/{}'.format(LOG_ITEMS_ROOT, log_item)


def add_log_item(server: server, log_group: str, DATA: Union[dict, list]) -> Union[bool, list]:
    '''Add a `"log item"` or multiple `"log item"` objects to a log group in Kepware's Datalogger. It can 
    be used to pass a list of log items to be added all at once.

    :param server: instance of the `server` class
    :param log_group: name of log group that the log items will be added
    :param DATA: Dict or a list of the log items to add through Kepware Configuration API

    :return: True - If a "HTTP 201 - Created" is received from Kepware server
    :return: If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    log items added that failed.

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''

    r = server._config_add(server.url + Log_Group._create_url(log_group) + _create_url(), DATA)
    if r.code == 201: return True
    elif r.code == 207:
        errors = [] 
        for item in r.payload:
            if item['code'] != 201:
                errors.append(item)
        return errors 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def del_log_item(server: server, log_group: str, log_item: str) -> bool:
    '''Delete a `"log item"` object of a log group in Kepware's Datalogger.
    
    :param server: instance of the `server` class
    :param log_group: name of log group that log item exists
    :param log_item: name of log item to delete

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_del(server.url + Log_Group._create_url(log_group) + _create_url(log_item))
    if r.code == 200: return True 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_log_item(server: server, log_group: str, DATA: dict, *, log_item: str = None, force: bool = False) -> bool:
    '''Modify a `"log_item"` object and it's properties in Kepware. If a `"log_item"` is not provided as an input,
    you need to identify the log_item in the *'common.ALLTYPES_NAME'* property field in the `"DATA"`. It will 
    assume that is the log_item that is to be modified.

    :param server: instance of the `server` class
    :param log_group: name of log group that log item exists
    :param DATA: Dict of the log item properties to be modified.
    :param log_item: *(optional)* name of log item to modify. Only needed if not existing in `"DATA"`
    :param force: *(optional)* if True, will force the configuration update to the Kepware server

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    
    log_item_data = server._force_update_check(force, DATA)
    
    if log_item == None:
        try:
            r = server._config_update(server.url + Log_Group._create_url(log_group) + _create_url(log_item_data['common.ALLTYPES_NAME']), log_item_data)
            if r.code == 200: return True 
            else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
        except KeyError as err:
            err_msg ='Error: No log item identified in DATA | Key Error: {}'.format(err)
            raise KepError(err_msg)
    else:
        r = server._config_update(server.url + Log_Group._create_url(log_group) + _create_url(log_item), log_item_data)
        if r.code == 200: return True 
        else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def get_log_item(server, log_group, log_item) -> dict:
    '''Returns the properties of the `"log item"` object.
    
    :param server: instance of the `server` class
    :param log_group: name of log group that log item exists
    :param log_item: name of log item to retrieve

    :return: Dict of properties for the log group requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(server.url + Log_Group._create_url(log_group) + _create_url(log_item))
    return r.payload

def get_all_log_items(server: server, log_group: str, *, options: dict = None) -> list:
    '''Returns the properties of all `"log item"` objects for a log group.
    
    :param server: instance of the `server` class
    :param log_group: name of log group that log item exists
    :param options: *(optional)* Dict of parameters to filter, sort or pagenate the list of log groups. Options are 'filter', 
    'sortOrder', 'sortProperty', 'pageNumber', and 'pageSize'. Only used when exchange_name is not defined.

    :return: list of properties for all log items in the log group requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(f'{server.url}{Log_Group._create_url(log_group)}{_create_url()}', params= options)
    return r.payload
