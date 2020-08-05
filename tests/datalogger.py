# -------------------------------------------------------------------------
# Copyright (c) 2020, PTC Inc. and/or all its affiliates. All rights reserved.
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
log_group_name = 'LG1'
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

def datalogger_test(server):
	log_group_data = {
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

	try:
		print(datalogger.log_group.add_log_group(server, log_group_data))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.log_group.get_log_group(server, log_group_name))
	except Exception as err:
		HTTPErrorHandler(err)

	try:
		print(datalogger.log_group.del_log_group(server, log_group_name))
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

