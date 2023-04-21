# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Simple Connectivity Example - Simple example on how to manage a connection and 
# exectute various calls for the conenctivity components of the Kepware
# configuration API


from kepconfig import connection, error
from kepconfig.connectivity import channel, device, tag

# Channel and Device name to be used
ch_name = 'Channel1'
dev_name = 'Device1'

def ErrorHandler(err):
    # Generic Handler for exception errors
    if isinstance(err,  error.KepHTTPError):
        print(err.code)
        print(err.msg)
        print(err.url)
        print(err.hdrs)
        print(err.payload)
    elif isinstance(err,  error.KepURLError):
        print(err.url)
        print(err.reason)
    elif isinstance(err, error.KepError):
        print(err.msg)
    else:
        print('Different Exception Received: {}'.format(err))


# This creates a server reference that is used to target all modifications of 
# the Kepware configuration
server = connection.server(host = '127.0.0.1', port = 57412, user = 'Administrator', pw = '')

# HTTP server reference examples. Uses the OS/systems trusted CA certificate store for cert validation as it uses the 
# "create_default_context()" function as described here: 
# https://docs.python.org/3/library/ssl.html#ssl.create_default_context
# https://docs.python.org/3/library/ssl.html#ssl.SSLContext.load_default_certs
# https://docs.python.org/3/library/ssl.html#ssl.SSLContext.set_default_verify_paths
serverHTTPS = connection.server(host = '127.0.0.1', port = 57512, user = 'Administrator', pw = '', https=True)

# Disable Hostname check when validating certificate:
serverHTTPS.SSL_ignore_hostname = True

# Trust all certificates:
# During certificate validation trust any certificate - if True, will "set SSL_ignore_hostname" to true
serverHTTPS.SSL_trust_all_certs = True

# Modify the Kepware project properties
project_prop = {
    "uaserverinterface.PROJECT_OPC_UA_ENABLE": True,
    "opcdaserver.PROJECT_OPC_DA_1_ENABLED": True,
	"opcdaserver.PROJECT_OPC_DA_2_ENABLED": True,
	"opcdaserver.PROJECT_OPC_DA_3_ENABLED": True
}
try:
    print("{} - {}".format("Modifying Project Properties",server.modify_project_properties(project_prop, force = True)))
except Exception as err:
    ErrorHandler(err)

# Add a Channel using the "Simulator Driver"
channel_data = {
    "common.ALLTYPES_NAME": ch_name,
    "servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator"
    }
try:
    print("{} - {}".format("Adding Channel", channel.add_channel(server,channel_data)))
except Exception as err:
    ErrorHandler(err)
# Add a Device to the created Channel
device_data = {
    "common.ALLTYPES_NAME": dev_name,
    "servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator"
    }
try:
    print("{} - {}".format("Adding Device", device.add_device(server,ch_name,device_data)))
except Exception as err:
    ErrorHandler(err)

# Add a collection of Tags and Tag Group objects.
all_tags_data = {
    "tags": [
        {
            "common.ALLTYPES_NAME": "Temp",
            "servermain.TAG_ADDRESS": "R0"
        }
    ],
    "tag_groups": [
        {
            "common.ALLTYPES_NAME": "ALARM",
            "tags": [
                {
                    "common.ALLTYPES_NAME": "ALARM_C_READY",
                    "servermain.TAG_ADDRESS": "R1"
                }
            ],
            "tag_groups": [
                {
                    "common.ALLTYPES_NAME": "ALARM2",
                    "tags": [
                        {
                            "common.ALLTYPES_NAME": "ALARM_C_READY2",
                            "servermain.TAG_ADDRESS": "R2"
                        }
                    ]
                }
            ]
        }
    ]
}
try:
    print("{} - {}".format("Adding Tags and Tag Groups", tag.add_all_tags(server, ch_name + '.' + dev_name, all_tags_data)))
except Exception as err:
    ErrorHandler(err)

# Add tag to an existing tag group
tag_info = [
    {
            "common.ALLTYPES_NAME": "Temp",
            "servermain.TAG_ADDRESS": "R0"
    },
    {
            "common.ALLTYPES_NAME": "Temp2",
            "servermain.TAG_ADDRESS": "R1"
    }
]
tag_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2')
try:
    print("{} - {}".format("Adding Tags to Existing Tag Group", tag.add_tag(server, tag_path, tag_info)))
except Exception as err:
    ErrorHandler(err)

#
# Examples of reading properties for various objects (channels, devices, tags, etc)
#

# Get Channel
try:
    print("{} - {}".format("Read Channel Properties", channel.get_channel(server,ch_name)))
except Exception as err:
    ErrorHandler(err)

# Get Channel and all Device config with Tags and Tag groups
try:
    print("{} - {}".format("Read Channel Properties and all Devices and Tag/Tag Groups", channel.get_channel_structure(server, ch_name)))
except Exception as err:
    ErrorHandler(err)


# Get Device
device_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2.temp')
try:
    print("{} - {}".format("Read Device Properties", device.get_device(server, device_path)))
except Exception as err:
    ErrorHandler(err)

# Get Device and all tags/tag groups
device_path = '{}.{}'.format(ch_name, dev_name)
try:
    print("{} - {}".format("Read Device Properties and all Tags/Tag groups", device.get_device_structure(server, device_path)))
except Exception as err:
    ErrorHandler(err)

# Get All Tags and Tag groups from a device
device_path = '{}.{}'.format(ch_name, dev_name)
try:
    print("{} {} - {}".format("Read All Tags and Tag Groups from device", device_path, device.get_all_tags_tag_groups(server, device_path)))
except Exception as err:
    ErrorHandler(err)

# Get Tag
tag_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2.temp')
try:
    print("{} - {}".format("Read Tag Properties", tag.get_tag(server, tag_path)))
except Exception as err:
    ErrorHandler(err)

# Get Tag Group
tag_group_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2')
try:
    print("{} - {}".format("Read Tag Group Properties", tag.get_tag_group(server, tag_group_path)))
except Exception as err:
    ErrorHandler(err)

# Get All Tags and Tag groups from a path
tag_group_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM')
try:
    print("{} {} - {}".format("Read All Tags and Tag Groups from device", device_path, tag.get_full_tag_structure(server, tag_group_path, recursive=True)))
except Exception as err:
    ErrorHandler(err)

# Get Tags and Tag groups only at a particular path
tag_group_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM')
try:
    print("{} {} - {}".format("Read All Tags and Tag Groups from device", device_path, tag.get_full_tag_structure(server, tag_group_path)))
except Exception as err:
    ErrorHandler(err)

# Channel Modify - Modify the description of the Channel that was created. "Force" will force the 
# update to the Kepware Server, if "FORCE_UPDATE" not provided in the JSON data.
channel_data = {
}
channel_data['common.ALLTYPES_DESCRIPTION'] = 'This is the test channel created'
try:
    print("{} - {}".format("Modifying Channel 'Description' Property", channel.modify_channel(server, channel_data, channel=ch_name, force=True)))
except Exception as err:
    ErrorHandler(err)

# If Modify function calls do not provide "FORCE_UPDATE" and the "Force" input is "False" 
# the API will first read the "PROJECT_ID" then use the ID when executing the modification.
try:
    print("{} - {}".format("Modifying Channel 'Description' Property", channel.modify_channel(server, channel_data, channel=ch_name, force=True)))
except Exception as err:
    ErrorHandler(err)

#
# Examples of deleting various objects (channels, devices, tags, etc)
#

# Delete Tag
tag_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2.temp')
try:
    print("{} - {}".format("Delete Tag", tag.del_tag(server, tag_path)))
except Exception as err:
    ErrorHandler(err)

# Delete Tag Group
tag_group_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2')
try:
    print("{} - {}".format("Delete Tag Group", tag.del_tag_group(server, tag_group_path)))
except Exception as err:
    ErrorHandler(err)

# Delete Device
try:
    print("{} - {}".format("Delete Device", device.del_device(server, device_path)))
except Exception as err:
    ErrorHandler(err)

# Delete Channel
try:
    print("{} - {}".format("Delete Channel", channel.del_channel(server,ch_name)))
except Exception as err:
    ErrorHandler(err)