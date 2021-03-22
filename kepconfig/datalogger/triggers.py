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


def add_trigger(server, log_group, DATA) -> Union[bool, list]:
    '''Add a "trigger" or multiple "trigger" objects to a log group in Kepware's Datalogger. It can 
    be used to pass a list of triggers to be added all at once.

    INPUTS:
    "server" - instance of the "server" class

    "log_group" - name of log group that the triggers will be added

    *DATA* - properly JSON object (dict) of the trigger expected by Kepware Configuration API

    RETURNS:
    True - If a "HTTP 201 - Created" is received from Kepware

    List - If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    triggers added that failed.

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

def del_trigger(server, log_group, trigger) -> bool:
    '''Delete a "trigger" object of a log group in Kepware's Datalogger.
    
    INPUTS:
    "server" - instance of the "server" class

    "log_group" - name of log group that trigger exists

    "trigger" - name of trigger to delete

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    r = server._config_del(server.url + Log_Group._create_url(log_group) + _create_url(trigger))
    if r.code == 200: return True
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_trigger(server, log_group, DATA, trigger = None, force = False)  -> bool:
    '''Modify a trigger object and it's properties in Kepware. If a "trigger" is not provided as an input,
    you need to identify the trigger in the 'common.ALLTYPES_NAME' property field in the "DATA". It will 
    assume that is the trigger that is to be modified.

    INPUTS:
    "server" - instance of the "server" class

    "log_group" - name of log group that trigger exists

    "DATA" - properly JSON object (dict) of the agent properties to be modified

    "trigger" (optional) - trigger to modify in the log group. Only needed if not existing in "DATA"

    "force" (optional) - if True, will force the configuration update to the Kepware server

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
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
    '''Returns the properties of the trigger object. Returned object is JSON.
    
    INPUTS:
    "server" - instance of the "server" class

    "log_group" - name of log group that trigger exists

    "trigger" - name of trigger to retrieve properties for

    RETURNS:
    dict - data for the trigger requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    r = server._config_get(server.url + Log_Group._create_url(log_group) + _create_url(trigger))
    return r.payload

def get_all_triggers(server, log_group) -> list:
    '''Returns the properties of all trigger objects for a log group. Returned object is JSON list.
    
    INPUTS:
    "server" - instance of the "server" class

    "log_group" - name of log group

    RETURNS:
    list - data for the triggers requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    r = server._config_get(server.url + Log_Group._create_url(log_group) + _create_url())
    return r.payload
