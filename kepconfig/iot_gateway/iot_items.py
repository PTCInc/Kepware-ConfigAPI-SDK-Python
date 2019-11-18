# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r""":mod:`iot_items` exposes an API to allow modifications (add, delete, modify) to 
iot_items objects within the Kepware Configuration API
"""

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


def add_iot_item(server, DATA, agent, agent_type):
    '''Add a "iot item" or multiple "iot item" objects to Kepware's IoT Gateway agent. Additionally 
    it can be used to pass a list of iot items to be added to an agent all at once.

    "server" - instance of the "server" class

    "DATA" - properly JSON object (dict) of the iot item or list of items
    expected by Kepware Configuration API.

    "agent" - name of IoT Agent

    "agent_type" - agent type
    '''
    return server._config_add(server.url + IOT.agent._create_url(agent_type, agent) + _create_url(), DATA)

def del_iot_item(server, iot_item, agent, agent_type):
    '''Delete a "iot item" object in Kepware.

    "server" - instance of the "server" class

    "iot_item" - IoT item to delete

    "agent" - name of IoT Agent

    "agent_type" - agent type 
    '''
    return server._config_del(server.url + IOT.agent._create_url(agent_type, agent) + _create_url(iot_item))

def modify_iot_item(server, DATA, agent, agent_type, iot_item = None, force = False):
    '''Modify a iot item object and it's properties in Kepware. If a "iot item" is not provided as an input,
    you need to identify the iot item in the 'common.ALLTYPES_NAME' property field in the "DATA". It will 
    assume that is the iot item that is to be modified.

    "server" - instance of the "server" class

    "DATA" - properly JSON object (dict) of the iot item properties to be modified.

    "agent" - name of IoT Agent

    "agent_type" - agent type 

    "iot_item" (optional) - IoT item to modify

    "force" (optional) - if True, will force the configuration update to the Kepware server
    '''
    
    agent_data = server._force_update_check(force, DATA)
    if iot_item == None:
        try:
            return server._config_update(server.url + IOT.agent._create_url(agent_type, agent) + _create_url(agent_data['common.ALLTYPES_NAME']), agent_data)
        except KeyError as err:
            return 'Error: No agent identified in DATA | Key Error: {}'.format(err)
        except:
            return 'Error: Error with {}'.format(inspect.currentframe().f_code.co_name)
    else:
        return server._config_update(server.url + IOT.agent._create_url(agent_type, agent) + _create_url(iot_item), agent_data)

def get_iot_item(server, iot_item, agent, agent_type):
    '''Returns the properties of the agent object. Returned object is JSON.

    "server" - instance of the "server" class
    
    "iot_item" - IoT item

    "agent" - name of IoT Agent

    "agent_type" - agent type
    '''
    return server._config_get(server.url + IOT.agent._create_url(agent_type, agent) + _create_url(iot_item))

def get_all_iot_items(server, agent, agent_type):
    '''Returns the properties of all iot item objects for an agent. Returned object is JSON list.
    
    "server" - instance of the "server" class

    "agent" - name of IoT Agent

    "agent_type" - agent type
    '''
    return server._config_get(server.url + IOT.agent._create_url(agent_type, agent) + _create_url())