# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


r"""`agent` exposes an API to allow modifications (add, delete, modify) to 
Iot Gateway agent objects within the Kepware Configuration API
"""

# from .. import connection 
from typing import Union
from ..connection import server
from .. import iot_gateway as IOT
from ..error import KepError, KepHTTPError
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


def add_iot_agent(server: server, DATA: Union[dict, list], agent_type: str = None) -> Union[bool, list]:
    '''Add a  `"agent"` or multiple `"agent"` objects of a specific type to Kepware's IoT Gateway. Can be used to pass children of an
    agent object such as iot items. This allows you to create an agent and iot items if desired. Multiple Agents need to be of the 
    same type.

    Additionally it can be used to pass a list of agents and it's children to be added all at once.

    :param server: instance of the `server` class
    :param DATA: Dict or List of Dicts of the agent and it's children
    expected by Kepware Configuration API
    :param agent_type: *(optional)* agent type to add to IoT Gateway. Only needed if not existing in `"DATA"`. Valid values are 
    `MQTT Client`, `REST Client` or `REST Server`

    :return: True - If a "HTTP 201 - Created" is received from Kepware server
    :return: If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    iot agents added that failed.

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    
    if agent_type == None:
        try:
            r = server._config_update(server.url + _create_url(DATA['iot_gateway.AGENTTYPES_TYPE']), DATA)
            if r.code == 201: return True 
            else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
        except KeyError as err:
            err_msg = 'Error: No agent identified in DATA | Key Error: {}'.format(err)
            raise KepError(err_msg)
    else:
        r = server._config_add(server.url + _create_url(agent_type), DATA)
        if r.code == 201: return True 
        elif r.code == 207:
            errors = [] 
            for item in r.payload:
                if item['code'] != 201:
                    errors.append(item)
            return errors
        else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def del_iot_agent(server: server, agent: str, agent_type: str) -> bool:
    '''Delete a `"agent"` object in Kepware. This will delete all children as well
    
    :param server: instance of the `server` class
    :param agent: name of IoT Agent to delete
    :param agent_type: *(optional)* agent type to delete in IoT Gateway. Valid values are 
    `MQTT Client`, `REST Client` or `REST Server`

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_del(server.url + _create_url(agent_type, agent))
    if r.code == 200: return True 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_iot_agent(server: server, DATA: dict, *, agent: str = None, agent_type: str = None, force: bool = False) -> bool:
    '''Modify a `"agent"` object and it's properties in Kepware. If a `"agent"` is not provided as an input,
    you need to identify the agent in the *'common.ALLTYPES_NAME'* property field in the `"DATA"`. It will 
    assume that is the agent that is to be modified.

    :param server: instance of the `server` class
    :param DATA: Dict of the iot agent properties to be modified.
    :param agent: *(optional)* name of IoT agent to modify. Only needed if not existing in `"DATA"`
    :param agent_type: *(optional)* agent type to modify. Only needed if not existing in `"DATA"`. Valid values are 
    `MQTT Client`, `REST Client` or `REST Server`
    :param force: *(optional)* if True, will force the configuration update to the Kepware server

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    
    agent_data = server._force_update_check(force, DATA)
    
    if agent_type == None:
        if 'iot_gateway.AGENTTYPES_TYPE' in DATA:
            agent_type = DATA['iot_gateway.AGENTTYPES_TYPE']
        else:
            err_msg = 'Error: Error with {}: {}'.format(inspect.currentframe().f_code.co_name, 'No Agent type defined.')
            raise KepError(err_msg)
    if agent == None:
        try:
            r = server._config_update(server.url + _create_url(agent_type, agent_data['common.ALLTYPES_NAME']), agent_data)
            if r.code == 200: return True 
            else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
        except KeyError as err:
            err_msg = 'Error: No agent identified in DATA | Key Error: {}'.format(err)
            raise KepError(err_msg)
    else:
        r = server._config_update(server.url + _create_url(agent_type, agent), agent_data)
        if r.code == 200: return True 
        else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def get_iot_agent(server: server, agent: str, agent_type: str) -> dict:
    '''Returns the properties of the `"agent"` object.
    
    :param server: instance of the `server` class
    :param DATA: Dict of the iot agent properties to be modified.
    :param agent: name of IoT agent to retrieve
    :param agent_type: agent type. Valid values are `MQTT Client`, `REST Client` or `REST Server`

    :return: Dict of properties for the iot agent requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(server.url + _create_url(agent_type, agent))
    return r.payload

def get_all_iot_agents(server: server, agent_type: str, *, options: dict = None) -> list:
    '''Returns the properties of all `"agent"` objects for a specific agent type. Returned object is JSON list.
    
    :param server: instance of the `server` class
    :param agent_type: agent type. Valid values are `MQTT Client`, `REST Client` or `REST Server`
    :param options: *(optional)* Dict of parameters to filter, sort or pagenate the list of IoT agents. Options are 'filter', 
    'sortOrder', 'sortProperty', 'pageNumber', and 'pageSize'. Only used when exchange_name is not defined.

    :return: list of properties for all IoT agents requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(f'{server.url}{_create_url(agent_type)}', params= options)
    return r.payload
