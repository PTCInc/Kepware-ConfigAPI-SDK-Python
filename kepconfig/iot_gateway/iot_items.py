# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


r"""`iot_items` exposes an API to allow modifications (add, delete, modify) to 
iot_items objects within the Kepware Configuration API
"""

from typing import Union
import kepconfig as helper
from .. import iot_gateway as IOT
import inspect

IOT_ITEMS_ROOT = '/iot_items'

def _create_url(tag = None):
    '''Creates url object for the "iot items" branch of Kepware's IoT Agents property model. Used 
    to build a part of Kepware Configuration API URL structure
    
    Returns the device specific url when a value is passed as the iot item name.
    '''
    if tag == None:
        return IOT_ITEMS_ROOT
    else: 
        normalized_tag = helper._address_dedecimal(tag)
        return '{}/{}'.format(IOT_ITEMS_ROOT,normalized_tag)


def add_iot_item(server, DATA, agent, agent_type) -> Union[bool, list]:
    '''Add a "iot item" or multiple "iot item" objects to Kepware's IoT Gateway agent. Additionally 
    it can be used to pass a list of iot items to be added to an agent all at once.

    INPUTS:
    "server" - instance of the "server" class

    "DATA" - properly JSON object (dict) of the iot item or list of items
    expected by Kepware Configuration API.

    "agent" - name of IoT Agent

    "agent_type" - agent type

    RETURNS:
    True - If a "HTTP 201 - Created" is received from Kepware

    List - If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    iot items added that failed.

    False - If a non-expected "2xx successful" code is returned

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    r = server._config_add(server.url + IOT.agent._create_url(agent_type, agent) + _create_url(), DATA)
    if r.code == 201: return True
    elif r.code == 207:
            errors = [] 
            for item in r.payload:
                if item['code'] != 201:
                    errors.append(item)
            return errors 
    else: return False

def del_iot_item(server, iot_item, agent, agent_type):
    '''Delete a "iot item" object in Kepware.

    INPUTS:
    "server" - instance of the "server" class

    "iot_item" - IoT item to delete

    "agent" - name of IoT Agent

    "agent_type" - agent type 

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    r = server._config_del(server.url + IOT.agent._create_url(agent_type, agent) + _create_url(iot_item))
    if r.code == 200: return True 
    else: return False

def modify_iot_item(server, DATA, agent, agent_type, iot_item = None, force = False):
    '''Modify a iot item object and it's properties in Kepware. If a "iot item" is not provided as an input,
    you need to identify the iot item in the 'common.ALLTYPES_NAME' property field in the "DATA". It will 
    assume that is the iot item that is to be modified.

    INPUTS:
    "server" - instance of the "server" class

    "DATA" - properly JSON object (dict) of the iot item properties to be modified.

    "agent" - name of IoT Agent

    "agent_type" - agent type 

    "iot_item" (optional) - IoT item to modify

    "force" (optional) - if True, will force the configuration update to the Kepware server

    RETURNS:
    True - If a "HTTP 200 - OK" is received from Kepware

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    
    agent_data = server._force_update_check(force, DATA)
    if iot_item == None:
        try:
            r = server._config_update(server.url + IOT.agent._create_url(agent_type, agent) + _create_url(agent_data['common.ALLTYPES_NAME']), agent_data)
            if r.code == 200: return True 
            else: return False
        except KeyError as err:
            print('Error: No agent identified in DATA | Key Error: {}'.format(err))
            return False
        # except:
        #     return 'Error: Error with {}'.format(inspect.currentframe().f_code.co_name)
    else:
        r = server._config_update(server.url + IOT.agent._create_url(agent_type, agent) + _create_url(iot_item), agent_data)
        if r.code == 200: return True 
        else: return False

def get_iot_item(server, iot_item, agent, agent_type):
    '''Returns the properties of the agent object. Returned object is JSON.

    INPUTS:
    "server" - instance of the "server" class
    
    "iot_item" - IoT item

    "agent" - name of IoT Agent

    "agent_type" - agent type

    RETURNS:
    JSON - data for the IoT item requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    r = server._config_get(server.url + IOT.agent._create_url(agent_type, agent) + _create_url(iot_item))
    return r.payload

def get_all_iot_items(server, agent, agent_type):
    '''Returns the properties of all iot item objects for an agent. Returned object is JSON list.
    
    INPUTS:
    "server" - instance of the "server" class

    "agent" - name of IoT Agent

    "agent_type" - agent type

    RETURNS:
    JSON - data for the IoT item requested

    EXCEPTIONS:
    KepHTTPError - If urllib provides an HTTPError
    KepURLError - If urllib provides an URLError
    '''
    r = server._config_get(server.url + IOT.agent._create_url(agent_type, agent) + _create_url())
    return r.payload