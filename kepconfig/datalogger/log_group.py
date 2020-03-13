# -------------------------------------------------------------------------
# Copyright (c) 2020, PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r""":mod:`log_group` exposes an API to allow modifications (add, delete, modify) to 
Log Group objects within the Kepware Configuration API
"""


LOG_GROUP_ROOT_URL = '/project/_datalogger/log_groups'

def _create_url(log_group = None):
    '''Creates url object for the "agent" branch of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure

    Returns the agent specific url when a value is passed as the agent name.
    '''

    if log_group == None:
        return '{}'.format(LOG_GROUP_ROOT_URL)
    else:
        return '{}/{}'.format(LOG_GROUP_ROOT_URL, log_group)


def add_log_group(server, DATA):
    '''Add a  "agent" or multiple "agent" objects of a specific type to Kepware's IoT Gateway. Can be used to pass children of an
    agent object such as iot items. This allows you to create an agent and iot items if desired.

    Additionally it can be used to pass a list of agents and it's children to be added all at once.

    INPUTS:
    "server" - instance of the "server" class

    *DATA* - properly JSON object (dict) of the agent and it's children
    expected by Kepware Configuration API

    "agent_type" (optional) - agent type to add to IoT Gateway. Only needed if not existing in "DATA"

    RETURNS:
    True - If a "HTTP 201 - Created" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''

    r = server._config_add(server.url + _create_url(), DATA)
    if r.code == 201: return True 
    else: return False

def del_log_group(server, log_group):
    '''Delete a "agent" object in Kepware. This will delete all children as well
    
    INPUTS:
    "server" - instance of the "server" class

    "agent" - name of IoT Agent

    "agent_type" - agent type to delete to IoT Gateway

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
    '''Modify a agent object and it's properties in Kepware. If a "agent" is not provided as an input,
    you need to identify the agent in the 'common.ALLTYPES_NAME' property field in the "DATA". It will 
    assume that is the agent that is to be modified.

    INPUTS:
    "server" - instance of the "server" class

    "DATA" - properly JSON object (dict) of the agent properties to be modified

    "agent" (optional) - name of IoT Agent. Only needed if not existing in "DATA"

    "agent_type" (optional) -agent type to modify to IoT Gateway. Only needed if not existing in "DATA"

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
            print('Error: No agent identified in DATA | Key Error: {}'.format(err))
            return False
        # except:
        #     return 'Error: Error with {}'.format(inspect.currentframe().f_code.co_name)
    else:
        r = server._config_update(server.url + _create_url(log_group), log_group_data)
        if r.code == 200: return True 
        else: return False

def get_log_group(server, log_group):
    '''Returns the properties of the agent object. Returned object is JSON.
    
    INPUTS:
    "server" - instance of the "server" class

    "agent" - name of IoT Agent

    "agent_type" - agent type

    RETURNS:
    JSON - data for the IoT Agent requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    r = server._config_get(server.url + _create_url(log_group))
    return r.payload

def get_all_log_groups(server):
    '''Returns the properties of all agent objects for a specific agent type. Returned object is JSON list.
    
    INPUTS:
    "server" - instance of the "server" class

    "agent_type" - agent type

    RETURNS:
    JSON - data for the IoT Agents requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    r = server._config_get(server.url + _create_url())
    return r.payload
