# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# IoT Gateway Test - Test to exersice all IoT Gateway related features

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kepconfig
import kepconfig.admin
import kepconfig.connectivity
import kepconfig.iot_gateway
import json
import time
import datetime
import pytest


# IoT Gateway configs to be used
mqtt_agent_name = 'MQTT'
rest_agent_name = 'REST Client'
rserver_agent_name = 'REST Server'
twx_agent_name = 'Thingworx'
iot_item_name ="System__Date"

agent_list = [
        [mqtt_agent_name, kepconfig.iot_gateway.MQTT_CLIENT_AGENT],
        [rest_agent_name, kepconfig.iot_gateway.REST_CLIENT_AGENT], 
        [rserver_agent_name, kepconfig.iot_gateway.REST_SERVER_AGENT]
        ]

agent_data = {
            "common.ALLTYPES_NAME": 'TempName',
            "iot_items":[
                {
                "common.ALLTYPES_NAME": "_System_Time",
                "common.ALLTYPES_DESCRIPTION": "",
                "iot_gateway.IOT_ITEM_SERVER_TAG": "_System._Time",
                "iot_gateway.IOT_ITEM_USE_SCAN_RATE": True,
                "iot_gateway.IOT_ITEM_SCAN_RATE_MS": 1000,
                "iot_gateway.IOT_ITEM_SEND_EVERY_SCAN": False,
                "iot_gateway.IOT_ITEM_DEADBAND_PERCENT": 0,
                "iot_gateway.IOT_ITEM_ENABLED": True,
                "iot_gateway.IOT_ITEM_DATA_TYPE": 5 
                }
            ]
            
        }

iot_item_data = {
                "common.ALLTYPES_NAME": iot_item_name,
                "common.ALLTYPES_DESCRIPTION": "",
                "iot_gateway.IOT_ITEM_SERVER_TAG": "_System._Date",
                "iot_gateway.IOT_ITEM_USE_SCAN_RATE": True,
                "iot_gateway.IOT_ITEM_SCAN_RATE_MS": 1000,
                "iot_gateway.IOT_ITEM_SEND_EVERY_SCAN": False,
                "iot_gateway.IOT_ITEM_DEADBAND_PERCENT": 0,
                "iot_gateway.IOT_ITEM_ENABLED": True,
                "iot_gateway.IOT_ITEM_DATA_TYPE": 5 
                }

def HTTPErrorHandler(err):
    if err.__class__ is kepconfig.error.KepHTTPError:
        print(err.code)
        print(err.msg)
        print(err.url)
        print(err.hdrs)
        print(err.payload)
    else:
        print('Different Exception Received: {}'.format(err))

def initialize(server):
    pass

def complete(server):
    # Delete all Agents
    for agent_type in agent_list:
        try:
            agent_left = kepconfig.iot_gateway.agent.get_all_iot_agents(server, agent_type[1])
            for x in agent_left:
                print(kepconfig.iot_gateway.agent.del_iot_agent(server,x['common.ALLTYPES_NAME'],agent_type[1]))
        except Exception as err:
            HTTPErrorHandler(err)

@pytest.fixture(scope="module")
def server(kepware_server):
    server = kepware_server
    
    # Initialize any configuration before testing in module
    initialize(server)

    # Everything below yield is run after module tests are completed
    yield server
    complete(server)

def test_agent_add(server):
    for agent_name, agent_type in agent_list:
        # Add Agent
        agent = agent_data.copy()
        agent['common.ALLTYPES_NAME'] = agent_name

        assert kepconfig.iot_gateway.agent.add_iot_agent(server, agent, agent_type)
        
        # Add Agent without Agent Type (error)
        agent['common.ALLTYPES_NAME'] = agent_name + "1"
        assert kepconfig.iot_gateway.agent.add_iot_agent(server, agent) == False

        # Add Agent with bad name (error)
        agent = [
            {
            "common.ALLTYPES_NAME": agent_name + "1"
            },
            {
            "common.ALLTYPES_NAME": "_" + agent_name
            },
        ]
        assert type(kepconfig.iot_gateway.agent.add_iot_agent(server, agent, agent_type)) == list

def test_agent_modify(server):
    for agent_name, agent_type in agent_list:
        # Modify Agent
        agent = {}
        agent['common.ALLTYPES_DESCRIPTION'] = 'This is the test agent created'
        assert kepconfig.iot_gateway.agent.modify_iot_agent(server,agent, agent_name, agent_type)

        # Modify Agent without type (error)
        agent = {}
        agent['common.ALLTYPES_DESCRIPTION'] = 'This is the test agent created'
        assert kepconfig.iot_gateway.agent.modify_iot_agent(server,agent, agent_name) == False
        
def test_agent_get(server):
    for agent_name, agent_type in agent_list:
        # Get Agent
        assert type(kepconfig.iot_gateway.agent.get_iot_agent(server, agent_name, agent_type)) == dict

        # Get All Agents
        assert type(kepconfig.iot_gateway.agent.get_all_iot_agents(server, agent_type)) == list
 

def test_iot_item_add(server):       
    for agent_name, agent_type in agent_list:
        # Add Iot Item
        assert kepconfig.iot_gateway.iot_items.add_iot_item(server, iot_item_data, agent_name, agent_type)
        
        # Add Iot Items with one failed
        
        iot_item_data2 = [
            {
                "common.ALLTYPES_NAME": iot_item_name + "1",
                "common.ALLTYPES_DESCRIPTION": "",
                "iot_gateway.IOT_ITEM_SERVER_TAG": "_System._Time_Minute",
                "iot_gateway.IOT_ITEM_USE_SCAN_RATE": True,
                "iot_gateway.IOT_ITEM_SCAN_RATE_MS": 1000,
                "iot_gateway.IOT_ITEM_SEND_EVERY_SCAN": False,
                "iot_gateway.IOT_ITEM_DEADBAND_PERCENT": 0,
                "iot_gateway.IOT_ITEM_ENABLED": True,
                "iot_gateway.IOT_ITEM_DATA_TYPE": 5 
            },
            {
                "common.ALLTYPES_NAME": iot_item_name,
                "common.ALLTYPES_DESCRIPTION": "",
                "iot_gateway.IOT_ITEM_SERVER_TAG": "_System._Time_Seconds",
                "iot_gateway.IOT_ITEM_USE_SCAN_RATE": True,
                "iot_gateway.IOT_ITEM_SCAN_RATE_MS": 1000,
                "iot_gateway.IOT_ITEM_SEND_EVERY_SCAN": False,
                "iot_gateway.IOT_ITEM_DEADBAND_PERCENT": 0,
                "iot_gateway.IOT_ITEM_ENABLED": True,
                "iot_gateway.IOT_ITEM_DATA_TYPE": 5 
            }
        ]
        assert type(kepconfig.iot_gateway.iot_items.add_iot_item(server, iot_item_data2, agent_name, agent_type)) == list
        
def test_iot_item_modify(server):
    for agent_name, agent_type in agent_list:
        # Modify IoT Item
        modify_iot_item = {
                "common.ALLTYPES_NAME": iot_item_name,
                "common.ALLTYPES_DESCRIPTION": "Modified the IoT Item"
        }
        assert kepconfig.iot_gateway.iot_items.modify_iot_item(server, modify_iot_item, agent_name, agent_type)

        # Modify IoT Item v 2
        modify_iot_item = {
                "iot_gateway.IOT_ITEM_SCAN_RATE_MS": 2000,
        }
        assert kepconfig.iot_gateway.iot_items.modify_iot_item(server, modify_iot_item, agent_name, agent_type, iot_item_name, force = True)

def test_iot_item_get(server):        
    for agent_name, agent_type in agent_list:
        # Read IoT Item
        assert type(kepconfig.iot_gateway.iot_items.get_iot_item(server, iot_item_name, agent_name, agent_type)) == dict

        # Read All IoT Items
        assert type(kepconfig.iot_gateway.iot_items.get_all_iot_items(server, agent_name, agent_type)) == list

def test_iot_item_del(server):        
    for agent_name, agent_type in agent_list:
        # Delete IoT Item
        assert kepconfig.iot_gateway.iot_items.del_iot_item(server, iot_item_name, agent_name, agent_type)

def test_agent_del(server):
    for agent_name, agent_type in agent_list:
        # Delete IoT Agent
        assert kepconfig.iot_gateway.agent.del_iot_agent(server, agent_name, agent_type)