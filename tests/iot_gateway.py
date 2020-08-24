# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Test Example - Test to exectute various calls for the conenctivity 
# parts of the Kepware configuration API

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kepconfig
import kepconfig.admin
import kepconfig.connectivity
import kepconfig.iot_gateway
import json
import time
import datetime


# Channel and Device name to be used
ch_name = 'Channel1'
dev_name = 'Device1'
mqtt_agent_name = 'MQTT'
rest_agent_name = 'REST Client'
rserver_agent_name = 'REST Server'
twx_agent_name = 'Thingworx'
iot_item_name ="System__Date"

def HTTPErrorHandler(err):
    if err.__class__ is kepconfig.error.KepHTTPError:
        print(err.code)
        print(err.msg)
        print(err.url)
        print(err.hdrs)
        print(err.payload)
    else:
        print('Different Exception Received: {}'.format(err))

def iot_gateway_test(server):
    # 
    # Execute IoT Gateway Tests
    # 


    # agent_list = [mqtt_agent_name, rest_agent_name, rserver_agent_name, twx_agent_name]
    # type_list = [kepconfig.iot_gateway.MQTT_CLIENT_AGENT,kepconfig.iot_gateway.REST_CLIENT_AGENT,kepconfig.iot_gateway.REST_SERVER_AGENT,kepconfig.iot_gateway.THINGWORX_AGENT]

    agent_list = [
        [mqtt_agent_name, kepconfig.iot_gateway.MQTT_CLIENT_AGENT],
        [rest_agent_name, kepconfig.iot_gateway.REST_CLIENT_AGENT], 
        [rserver_agent_name, kepconfig.iot_gateway.REST_SERVER_AGENT]
        ]

    for agent_name, agent_type in agent_list:
        # Add Agent
        agent_data = {
            "common.ALLTYPES_NAME": agent_name,
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
        try:
            print(kepconfig.iot_gateway.agent.add_iot_agent(server, agent_data, agent_type))
        except Exception as err:
            HTTPErrorHandler(err)
        
        # Add Agent without Agent Type (error)
        agent_data = {
            "common.ALLTYPES_NAME": agent_name,
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
        try:
            print(kepconfig.iot_gateway.agent.add_iot_agent(server, agent_data))
        except Exception as err:
            HTTPErrorHandler(err)   

        # Modify Agent
        agent_data = {
        }
        agent_data['common.ALLTYPES_DESCRIPTION'] = 'This is the test agent created'
        try:
            print(kepconfig.iot_gateway.agent.modify_iot_agent(server,agent_data, agent_name, agent_type))
        except Exception as err:
            HTTPErrorHandler(err)

        # Modify Agent without type (error)
        agent_data = {
        }
        agent_data['common.ALLTYPES_DESCRIPTION'] = 'This is the test agent created'
        try:
            print(kepconfig.iot_gateway.agent.modify_iot_agent(server,agent_data, agent_name))
        except Exception as err:
            HTTPErrorHandler(err)

        # Get Agent
        try:
            print(kepconfig.iot_gateway.agent.get_iot_agent(server, agent_name, agent_type))
        except Exception as err:
            HTTPErrorHandler(err)
        # Get All Agents
        try:
            print(kepconfig.iot_gateway.agent.get_all_iot_agents(server, agent_type))
        except Exception as err:
            HTTPErrorHandler(err)   
        
        # Add Iot Item
        
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
        try:
            print(kepconfig.iot_gateway.iot_items.add_iot_item(server, iot_item_data, agent_name, agent_type))
        except Exception as err:
            HTTPErrorHandler(err)

        # Modify IoT Item
        modify_iot_item = {
                "common.ALLTYPES_NAME": iot_item_name,
                "common.ALLTYPES_DESCRIPTION": "Modified the IoT Item"
        }
        try:
            print(kepconfig.iot_gateway.iot_items.modify_iot_item(server, modify_iot_item, agent_name, agent_type))
        except Exception as err:
            HTTPErrorHandler(err)

        # Modify IoT Item v 2
        modify_iot_item = {
                "iot_gateway.IOT_ITEM_SCAN_RATE_MS": 2000,
        }
        try:
            print(kepconfig.iot_gateway.iot_items.modify_iot_item(server, modify_iot_item, agent_name, agent_type, iot_item_name, force = True))
        except Exception as err:
            HTTPErrorHandler(err)
        
        # Read IoT Item
        try:
            print(kepconfig.iot_gateway.iot_items.get_iot_item(server, iot_item_name, agent_name, agent_type))
        except Exception as err:
            HTTPErrorHandler(err)

        # Read All IoT Items
        try:
            print(kepconfig.iot_gateway.iot_items.get_all_iot_items(server, agent_name, agent_type))
        except Exception as err:
            HTTPErrorHandler(err)
        
        # Delete IoT Item
        try:
            print(kepconfig.iot_gateway.iot_items.del_iot_item(server, iot_item_name, agent_name, agent_type))
        except Exception as err:
            HTTPErrorHandler(err)
        # Delete IoT Agent
        try:
            print(kepconfig.iot_gateway.agent.del_iot_agent(server, agent_name, agent_type))
        except Exception as err:
            HTTPErrorHandler(err)  

if __name__ == "__main__":
    time_start = time.perf_counter()

    # This creates a server reference that is used to target all modifications of 
    # the Kepware configuration
    server = kepconfig.connection.server(host = 'localhost', port = 57412, user = 'Administrator', pw = '', https = False)

    iot_gateway_test(server)

    time_end = time.perf_counter()
    print('Complete {}! {} - Took {} seconds'.format(os.path.basename(__file__),time.asctime(), time_end - time_start))