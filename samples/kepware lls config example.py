# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Kepware LLS Config Example - Simple example on how to manage properties of a Kepware instance
# to connect to a Local License Server through the Kepware Configuration API

from kepconfig import connection, error
from kepconfig.admin import lls

def ErrorHandler(err):
    # Generic Handler for exception errors
    if err.__class__ is error.KepError:
        print(err.msg)
    elif err.__class__ is error.KepHTTPError:
        print(err.code)
        print(err.msg)
        print(err.url)
        print(err.hdrs)
        print(err.payload)
    elif err.__class__ is error.KepURLError:
        print(err.url)
        print(err.reason)
    else:
        print('Different Exception Received: {}'.format(err))

# This creates a server reference that is used to target all modifications of 
# the Kepware configuration
server = connection.server(host = '127.0.0.1', port = 57412, user = 'Administrator', pw = '')



# Retreive the LLS properties from a Kepware instance and return a lls_config class object
try:
    LLSconfig = lls.get_lls_config(server)
    print("{} - {}".format("Get Local License Server parameters for Kepware instance",LLSconfig))
except Exception as err:
    ErrorHandler(err)


# Create a lls_config class object from Dict parameters
JSON_lls_config = {
    "libadminsettings.LICENSING_SERVER_PORT": 80,
    "libadminsettings.LICENSING_SERVER_NAME": "test_host",
    "libadminsettings.LICENSING_CHECK_PERIOD_MINS": 20,
    "libadminsettings.LICENSING_SERVER_SSL_PORT": 7777,
    "libadminsettings.LICENSING_SERVER_ALLOW_INSECURE_COMMS": True,
    "libadminsettings.LICENSING_SERVER_ALLOW_SELF_SIGNED_CERTS": True,
    "libadminsettings.LICENSING_CLIENT_ALIAS": "TestAliasName"
}

try:
    print("{} - {}".format("Create Local License Server parameters object from Dict", lls.lls_config(JSON_lls_config)))
except Exception as err:
    ErrorHandler(err)


# Update lls_config object with new values and update the Kepware instance with new parameters
LLSconfig.server_name = 'HOSTNAME'
try:
    print("{} - {}".format("Update Local License Server parameters for Kepware instance",lls.update_lls_config(server, LLSconfig)))
except Exception as err:
    ErrorHandler(err)

# Enable the LLS connection for the Kepware instance
try:
    print("{} - {}".format("Enable Local License Server connection for Kepware instance",lls.enable_lls(server)))
except Exception as err:
    ErrorHandler(err)

# Disable the LLS connection for the Kepware instance
try:
    print("{} - {}".format("Disable Local License Server connection for Kepware instance",lls.disable_lls(server)))
except Exception as err:
    ErrorHandler(err)