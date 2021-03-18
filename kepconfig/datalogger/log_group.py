# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`log_group` exposes an API to allow modifications (add, delete, modify) to 
log group objects in DataLogger within the Kepware Configuration API
"""
from typing import Union
from kepconfig.connection import KepServiceResponse
from kepconfig import connection, error as KepError

ENABLE_PROPERTY = 'datalogger.LOG_GROUP_ENABLED'
LOG_GROUP_ROOT = '/project/_datalogger/log_groups'
SERVICES_ROOT = '/services'
def _create_url(log_group = None):
    '''Creates url object for the "log_group" branch of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure

    Returns the agent specific url when a value is passed as the agent name.
    '''

    if log_group == None:
        return '{}'.format(LOG_GROUP_ROOT)
    else:
        return '{}/{}'.format(LOG_GROUP_ROOT, log_group)


def add_log_group(server, DATA) -> Union[bool, list]:
    '''Add a "log group" or multiple "log groups" objects to Kepware's DataLogger. It can be used 
    to pass a list of log groups to be added all at once.

    INPUTS:
    "server" - instance of the "server" class

    *DATA* - properly JSON object (dict) of the log group expected by Kepware Configuration API

    RETURNS:
    True - If a "HTTP 201 - Created" is received from Kepware

    List - If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    log groups added that failed.

    False - If a non-expected "2xx successful" code is returned

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_add(server.url + _create_url(), DATA)
    if r.code == 201: return True 
    elif r.code == 207:
        errors = [] 
        for item in r.payload:
            if item['code'] != 201:
                errors.append(item)
        return errors
    else: return False

def del_log_group(server, log_group):
    '''Delete a "log group" object in Kepware's Datalogger.
    
    INPUTS:
    "server" - instance of the "server" class

    "log_group" - name of log group

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    r = server._config_del(server.url + _create_url(log_group))
    if r.code == 200: return True 
    else: return False

def modify_log_group(server, DATA, log_group = None, force = False):
    '''Modify a log group object and it's properties in Kepware's Datalogger. If a "log group" is not provided as an input,
    you need to identify the log group in the 'common.ALLTYPES_NAME' property field in the "DATA". It will 
    assume that is the log group that is to be modified.

    INPUTS:
    "server" - instance of the "server" class

    "DATA" - properly JSON object (dict) of the agent properties to be modified

    "log_group" (optional) - name of log group. Only needed if not existing in "DATA"

    "force" (optional) - if True, will force the configuration update to the Kepware server

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    
    log_group_data = server._force_update_check(force, DATA)
    
    if log_group == None:
        try:
            r = server._config_update(server.url + _create_url(log_group_data['common.ALLTYPES_NAME']), log_group_data)
            if r.code == 200: return True 
            else: return False
        except KeyError as err:
            print('Error: No log group identified in DATA | Key Error: {}'.format(err))
            return False
        # except:
        #     return 'Error: Error with {}'.format(inspect.currentframe().f_code.co_name)
    else:
        r = server._config_update(server.url + _create_url(log_group), log_group_data)
        if r.code == 200: return True 
        else: return False

def get_log_group(server, log_group):
    '''Returns the properties of the log group object. Returned object is JSON.
    
    INPUTS:
    "server" - instance of the "server" class

    "log_group" - name of log group

    RETURNS:
    JSON - data for the log group requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    r = server._config_get(server.url + _create_url(log_group))
    return r.payload

def get_all_log_groups(server):
    '''Returns the properties of all log group objects for Kepware's Datalogger. Returned object is JSON list.
    
    INPUTS:
    "server" - instance of the "server" class

    RETURNS:
    JSON - data for the log groups requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    r = server._config_get(server.url + _create_url())
    return r.payload

def enable_log_group(server, log_group):
    '''Enable the log group. Returned object is JSON.
    
    INPUTS:
    "server" - instance of the "server" class

    "log_group" - name of log group

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    DATA = {ENABLE_PROPERTY: True}
    return modify_log_group(server, DATA, log_group)

def disable_log_group(server, log_group):
    '''Disable the log group. Returned object is JSON.
    
    INPUTS:
    "server" - instance of the "server" class

    "log_group" - name of log group

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    DATA = {ENABLE_PROPERTY: False}
    return modify_log_group(server, DATA, log_group)

def reset_column_mapping_service(server, log_group, job_ttl = None) -> KepServiceResponse:
    '''Executes a ResetColumnMapping serivce call to the log group

    INPUTS:
    "server" - instance of the "server" class

    "log_group" - name of log group

    RETURNS:
    KepServiceResponse instance with job information
    
    EXCEPTIONS (If not HTTP 200 or 429 returned):
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    try:
        url = server.url + _create_url(log_group) + SERVICES_ROOT + '/ResetColumnMapping'
        job = server._kep_service_execute(url, job_ttl)
        return job
    except Exception as err:
        raise err