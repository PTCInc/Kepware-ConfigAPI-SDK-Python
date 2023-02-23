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
WINFILENAME = 'test\\project.opf'
WINFILENAMEENCRYPT = 'test\\project.sopf'
WINFILEPATH = 'C:\\ProgramData\\PTC\\ThingWorx Kepware Server\\V6\\'
LINUXFILENAME = 'project.lpf'
LINUXFILENAMEENCRYPT = 'project.slpf'
LINUXFILEPATH = 'C:\\DockerMounts\\tke1_5\\user_data\\'
FILEPASSWORD = 'Password'


def initialize(server):
    pass

def complete(server):
    if server_type == 'TKE':
        file = LINUXFILENAME
        file_encrypt = LINUXFILENAMEENCRYPT
        filepath = LINUXFILEPATH
    else:
        file = WINFILENAME
        file_encrypt = WINFILENAMEENCRYPT
        filepath = WINFILEPATH
    files = ['{}{}'.format(filepath, file), '{}{}'.format(filepath, file_encrypt)]
    try:
        for x in files:
            if os.path.exists(x):
                os.remove(x)
            else:
                print("The file does not exist")
    except PermissionError as e:
        print (e)

@pytest.fixture(scope="module")
def server(kepware_server):
    server = kepware_server[0]
    global server_type
    server_type = kepware_server[1]
    
    # Initialize any configuration before testing in module
    initialize(server)

    # Everything below yield is run after module tests are completed
    yield server
    complete(server)
    
def test_connection_params(server: kepconfig.connection.server):
    current = [server.SSL_trust_all_certs,server.SSL_ignore_hostname]
    server.SSL_trust_all_certs = True
    assert server.SSL_trust_all_certs == True
    server.SSL_ignore_hostname = True
    assert server.SSL_ignore_hostname == True

    server.SSL_trust_all_certs = False
    assert server.SSL_trust_all_certs == False
    server.SSL_ignore_hostname = False
    assert server.SSL_ignore_hostname == False

    server.SSL_trust_all_certs = current[0]
    server.SSL_ignore_hostname = current[1]
    

def test_reinitialize_service_status(server: kepconfig.connection.server):
    job = server.reinitialize()
    assert type(job) == kepconfig.connection.KepServiceResponse
    time.sleep(1)
    status = server.service_status(job)
    assert type(status) == kepconfig.connection.KepServiceStatus
    job = server.reinitialize(60)
    assert type(job) == kepconfig.connection.KepServiceResponse


def test_project_props(server: kepconfig.connection.server):
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

def test_event_log(server: kepconfig.connection.server):
    assert type(server.get_event_log(25, None, None)) == list
    
    assert type(server.get_event_log(None, datetime.datetime.fromisoformat('2022-02-21T14:23:23.000'), datetime.datetime.utcnow())) == list

def test_projectsave_service(server: kepconfig.connection.server):
    if server_type == 'TKE':
        file = LINUXFILENAME
        file_encrypt = LINUXFILENAMEENCRYPT
        filepath = LINUXFILEPATH
    else:
        file = WINFILENAME
        file_encrypt = WINFILENAMEENCRYPT
        filepath = WINFILEPATH

    # Save non-encrypted file
    time.sleep(1)
    job = server.save_project(file, None, 60)
    assert type(job) == kepconfig.connection.KepServiceResponse
    time.sleep(1)
    # status = server.service_status(job)

    # Wait for service to be completed
    while True:
        time.sleep(1)
        status = server.service_status(job)
        if (status.complete == True): break
        assert type(status) == kepconfig.connection.KepServiceStatus

    # Save encrypted file
    time.sleep(1)
    job = server.save_project(file_encrypt, FILEPASSWORD, 60)
    assert type(job) == kepconfig.connection.KepServiceResponse
    time.sleep(1)
    status = server.service_status(job)

    # Wait for service to be completed
    while True:
        time.sleep(1)
        status = server.service_status(job)
        if (status.complete == True): break
        assert type(status) == kepconfig.connection.KepServiceStatus

def test_projectload_service(server: kepconfig.connection.server):
    
    if server_type == 'TKE':
        file = LINUXFILENAME
        file_encrypt = LINUXFILENAMEENCRYPT
        filepath = ''
    else:
        file = WINFILENAME
        file_encrypt = WINFILENAMEENCRYPT
        filepath = WINFILEPATH

    # Load non-encrypted file
    time.sleep(1)
    job = server.load_project('{}{}'.format(filepath, file), None, 60)
    assert type(job) == kepconfig.connection.KepServiceResponse

    # Wait for service to be completed
    while True:
        time.sleep(1)
        status = server.service_status(job)
        if (status.complete == True): break
        assert type(status) == kepconfig.connection.KepServiceStatus

    # Load encrypted file
    time.sleep(1)
    job = server.load_project('{}{}'.format(filepath, file_encrypt), FILEPASSWORD, 60)
    assert type(job) == kepconfig.connection.KepServiceResponse

    # Wait for service to be completed
    while True:
        time.sleep(1)
        status = server.service_status(job)
        if (status.complete == True): break
        assert type(status) == kepconfig.connection.KepServiceStatus

def test_get_status(server: kepconfig.connection.server):
    assert type(server.get_status()) == list

def test_get_info(server: kepconfig.connection.server):
    assert type(server.get_info()) == dict