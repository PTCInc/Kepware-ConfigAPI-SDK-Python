# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r""":mod:`agent` exposes an API to allow modifications (add, delete, modify) to 
Iot Gateway agent objects within the Kepware Configuration API
"""

# from .. import connection 
from .. import iot_gateway as IOT
import inspect

IOT_ROOT_URL = '/project/_iot_gateway'
MQTT_CLIENT_URL = '/mqtt_clients'
REST_CLIENT_URL = '/rest_clients'
REST_SERVER_URL = '/rest_servers'
THINGWORX_URL = '/thingworx_clients'

def _create_url(agent_type, agent = None):
    '''Creates url object for the "agent" branch of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure

    Returns the agent specific url when a value is passed as the agent name.
    '''

    if agent == None:
        if agent_type == IOT.MQTT_CLIENT_AGENT:
            return '{}{}'.format(IOT_ROOT_URL, MQTT_CLIENT_URL)
        elif agent_type == IOT.REST_CLIENT_AGENT:
            return '{}{}'.format(IOT_ROOT_URL, REST_CLIENT_URL)
        elif agent_type == IOT.REST_SERVER_AGENT:
            return '{}{}'.format(IOT_ROOT_URL, REST_SERVER_URL)
        elif agent_type == IOT.THINGWORX_AGENT:
            return '{}{}'.format(IOT_ROOT_URL, THINGWORX_URL)
        else:
            pass
    else:
        if agent_type == IOT.MQTT_CLIENT_AGENT:
            return '{}{}/{}'.format(IOT_ROOT_URL, MQTT_CLIENT_URL, agent)
        elif agent_type == IOT.REST_CLIENT_AGENT:
            return '{}{}/{}'.format(IOT_ROOT_URL, REST_CLIENT_URL, agent)
        elif agent_type == IOT.REST_SERVER_AGENT:
            return '{}{}/{}'.format(IOT_ROOT_URL, REST_SERVER_URL,agent)
        elif agent_type == IOT.THINGWORX_AGENT:
            return '{}{}/{}'.format(IOT_ROOT_URL, THINGWORX_URL, agent)
        else:
            pass


def add_iot_agent(server, DATA, agent_type = None):
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
    
    if agent_type == None:
        try:
            r = server._config_update(server.url + _create_url(DATA['iot_gateway.AGENTTYPES_TYPE']), DATA)
            if r.code == 201: return True 
            else: return False
        except KeyError as err:
            # print('Error: No agent identified in DATA | Key Error: {}'.format(err))
            return False
        # except:
        #     return 'Error: Error with {}'.format(inspect.currentframe().f_code.co_name)
    else:
        r = server._config_add(server.url + _create_url(agent_type), DATA)
        if r.code == 201: return True 
        else: return False

def del_iot_agent(server, agent, agent_type):
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
    r = server._config_del(server.url + _create_url(agent_type, agent))
    if r.code == 200: return True 
    else: return False

def modify_iot_agent(server, DATA, agent = None, agent_type = None, force = False):
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
    
    agent_data = server._force_update_check(force, DATA)
    
    if agent_type == None:
        if 'iot_gateway.AGENTTYPES_TYPE' in DATA:
            agent_type = DATA['iot_gateway.AGENTTYPES_TYPE']
        else:
            # print('Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, 'No Agent type defined.'))
            return False
    if agent == None:
        try:
            r = server._config_update(server.url + _create_url(agent_type, agent_data['common.ALLTYPES_NAME']), agent_data)
            if r.code == 200: return True 
            else: return False
        except KeyError as err:
            print('Error: No agent identified in DATA | Key Error: {}'.format(err))
            return False
        # except:
        #     return 'Error: Error with {}'.format(inspect.currentframe().f_code.co_name)
    else:
        r = server._config_update(server.url + _create_url(agent_type, agent), agent_data)
        if r.code == 200: return True 
        else: return False

def get_iot_agent(server, agent, agent_type):
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
    r = server._config_get(server.url + _create_url(agent_type, agent))
    return r.payload

def get_all_iot_agents(server, agent_type):
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
    r = server._config_get(server.url + _create_url(agent_type))
    return r.payload
