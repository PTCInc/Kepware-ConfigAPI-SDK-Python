# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Datalogger Test - Test to exectute various calls for the Datalogger 
# parts of the Kepware configuration API

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kepconfig
import kepconfig.connectivity
import kepconfig.iot_gateway
from kepconfig import datalogger
import json
import time
import datetime


# Channel and Device name to be used
ch_name = 'Channel1'
dev_name = 'Device1'
log_group_name = 'LG'
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

def __log_items_test(server, log_group):
	log_item1 = {
		"common.ALLTYPES_NAME": "LogItem1",
		"datalogger.LOG_ITEM_ID": "_System._Time"
	}

	log_item2 = {
		"common.ALLTYPES_NAME": "LogItem2",
		"datalogger.LOG_ITEM_ID": "_System._Date"
	}

	log_item3 = {
		"common.ALLTYPES_NAME": "LogItem3",
		"datalogger.LOG_ITEM_ID": "_System._Time_Second"
	}

	try:
		print(datalogger.log_items.add_log_item(server, log_group, log_item1))
	except Exception as err:
		HTTPErrorHandler(err)
	try:
		print(datalogger.log_items.del_log_item(server, log_group, log_item1['common.ALLTYPES_NAME']))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.log_items.add_log_item(server, log_group, [log_item1, log_item2]))
	except Exception as err:
		HTTPErrorHandler(err)
	
	# Fails for item 2 since it's already existing
	try:
		print(datalogger.log_items.add_log_item(server, log_group, [log_item2, log_item3]))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.log_items.modify_log_item(server, log_group, {"datalogger.LOG_ITEM_NUMERIC_ID": "1"} ,log_item1['common.ALLTYPES_NAME'], force=True))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.log_items.modify_log_item(server, log_group, {"datalogger.LOG_ITEM_NUMERIC_ID": "0"} ,log_item1['common.ALLTYPES_NAME']))
	except Exception as err:
		HTTPErrorHandler(err)

	# Fail due to item not identified
	try:
		print(datalogger.log_items.modify_log_item(server, log_group, {"datalogger.LOG_ITEM_NUMERIC_ID": "0"}))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.log_items.modify_log_item(server, log_group, {"common.ALLTYPES_NAME": "LogItem1","datalogger.LOG_ITEM_NUMERIC_ID": "0"}, force= True))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.log_items.get_log_item(server, log_group,log_item1['common.ALLTYPES_NAME']))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.log_items.get_all_log_items(server, log_group))
	except Exception as err:
		HTTPErrorHandler(err)

	# Execute mapping test before deleting items
	# Modify group to wide format
	try:
		print(datalogger.log_group.modify_log_group(server, {"datalogger.LOG_GROUP_TABLE_FORMAT": 1}, log_group, force=True))
	except Exception as err:
		HTTPErrorHandler(err)
	
	__mapping_test(server, log_group)

	# Delete Items
	try:
		print(datalogger.log_items.del_log_item(server, log_group,log_item1['common.ALLTYPES_NAME']))
	except Exception as err:
		HTTPErrorHandler(err)
	
	try:
		print(datalogger.log_items.del_log_item(server, log_group,log_item2['common.ALLTYPES_NAME']))
	except Exception as err:
		HTTPErrorHandler(err)

def __triggers_test(server, log_group):
	trigger1 = {
		"common.ALLTYPES_NAME": "Trigger2",
		"datalogger.TRIGGER_TYPE": 0
	}

	trigger2 = {

		"common.ALLTYPES_NAME": "Trigger3",
		"datalogger.TRIGGER_TYPE": 1
	}

	trigger3 = {

		"common.ALLTYPES_NAME": "Trigger4",
		"datalogger.TRIGGER_TYPE": 1
	}
	
	try:
		print(datalogger.triggers.add_trigger(server, log_group, trigger1))
	except Exception as err:
		HTTPErrorHandler(err)
	try:
		print(datalogger.triggers.del_trigger(server, log_group, trigger1['common.ALLTYPES_NAME']))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.triggers.add_trigger(server, log_group, [trigger1, trigger2]))
	except Exception as err:
		HTTPErrorHandler(err)
	
	# Fails adding trigger 2 since it exists
	try:
		print(datalogger.triggers.add_trigger(server, log_group, [trigger2, trigger3]))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.triggers.modify_trigger(server, log_group, {"datalogger.TRIGGER_STATIC_INTERVAL": 1000} ,trigger1['common.ALLTYPES_NAME'], force=True))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.triggers.modify_trigger(server, log_group, {"datalogger.TRIGGER_STATIC_INTERVAL": 500} ,trigger1['common.ALLTYPES_NAME']))
	except Exception as err:
		HTTPErrorHandler(err)

	# Fail due to trigger not identified
	try:
		print(datalogger.triggers.modify_trigger(server, log_group, {"datalogger.TRIGGER_STATIC_INTERVAL": 500}))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.triggers.modify_trigger(server, log_group, {"common.ALLTYPES_NAME": trigger1['common.ALLTYPES_NAME'],"datalogger.TRIGGER_STATIC_INTERVAL": 1000}, force= True))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.triggers.get_trigger(server, log_group,trigger1['common.ALLTYPES_NAME']))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.triggers.get_all_triggers(server, log_group))
	except Exception as err:
		HTTPErrorHandler(err)

	# Delete triggers
	try:
		print(datalogger.triggers.del_trigger(server, log_group,trigger1['common.ALLTYPES_NAME']))
	except Exception as err:
		HTTPErrorHandler(err)
	
	try:
		print(datalogger.triggers.del_trigger(server, log_group,trigger2['common.ALLTYPES_NAME']))
	except Exception as err:
		HTTPErrorHandler(err)

def __mapping_test(server, log_group):
	
	map = []
	try:
		map = datalogger.mapping.get_all_mappings(server, log_group)
		print(map)
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.mapping.get_mapping(server, log_group, map[0]['common.ALLTYPES_NAME']))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.mapping.modify_mapping(server, log_group, {"datalogger.TABLE_ALIAS_SQL_LENGTH_QUALITY": 10} , map[0]['common.ALLTYPES_NAME'], force=True))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.mapping.modify_mapping(server, log_group, {"datalogger.TABLE_ALIAS_SQL_LENGTH_QUALITY": 15} , map[0]['common.ALLTYPES_NAME']))
	except Exception as err:
		HTTPErrorHandler(err)

	# Fail due to map not identified
	try:
		print(datalogger.mapping.modify_mapping(server, log_group, {"datalogger.TABLE_ALIAS_SQL_LENGTH_QUALITY": 1}))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.mapping.modify_mapping(server, log_group, {"common.ALLTYPES_NAME": map[0]['common.ALLTYPES_NAME'],"datalogger.TABLE_ALIAS_SQL_LENGTH_QUALITY": 0}, force= True))
	except Exception as err:
		HTTPErrorHandler(err)

def datalogger_test(server):
	log_group_data1 = {
		"common.ALLTYPES_NAME": log_group_name,
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
	log_group_data2 = {
		"common.ALLTYPES_NAME": log_group_name +'1',
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

	log_group_data3 = {
		"common.ALLTYPES_NAME": log_group_name +'2',
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

	try:
		print(datalogger.log_group.add_log_group(server, log_group_data1))
	except Exception as err:
		HTTPErrorHandler(err)
	
	try:
		print(datalogger.log_group.enable_log_group(server,log_group_name))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.log_group.disable_log_group(server,log_group_name))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.log_group.del_log_group(server, log_group_name))
	except Exception as err:
		HTTPErrorHandler(err)
	
	try:
		print(datalogger.log_group.add_log_group(server, [log_group_data1, log_group_data2]))
	except Exception as err:
		HTTPErrorHandler(err)
	
	# Log Group 2 should fail since it exists
	try:
		print(datalogger.log_group.add_log_group(server, [log_group_data2, log_group_data3]))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.log_group.modify_log_group(server, {"datalogger.LOG_GROUP_USE_LOCAL_TIME_FOR_TIMESTAMP_INSERTS": False},log_group_data1['common.ALLTYPES_NAME'], force=True))
	except Exception as err:
		HTTPErrorHandler(err)
	
	try:
		print(datalogger.log_group.modify_log_group(server,{"datalogger.LOG_GROUP_USE_LOCAL_TIME_FOR_TIMESTAMP_INSERTS": True},log_group_data1['common.ALLTYPES_NAME']))
	except Exception as err:
		HTTPErrorHandler(err)

	# Fail due to no log_group name provided
	try:
		print(datalogger.log_group.modify_log_group(server,{"datalogger.LOG_GROUP_USE_LOCAL_TIME_FOR_TIMESTAMP_INSERTS": True}))
	except Exception as err:
		HTTPErrorHandler(err)
	
	try:
		print(datalogger.log_group.modify_log_group(server,{"common.ALLTYPES_NAME": log_group_name,"datalogger.LOG_GROUP_USE_LOCAL_TIME_FOR_TIMESTAMP_INSERTS": True}))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.log_group.get_log_group(server, log_group_name))
	except Exception as err:
		HTTPErrorHandler(err)
	
	try:
		print(datalogger.log_group.get_all_log_groups(server))
	except Exception as err:
		HTTPErrorHandler(err)

	# Execute Log Items testing
	__log_items_test(server, log_group_name)

	# Execute Triggers testing
	__triggers_test(server, log_group_name)

	# Execute Services
	try:
		print(datalogger.log_group.reset_column_mapping_service(server,log_group_name))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		lg_left = datalogger.log_group.get_all_log_groups(server)
		for x in lg_left:
			print(datalogger.log_group.del_log_group(server, x['common.ALLTYPES_NAME']))
	except Exception as err:
		HTTPErrorHandler(err)

if __name__ == "__main__":
	time_start = time.perf_counter()

	# This creates a server reference that is used to target all modifications of 
	# the Kepware configuration
	server = kepconfig.connection.server(host = 'localhost', port = 57412, user = 'Administrator', pw = '', https = False)
	
	datalogger_test(server)

	time_end = time.perf_counter()
	print ('Complete {}! {} - Took {} seconds'.format(os.path.basename(__file__),time.asctime(), time_end - time_start))	

