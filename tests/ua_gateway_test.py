# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# UA Gateway Test - Test to exectute various UA Gateway API configuration 
# features

import os, sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kepconfig import error, connection
from kepconfig.ua_gateway import common, certificates, client, server as UAGServers
import pytest

CLIENTNAME = 'TESTC'
SERVERNAME = 'TESTS'

def HTTPErrorHandler(err):
    if err.__class__ is error.KepHTTPError:
        print(err.code)
        print(err.msg)
        print(err.url)
        print(err.hdrs)
        print(err.payload)
    else:
        print('Different Exception Received: {}'.format(err))

def initialize(server):
    if server_type == 'TKE': pytest.skip("UA Gateway not configurable in {}.".format(server_type), allow_module_level=True)
    try:
        server._config_get(server.url + common.SERVER_ROOT)
    except Exception as err:
        pytest.skip("UA Gateway plug-in is not installed", allow_module_level=True)

def complete(server):
    try:
        clients_left = client.get_all_ua_client_connections(server)
        for x in clients_left:
            print(client.del_ua_client_connection(server,x['common.ALLTYPES_NAME']))
        endpoint_list = UAGServers.get_all_ua_server_endpoints(server)
        for x in endpoint_list:
            print(UAGServers.del_ua_server_endpoint(server,x['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)

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

def test_UAG_server_interface_properties_get(server: connection.server):
    assert type(UAGServers.get_uag_server_interface_properties(server)) == dict

def test_UAG_server_interface_properties_modify(server: connection.server):
    propertychange = {
        "ua_gateway.UA_SERVER_INTERFACE_USER_IDENTITY_POLICY_ANONYMOUS": True,
    }

    assert UAGServers.modify_uag_server_interface_properties(server, propertychange, force= False)

def test_UAG_instance_certificate_get(server: connection.server):
    pytest.skip("Skipping Deprecated Method Test", allow_module_level=True)
    # Get all UAG instance certs
    # TODO: Implement if/when multiple instance certificates can be configured.
    # cert_list = certificates.get_all_certificates(server)
    # assert type(cert_list) == list

    # Read a specific instance cert
    assert type(certificates.get_instance_certificate(server)) == dict

    # TODO: Create test for filter

def test_UAG_server_instance_certificate_get(server: connection.server):
    # Get all UAG instance certs
    # TODO: Implement if/when multiple instance certificates can be configured.
    # cert_list = certificates.get_all_certificates(server)
    # assert type(cert_list) == list

    # Read a specific instance cert
    assert type(UAGServers.get_instance_certificate(server)) == dict

def test_UAG_client_instance_certificate_get(server: connection.server):
    # Get all UAG instance certs
    # TODO: Implement if/when multiple instance certificates can be configured.
    # cert_list = certificates.get_all_certificates(server)
    # assert type(cert_list) == list

    # Read a specific instance cert
    assert type(client.get_instance_certificate(server)) == dict

def test_UAG_instance_certificate_reissue(server: connection.server):
    pytest.skip("Skipping Deprecated Method Test", allow_module_level=True)
    assert certificates.reissue_self_signed_instance_certificate(server)

def test_UAG_server_instance_certificate_reissue(server: connection.server):
    job = UAGServers.reissue_self_signed_instance_certificate(server)
    assert type(job) == connection.KepServiceResponse
    time.sleep(1)

    # Wait for service to be completed
    while True:
        time.sleep(1)
        status = server.service_status(job)
        if (status.complete == True): break
        assert type(status) == connection.KepServiceStatus

def test_UAG_client_instance_certificate_reissue(server: connection.server):
    job = client.reissue_self_signed_instance_certificate(server)
    assert type(job) == connection.KepServiceResponse
    time.sleep(1)

    # Wait for service to be completed
    while True:
        time.sleep(1)
        status = server.service_status(job)
        if (status.complete == True): break
        assert type(status) == connection.KepServiceStatus

def test_UAG_client_conn_add(server: connection.server):
    # Add one client
    sClient = {
        "common.ALLTYPES_NAME": f"{CLIENTNAME}1"
    }

    assert client.add_ua_client_connection(server, sClient)

    # Add multiple clients, with single failure
    dClient = [
        sClient,
        {
            "common.ALLTYPES_NAME": f"{CLIENTNAME}2"
        }
    ]

    assert type(client.add_ua_client_connection(server, dClient)) == list

    # Add existing client check

    with pytest.raises(error.KepHTTPError) as e:
        client.add_ua_client_connection(server, sClient)
    assert e.type == error.KepHTTPError

def test_UAG_client_conn_get(server: connection.server):
    # Get one client connection
    assert type(client.get_ua_client_connection(server, f'{CLIENTNAME}1')) == dict

    # Get all client connections
    assert type(client.get_all_ua_client_connections(server)) == list

    # TODO: Test with options

def test_UAG_client_conn_modify(server: connection.server):
    # Modify with name in data
    conn_data = {
        "common.ALLTYPES_NAME": f"{CLIENTNAME}1",
        'common.ALLTYPES_DESCRIPTION': "Test Modify"
    }

    assert client.modify_ua_client_connection(server, conn_data)

    # Modify with name not in data
    conn_data = {
        'common.ALLTYPES_DESCRIPTION': "Test Modify"
    }
    assert client.modify_ua_client_connection(server, conn_data, ua_client_connection=f"{CLIENTNAME}1")

def test_UAG_client_conn_del(server: connection.server):
    # Delete Connection
    assert client.del_ua_client_connection(server, f"{CLIENTNAME}1")   

    # Delete non existing connection
    with pytest.raises(error.KepHTTPError) as e:
        client.del_ua_client_connection(server, f"{CLIENTNAME}1")
    assert e.type == error.KepHTTPError

def test_UAG_client_conn_cert_get(server: connection.server):
    # Get all certs for Client Connections
    certs = client.get_all_certificates(server)
    assert type(certs) == list

    if not certs:
        # No certs to test get specific cert with
        pytest.skip(f"No certs available to read. Certs list: {certs}")
    
    assert type(client.get_certificate(server, certs[0]["common.ALLTYPES_NAME"])) == dict

def test_UAG_client_conn_cert_del(server: connection.server):
    pytest.skip(f"Client connection cert deletion is disabled.")
    # Get all certs for Client Connections
    certs = client.get_all_certificates(server)
    assert type(certs) == list

    if not certs:
        # No certs to test get specific cert with
        pytest.skip(f"No certs available to read. Certs list: {certs}")
    assert client.delete_certificate(server, certs[-1]["common.ALLTYPES_NAME"])

def test_UAG_client_conn_cert_trust(server: connection.server):
    # Get first cert and reject then trust the certificate
    certs = client.get_all_certificates(server)
    if not certs:
        # No certs to test get specific cert with
        pytest.skip(f"No certs available to read. Certs list: {certs}")
    
    assert client.reject_certificate(server, certs[0]["common.ALLTYPES_NAME"])

    assert client.trust_certificate(server, certs[0]["common.ALLTYPES_NAME"])

def test_UAG_server_end_add(server: connection.server):
    # Add one client
    sServer = {
        "common.ALLTYPES_NAME": f"{SERVERNAME}1"
    }

    assert UAGServers.add_ua_server_endpoint(server, sServer)

    # Add multiple clients, with single failure
    dServer = [
        sServer,
        {
            "common.ALLTYPES_NAME": f"{SERVERNAME}2"
        }
    ]

    assert type(UAGServers.add_ua_server_endpoint(server, dServer)) == list

    # Add existing client check

    with pytest.raises(error.KepHTTPError) as e:
        UAGServers.add_ua_server_endpoint(server, sServer)
    assert e.type == error.KepHTTPError

def test_UAG_server_end_get(server: connection.server):
    # Get one client connection
    assert type(UAGServers.get_ua_server_endpoint(server, f'{SERVERNAME}1')) == dict

    # Get all client connections
    assert type(UAGServers.get_all_ua_server_endpoints(server)) == list

    # TODO: Test with options

def test_UAG_server_end_modify(server: connection.server):
    # Modify with name in data
    endp_data = {
        "common.ALLTYPES_NAME": f"{SERVERNAME}1",
        'common.ALLTYPES_DESCRIPTION': "Test Modify"
    }

    assert UAGServers.modify_ua_server_endpoint(server, endp_data)

    # Modify with name not in data
    endp_data = {
        'common.ALLTYPES_DESCRIPTION': "Test Modify"
    }
    assert UAGServers.modify_ua_server_endpoint(server, endp_data, ua_server_endpoint=f"{SERVERNAME}1")

def test_UAG_server_end_del(server: connection.server):
    # Delete Connection
    assert UAGServers.del_ua_server_endpoint(server, f"{SERVERNAME}1")   

    # Delete non existing connection
    with pytest.raises(error.KepHTTPError) as e:
        UAGServers.del_ua_server_endpoint(server, f"{SERVERNAME}1")
    assert e.type == error.KepHTTPError

def test_UAG_server_end_cert_get(server: connection.server):
    # Get all certs for Client Connections
    certs = UAGServers.get_all_certificates(server)
    assert type(certs) == list

    if not certs:
        # No certs to test get specific cert with
        pytest.skip(f"No certs available to read. Certs list: {certs}")
    
    assert type(UAGServers.get_certificate(server, certs[0]["common.ALLTYPES_NAME"])) == dict

def test_UAG_server_conn_cert_del(server: connection.server):
    pytest.skip(f"Server connection cert deletion is disabled.")
    # Get all certs for Server Connections
    certs = UAGServers.get_all_certificates(server)
    assert type(certs) == list

    if not certs:
        # No certs to test get specific cert with
        pytest.skip(f"No certs available to read. Certs list: {certs}")
    assert UAGServers.delete_certificate(server, certs[-1]["common.ALLTYPES_NAME"])

def test_UAG_server_end_cert_trust(server: connection.server):
    # Get first cert and reject then trust the certificate
    certs = UAGServers.get_all_certificates(server)
    if not certs:
        # No certs to test get specific cert with
        pytest.skip(f"No certs available to read. Certs list: {certs}")
    
    assert UAGServers.reject_certificate(server, certs[0]["common.ALLTYPES_NAME"])

    assert UAGServers.trust_certificate(server, certs[0]["common.ALLTYPES_NAME"])





