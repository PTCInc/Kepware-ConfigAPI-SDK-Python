# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Simple Connectivity Example - Simple example on how to manage a connection and 
# exectute various calls for the conenctivity components of the Kepware
# configuration API



from kepconfig import connection
from kepconfig.connectivity import channel, device, tag
import json
import time

# Channel and Device name to be used
ch_name = 'Channel1'
dev_name = 'Device1'

# This creates a server reference that is used to target all modifications of 
# the Kepware configuration
server = connection.server(host = '127.0.0.1', port = 57412, user = 'Administrator', pw = '')


# Add a Channel using the "Simulator Driver"
channel_data = {
    "common.ALLTYPES_NAME": ch_name,
    "servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator"
    }
print("{} - {}".format("Adding Channel", channel.add_channel(server,channel_data)))

# Add a Device to the created Channel
device_data = {
    "common.ALLTYPES_NAME": dev_name,
    "servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator"
    }
print("{} - {}".format("Adding Device", device.add_device(server,ch_name,device_data)))

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
print("{} - {}".format("Adding Tags and Tag Groups", tag.add_all_tags(server, ch_name + '.' + dev_name, all_tags_data)))

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
print("{} - {}".format("Adding Tags to Existing Tag Group", tag.add_tag(server, tag_path, tag_info)))

#
# Examples of reading properties for various objects (channels, devices, tags, etc)
#

# Get Channel
print("{} - {}".format("Read Channel Properties", channel.get_channel(server,ch_name)))

# Get Device
device_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2.temp')
print("{} - {}".format("Read Device Properties", device.get_device(server, device_path)))

# Get Tag
tag_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2.temp')
print("{} - {}".format("Read Tag Properties", tag.get_tag(server, tag_path)))

# Get Tag Group
tag_group_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2')
print("{} - {}".format("Read Tag Group Properties", tag.get_tag_group(server, tag_group_path)))


# Channel Modify - Modify the description of the Channel that was created. "Force" will force the 
# update to the Kepware Server, if "FORCE_UPDATE" not provided in the JSON data.
channel_data = {
}
channel_data['common.ALLTYPES_DESCRIPTION'] = 'This is the test channel created'
print("{} - {}".format("Modifying Channel 'Description' Property", channel.modify_channel(server, channel_data, channel=ch_name, force=True)))

# If Modify function calls do not provide "FORCE_UPDATE" and the "Force" input is "False" 
# the API will first read the "PROJECT_ID" then use the ID when executing the modification.
print("{} - {}".format("Modifying Channel 'Description' Property", channel.modify_channel(server, channel_data, channel=ch_name, force=True)))


#
# Examples of deleting various objects (channels, devices, tags, etc)
#

# Delete Tag
tag_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2.temp')
print("{} - {}".format("Delete Tag", tag.del_tag(server, tag_path)))

# Delete Tag Group
tag_group_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2')
print("{} - {}".format("Delete Tag Group", tag.del_tag_group(server, tag_group_path)))

# Delete Device
print("{} - {}".format("Delete Device", device.del_device(server, device_path)))

# Delete Channel
print("{} - {}".format("Delete Channel", channel.del_channel(server,ch_name)))