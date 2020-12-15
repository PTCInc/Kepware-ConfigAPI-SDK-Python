# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Test Example - Test to exectute various calls for the conenctivity 
# parts of the Kepware configuration API

import os, sys
import pytest
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

group1 = {'common.ALLTYPES_NAME': 'Operators'}
group2 = {'common.ALLTYPES_NAME': 'Group1'}
group3 = {'common.ALLTYPES_NAME': 'Group2'}

def HTTPErrorHandler(err):
    if err.__class__ is kepconfig.error.KepHTTPError:
        print(err.code)
        print(err.msg)
        print(err.url)
        print(err.hdrs)
        print(err.payload)
    else:
        print('Different Exception Received: {}'.format(err))

def initialize(server):
    pass

def complete(server):
    try: 
        print(kepconfig.admin.user_groups.del_user_group(server,group1['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)

    try: 
        print(kepconfig.admin.user_groups.del_user_group(server,group2['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)

    try: 
        print(kepconfig.admin.user_groups.del_user_group(server,group3['common.ALLTYPES_NAME']))
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
    

def test_uaserver(server):
    uaendpoint1 = {
        "common.ALLTYPES_NAME": "DefaultEndpoint2",
        "libadminsettings.UACONFIGMANAGER_ENDPOINT_PORT": 49331
    }
    uaendpoint2 = {
        "common.ALLTYPES_NAME": "DefaultEndpoint3",
        "libadminsettings.UACONFIGMANAGER_ENDPOINT_PORT": 49332
    }
    uaendpoint3 = {
        "common.ALLTYPES_NAME": "DefaultEndpoint4",
        "libadminsettings.UACONFIGMANAGER_ENDPOINT_PORT": 49333
    }

    try: 
        print(kepconfig.admin.ua_server.add_endpoint(server,uaendpoint1))
    except Exception as err:
        HTTPErrorHandler(err)
    
    try: 
        print(kepconfig.admin.ua_server.del_endpoint(server,uaendpoint1['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)
    
    try: 
        print(kepconfig.admin.ua_server.add_endpoint(server,[uaendpoint1,uaendpoint2]))
    except Exception as err:
        HTTPErrorHandler(err)

# Endpoint 2 fails since it already exists
    try: 
        print(kepconfig.admin.ua_server.add_endpoint(server,[uaendpoint2,uaendpoint3]))
    except Exception as err:
        HTTPErrorHandler(err)

    try: 
        print(kepconfig.admin.ua_server.modify_endpoint(server,{"libadminsettings.UACONFIGMANAGER_ENDPOINT_ENABLE": False},uaendpoint1['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)
    
    # Bad Input test
    try: 
        print(kepconfig.admin.ua_server.modify_endpoint(server,{"libadminsettings.UACONFIGMANAGER_ENDPOINT_ENABLE": False}))
    except Exception as err:
        HTTPErrorHandler(err)

    try: 
        print(kepconfig.admin.ua_server.modify_endpoint(server,{"common.ALLTYPES_NAME": "DefaultEndpoint3","libadminsettings.UACONFIGMANAGER_ENDPOINT_SECURITY_NONE": True}))
    except Exception as err:
        HTTPErrorHandler(err)
    
    try: 
        print(kepconfig.admin.ua_server.get_endpoint(server,uaendpoint1['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)
    
    try: 
        print(kepconfig.admin.ua_server.get_all_endpoints(server))
    except Exception as err:
        HTTPErrorHandler(err)
    
    try: 
        print(kepconfig.admin.ua_server.del_endpoint(server,uaendpoint1['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)
    
    try: 
        print(kepconfig.admin.ua_server.del_endpoint(server,uaendpoint2['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)

def test_user_groups(server):
    # User Group tests
    assert kepconfig.admin.user_groups.add_user_group(server,group1)
    
    assert kepconfig.admin.user_groups.del_user_group(server,group1['common.ALLTYPES_NAME'])

    assert kepconfig.admin.user_groups.add_user_group(server,[group1, group2])

# Group 2 fails since it already exists
    assert type(kepconfig.admin.user_groups.add_user_group(server,[group2, group3])) == list
    
    assert kepconfig.admin.user_groups.modify_user_group(server,{"libadminsettings.USERMANAGER_GROUP_ENABLED": False},
            group1['common.ALLTYPES_NAME'])
    
    assert kepconfig.admin.user_groups.modify_user_group(server,{"libadminsettings.USERMANAGER_GROUP_ENABLED": True},
            group1['common.ALLTYPES_NAME'])

    # Bad Inputs
    assert kepconfig.admin.user_groups.modify_user_group(server,{"libadminsettings.USERMANAGER_GROUP_ENABLED": False}) == False

    assert kepconfig.admin.user_groups.modify_user_group(server,{'common.ALLTYPES_NAME': 'Group1',"libadminsettings.USERMANAGER_GROUP_ENABLED": False})
    
    assert kepconfig.admin.user_groups.modify_user_group(server,{'common.ALLTYPES_NAME': 'Group1',"libadminsettings.USERMANAGER_GROUP_ENABLED": True})

    assert type(kepconfig.admin.user_groups.get_user_group(server,group1['common.ALLTYPES_NAME'])) == dict
    
    assert type(kepconfig.admin.user_groups.get_all_user_groups(server)) == list
    
    assert kepconfig.admin.user_groups.disable_user_group(server, group1['common.ALLTYPES_NAME'])

    assert kepconfig.admin.user_groups.enable_user_group(server, group1['common.ALLTYPES_NAME'])

def test_users(server):
    # User tests
    user1 = {
        "common.ALLTYPES_NAME": "Client1",
        "common.ALLTYPES_DESCRIPTION": "Built-in account representing data clients",
        "libadminsettings.USERMANAGER_USER_GROUPNAME": "Operators",
        "libadminsettings.USERMANAGER_USER_ENABLED": True,
        "libadminsettings.USERMANAGER_USER_PASSWORD": "Kepware400400400"
    }
    user2 = {
        "common.ALLTYPES_NAME": "Client2",
        "common.ALLTYPES_DESCRIPTION": "Built-in account representing data clients",
        "libadminsettings.USERMANAGER_USER_GROUPNAME": "Group1",
        "libadminsettings.USERMANAGER_USER_ENABLED": True,
        "libadminsettings.USERMANAGER_USER_PASSWORD": "Kepware400400400"      
    }
    user3 = {
        "common.ALLTYPES_NAME": "Client3",
        "common.ALLTYPES_DESCRIPTION": "Built-in account representing data clients",
        "libadminsettings.USERMANAGER_USER_GROUPNAME": "Group1",
        "libadminsettings.USERMANAGER_USER_ENABLED": True,
        "libadminsettings.USERMANAGER_USER_PASSWORD": "Kepware400400400"      
    }

    assert kepconfig.admin.users.add_user(server,user1)
    
    assert kepconfig.admin.users.del_user(server,user1['common.ALLTYPES_NAME'])

    assert kepconfig.admin.users.add_user(server,[user1, user2])
    
# User 2 fails since it already exists
    assert type(kepconfig.admin.users.add_user(server,[user2, user3])) == list
    
    assert kepconfig.admin.users.modify_user(server,{"libadminsettings.USERMANAGER_USER_ENABLED": False}, user1['common.ALLTYPES_NAME'])
    
    # Bad Inputs
    assert kepconfig.admin.users.modify_user(server,{'common.ALLTYPES_DESCRIPTION': 'TEST'}) == False
    
    assert kepconfig.admin.users.modify_user(server,{"common.ALLTYPES_NAME": "Client2",'common.ALLTYPES_DESCRIPTION': 'TEST'})

    assert type(kepconfig.admin.users.get_user(server,user1['common.ALLTYPES_NAME'])) == dict
    
    assert type(kepconfig.admin.users.get_all_users(server)) == list
    
    assert kepconfig.admin.users.disable_user(server, user1['common.ALLTYPES_NAME'])

    assert kepconfig.admin.users.enable_user(server, user1['common.ALLTYPES_NAME'])

    assert kepconfig.admin.users.del_user(server, user1['common.ALLTYPES_NAME'])
    
    assert kepconfig.admin.users.del_user(server, user2['common.ALLTYPES_NAME'])
