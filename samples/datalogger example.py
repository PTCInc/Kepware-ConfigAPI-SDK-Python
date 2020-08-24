# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Datalogger Example - Simple example on how to manage a connection and 
# execute various calls for the Datalogger components of the Kepware
# Configuration API

from kepconfig import connection, error
from kepconfig.connectivity import channel
import kepconfig.datalogger as DL 
import json

# Log Group to be used with properties that can be configured

# Note: Ensure that all DSN and table configuraiton is updated appropriately 
# to target the DSN and table to log data
log_group1 = {
		"common.ALLTYPES_NAME": "Log_Group1",
		"common.ALLTYPES_DESCRIPTION": "",
		"datalogger.LOG_GROUP_ENABLED": False,
		"datalogger.LOG_GROUP_UPDATE_RATE_MSEC": 100,
		"datalogger.LOG_GROUP_UPDATE_RATE_UNITS": 0,
		"datalogger.LOG_GROUP_MAP_NUMERIC_ID_TO_VARCHAR": False,
		"datalogger.LOG_GROUP_USE_LOCAL_TIME_FOR_TIMESTAMP_INSERTS": True,
		"datalogger.LOG_GROUP_STORE_AND_FORWARD_ENABLED": False,
		"datalogger.LOG_GROUP_STORE_AND_FORWARD_STORAGE_DIRECTORY": "C:\\ProgramData\\PTC\\ThingWorx Kepware Server\\V6\\DataLogger",
		"datalogger.LOG_GROUP_STORE_AND_FORWARD_MAX_STORAGE_SIZE": 10,
		"datalogger.LOG_GROUP_MAX_ROW_BUFFER_SIZE": 1000,
		"datalogger.LOG_GROUP_DSN": "",
		"datalogger.LOG_GROUP_DSN_USERNAME": "",
		"datalogger.LOG_GROUP_DSN_PASSWORD": "",
		"datalogger.LOG_GROUP_DSN_LOGIN_TIMEOUT": 10,
		"datalogger.LOG_GROUP_DSN_QUERY_TIMEOUT": 15,
		"datalogger.LOG_GROUP_TABLE_SELECTION": 0,
		"datalogger.LOG_GROUP_TABLE_NAME": "",
		"datalogger.LOG_GROUP_TABLE_FORMAT": 0,
		"datalogger.LOG_GROUP_BATCH_ID_ITEM": "",
		"datalogger.LOG_GROUP_BATCH_ID_ITEM_TYPE": "Default",
		"datalogger.LOG_GROUP_BATCH_ID_UPDATE_RATE": 1000,
		"datalogger.LOG_GROUP_BATCH_ID_UPDATE_RATE_UNITS": 0,
		"datalogger.LOG_GROUP_REGENERATE_ALIAS_TABLE_ON_DSN_CHANGE": True,
		"datalogger.LOG_GROUP_REGENERATE_ALIAS_TABLE_ON_BATCH_ID_CHANGE": True,
		"datalogger.LOG_GROUP_REGENERATE_ALIAS_TABLE_ON_TABLE_NAME_CHANGE": False,
		"datalogger.LOG_GROUP_REGENERATE_ALIAS_TABLE_ON_TABLE_SELECTION_CHANGE": False
	}
#Log Items to add to the Log Group
log_item1 = {
		"common.ALLTYPES_NAME": "LogItem1",
		"datalogger.LOG_ITEM_ID": "Channel1.Device1.Tag1"
	}

log_item2 = {
		"common.ALLTYPES_NAME": "LogItem2",
		"datalogger.LOG_ITEM_ID": "Channel1.Device1.Tag2"
	}

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


# Add a Channel using the "Simulator Driver" with device and tags. 
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


# Add the Datalogger Log Group with the appropriate parameters
try:
    print("{} - {}".format("Add the Datalogger Log Group", DL.log_group.add_log_group(server, log_group1)))
except Exception as err:
    HTTPErrorHandler(err)

# Modify a property of the Log Group If the "common.ALLTYPES_Name" is defined
# the "modify_log_group" function does not need have the log group name as an input

# Change Update rate to 1000 ms
log_group_mod_properties = {
    "datalogger.LOG_GROUP_UPDATE_RATE_MSEC": 1000
}
try:
    print("{} - {}".format("Modify property in the Log Group", DL.log_group.modify_log_group(server,log_group_mod_properties,log_group1['common.ALLTYPES_NAME'])))
except Exception as err:
    HTTPErrorHandler(err)

# Get properties for the log group that was created. It will return the 
# JSON of the properties
try:
    print("{} - {}".format("Read properties of the Log Group", DL.log_group.get_log_group(server, log_group1['common.ALLTYPES_NAME'])))
except Exception as err:
    HTTPErrorHandler(err)

# Get a list of all Log Groups that are configured
try:
    print("{} - {}".format("Getting list of Log Groups", DL.log_group.get_all_log_groups(server)))
except Exception as err:
    HTTPErrorHandler(err)

# Add an tag or log item to the to the log group
try:
    print("{} - {}".format("Add new tags to the Log Group", DL.log_items.add_log_item(server, log_group1['common.ALLTYPES_NAME'], [log_item1,log_item2])))
except Exception as err:
    HTTPErrorHandler(err)

# Modify properties of the tag or log item. If the "common.ALLTYPES_Name" is defined
# the "modify_log_item" function does not need have the log item name as an input
modify_log_item = {
    "common.ALLTYPES_NAME": "LogItem1",
    "datalogger.LOG_ITEM_NUMERIC_ID": "1"
}
try:
    print("{} - {}".format("Modify the tag or Log Item added", DL.log_items.modify_log_item(server, log_group1['common.ALLTYPES_NAME'], modify_log_item)))
except Exception as err:
    HTTPErrorHandler(err)

# Modify properties of the tag or log Item. (Version 2) It is not necessary to pass JSON 
# with the "common.ALLTYPES_Name" of the tag to modify. It can be passed as a input
# for the "modify_log_item" function. "Force" will force the 
# update to the Kepware Server, if "FORCE_UPDATE" not provided in the JSON data.
modify_log_item = {
    "datalogger.LOG_ITEM_NUMERIC_ID": "0"
}
try:
    print("{} - {}".format("Modify the tag or Log Item added", DL.log_items.modify_log_item(server, log_group1['common.ALLTYPES_NAME'], modify_log_item, log_item1['common.ALLTYPES_NAME'])))
except Exception as err:
    HTTPErrorHandler(err)

# Read the tag or log Item configured in the Log Group
try:
    print("{} - {}".format("Read the properties of the Log Item", DL.log_items.get_log_item(server, log_group1['common.ALLTYPES_NAME'], log_item1['common.ALLTYPES_NAME'])))
except Exception as err:
    HTTPErrorHandler(err)

# Get a list of all tags or log Items configured in the Log Group
try:
    print("{} - {}".format("Get a list of all the Log Items configured in the Log Group", DL.log_items.get_all_log_items(server, log_group1['common.ALLTYPES_NAME'])))
except Exception as err:
    HTTPErrorHandler(err)

# Setup a trigger in the log group

# Trigger will only log data on DataChange - Disable static interval and ensure the trigger type is Always On
trigger_data = {
    "common.ALLTYPES_NAME": "DataChange Only",
    "datalogger.TRIGGER_TYPE": 0,
    "datalogger.TRIGGER_LOG_ON_STATIC_INTERVAL": False,
    "datalogger.TRIGGER_LOG_ON_DATA_CHANGE": True
}
try:
    print("{} - {}".format("Add new trigger to the Log Group", DL.triggers.add_trigger(server, log_group1['common.ALLTYPES_NAME'],trigger_data)))
except Exception as err:
    HTTPErrorHandler(err)

# Once configured, enable log group
try:
    print("{} - {}".format("Enable the Log Group", DL.log_group.enable_log_group(server, log_group1['common.ALLTYPES_NAME'])))
except Exception as err:
    HTTPErrorHandler(err)

# Note: Changes cannot be made to the log group while enabled

# Disable log group
try:
    print("{} - {}".format("Disable the Log Group", DL.log_group.disable_log_group(server, log_group1['common.ALLTYPES_NAME'])))
except Exception as err:
    HTTPErrorHandler(err)

# Delete the Log Group
try:
    print("{} - {}".format("Delete the Log Group", DL.log_group.del_log_group(server, log_group1['common.ALLTYPES_NAME'])))
except Exception as err:
    HTTPErrorHandler(err)