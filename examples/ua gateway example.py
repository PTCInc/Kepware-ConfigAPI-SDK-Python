# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# UA Gateway Example - Simple example on how to manage a connection and 
# execute various calls for the UA Gateway components of the Kepware
# Configuration API

from kepconfig import connection, error, ua_gateway


def ErrorHandler(err):
    # Generic Handler for exception errors
    if isinstance(err,  error.KepHTTPError):
        print(err.code)
        print(err.msg)
        print(err.url)
        print(err.hdrs)
        print(err.payload)
    elif isinstance(err,  error.KepURLError):
        print(err.url)
        print(err.reason)
    elif isinstance(err, error.KepError):
        print(err.msg)
    else:
        print('Different Exception Received: {}'.format(err))
        
# This creates a server reference that is used to target all modifications of 
# the Kepware configuration
server = connection.server(host = '127.0.0.1', port = 57412, user = 'Administrator', pw = '')

# Print UAG Instance Certificate information
try: 
    print("{} - {}".format("Read UA Gateway Instance Certificate properties", ua_gateway.certificates.get_instance_certificate(server)))
except Exception as err:
    ErrorHandler(err)

# Reissue self-signed UAG Instance Certificate
try: 
    print("{} - {}".format("Reissue UA Gateway self-signed Instance Certificate", ua_gateway.certificates.reissue_self_signed_instance_certificate(server)))
except Exception as err:
    ErrorHandler(err)

# Get the UAG Server Interface properties. These properties expose User Identify
# Policy, Security Policy and other Communication properties that are applied across 
# all UAG server endpoints.

try: 
    print("{} - {}".format("Get properties from UAG Server Interface configuration", ua_gateway.server.get_uag_server_interface_properties(server)))
except Exception as err:
    ErrorHandler(err)

# Modify the properties of a server interface properties in UAG. In this example, we are enabling to allow anonymous user
# identification for clients connecting to UAG server endpoints.
UAGServerInterfaceChange = {
        "ua_gateway.UA_SERVER_INTERFACE_USER_IDENTITY_POLICY_ANONYMOUS": True,
    }

try: 
    print("{} - {}".format("Update the properties of a UAG Server Interface", ua_gateway.server.modify_uag_server_interface_properties(server, UAGServerInterfaceChange, force= True) ))
except Exception as err:
    ErrorHandler(err)


# Create a new Server Endpoint for the UAG. This will create an endpoint for client applications to conenct to UAG and 
# access all downstream OPC UA servers that the UAG Client Connections will aggregate.

UAGServerEndpoint = {
        "common.ALLTYPES_NAME": "UAGServerEndpointTest",
        "common.ALLTYPES_DESCRIPTION": "",
        "ua_gateway.UA_SERVER_ENDPOINT_NETWORK_ADAPTER": 16777343,
        "ua_gateway.UA_SERVER_ENDPOINT_PORT": 58221,
        "ua_gateway.UA_SERVER_ENDPOINT_PROTOCOL": 0,
        "ua_gateway.UA_SERVER_ENDPOINT_ENABLED": True
    }

try: 
    print("{} {} - {}".format("Create new UAG Server Endpoint for UA Gateway", UAGServerEndpoint["common.ALLTYPES_DESCRIPTION"], ua_gateway.server.add_ua_server_endpoint(server, UAGServerEndpoint)))
except Exception as err:
    ErrorHandler(err)

# List the certificates in the UAG Server Endpoint trust store.
server_endpoints_cert_list = None
try: 
    server_endpoints_cert_list = ua_gateway.server.get_all_certificates(server)
    print("{} - {}".format("List of certificates in the UAG Client connection trust store", server_endpoints_cert_list ))
except Exception as err:
    ErrorHandler(err)

# Assuming that the first in the list is a new/untrusted instance certificate from a UA client, trust this certificate to allow
# the client connection to be established to the UAG server endpoint.
try: 
    print("{} - {}".format("Trust a certificate in UAG Server Endpoint trust store", ua_gateway.server.trust_certificate(server, server_endpoints_cert_list[0]["common.ALLTYPES_NAME"]) ))
except Exception as err:
    ErrorHandler(err)

# Modify the properties of a server endpoint in UAG. In this example, we are disabling the endpoint.
UAGServerEndpointChange = {
        "ua_gateway.UA_SERVER_ENDPOINT_ENABLED": False
    }

try: 
    print("{} - {}".format("Update the properties of a UAG Server Endpoint", ua_gateway.server.modify_ua_server_endpoint(server, UAGServerEndpointChange, ua_server_endpoint= UAGServerEndpoint["common.ALLTYPES_NAME"], force= True) ))
except Exception as err:
    ErrorHandler(err)

# Delete a server endpoint in the UAG
try: 
    print("{} - {}".format("Delete a UAG Server Endpoint", ua_gateway.server.del_ua_server_endpoint(server, ua_server_endpoint= UAGServerEndpoint["common.ALLTYPES_NAME"]) ))
except Exception as err:
    ErrorHandler(err)



# Create a new Client connection for the UAG. This will create a connection from UAG to the target UA server.
UAGClientConnection = {
        "common.ALLTYPES_NAME": "LocalKepwareConnectionSecure",
        "common.ALLTYPES_DESCRIPTION": "",
        "ua_gateway.UA_CLIENT_CONNECTION_STATUS": "Disconnected",
        "ua_gateway.UA_CLIENT_CONNECTION_URL_NAME": "opc.tcp://localhost:49320",
        "ua_gateway.UA_CLIENT_CONNECTION_IDENTITY_POLICY": 0,
        "ua_gateway.UA_CLIENT_CONNECTION_USER_NAME": "",
        "ua_gateway.UA_CLIENT_CONNECTION_USER_PASSWORD": "",
        "ua_gateway.UA_CLIENT_CONNECTION_SECURITY_POLICY": 3,
        "ua_gateway.UA_CLIENT_CONNECTION_MESSAGE_MODE": 2,
        "ua_gateway.UA_CLIENT_CONNECTION_ENABLED": True,
        "ua_gateway.UA_CLIENT_CONNECTION_PUBLISHING_INTERVAL": 500,
        "ua_gateway.UA_CLIENT_CONNECTION_SUBSCRIPTION_LIFETIME": 500000,
        "ua_gateway.UA_CLIENT_CONNECTION_SESSION_TIMEOUT": 60000,
        "ua_gateway.UA_CLIENT_CONNECTION_PASSTHROUGH_ENABLED": True,
        "ua_gateway.UA_CLIENT_CONNECTION_MONITORED_ITEM_QUEUE_SIZE_OVERRIDE": 1,
        "ua_gateway.UA_CLIENT_CONNECTION_DISCARD_OLDEST_OVERRIDE": 0
    }

try: 
    print("{} {} - {}".format("Create new UAG Client connection for UA Gateway to server", UAGClientConnection["common.ALLTYPES_DESCRIPTION"], ua_gateway.client.add_ua_client_connection(server, UAGClientConnection)))
except Exception as err:
    ErrorHandler(err)

# List the certificates in the UAG Client Connections trust store.
client_connection_cert_list = None
try: 
    client_connection_cert_list = ua_gateway.client.get_all_certificates(server)
    print("{} - {}".format("List of certificates in the UAG Client connection trust store", client_connection_cert_list ))
except Exception as err:
    ErrorHandler(err)

# Assuming that the first in the list is a new/untrusted instance certificate from a UA server, trust this certificate to allow
# the client connection to be established.
try: 
    print("{} - {}".format("Trust a certificate in UAG Client connection trust store", ua_gateway.client.trust_certificate(server, client_connection_cert_list[0]["common.ALLTYPES_NAME"]) ))
except Exception as err:
    ErrorHandler(err)

# Modify the properties of a client connection in UAG. In this example, we are disabling the client connection.
UAGClientConnectionChange = {
        "ua_gateway.UA_CLIENT_CONNECTION_ENABLED": False
    }

try: 
    print("{} - {}".format("Update the properties of a UAG Client connection", ua_gateway.client.modify_ua_client_connection(server, UAGClientConnectionChange, ua_client_connection= UAGClientConnection["common.ALLTYPES_NAME"], force= True) ))
except Exception as err:
    ErrorHandler(err)

# Delete a client connection in the UAG
try: 
    print("{} - {}".format("Delete a UAG Client connection", ua_gateway.client.del_ua_client_connection(server, ua_client_connection= UAGClientConnection["common.ALLTYPES_NAME"]) ))
except Exception as err:
    ErrorHandler(err)
