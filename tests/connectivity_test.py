# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Connectivity Test - Test to exectute various calls for the basic driver/connectivity 
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
import pytest


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

def remove_projectid(DATA):
    if type(DATA) is dict:
        DATA.pop('PROJECT_ID', None)
    elif type(DATA) is list:
        for item in DATA:
            item = remove_projectid(item)
    return DATA

def initialize(server):
    pass

def complete(server):
    # Delete all Channels
    try:
        ch_left = kepconfig.connectivity.channel.get_all_channels(server)
        for x in ch_left:
            print(kepconfig.connectivity.channel.del_channel(server,x['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)

@pytest.fixture(scope="module")
def server(kepware_server: list[kepconfig.connection.server, str]):
    server = kepware_server[0]
    global server_type
    server_type = kepware_server[1]
    
    # Initialize any configuration before testing in module
    initialize(server)

    # Everything below yield is run after module tests are completed
    yield server
    complete(server)

# def connectivity_test(server):
def test_channel_add(server):
    # Add a Channel using the "Simulator Driver"
    channel_data = {"common.ALLTYPES_NAME": ch_name,"servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator"}
    assert kepconfig.connectivity.channel.add_channel(server,channel_data)
    
    # Add multi channels with one failure
    channel_data = [
        {"common.ALLTYPES_NAME": ch_name+"1","servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator"},
        {"common.ALLTYPES_NAME": "_" + ch_name,"servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator"}
    ]
    assert type(kepconfig.connectivity.channel.add_channel(server,channel_data)) == list

def test_device_add(server):
    # Add a Device to the created Channel
    device_data = {"common.ALLTYPES_NAME": dev_name,"servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator"}
    assert kepconfig.connectivity.device.add_device(server,ch_name,device_data)
    
    # Add multi devices with one failure
    device_data = [
        {"common.ALLTYPES_NAME": dev_name,"servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator"},
        {"common.ALLTYPES_NAME": dev_name+"1","servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator"}
    ]
    assert type(kepconfig.connectivity.device.add_device(server,ch_name,device_data)) == list

def test_all_tag_tg_add(server):
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
    assert kepconfig.connectivity.tag.add_all_tags(server, ch_name + '.' + dev_name, all_tags_data)

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
    assert type(kepconfig.connectivity.tag.add_all_tags(server, ch_name + '.' + dev_name, all_tags_data)) == list
    
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
    assert type(kepconfig.connectivity.tag.add_all_tags(server, ch_name + '.' + dev_name, all_tags_data)) == list

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
    assert type(kepconfig.connectivity.tag.add_all_tags(server, ch_name + '.' + dev_name, all_tags_data)) == list

def test_tag_add(server):
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
    assert kepconfig.connectivity.tag.add_tag(server, tag_path, tag_info)


    # Add tag to at device level (test for no "tag path")
    tag_info = [
        {
                "common.ALLTYPES_NAME": "Temp",
                "servermain.TAG_ADDRESS": "R0"
        },
        {
                "common.ALLTYPES_NAME": "Temp_",
                "servermain.TAG_ADDRESS": "R1"
        }
    ]
    tag_path = '{}.{}'.format(ch_name, dev_name)
    assert kepconfig.connectivity.tag.add_tag(server, tag_path, tag_info)

def test_tag_group_add(server):
    # Add tag group to an existing tag group
    tag_group_info = [
        {
                "common.ALLTYPES_NAME": "NewGroup"
        }
    ]
    tag_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM')
    assert kepconfig.connectivity.tag.add_tag_group(server, tag_path, tag_group_info)

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
    assert kepconfig.connectivity.tag.add_tag_group(server, tag_path, tag_group_info)

    #
    # Examples of reading properties for various objects (channels, devices, tags, etc)
    #
def test_channel_get(server):
    # Get Channel
    assert type(kepconfig.connectivity.channel.get_channel(server,ch_name)) == dict

    # Get all Channels
    assert type(kepconfig.connectivity.channel.get_all_channels(server)) == list

def test_channel_struct_get(server):
    assert type(kepconfig.connectivity.channel.get_channel_structure(server,ch_name)) == dict

def test_device_get(server):
    # Get Device
    device_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2.temp')
    assert type(kepconfig.connectivity.device.get_device(server, device_path)) == dict


    # Get all Devices
    assert type(kepconfig.connectivity.device.get_all_devices(server, ch_name)) == list

def test_device_tag_struct_only_get(server):
    # Get ProjectID
    # props = server.get_project_properties()
    # proj_id = props['PROJECT_ID']
    dev_path = '{}.{}'.format(ch_name, dev_name)
    assert type(kepconfig.connectivity.device.get_all_tags_tag_groups(server, dev_path)) == dict

def test_device_tag_all_get(server):
    # Get ProjectID
    # props = server.get_project_properties()
    # proj_id = props['PROJECT_ID']
    dev_path = '{}.{}'.format(ch_name, dev_name)
    assert type(kepconfig.connectivity.device.get_device_structure(server, dev_path)) == dict

def test_tag_get(server):
    # Get Tag
    tag_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2.temp')
    assert type(kepconfig.connectivity.tag.get_tag(server, tag_path)) == dict

    # Get All Tags
    tag_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2')
    assert type(kepconfig.connectivity.tag.get_all_tags(server, tag_path)) == list
    
    #
    # TEST for GETs at Device level (no tag_path)
    #
    # Get Tag
    tag_path = '{}.{}.{}'.format(ch_name, dev_name, 'temp')
    assert type(kepconfig.connectivity.tag.get_tag(server, tag_path)) == dict

    # Get All Tags
    tag_path = '{}.{}'.format(ch_name, dev_name)
    assert type(kepconfig.connectivity.tag.get_all_tags(server, tag_path)) == list

def test_tag_group_get(server):
    # Get Tag Group
    tag_group_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2')
    assert type(kepconfig.connectivity.tag.get_tag_group(server, tag_group_path)) == dict


    # Get All Tag Groups
    tag_group_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM')
    assert type(kepconfig.connectivity.tag.get_all_tag_groups(server,tag_group_path)) == list

    #
    # TEST for GETs at Device level (no tag_path)
    #

    # Get Tag Group
    tag_group_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM')
    assert type(kepconfig.connectivity.tag.get_tag_group(server, tag_group_path)) == dict

    # Get All Tag Groups
    tag_group_path = '{}.{}'.format(ch_name, dev_name)
    assert type(kepconfig.connectivity.tag.get_all_tag_groups(server,tag_group_path)) == list

def test_tag_struct_get(server):
    # Get ProjectID
    # props = server.get_project_properties()
    # proj_id = props['PROJECT_ID']
    tag_path = '{}.{}'.format(ch_name, dev_name)
    assert type(kepconfig.connectivity.tag.get_full_tag_structure(server, tag_path, recursive=True)) == dict
    tag_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2')
    assert type(kepconfig.connectivity.tag.get_full_tag_structure(server, tag_path)) == dict


def test_channel_modify(server):
    # Channel Modify - Modify the description of the Channel that was created. "Force" will force the 
    # update to the Kepware Server, if not provided in the JSON data.
    channel_data = {
    }
    channel_data['common.ALLTYPES_DESCRIPTION'] = 'This is the test channel created'
    assert kepconfig.connectivity.channel.modify_channel(server, channel_data, channel=ch_name, force=True)

def test_auto_tag_gen(server):
    # Add a Channel and Device using the "Controllogix Driver"
    channel_data = {
        "common.ALLTYPES_NAME": "Logix",
        "servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Allen-Bradley Controllogix Ethernet",
        "devices": [
            {
                "common.ALLTYPES_NAME": "Logix",
                "servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Allen-Bradley Controllogix Ethernet",
                "servermain.DEVICE_MODEL": 0,
                "servermain.DEVICE_ID_STRING": "<127.0.0.1>,1,0"
            }
        ]
    }
    assert kepconfig.connectivity.channel.add_channel(server,channel_data)
    job = kepconfig.connectivity.device.auto_tag_gen(server,"Logix.Logix")
    assert type(job) == kepconfig.connection.KepServiceResponse
    job = kepconfig.connectivity.device.auto_tag_gen(server,"Logix.Logix", 60)
    assert type(job) == kepconfig.connection.KepServiceResponse

def test_tag_del(server):
    # Delete Tag
    tag_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2.temp')
    assert kepconfig.connectivity.tag.del_tag(server, tag_path)

def test_tag_group_del(server):       
    # Delete Tag Group
    tag_group_path = '{}.{}.{}'.format(ch_name, dev_name, 'ALARM.ALARM2')
    assert kepconfig.connectivity.tag.del_tag_group(server, tag_group_path)

def test_device_del(server):
    # Delete Device
    device_path = '{}.{}'.format(ch_name, dev_name)
    assert kepconfig.connectivity.device.del_device(server, device_path)

def test_channel_del(server):
    # Delete Channel
    assert kepconfig.connectivity.channel.del_channel(server,ch_name)
