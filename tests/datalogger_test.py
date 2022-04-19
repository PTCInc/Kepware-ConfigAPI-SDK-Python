# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Datalogger Test - Test to exectute various calls for the Datalogger 
# parts of the Kepware configuration API

from kepconfig.error import KepError
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kepconfig
import kepconfig.connectivity
import kepconfig.iot_gateway
from kepconfig import datalogger
import json
import time
import datetime
import pytest


# Datalogger configs to be used
log_group_name = 'LG'

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

def HTTPErrorHandler(err):
    if err.__class__ is kepconfig.error.KepHTTPError:
        print(err.code)
        print(err.msg)
        print(err.url)
        print(err.hdrs)
        print(err.payload)
    else:
        print('Different Exception Received: {}'.format(err))
		
def initialize(server: kepconfig.connection.server):
	try:
		server._config_get(server.url +"/project/_datalogger")
	except Exception as err:
		pytest.skip("DataLogger plug-in is not installed", allow_module_level=True)

def complete(server):
	try:
		lg_left = datalogger.log_group.get_all_log_groups(server)
		for x in lg_left:
			print(datalogger.log_group.del_log_group(server, x['common.ALLTYPES_NAME']))
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

def test_log_group_add(server):
	assert datalogger.log_group.add_log_group(server, log_group_data1)
	
	assert datalogger.log_group.enable_log_group(server,log_group_name)

	assert datalogger.log_group.disable_log_group(server,log_group_name)

	assert datalogger.log_group.del_log_group(server, log_group_name)
	
	assert datalogger.log_group.add_log_group(server, [log_group_data1, log_group_data2])
	
	# Log Group 2 should fail since it exists
	assert type(datalogger.log_group.add_log_group(server, [log_group_data2, log_group_data3])) == list

def test_log_group_modify(server):
	assert datalogger.log_group.modify_log_group(server, {"datalogger.LOG_GROUP_USE_LOCAL_TIME_FOR_TIMESTAMP_INSERTS": False},log_group_data1['common.ALLTYPES_NAME'], force=True)
	
	assert datalogger.log_group.modify_log_group(server,{"datalogger.LOG_GROUP_USE_LOCAL_TIME_FOR_TIMESTAMP_INSERTS": True},log_group_data1['common.ALLTYPES_NAME'])

	# Fail due to no log_group name provided
	with pytest.raises(KepError):
		assert datalogger.log_group.modify_log_group(server,{"datalogger.LOG_GROUP_USE_LOCAL_TIME_FOR_TIMESTAMP_INSERTS": True})
	
	assert datalogger.log_group.modify_log_group(server,{"common.ALLTYPES_NAME": log_group_name,"datalogger.LOG_GROUP_USE_LOCAL_TIME_FOR_TIMESTAMP_INSERTS": True})

def test_log_group_get(server):
	assert type(datalogger.log_group.get_log_group(server, log_group_name)) == dict
	
	assert type(datalogger.log_group.get_all_log_groups(server)) == list

def test_log_item_add(server):
	assert datalogger.log_items.add_log_item(server, log_group_name, log_item1)

	assert datalogger.log_items.del_log_item(server, log_group_name, log_item1['common.ALLTYPES_NAME'])

	assert datalogger.log_items.add_log_item(server, log_group_name, [log_item1, log_item2])
	
	# Fails for item 2 since it's already existing
	assert type(datalogger.log_items.add_log_item(server, log_group_name, [log_item2, log_item3])) == list

def test_log_item_modify(server):
	assert datalogger.log_items.modify_log_item(server, log_group_name, {"datalogger.LOG_ITEM_NUMERIC_ID": "1"} ,log_item1['common.ALLTYPES_NAME'], force=True)

	assert datalogger.log_items.modify_log_item(server, log_group_name, {"datalogger.LOG_ITEM_NUMERIC_ID": "0"} ,log_item1['common.ALLTYPES_NAME'])

	# Fail due to item not identified
	with pytest.raises(KepError):
		assert datalogger.log_items.modify_log_item(server, log_group_name, {"datalogger.LOG_ITEM_NUMERIC_ID": "0"})

	assert datalogger.log_items.modify_log_item(server, log_group_name, {"common.ALLTYPES_NAME": "LogItem1","datalogger.LOG_ITEM_NUMERIC_ID": "0"}, force= True)

def test_log_item_get(server):
	assert type (datalogger.log_items.get_log_item(server, log_group_name,log_item1['common.ALLTYPES_NAME'])) == dict

	assert type(datalogger.log_items.get_all_log_items(server, log_group_name)) == list

	# Execute mapping test before deleting items
	# Modify group to wide format
	assert datalogger.log_group.modify_log_group(server, {"datalogger.LOG_GROUP_TABLE_FORMAT": 1}, log_group_name, force=True)

def test_mapping_get(server):
	mapping_list = []
	mapping_list = datalogger.mapping.get_all_mappings(server, log_group_name)

	assert type(mapping_list) == list

	assert type(datalogger.mapping.get_mapping(server, log_group_name, mapping_list[0]['common.ALLTYPES_NAME'])) == dict

def test_mapping_modify(server):
	mapping_list = []
	mapping_list = datalogger.mapping.get_all_mappings(server, log_group_name)
	assert datalogger.mapping.modify_mapping(server, log_group_name, {"datalogger.TABLE_ALIAS_SQL_LENGTH_QUALITY": 10} , mapping_list[0]['common.ALLTYPES_NAME'], force=True)

	assert datalogger.mapping.modify_mapping(server, log_group_name, {"datalogger.TABLE_ALIAS_SQL_LENGTH_QUALITY": 15} , mapping_list[0]['common.ALLTYPES_NAME'])

	# Fail due to map not identified
	with pytest.raises(KepError):
		assert datalogger.mapping.modify_mapping(server, log_group_name, {"datalogger.TABLE_ALIAS_SQL_LENGTH_QUALITY": 1})

	assert datalogger.mapping.modify_mapping(server, log_group_name, {"common.ALLTYPES_NAME": mapping_list[0]['common.ALLTYPES_NAME'],"datalogger.TABLE_ALIAS_SQL_LENGTH_QUALITY": 0}, force= True)

def test_log_item_del(server):
	# Delete Items
	assert datalogger.log_items.del_log_item(server, log_group_name,log_item1['common.ALLTYPES_NAME'])

	assert datalogger.log_items.del_log_item(server, log_group_name,log_item2['common.ALLTYPES_NAME'])

def test_trigger_add(server):
	assert datalogger.triggers.add_trigger(server, log_group_name, trigger1)
	
	assert datalogger.triggers.del_trigger(server, log_group_name, trigger1['common.ALLTYPES_NAME'])

	assert datalogger.triggers.add_trigger(server, log_group_name, [trigger1, trigger2])
	
	# Fails adding trigger 2 since it exists
	assert type(datalogger.triggers.add_trigger(server, log_group_name, [trigger2, trigger3])) == list
	
def test_trigger_modify(server):
	assert datalogger.triggers.modify_trigger(server, log_group_name, {"datalogger.TRIGGER_STATIC_INTERVAL": 1000} ,trigger1['common.ALLTYPES_NAME'], force=True)

	assert datalogger.triggers.modify_trigger(server, log_group_name, {"datalogger.TRIGGER_STATIC_INTERVAL": 500} ,trigger1['common.ALLTYPES_NAME'])

	# Fail due to trigger not identified
	with pytest.raises(KepError):
		assert datalogger.triggers.modify_trigger(server, log_group_name, {"datalogger.TRIGGER_STATIC_INTERVAL": 500})

	assert datalogger.triggers.modify_trigger(server, log_group_name, {"common.ALLTYPES_NAME": trigger1['common.ALLTYPES_NAME'],"datalogger.TRIGGER_STATIC_INTERVAL": 1000}, force= True)

def test_trigger_get(server):
	assert type(datalogger.triggers.get_trigger(server, log_group_name,trigger1['common.ALLTYPES_NAME'])) == dict
	assert type(datalogger.triggers.get_all_triggers(server, log_group_name)) == list

def test_trigger_del(server):
	# Delete triggers
	assert datalogger.triggers.del_trigger(server, log_group_name,trigger1['common.ALLTYPES_NAME'])
	
	assert datalogger.triggers.del_trigger(server, log_group_name,trigger2['common.ALLTYPES_NAME'])

def test_log_group_services(server):
	# Execute Services
	job = datalogger.log_group.reset_column_mapping_service(server,log_group_name)
	assert type(job) == kepconfig.connection.KepServiceResponse
	job = datalogger.log_group.reset_column_mapping_service(server,log_group_name, 60)
	assert type(job) == kepconfig.connection.KepServiceResponse

