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

def test_connection_params(kepware_server):

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

def test_project_props(kepware_server):
    # Get Project Properties
    assert type(kepware_server.get_project_properties()) == dict

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
