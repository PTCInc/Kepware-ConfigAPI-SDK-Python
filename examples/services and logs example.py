# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Services and Logs Example - Simple example on how to call services and
# get logs from the Kepware Configuration API

from kepconfig import connection, error
from kepconfig.connectivity import channel, device
import json
import datetime

# Channel and Device name to be used
ch_name = 'ControlLogix_Channel'
dev_name = 'Device1'
device_IP = '192.168.1.100'
# Service Response Global
r = {}

def ErrorHandler(err):
    # Generic Handler for exception errors
    if err.__class__ is error.KepError:
        print(err.msg)
    elif err.__class__ is error.KepHTTPError:
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

# This Reinitializes Kepware's Server Runtime process, similar to manually reinitializing
# using the Configuration UI or the Administrator tool.
try:
    r = server.reinitialize()
    print('{} - {}'.format("Execute Reinitialize Service", r))
except Exception as err:
    ErrorHandler(err)

# This reads the Reinitialize Service Job Status using the returned KepServiceResponse

try:
    print('{} - {}'.format("Read Reinitialize Service Status", server.service_status(r)))
except Exception as err:
    ErrorHandler(err)

# Add a Channel using the "ControlLogix Driver" with a ControlLogix 5500 family device. 
# This will be used to demonstrate the "Auto Tag Generation" service available.
channel_data = {
    "common.ALLTYPES_NAME": ch_name,
    "common.ALLTYPES_DESCRIPTION": "This is the test channel created",
    "servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Allen-Bradley Controllogix Ethernet",
    "devices": [
        {
            "common.ALLTYPES_NAME": dev_name,
            "common.ALLTYPES_DESCRIPTION": "Hello, new description",
            "servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Allen-Bradley Controllogix Ethernet",
            "servermain.DEVICE_MODEL": 0,
            "servermain.DEVICE_ID_STRING": "<{}>,1,0".format(device_IP)
        }
    ]
}
try:
    print("{} - {}".format("Adding Controllogix Channel and Device", channel.add_channel(server,channel_data)))
except Exception as err:
    ErrorHandler(err)

# Execute the "TagGeneration" service available in the Kepware Configuration API
try:
    r = device.auto_tag_gen(server, '{}.{}'.format(ch_name, dev_name))
    print("{} - {}".format("Executing ATG for Controllogix Device", r))
except Exception as err:
    ErrorHandler(err)

# This reads the TagGeneration Service Job Status using the returned KepServiceResponse
try:
    print('{} - {}'.format("Read Service Status", server.service_status(r)))
except Exception as err:
    ErrorHandler(err)

# Get Event Log from Kepware instance.
# Time parameters need to be UTC values.
try:
    print("{} - {}".format("Here is the last Event Log Entry", json.dumps(server.get_event_log(1), indent=4)))
except Exception as err:
    ErrorHandler(err)
try:
    print("{} - {}".format("Here are the last 25 entries of the Event Log", json.dumps(server.get_event_log(25, datetime.datetime.fromisoformat('2019-11-03T23:35:23.000'), datetime.datetime.utcnow()), indent=4)))
except Exception as err:
    ErrorHandler(err)

#Get Configuration API Transaction Log
try:
    print("{} - {}".format("Here is the last API Transaction Log Entry", json.dumps(server.get_transaction_log(1), indent=4)))
except Exception as err:
    ErrorHandler(err)

