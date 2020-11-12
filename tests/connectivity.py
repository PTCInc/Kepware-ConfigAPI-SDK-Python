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

def connectivity_test(server):
    # Add a Channel using the "Simulator Driver"
    try:
        channel_data = {"common.ALLTYPES_NAME": ch_name,"servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator"}
        print(kepconfig.connectivity.channel.add_channel(server,channel_data))
    except Exception as err:
        HTTPErrorHandler(err)
    
    # Add multi channels with one failure
    try:
        channel_data = [
            {"common.ALLTYPES_NAME": ch_name+"1","servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator"},
            {"common.ALLTYPES_NAME": "_" + ch_name,"servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator"}
        ]
        print(kepconfig.connectivity.channel.add_channel(server,channel_data))
    except Exception as err:
        HTTPErrorHandler(err)

    # Add a Device to the created Channel
    try:
        device_data = {"common.ALLTYPES_NAME": dev_name,"servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator"}
        print(kepconfig.connectivity.device.add_device(server,ch_name,device_data))
    except Exception as err:
        HTTPErrorHandler(err)
    
    # Add multi devices with one failure
    try:
        device_data = [
            {"common.ALLTYPES_NAME": dev_name,"servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator"},
            {"common.ALLTYPES_NAME": dev_name+"1","servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator"}
        ]
        print(kepconfig.connectivity.device.add_device(server,ch_name,device_data))
    except Exception as err:
        HTTPErrorHandler(err)

    # Add a collection of Tags and Tag Group objects
    all_tags_data = {
        "tags": [
            {
                "common.ALLTYPES_NAME": "Temp1",
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
        print(kepconfig.connectivity.tag.add_all_tags(server, ch_name + '.' + dev_name, all_tags_data))
    except Exception as err:
        HTTPErrorHandler(err)

    # Add a collection with bad tag
    all_tags_data = {
        "tags": [
            {
                "common.ALLTYPES_NAME": "_Temp1",
                "servermain.TAG_ADDRESS": "R0"
            },
            {
                "common.ALLTYPES_NAME": "Temp2",
                "servermain.TAG_ADDRESS": "R0"
            }
        ],
        "tag_groups": [
            {
                "common.ALLTYPES_NAME": "ALARM3",
                "tags": [
                    {
                        "common.ALLTYPES_NAME": "ALARM_C_READY",
                        "servermain.TAG_ADDRESS": "R1"
                    }
                ],
                "tag_groups": [
                    {
                        "common.ALLTYPES_NAME": "ALARM4",
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
        print(kepconfig.connectivity.tag.add_all_tags(server, ch_name + '.' + dev_name, all_tags_data))
    except Exception as err:
        HTTPErrorHandler(err)
    
    # Add a collection with bad tag_group child
    all_tags_data = {
        "tags": [
            {
                "common.ALLTYPES_NAME": "Temp3",
                "servermain.TAG_ADDRESS": "R0"
            }
        ],
        "tag_groups": [
            {
                "common.ALLTYPES_NAME": "ALARM5",
                "tags": [
                    {
                        "common.ALLTYPES_NAME": "_ALARM_C_READY",
                        "servermain.TAG_ADDRESS": "R1"
                    }
                ],
                "tag_groups": [
                    {
                        "common.ALLTYPES_NAME": "ALARM6",
                        "tags": [
                            {
                                "common.ALLTYPES_NAME": "ALARM_C_READY2",
                                "servermain.TAG_ADDRESS": "R2"
                            }
                        ]
                    }
                ]
            },
            {
                "common.ALLTYPES_NAME": "ALARM5"
            }
        ]
    }
    try:
        print(kepconfig.connectivity.tag.add_all_tags(server, ch_name + '.' + dev_name, all_tags_data))
    except Exception as err:
        HTTPErrorHandler(err)

    # Add a collection with bad tag and tag_group child
    all_tags_data = {
        "tags": [
            {
                "common.ALLTYPES_NAME": "_Temp4",
                "servermain.TAG_ADDRESS": "R0"
            },
            {
                "common.ALLTYPES_NAME": "Temp4",
                "servermain.TAG_ADDRESS": "R0"
            }
        ],
        "tag_groups": [
            {
                "common.ALLTYPES_NAME": "ALARM7",
                "tags": [
                    {
                        "common.ALLTYPES_NAME": "_ALARM_C_READY",
                        "servermain.TAG_ADDRESS": "R1"
                    }
                ],
                "tag_groups": [
                    {
                        "common.ALLTYPES_NAME": "ALARM6",
                        "tags": [
                            {
                                "common.ALLTYPES_NAME": "ALARM_C_READY2",
                                "servermain.TAG_ADDRESS": "R2"
                            }
                        ]
                    }
                ]
            },
            {
                "common.ALLTYPES_NAME": "ALARM8"
            }

        ]
    }
    try:
        print(kepconfig.connectivity.tag.add_all_tags(server, ch_name + '.' + dev_name, all_tags_data))
    except Exception as err:
        HTTPErrorHandler(err)

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
        print(kepconfig.connectivity.tag.add_tag(server, tag_path, tag_info))
    except Exception as err:
        HTTPErrorHandler(err)

    # Add tag to at device level (test for no "tag path")
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
    tag_path = '{}.{}'.format(ch_name, dev_name)
    try:
        print(kepconfig.connectivity.tag.add_tag(server, tag_path, tag_info))
    except Exception as err:
        HTTPErrorHandler(err)

    # Add tag group to an existing tag group
    tag_group_info = [
        {
                "common.ALLTYPES_NAME": "NewGroup"
        }
    ]
    tag_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM')
    try: 
        print(kepconfig.connectivity.tag.add_tag_group(server, tag_path, tag_group_info))
    except Exception as err:
        HTTPErrorHandler(err)
    # Add tag group to at device level (test for no "tag path")
    tag_group_info = [
        {
                "common.ALLTYPES_NAME": "Group1"
        },
        {
                "common.ALLTYPES_NAME": "Group2"
        }
    ]
    tag_path = '{}.{}'.format(ch_name, dev_name)
    try:
        print(kepconfig.connectivity.tag.add_tag_group(server, tag_path, tag_group_info))
    except Exception as err:
        HTTPErrorHandler(err)

    #
    # Examples of reading properties for various objects (channels, devices, tags, etc)
    #

    # Get Channel
    try:
        print(kepconfig.connectivity.channel.get_channel(server,ch_name))
    except Exception as err:
        HTTPErrorHandler(err)

    # Get all Channels
    try:
        print(kepconfig.connectivity.channel.get_all_channels(server))
    except Exception as err:
        HTTPErrorHandler(err)

    # Get Device
    device_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2.temp')
    try:
        print(kepconfig.connectivity.device.get_device(server, device_path))
    except Exception as err:
        HTTPErrorHandler(err)

    # Get all Devices
    try:
        print(kepconfig.connectivity.device.get_all_devices(server, ch_name))
    except Exception as err:
        HTTPErrorHandler(err)

    # Get Tag
    tag_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2.temp')
    try:
        print(kepconfig.connectivity.tag.get_tag(server, tag_path))
    except Exception as err:
        HTTPErrorHandler(err)

    # Get All Tags
    tag_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2')
    try:
        print(kepconfig.connectivity.tag.get_all_tags(server, tag_path))
    except Exception as err:
        HTTPErrorHandler(err)

    # Get Tag Group
    tag_group_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2')
    try:
        print(kepconfig.connectivity.tag.get_tag_group(server, tag_group_path))
    except Exception as err:
        HTTPErrorHandler(err)

    # Get All Tag Groups
    tag_group_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM')
    try:
        print(kepconfig.connectivity.tag.get_all_tag_groups(server,tag_group_path))
    except Exception as err:
        HTTPErrorHandler(err)

    #
    # TEST for GETs at Device level (no tag_path)
    #

    # Get Tag
    tag_path = '{}.{}.{}'.format(ch_name, dev_name, 'temp')
    try: 
        print(kepconfig.connectivity.tag.get_tag(server, tag_path))
    except Exception as err:
        HTTPErrorHandler(err)

    # Get All Tags
    tag_path = '{}.{}'.format(ch_name, dev_name)
    try:
        print(kepconfig.connectivity.tag.get_all_tags(server, tag_path))
    except Exception as err:
        HTTPErrorHandler(err)

    # Get Tag Group
    tag_group_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM')
    try:
        print(kepconfig.connectivity.tag.get_tag_group(server, tag_group_path))
    except Exception as err:
        HTTPErrorHandler(err)

    # Get All Tag Groups
    tag_group_path = '{}.{}'.format(ch_name, dev_name)
    try:
        print(kepconfig.connectivity.tag.get_all_tag_groups(server,tag_group_path))
    except Exception as err:
        HTTPErrorHandler(err)

    # Channel Modify - Modify the description of the Channel that was created. "Force" will force the 
    # update to the Kepware Server, if not provided in the JSON data.
    channel_data = {
    }
    channel_data['common.ALLTYPES_DESCRIPTION'] = 'This is the test channel created'
    try:
        print (kepconfig.connectivity.channel.modify_channel(server, channel_data, channel=ch_name, force=True))
    except Exception as err:
        HTTPErrorHandler(err)
    
     #
    # Examples of deleting various objects (channels, devices, tags, etc)
    #

    # Delete Tag
    tag_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2.temp')
    try:
        print(kepconfig.connectivity.tag.del_tag(server, tag_path))
    except Exception as err:
        HTTPErrorHandler(err)
        
    # Delete Tag Group
    tag_group_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2')
    try:
        print(kepconfig.connectivity.tag.del_tag_group(server, tag_group_path))
    except Exception as err:
        HTTPErrorHandler(err)

    # Delete Device
    # device_path = '{}.{}'.format(ch_name, dev_name)
    try:
        print(kepconfig.connectivity.device.del_device(server, device_path))
    except Exception as err:
        HTTPErrorHandler(err)

    # Delete Channel
    try:
        print(kepconfig.connectivity.channel.del_channel(server,ch_name))
    except Exception as err:
        HTTPErrorHandler(err)
    
    # Delete all Channels
    try:
        ch_left = kepconfig.connectivity.channel.get_all_channels(server)
        for x in ch_left:
            print(kepconfig.connectivity.channel.del_channel(server,x['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)

if __name__ == "__main__":
    time_start = time.perf_counter()

    # This creates a server reference that is used to target all modifications of 
    # the Kepware configuration
    server = kepconfig.connection.server(host = 'localhost', port = 57412, user = 'Administrator', pw = '', https = False)

    connectivity_test(server)

    time_end = time.perf_counter()
    print('Complete {}! {} - Took {} seconds'.format(os.path.basename(__file__),time.asctime(), time_end - time_start))