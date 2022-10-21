# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Admin Test - Test to exectute various calls for the Administrator 
# parts of the Kepware configuration API

from wsgiref.simple_server import server_version
from kepconfig.error import KepError, KepHTTPError
import os, sys
from typing import Dict, List
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kepconfig
from kepconfig import admin
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

default_lls_config = {
    "libadminsettings.LICENSING_SERVER_PORT": 7070,
    "libadminsettings.LICENSING_SERVER_NAME": "",
    "libadminsettings.LICENSING_CHECK_PERIOD_MINS": 5,
    "libadminsettings.LICENSING_SERVER_SSL_PORT": 1443,
    "libadminsettings.LICENSING_SERVER_ALLOW_INSECURE_COMMS": False,
    "libadminsettings.LICENSING_SERVER_ALLOW_SELF_SIGNED_CERTS": False,
    "libadminsettings.LICENSING_CLIENT_ALIAS": ""
}

def HTTPErrorHandler(err):
    if err.__class__ is KepHTTPError:
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
    endpoint_list = [uaendpoint1, uaendpoint2, uaendpoint3]
    usergroup_list = [group1, group2, group3]
    
    for ua in endpoint_list:
        try:
            admin.ua_server.del_endpoint(server,ua['common.ALLTYPES_NAME'])
        except Exception as err:
            pass
    
    
    for ug in usergroup_list:
        try: 
            admin.user_groups.del_user_group(server,ug['common.ALLTYPES_NAME'])
        except Exception as err:
            pass
    
    admin.lls.update_lls_config(server,admin.lls.lls_config(default_lls_config))
    

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
    
def test_uaserver(server):
    if server_type == 'TKS': pytest.skip("UA Endpoints not configurable in {}.".format(server_type))

    assert admin.ua_server.add_endpoint(server,uaendpoint1)
    
    assert admin.ua_server.del_endpoint(server,uaendpoint1['common.ALLTYPES_NAME'])
    
    assert admin.ua_server.add_endpoint(server,[uaendpoint1,uaendpoint2])


# Endpoint 2 fails since it already exists
    assert type(admin.ua_server.add_endpoint(server,[uaendpoint2,uaendpoint3])) == list

    assert admin.ua_server.modify_endpoint(server,{"libadminsettings.UACONFIGMANAGER_ENDPOINT_ENABLE": False},uaendpoint1['common.ALLTYPES_NAME'])
    
    # Bad Input test
    with pytest.raises(KepError):
        assert admin.ua_server.modify_endpoint(server,{"libadminsettings.UACONFIGMANAGER_ENDPOINT_ENABLE": False})

    assert admin.ua_server.modify_endpoint(server,{"common.ALLTYPES_NAME": "DefaultEndpoint3","libadminsettings.UACONFIGMANAGER_ENDPOINT_SECURITY_NONE": True})
    
    assert type(admin.ua_server.get_endpoint(server,uaendpoint1['common.ALLTYPES_NAME'])) ==  dict
    
    assert type(admin.ua_server.get_all_endpoints(server)) == list
    
    assert admin.ua_server.del_endpoint(server,uaendpoint1['common.ALLTYPES_NAME'])
    
    assert admin.ua_server.del_endpoint(server,uaendpoint2['common.ALLTYPES_NAME'])

def test_user_groups(server):
    # User Group tests
    assert admin.user_groups.add_user_group(server,group1)
    
    assert admin.user_groups.del_user_group(server,group1['common.ALLTYPES_NAME'])

    assert admin.user_groups.add_user_group(server,[group1, group2])

# Group 2 fails since it already exists
    assert type(admin.user_groups.add_user_group(server,[group2, group3])) == list
    
    assert admin.user_groups.modify_user_group(server,{"libadminsettings.USERMANAGER_GROUP_ENABLED": False},
            group1['common.ALLTYPES_NAME'])
    
    assert admin.user_groups.modify_user_group(server,{"libadminsettings.USERMANAGER_GROUP_ENABLED": True},
            group1['common.ALLTYPES_NAME'])

    # Bad Inputs
    with pytest.raises(KepError):
        assert admin.user_groups.modify_user_group(server,{"libadminsettings.USERMANAGER_GROUP_ENABLED": False})

    assert admin.user_groups.modify_user_group(server,{'common.ALLTYPES_NAME': 'Group1',"libadminsettings.USERMANAGER_GROUP_ENABLED": False})
    
    assert admin.user_groups.modify_user_group(server,{'common.ALLTYPES_NAME': 'Group1',"libadminsettings.USERMANAGER_GROUP_ENABLED": True})

    assert type(admin.user_groups.get_user_group(server,group1['common.ALLTYPES_NAME'])) == dict
    
    assert type(admin.user_groups.get_all_user_groups(server)) == list
    
    assert admin.user_groups.disable_user_group(server, group1['common.ALLTYPES_NAME'])

    assert admin.user_groups.enable_user_group(server, group1['common.ALLTYPES_NAME'])

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

    assert admin.users.add_user(server,user1)
    
    assert admin.users.del_user(server,user1['common.ALLTYPES_NAME'])

    assert admin.users.add_user(server,[user1, user2])
    
# User 2 fails since it already exists
    assert type(admin.users.add_user(server,[user2, user3])) == list
    
    assert admin.users.modify_user(server,{"libadminsettings.USERMANAGER_USER_ENABLED": False}, user1['common.ALLTYPES_NAME'])
    
    # Bad Inputs
    with pytest.raises(KepError):
        assert admin.users.modify_user(server,{'common.ALLTYPES_DESCRIPTION': 'TEST'})
    
    assert admin.users.modify_user(server,{"common.ALLTYPES_NAME": "Client2",'common.ALLTYPES_DESCRIPTION': 'TEST'})

    assert type(admin.users.get_user(server,user1['common.ALLTYPES_NAME'])) == dict
    
    assert type(admin.users.get_all_users(server)) == list
    
    assert admin.users.disable_user(server, user1['common.ALLTYPES_NAME'])

    assert admin.users.enable_user(server, user1['common.ALLTYPES_NAME'])

    assert admin.users.del_user(server, user1['common.ALLTYPES_NAME'])
    
    assert admin.users.del_user(server, user2['common.ALLTYPES_NAME'])

def test_LLS(server):

    assert type(admin.lls.get_lls_config(server)) == admin.lls.lls_config

    lls_config = {"libadminsettings.LICENSING_SERVER_PORT": 80,
    "libadminsettings.LICENSING_SERVER_NAME": "test_host",
    "libadminsettings.LICENSING_CHECK_PERIOD_MINS": 20,
    "libadminsettings.LICENSING_SERVER_SSL_PORT": 7777,
    "libadminsettings.LICENSING_SERVER_ALLOW_INSECURE_COMMS": True,
    "libadminsettings.LICENSING_SERVER_ALLOW_SELF_SIGNED_CERTS": True,
    "libadminsettings.LICENSING_CLIENT_ALIAS": "Dumb"}

    r = admin.lls.lls_config(lls_config)
    assert type(r) == admin.lls.lls_config

    assert admin.lls.update_lls_config(server, r)

    assert admin.lls.enable_lls(server)

    assert admin.lls.disable_lls(server)