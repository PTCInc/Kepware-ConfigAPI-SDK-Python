# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`triggers` exposes an API to allow modifications (add, delete, modify) to 
trigger objects in a Datalogger log group within the Kepware Configuration API
"""

from typing import Union
from . import log_group as Log_Group
from ..error import KepError, KepHTTPError
from ..connection import server

TRIGGERS_ROOT = '/triggers'

def _create_url(trigger = None):
    '''Creates url object for the "trigger" branch of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure

    Returns the trigger specific url when a value is passed as the trigger name.
    '''

    if trigger == None:
        return '{}'.format(TRIGGERS_ROOT)
    else:
        return '{}/{}'.format(TRIGGERS_ROOT, trigger)


def add_trigger(server: server, log_group: str, DATA: Union[dict, list]) -> Union[bool, list]:
    '''Add a `"trigger"` or multiple `"trigger"` objects to a log group in Kepware's Datalogger. It can 
    be used to pass a list of triggers to be added all at once.

    :param server: instance of the `server` class
    :param log_group: name of log group for the trigger items
    :param DATA: Dict or a list of the trigger items to add through Kepware Configuration API

    :return: True - If a "HTTP 201 - Created" is received from Kepware server
    :return: If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    triggers added that failed.

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

def del_trigger(server: server, log_group: str, trigger: str) -> bool:
    '''Delete a `"trigger"` object of a log group in Kepware's Datalogger.
    
    :param server: instance of the `server` class
    :param log_group: name of log group for the trigger items
    :param trigger: name of trigger to delete

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_del(server.url + Log_Group._create_url(log_group) + _create_url(trigger))
    if r.code == 200: return True
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_trigger(server: server, log_group: str, DATA: dict, *, trigger: str = None, force: bool = False)  -> bool:
    '''Modify a `"trigger"` object and it's properties in Kepware. If a `"trigger"` is not provided as an input,
    you need to identify the trigger in the *'common.ALLTYPES_NAME'* property field in the `"DATA"`. It will 
    assume that is the trigger that is to be modified.

    :param server: instance of the `server` class
    :param log_group: name of log group for the trigger items
    :param DATA: Dict of the trigger properties to be modified.
    :param trigger: *(optional)* name of trigger to modify in the log group. Only needed if not existing in `"DATA"`
    :param force: *(optional)* if True, will force the configuration update to the Kepware server

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    
    trigger_data = server._force_update_check(force, DATA)
    
    if trigger == None:
        try:
            r = server._config_update(server.url + Log_Group._create_url(log_group) + _create_url(trigger_data['common.ALLTYPES_NAME']), trigger_data)
            if r.code == 200: return True 
            else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
        except KeyError as err:
            err_msg = 'Error: No trigger identified in DATA | Key Error: {}'.format(err)
            raise KepError(err_msg)
        # except:
        #     return 'Error: Error with {}'.format(inspect.currentframe().f_code.co_name)
    else:
        r = server._config_update(server.url + Log_Group._create_url(log_group) + _create_url(trigger), trigger_data)
        if r.code == 200: return True 
        else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def get_trigger(server, log_group, trigger) -> dict:
    '''Returns the properties of the `"trigger"` object.
    
    :param server: instance of the `server` class
    :param log_group: name of log group for the trigger items
    :param trigger: name of trigger to retrieve

    :return: Dict of properties for the trigger requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(server.url + Log_Group._create_url(log_group) + _create_url(trigger))
    return r.payload

def get_all_triggers(server: server, log_group: str, *, options: dict = None) -> list:
    '''Returns the properties of all `"trigger"` objects for a log group.
    
    :param server: instance of the `server` class
    :param log_group: name of log group for the trigger items

    :return: Dict of properties for the trigger requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    :param options: *(optional)* Dict of parameters to filter, sort or pagenate the list of triggers. Options are 'filter', 
    'sortOrder', 'sortProperty', 'pageNumber', and 'pageSize'. Only used when exchange_name is not defined.

    :return: list of properties for all triggers in the log group requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(f'{server.url}{Log_Group._create_url(log_group)}{_create_url()}', params= options)
    return r.payload
