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


def add_log_item(server, log_group, DATA) -> Union[bool, list]:
    '''Add a "log item" or multiple "log item" objects to a log group in Kepware's Datalogger. It can 
    be used to pass a list of log items to be added all at once.

    INPUTS:
    "server" - instance of the "server" class

    "log_group" - name of log group that the log items will be added

    *DATA* - properly JSON object (dict) of the log item expected by Kepware Configuration API

    RETURNS:
    True - If a "HTTP 201 - Created" is received from Kepware

    List - If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    log items added that failed.

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
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

def del_log_item(server, log_group, log_item) -> bool:
    '''Delete a "log item" object of a log group in Kepware's Datalogger.
    
    INPUTS:
    "server" - instance of the "server" class

    "log_group" - name of log group that log item exists

    "log_item" - name of log item to delete

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    r = server._config_del(server.url + Log_Group._create_url(log_group) + _create_url(log_item))
    if r.code == 200: return True 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_log_item(server, log_group, DATA, log_item = None, force = False) -> bool:
    '''Modify a log_item object and it's properties in Kepware. If a "log_item" is not provided as an input,
    you need to identify the log_item in the 'common.ALLTYPES_NAME' property field in the "DATA". It will 
    assume that is the log_item that is to be modified.

    INPUTS:
    "server" - instance of the "server" class

    "log_group" - name of log group that log item exists

    "DATA" - properly JSON object (dict) of the agent properties to be modified

    "log_item" (optional) - log item to modify in the log group. Only needed if not existing in "DATA"

    "force" (optional) - if True, will force the configuration update to the Kepware server

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
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
        # except:
        #     return 'Error: Error with {}'.format(inspect.currentframe().f_code.co_name)
    else:
        r = server._config_update(server.url + Log_Group._create_url(log_group) + _create_url(log_item), log_item_data)
        if r.code == 200: return True 
        else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def get_log_item(server, log_group, log_item) -> dict:
    '''Returns the properties of the log item object. Returned object is JSON.
    
    INPUTS:
    "server" - instance of the "server" class

    "log_group" - name of log group that log item exists

    "log_item" - name of log item to retrieve properties for

    RETURNS:
    dict - data for the log item requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    r = server._config_get(server.url + Log_Group._create_url(log_group) + _create_url(log_item))
    return r.payload

def get_all_log_items(server: server, log_group: str, *, options: dict = None) -> list:
    '''Returns the properties of all log item objects for a log group. Returned object is JSON list.
    
    INPUTS:
    server - instance of the "server" class

    log_group - name of log group

    options - (optional) Dict of parameters to filter, sort or pagenate the list of log items. Options are 'filter', 
    'sortOrder', 'sortProperty', 'pageNumber', and 'pageSize'

    RETURNS:
    list - data for the log items requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    r = server._config_get(f'{server.url}{Log_Group._create_url(log_group)}{_create_url()}', params= options)
    return r.payload
