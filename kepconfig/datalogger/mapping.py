# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`mapping` exposes an API to allow modifications (add, delete, modify) to 
column mapping objects in a Datalogger log group within the Kepware Configuration API
"""

from . import log_group as Log_Group

MAPPING_ROOT = '/column_mappings'

def _create_url(mapping = None):
    '''Creates url object for the "column_mappings" branch of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure

    Returns the mapping specific url when a value is passed as the column_mapping name.
    '''

    if mapping == None:
        return '{}'.format(MAPPING_ROOT)
    else:
        return '{}/{}'.format(MAPPING_ROOT, mapping)

def modify_mapping(server, log_group, DATA, mapping = None, force = False):
    '''Modify a column mapping object and it's properties in Kepware. If a "mapping" is not provided as an input,
    you need to identify the column mapping in the 'common.ALLTYPES_NAME' property field in the "DATA". It will 
    assume that is the column mapping that is to be modified.

    INPUTS:
    "server" - instance of the "server" class

    "log_group" - name of log group that mapping exists

    "DATA" - properly JSON object (dict) of the agent properties to be modified

    "mapping" (optional) - column mapping to modify in the log group. Only needed if not existing in "DATA"

    "force" (optional) - if True, will force the configuration update to the Kepware server

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    
    mapping_data = server._force_update_check(force, DATA)
    
    if mapping == None:
        try:
            r = server._config_update(server.url + Log_Group._create_url(log_group) + _create_url(mapping_data['common.ALLTYPES_NAME']), mapping_data)
            if r.code == 200: return True 
            else: return False
        except KeyError as err:
            print('Error: No column mapping identified in DATA | Key Error: {}'.format(err))
            return False
        # except:
        #     return 'Error: Error with {}'.format(inspect.currentframe().f_code.co_name)
    else:
        r = server._config_update(server.url + Log_Group._create_url(log_group) + _create_url(mapping), mapping_data)
        if r.code == 200: return True 
        else: return False

def get_mapping(server, log_group, mapping):
    '''Returns the properties of the mapping object. Returned object is JSON.
    
    INPUTS:
    "server" - instance of the "server" class

    "log_group" - name of log group that mapping exists

    "mapping" - name of column mapping to retrieve properties for

    RETURNS:
    JSON - data for the column mapping requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    r = server._config_get(server.url + Log_Group._create_url(log_group) + _create_url(mapping))
    return r.payload

def get_all_mappings(server, log_group):
    '''Returns the properties of all column mapping objects for a log group. Returned object is JSON list.
    
    INPUTS:
    "server" - instance of the "server" class

    "log_group" - name of log group

    RETURNS:
    JSON - data for the column mappings requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    r = server._config_get(server.url + Log_Group._create_url(log_group) + _create_url())
    return r.payload
