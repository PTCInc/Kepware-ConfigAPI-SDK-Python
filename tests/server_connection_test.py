# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Master Test - Test to exectute various test modules to exersice the 
# parts of the Kepware configuration API

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kepconfig
import time
import datetime
import pytest
# import connectivity, admin, iot_gateway, datalogger


# Channel and Device name to be used
ch_name = 'Channel1'
dev_name = 'Device1'
mqtt_agent_name = 'MQTT'
rest_agent_name = 'REST Client'
rserver_agent_name = 'REST Server'
twx_agent_name = 'Thingworx'
iot_item_name ="System__Date"

# This creates a server reference that is used to target all modifications of 
# the Kepware configuration
server = kepconfig.connection.server(host = 'localhost', port = 57412, user = 'Administrator', pw = '', https = False)
tke_server = kepconfig.connection.server(host = '192.168.192.136', port = 57513, user = 'Administrator', pw = 'Kepware400400400', https = True)

def test_connection_params(kepware_server):

    tke_server.SSL_trust_all_certs = True
    assert tke_server.SSL_trust_all_certs == True
    tke_server.SSL_ignore_hostname = True
    assert tke_server.SSL_ignore_hostname == True

    kepware_server.SSL_trust_all_certs = True
    assert kepware_server.SSL_trust_all_certs == True
    kepware_server.SSL_ignore_hostname = True
    assert kepware_server.SSL_ignore_hostname == True

    kepware_server.SSL_trust_all_certs = False
    assert kepware_server.SSL_trust_all_certs == False
    kepware_server.SSL_ignore_hostname = False
    assert kepware_server.SSL_ignore_hostname == False

def test_reinitialize(kepware_server):
    job = kepware_server.reinitialize()
    assert type(job) == kepconfig.connection.KepServiceResponse

def test_modify_project_props(kepware_server):
    # Modify Project Properties
    project_prop = {
        "uaserverinterface.PROJECT_OPC_UA_ENABLE": False,
        "opcdaserver.PROJECT_OPC_DA_1_ENABLED": False,
        "opcdaserver.PROJECT_OPC_DA_2_ENABLED": False,
        "opcdaserver.PROJECT_OPC_DA_3_ENABLED": False
    }
    assert kepware_server.modify_project_properties(project_prop, force = True)

    project_prop = {
        "uaserverinterface.PROJECT_OPC_UA_ENABLE": True,
        "opcdaserver.PROJECT_OPC_DA_1_ENABLED": True,
        "opcdaserver.PROJECT_OPC_DA_2_ENABLED": True,
        "opcdaserver.PROJECT_OPC_DA_3_ENABLED": True
    }
    assert kepware_server.modify_project_properties(project_prop, force = True)

def test_event_log(kepware_server):
    assert type(kepware_server.get_event_log(25, None, None)) == list
    
    assert type(kepware_server.get_event_log(25, datetime.datetime.fromisoformat('2019-11-03T23:35:23.000'), datetime.datetime.now())) == list

# if __name__ == "__main__":
#     # Reinitialize TKE instance
#     try:
#         job = server.reinitialize()
#         print(job)
#     except Exception as err:
#         # HTTPErrorHandler(err)
#         assert False

#     # Modify Project Properties
#     project_prop = {
#         "uaserverinterface.PROJECT_OPC_UA_ENABLE": False,
#         "opcdaserver.PROJECT_OPC_DA_1_ENABLED": False,
#         "opcdaserver.PROJECT_OPC_DA_2_ENABLED": False,
#         "opcdaserver.PROJECT_OPC_DA_3_ENABLED": False
#     }
#     try:
#         print(server.modify_project_properties(project_prop, force = True))
#     except Exception as err:
#         HTTPErrorHandler(err)

#     project_prop = {
#         "uaserverinterface.PROJECT_OPC_UA_ENABLE": True,
#         "opcdaserver.PROJECT_OPC_DA_1_ENABLED": True,
#         "opcdaserver.PROJECT_OPC_DA_2_ENABLED": True,
#         "opcdaserver.PROJECT_OPC_DA_3_ENABLED": True
#     }
#     try:
#         print(server.modify_project_properties(project_prop, force = True))
#     except Exception as err:
#         HTTPErrorHandler(err)

#     #ATG when it is a device that supports it
#     # try:
#     #     # print(kepconfig.connectivity.device.auto_tag_gen(server, 'Channel3.Device1'))
#     #     job = kepconfig.connectivity.device.auto_tag_gen(server, 'Channel1.Device1')
#     #     print(job)
#     # except Exception as err:
#     #     HTTPErrorHandler(err)

#     # Get Event Log
#     try:
#         print(server.get_event_log(25, None, None))
#     except Exception as err:
#         HTTPErrorHandler(err)
#     try:
#         print(server.get_event_log(25, datetime.datetime.fromisoformat('2019-11-03T23:35:23.000'), datetime.datetime.now()))
#     except Exception as err:
#         HTTPErrorHandler(err)


#     # # Execute Module Tests
#     # admin.user_manager_test(server)
   
#     # # runs on TKE since UA Endpoint management isn't available in TKS
#     # admin.uaserver_test(tke_server)
    
#     # connectivity.connectivity_test(server)
#     # iot_gateway.iot_gateway_test(server)
#     # datalogger.datalogger_test(server)


#     time_end = time.perf_counter()
#     print('Complete {}! {} - Took {} seconds'.format(os.path.basename(__file__),time.asctime(), time_end - time_start))