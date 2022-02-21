# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Basic Server Connection Test - Test to exectute various server class functions 
# that exersice parts of the Kepware configuration API

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

def initialize(server):
    pass

def complete(server):
    pass

@pytest.fixture(scope="module")
def server(kepware_server):
    server = kepware_server
    
    # Initialize any configuration before testing in module
    initialize(server)

    # Everything below yield is run after module tests are completed
    yield server
    complete(server)
    
def test_connection_params(server):

    server.SSL_trust_all_certs = True
    assert server.SSL_trust_all_certs == True
    server.SSL_ignore_hostname = True
    assert server.SSL_ignore_hostname == True

    server.SSL_trust_all_certs = False
    assert server.SSL_trust_all_certs == False
    server.SSL_ignore_hostname = False
    assert server.SSL_ignore_hostname == False

def test_reinitialize(server):
    job = server.reinitialize()
    assert type(job) == kepconfig.connection.KepServiceResponse
    job = server.reinitialize(60)
    assert type(job) == kepconfig.connection.KepServiceResponse

def test_project_props(server):
    # Get Project Properties
    assert type(server.get_project_properties()) == dict

    # Modify Project Properties
    project_prop = {
        "uaserverinterface.PROJECT_OPC_UA_ENABLE": False,
        "uaserverinterface.PROJECT_OPC_UA_ANONYMOUS_LOGIN": True,
        "thingworxinterface.ENABLED": True
    }
    assert server.modify_project_properties(project_prop, force = True)

    project_prop = {
        "uaserverinterface.PROJECT_OPC_UA_ENABLE": True,
        "uaserverinterface.PROJECT_OPC_UA_ANONYMOUS_LOGIN": False,
        "thingworxinterface.ENABLED": False
    }
    assert server.modify_project_properties(project_prop, force = True)

def test_event_log(server):
    assert type(server.get_event_log(25, None, None)) == list
    
    assert type(server.get_event_log(None, datetime.datetime.fromisoformat('2022-02-21T14:23:23.000'), datetime.datetime.utcnow())) == list
