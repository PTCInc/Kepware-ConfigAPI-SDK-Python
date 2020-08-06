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

def uaserver_test(server):
    uaendpoint1 = {
        "common.ALLTYPES_NAME": "DefaultEndpoint2",
        "libadminsettings.UACONFIGMANAGER_ENDPOINT_PORT": 49331
    }
    uaendpoint2 = {
        "common.ALLTYPES_NAME": "DefaultEndpoint3",
        "libadminsettings.UACONFIGMANAGER_ENDPOINT_PORT": 49332
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

def user_manager_test(server):
    # User Group tests
    group1 = {'common.ALLTYPES_NAME': 'Operators'}
    group2 = {'common.ALLTYPES_NAME': 'DipShits'}
    
    try: 
        print(kepconfig.admin.user_groups.add_user_group(server,group1))
    except Exception as err:
        HTTPErrorHandler(err)
    try: 
        print(kepconfig.admin.user_groups.del_user_group(server,group1['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)

    try: 
        print(kepconfig.admin.user_groups.add_user_group(server,[group1, group2]))
    except Exception as err:
        HTTPErrorHandler(err)
    
    try: 
        print(kepconfig.admin.user_groups.modify_user_group(server,{"libadminsettings.USERMANAGER_GROUP_ENABLED": False},
            group1['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)

    # Bad Inputs
    try: 
        print(kepconfig.admin.user_groups.modify_user_group(server,{"libadminsettings.USERMANAGER_GROUP_ENABLED": False}))
    except Exception as err:
        HTTPErrorHandler(err)

    try: 
        print(kepconfig.admin.user_groups.modify_user_group(server,{'common.ALLTYPES_NAME': 'DipShits',"libadminsettings.USERMANAGER_GROUP_ENABLED": False}))
    except Exception as err:
        HTTPErrorHandler(err)

    try: 
        print(kepconfig.admin.user_groups.get_user_group(server,group1['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)
    
    try: 
        print(kepconfig.admin.user_groups.get_all_user_groups(server))
    except Exception as err:
        HTTPErrorHandler(err)

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
        "libadminsettings.USERMANAGER_USER_GROUPNAME": "DipShits",
        "libadminsettings.USERMANAGER_USER_ENABLED": True,
        "libadminsettings.USERMANAGER_USER_PASSWORD": "Kepware400400400"      
    }

    try: 
        print(kepconfig.admin.users.add_user(server,user1))
    except Exception as err:
        HTTPErrorHandler(err)
    
    try:
        print(kepconfig.admin.users.del_user(server,user1['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)

    try: 
        print(kepconfig.admin.users.add_user(server,[user1, user2]))
    except Exception as err:
        HTTPErrorHandler(err)
    
    try: 
        print(kepconfig.admin.users.modify_user(server,{"libadminsettings.USERMANAGER_USER_ENABLED": False}, user1['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)
    
    # Bad Inputs
    try: 
        print(kepconfig.admin.users.modify_user(server,{'common.ALLTYPES_DESCRIPTION': 'TEST'}))
    except Exception as err:
        HTTPErrorHandler(err)
    
    try: 
        print(kepconfig.admin.users.modify_user(server,{"common.ALLTYPES_NAME": "Client2",'common.ALLTYPES_DESCRIPTION': 'TEST'}))
    except Exception as err:
        HTTPErrorHandler(err)

    try: 
        print(kepconfig.admin.users.get_user(server,user1['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)
    
    try: 
        print(kepconfig.admin.users.get_all_users(server))
    except Exception as err:
        HTTPErrorHandler(err)
    
    try: 
        print(kepconfig.admin.users.del_user(server, user1['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)
    
    try: 
        print(kepconfig.admin.users.del_user(server, user2['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)

    # Delete User Groups
    try: 
        print(kepconfig.admin.user_groups.del_user_group(server,group1['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)
    
    try: 
        print(kepconfig.admin.user_groups.del_user_group(server,group2['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)






if __name__ == "__main__":
    time_start = time.perf_counter()

    # This creates a server reference that is used to target all modifications of 
    # the Kepware configuration
    server = kepconfig.connection.server(host = '192.168.192.136', port = 57513, user = 'Administrator', pw = 'Kepware400400400', https = True)
    server.SSL_ignore_hostname = True
    server.SSL_trust_all_certs = True
    
    user_manager_test(server)
    uaserver_test(server)

    time_end = time.perf_counter()
    print('Complete {}! {} - Took {} seconds'.format(os.path.basename(__file__),time.asctime(), time_end - time_start))