# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# UA Server Configuration Example - Simple example on how to manage a connection and 
# execute various calls for configuring the UA Server properties of the Kepware
# Configuration API

from kepconfig import connection, error
import kepconfig.admin.ua_server as ua_server

# UA Endpoints to be created with properties that can be configured
uaendpoint1 = {
    "common.ALLTYPES_NAME": "DefaultEndpoint3",
    "libadminsettings.UACONFIGMANAGER_ENDPOINT_ENABLE": True,
    "libadminsettings.UACONFIGMANAGER_ENDPOINT_ADAPTER": "Default",
    "libadminsettings.UACONFIGMANAGER_ENDPOINT_PORT": 49331,
    "libadminsettings.UACONFIGMANAGER_ENDPOINT_SECURITY_NONE": False,
    "libadminsettings.UACONFIGMANAGER_ENDPOINT_SECURITY_BASIC128_RSA15": 0,
    "libadminsettings.UACONFIGMANAGER_ENDPOINT_SECURITY_BASIC256": 0,
    "libadminsettings.UACONFIGMANAGER_ENDPOINT_SECURITY_BASIC256_SHA256": 2
}
uaendpoint2 = {
    "common.ALLTYPES_NAME": "DefaultEndpoint4",
    "libadminsettings.UACONFIGMANAGER_ENDPOINT_ENABLE": True,
    "libadminsettings.UACONFIGMANAGER_ENDPOINT_ADAPTER": "Default",
    "libadminsettings.UACONFIGMANAGER_ENDPOINT_PORT": 49332,
    "libadminsettings.UACONFIGMANAGER_ENDPOINT_SECURITY_NONE": False,
    "libadminsettings.UACONFIGMANAGER_ENDPOINT_SECURITY_BASIC128_RSA15": 0,
    "libadminsettings.UACONFIGMANAGER_ENDPOINT_SECURITY_BASIC256": 0,
    "libadminsettings.UACONFIGMANAGER_ENDPOINT_SECURITY_BASIC256_SHA256": 2
}
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
server = connection.server(host = 'localhost', port = 57513, user = 'Administrator', pw = '', https=True)

# Disabling certificate validation (INSECURE)
server.SSL_ignore_hostname = True
server.SSL_trust_all_certs = True

# Add the UA Endpoints to Kepware's UA server
try: 
    print("{} - {}".format("Adding multiple UA Endpoints",ua_server.add_endpoint(server,[uaendpoint1,uaendpoint2])))
except Exception as err:
    ErrorHandler(err)

# Modify Endpoint to disable all encryption and allow unencrypted connections

modify_ua = {
    "libadminsettings.UACONFIGMANAGER_ENDPOINT_SECURITY_NONE": True,
    "libadminsettings.UACONFIGMANAGER_ENDPOINT_SECURITY_BASIC128_RSA15": 0,
    "libadminsettings.UACONFIGMANAGER_ENDPOINT_SECURITY_BASIC256": 0,
    "libadminsettings.UACONFIGMANAGER_ENDPOINT_SECURITY_BASIC256_SHA256": 0
}

try: 
    print("{} - {}".format("Modify UA Endpoint to remove all encrypted enpoints",ua_server.modify_endpoint(server, modify_ua ,uaendpoint1['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)

# Delete an Endpoint
try: 
    print("{} - {}".format("Delete an UA Endpoint",ua_server.del_endpoint(server,uaendpoint2['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)

# All changes will not update until Kepware is Reinitialized
try: 
    print("{} - {}".format("Reinitialize Kepware to update UA Endpoint Configuration",server.reinitialize()))
except Exception as err:
    ErrorHandler(err)

# Get all UA Endpoints that are configured
try: 
    print("{} - {}".format("Get all UA Endpoint Configurations",ua_server.get_all_endpoints(server)))
except Exception as err:
    ErrorHandler(err)

# Delete an Endpoint
try: 
    print("{} - {}".format("Delete an UA Endpoint",ua_server.del_endpoint(server,uaendpoint1['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)


