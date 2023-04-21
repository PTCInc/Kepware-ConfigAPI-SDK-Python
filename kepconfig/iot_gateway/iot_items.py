# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


r"""`iot_items` exposes an API to allow modifications (add, delete, modify) to 
iot_items objects within the Kepware Configuration API
"""

from typing import Union
from .. import utils
from ..connection import server
from .. import iot_gateway as IOT
from ..error import KepError, KepHTTPError

IOT_ITEMS_ROOT = '/iot_items'

def _create_url(tag = None):
    '''Creates url object for the "iot items" branch of Kepware's IoT Agents property model. Used 
    to build a part of Kepware Configuration API URL structure
    
    Returns the device specific url when a value is passed as the iot item name.
    '''
    if tag == None:
        return IOT_ITEMS_ROOT
    else: 
        normalized_tag = utils._address_dedecimal(tag)
        return '{}/{}'.format(IOT_ITEMS_ROOT,normalized_tag)


def add_iot_item(server: server, DATA: dict | list, agent: str, agent_type: str) -> Union[bool, list]:
    '''Add a `"iot item"` or multiple `"iot item"` objects to Kepware's IoT Gateway agent. Additionally 
    it can be used to pass a list of iot items to be added to an agent all at once.

    :param server: instance of the `server` class
    :param DATA: Dict or List of Dicts of the iot item or list of items
    expected by Kepware Configuration API
    :param agent: name of IoT Agent
    :param agent_type: agent type. Valid values are `MQTT Client`, `REST Client` or `REST Server`

    :return: True - If a "HTTP 201 - Created" is received from Kepware server
    :return: If a "HTTP 207 - Multi-Status" is received from Kepware with a list of dict error responses for all 
    iot items added that failed.

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_add(server.url + IOT.agent._create_url(agent_type, agent) + _create_url(), DATA)
    if r.code == 201: return True
    elif r.code == 207:
            errors = [] 
            for item in r.payload:
                if item['code'] != 201:
                    errors.append(item)
            return errors 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def del_iot_item(server: server, iot_item: str, agent: str, agent_type: str) -> bool:
    '''Delete an `"iot item"` object in Kepware.

    :param server: instance of the `server` class
    :param iot_item: IoT item to delete
    :param agent: name of IoT Agent
    :param agent_type: agent type. Valid values are `MQTT Client`, `REST Client` or `REST Server`

    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_del(server.url + IOT.agent._create_url(agent_type, agent) + _create_url(iot_item))
    if r.code == 200: return True 
    else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def modify_iot_item(server: server, DATA: dict, agent: str, agent_type: str, *, iot_item: str = None, force: bool = False) -> bool:
    '''Modify an `"iot item"` object and it's properties in Kepware. If a `"iot item"` is not provided as an input,
    you need to identify the iot item in the *'common.ALLTYPES_NAME'* property field in the `"DATA"`. It will 
    assume that is the iot item that is to be modified.

    :param server: instance of the `server` class
    :param DATA: Dict of the iot item properties to be modified.
    :param agent: name of IoT Agent
    :param agent_type: agent type. Valid values are `MQTT Client`, `REST Client` or `REST Server`
    :param iot_item: *(optional)* name of IoT item to modify. Only needed if not existing in `"DATA"`
    :param force: *(optional)* if True, will force the configuration update to the Kepware server
    
    :return: True - If a "HTTP 200 - OK" is received from Kepware server

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    
    agent_data = server._force_update_check(force, DATA)
    if iot_item == None:
        try:
            r = server._config_update(server.url + IOT.agent._create_url(agent_type, agent) + _create_url(agent_data['common.ALLTYPES_NAME']), agent_data)
            if r.code == 200: return True 
            else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)
        except KeyError as err:
            err_msg = 'Error: No agent identified in DATA | Key Error: {}'.format(err)
            raise KepError(err_msg)
    else:
        r = server._config_update(server.url + IOT.agent._create_url(agent_type, agent) + _create_url(iot_item), agent_data)
        if r.code == 200: return True 
        else: raise KepHTTPError(r.url, r.code, r.msg, r.hdrs, r.payload)

def get_iot_item(server: server, iot_item: str, agent: str, agent_type: str)-> dict:
    '''Returns the properties of the `"iot item"` object.

    :param server: instance of the `server` class
    :param iot_item: name of IoT item to retrieve properties
    :param agent: name of IoT Agent
    :param agent_type: agent type. Valid values are `MQTT Client`, `REST Client` or `REST Server`

    :return: Dict of properties for the iot item requested

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(server.url + IOT.agent._create_url(agent_type, agent) + _create_url(iot_item))
    return r.payload

def get_all_iot_items(server: server, agent: str, agent_type: str, *, options: dict = None) -> list:
    '''Returns the properties of all `"iot item"` objects for an agent.
    
    :param server: instance of the `server` class
    :param iot_item: name of IoT item to retrieve properties
    :param agent: name of IoT Agent
    :param agent_type: agent type. Valid values are `MQTT Client`, `REST Client` or `REST Server`
    :param options: *(optional)* Dict of parameters to filter, sort or pagenate the list of IoT items. Options are 'filter', 
    'sortOrder', 'sortProperty', 'pageNumber', and 'pageSize'. Only used when exchange_name is not defined.

    :return: list of properties for all IoT items

    :raises KepHTTPError: If urllib provides an HTTPError
    :raises KepURLError: If urllib provides an URLError
    '''
    r = server._config_get(f'{server.url}{IOT.agent._create_url(agent_type, agent)}{_create_url()}', params= options)
    return r.payload