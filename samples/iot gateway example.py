# -------------------------------------------------------------------------
# Copyright (c) 2020, PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# IoT Gateway Example - Simple example on how to manage a connection and 
# exectute various calls for the IoT Gateway components of the Kepware
# configuration API

from kepconfig import connection, error
from kepconfig.connectivity import channel
import kepconfig.iot_gateway as IoT
from kepconfig.iot_gateway import agent, iot_items
import json

# Agent name and Type to be used - constants from kepconfig.iotgateway 
# can be used to identify the type of agent
agent_name = 'MQTT Agent 1'
agent_type = IoT.MQTT_CLIENT_AGENT

#Tag Address to add to the IoT agent
iot_item_name = "Channel1.Device1.Tag1"

def HTTPErrorHandler(err):
    # Generic Handler for exception errors
    if err.__class__ is error.KepHTTPError:
        print(err.code)
        print(err.msg)
        print(err.url)
        print(err.hdrs)
        print(err.payload)
    elif err.__class__ is error.KepURLError:
        print(err.url)
        print(err.reason)
    else:
        print('Different Exception Received: {}'.format(err))

# This creates a server reference that is used to target all modifications of 
# the Kepware configuration
server = connection.server(host = '127.0.0.1', port = 57412, user = 'Administrator', pw = '')


# Add a Channel using the "Simulator Driver"with device and tags. 
# These tags will be added to the IoT Agent.
channel_data = {
    "common.ALLTYPES_NAME": "Channel1",
    "common.ALLTYPES_DESCRIPTION": "This is the test channel created",
    "servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator",
    "devices": [
        {
            "common.ALLTYPES_NAME": "Device1",
            "common.ALLTYPES_DESCRIPTION": "Hello, new description",
            "servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator",
            "servermain.DEVICE_MODEL": 0,
            "tags": [
                {
                    "common.ALLTYPES_NAME": "Tag1",
                    "common.ALLTYPES_DESCRIPTION": "Ramping Read/Write tag used to verify client connection",
                    "servermain.TAG_ADDRESS": "R0001",
                    "servermain.TAG_DATA_TYPE": 5,
                    "servermain.TAG_READ_WRITE_ACCESS": 1,
                    "servermain.TAG_SCAN_RATE_MILLISECONDS": 100,
                    "servermain.TAG_SCALING_TYPE": 0
                },
                {
                    "common.ALLTYPES_NAME": "Tag2",
                    "common.ALLTYPES_DESCRIPTION": "Constant Read/Write tag used to verify client connection",
                    "servermain.TAG_ADDRESS": "K0001",
                    "servermain.TAG_DATA_TYPE": 5,
                    "servermain.TAG_READ_WRITE_ACCESS": 1,
                    "servermain.TAG_SCAN_RATE_MILLISECONDS": 100,
                    "servermain.TAG_SCALING_TYPE": 0
                }
            ]
        }
    ]
}
try:
    print("{} - {}".format("Adding Channel, Device and tags", channel.add_channel(server,channel_data)))
except Exception as err:
    HTTPErrorHandler(err)


# Add the MQTT Agent with the appropriate parameters
agent_data = {
    "common.ALLTYPES_NAME": agent_name,
	"iot_gateway.AGENTTYPES_ENABLED": True,
	"iot_gateway.MQTT_CLIENT_URL": "tcp://localhost:1883",
	"iot_gateway.MQTT_CLIENT_TOPIC": "iotgateway",
	"iot_gateway.MQTT_CLIENT_QOS": 1,
	"iot_gateway.AGENTTYPES_RATE_MS": 10000,
	"iot_gateway.AGENTTYPES_PUBLISH_FORMAT": 0,
	"iot_gateway.AGENTTYPES_MAX_EVENTS": 1000,
	"iot_gateway.AGENTTYPES_TIMEOUT_S": 5,
	"iot_gateway.AGENTTYPES_MESSAGE_FORMAT": 0,
    "iot_gateway.MQTT_CLIENT_CLIENT_ID": "",
	"iot_gateway.MQTT_CLIENT_USERNAME": "",
	"iot_gateway.MQTT_CLIENT_PASSWORD": ""
}
try:
    print("{} - {}".format("Add the MQTT Agent", agent.add_iot_agent(server, agent_data, agent_type)))
except Exception as err:
    HTTPErrorHandler(err)

# Modify a parperty of the Agent
agent_data = {
}
agent_data['common.ALLTYPES_DESCRIPTION'] = 'This is the test agent created'
try:
    print("{} - {}".format("Modify property in the MQTT Agent", agent.modify_iot_agent(server,agent_data, agent_name, agent_type)))
except Exception as err:
    HTTPErrorHandler(err)

# Get Agent the properties for the agent that was created. It will return the 
# JSON of the properties
try:
    print("{} - {}".format("Read properties of the MQTT Agent", agent.get_iot_agent(server, agent_name, agent_type)))
except Exception as err:
    HTTPErrorHandler(err)

# Get a list of all MQTT Agents that are configured
try:
    print("{} - {}".format("Getting list of MQTT Agents", agent.get_all_iot_agents(server, agent_type)))
except Exception as err:
    HTTPErrorHandler(err)

# Add an tag or IoT Item to the MQTT Agent to start publishing
iot_item_data = {
        "common.ALLTYPES_NAME": iot_item_name,
        "common.ALLTYPES_DESCRIPTION": "",
        "iot_gateway.IOT_ITEM_SERVER_TAG": iot_item_name,
        "iot_gateway.IOT_ITEM_USE_SCAN_RATE": True,
        "iot_gateway.IOT_ITEM_SCAN_RATE_MS": 1000,
        "iot_gateway.IOT_ITEM_SEND_EVERY_SCAN": False,
        "iot_gateway.IOT_ITEM_DEADBAND_PERCENT": 0,
        "iot_gateway.IOT_ITEM_ENABLED": True,
        "iot_gateway.IOT_ITEM_DATA_TYPE": 5 
        }
try:
    print("{} - {}".format("Add new tag to the MQTT Agent", iot_items.add_iot_item(server, iot_item_data, agent_name, agent_type)))
except Exception as err:
    HTTPErrorHandler(err)

# Modify properties of the tag or IoT Item. If the "common.ALLTYPES_Name" is defined
# the "modify_iot_item" function does not need have the agent name as an input
modify_iot_item = {
        "common.ALLTYPES_NAME": iot_item_name,
        "iot_gateway.IOT_ITEM_SCAN_RATE_MS": 500
}
try:
    print("{} - {}".format("Modify the tag or IoT Item added", iot_items.modify_iot_item(server, modify_iot_item, agent_name, agent_type)))
except Exception as err:
    HTTPErrorHandler(err)

# Modify properties of the tag or IoT Item. (Version 2) It is not necessary to pass JSON 
# with the "common.ALLTYPES_Name" of the tag to modify. It can be passed as a input
# for the "modify_iot_item" function. "Force" will force the 
# update to the Kepware Server, if "FORCE_UPDATE" not provided in the JSON data.
modify_iot_item = {
        "iot_gateway.IOT_ITEM_SCAN_RATE_MS": 2000
}
try:
    print("{} - {}".format("Modify the tag or IoT Item added again", iot_items.modify_iot_item(server, modify_iot_item, agent_name, agent_type, iot_item_name, force = True)))
except Exception as err:
    HTTPErrorHandler(err)

# Read the tag or IoT Item configured in the MQTT Agent
try:
    print("{} - {}".format("Read the properties of the IoT Item", iot_items.get_iot_item(server, iot_item_name, agent_name, agent_type)))
except Exception as err:
    HTTPErrorHandler(err)

# Get a list of all tags or IoT Items configured in the MQTT Agent
try:
    print("{} - {}".format("Get a list of all the IoT Items configured in the MQTT Agent", iot_items.get_all_iot_items(server, agent_name, agent_type)))
except Exception as err:
    HTTPErrorHandler(err)

# Delete a tag or IoT Item configured in the MQTT Agent
try:
    print("{} - {}".format("Delete the IoT Item", iot_items.del_iot_item(server, iot_item_name, agent_name, agent_type)))
except Exception as err:
    HTTPErrorHandler(err)

# Delete the MQTT Agent
try:
    print("{} - {}".format("Delete the MQTT Agent", agent.del_iot_agent(server, agent_name, agent_type)))
except Exception as err:
    HTTPErrorHandler(err)