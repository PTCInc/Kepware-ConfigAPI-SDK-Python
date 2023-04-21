# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# User Management Example - Simple example on how to manage a connection and 
# execute various calls for configuring the user and user group properties of the Kepware
# Configuration API

from kepconfig import connection, error
from kepconfig.admin import user_groups, users

# User Groups
group1 = {
    'common.ALLTYPES_NAME': 'Operators',
    "libadminsettings.USERMANAGER_GROUP_ENABLED": True,
    "libadminsettings.USERMANAGER_IO_TAG_READ": True,
    "libadminsettings.USERMANAGER_IO_TAG_WRITE": True,
    "libadminsettings.USERMANAGER_IO_TAG_DYNAMIC_ADDRESSING": True,
    "libadminsettings.USERMANAGER_SYSTEM_TAG_READ": True,
    "libadminsettings.USERMANAGER_SYSTEM_TAG_WRITE": True,
    "libadminsettings.USERMANAGER_INTERNAL_TAG_READ": True,
    "libadminsettings.USERMANAGER_INTERNAL_TAG_WRITE": True,
    "libadminsettings.USERMANAGER_SERVER_MANAGE_LICENSES": True,
    "libadminsettings.USERMANAGER_SERVER_RESET_OPC_DIAGS_LOG": True,
    "libadminsettings.USERMANAGER_SERVER_RESET_COMM_DIAGS_LOG": True,
    "libadminsettings.USERMANAGER_SERVER_MODIFY_SERVER_SETTINGS": True,
    "libadminsettings.USERMANAGER_SERVER_DISCONNECT_CLIENTS": True,
    "libadminsettings.USERMANAGER_SERVER_RESET_EVENT_LOG": True,
    "libadminsettings.USERMANAGER_SERVER_OPCUA_DOTNET_CONFIGURATION": True,
    "libadminsettings.USERMANAGER_SERVER_CONFIG_API_LOG_ACCESS": True,
    "libadminsettings.USERMANAGER_SERVER_REPLACE_RUNTIME_PROJECT": True,
    "libadminsettings.USERMANAGER_BROWSE_BROWSENAMESPACE": True
    }
group2 = {
    'common.ALLTYPES_NAME': 'UA Users',
    "libadminsettings.USERMANAGER_GROUP_ENABLED": True,
    "libadminsettings.USERMANAGER_IO_TAG_READ": True,
    "libadminsettings.USERMANAGER_IO_TAG_WRITE": True,
    "libadminsettings.USERMANAGER_IO_TAG_DYNAMIC_ADDRESSING": True,
    "libadminsettings.USERMANAGER_SYSTEM_TAG_READ": True,
    "libadminsettings.USERMANAGER_SYSTEM_TAG_WRITE": True,
    "libadminsettings.USERMANAGER_INTERNAL_TAG_READ": True,
    "libadminsettings.USERMANAGER_INTERNAL_TAG_WRITE": True,
    "libadminsettings.USERMANAGER_SERVER_MANAGE_LICENSES": False,
    "libadminsettings.USERMANAGER_SERVER_RESET_OPC_DIAGS_LOG": False,
    "libadminsettings.USERMANAGER_SERVER_RESET_COMM_DIAGS_LOG": False,
    "libadminsettings.USERMANAGER_SERVER_MODIFY_SERVER_SETTINGS": True,
    "libadminsettings.USERMANAGER_SERVER_DISCONNECT_CLIENTS": False,
    "libadminsettings.USERMANAGER_SERVER_RESET_EVENT_LOG": False,
    "libadminsettings.USERMANAGER_SERVER_OPCUA_DOTNET_CONFIGURATION": False,
    "libadminsettings.USERMANAGER_SERVER_CONFIG_API_LOG_ACCESS": False,
    "libadminsettings.USERMANAGER_SERVER_REPLACE_RUNTIME_PROJECT": False,
    "libadminsettings.USERMANAGER_BROWSE_BROWSENAMESPACE": True
    }

# Users
user1 = {
    "common.ALLTYPES_NAME": "Client1",
    "libadminsettings.USERMANAGER_USER_GROUPNAME": "Operators",
    "libadminsettings.USERMANAGER_USER_ENABLED": True,
    "libadminsettings.USERMANAGER_USER_PASSWORD": "Password123456"
}
user2 = {
    "common.ALLTYPES_NAME": "Client2",
    "libadminsettings.USERMANAGER_USER_GROUPNAME": "UA Users",
    "libadminsettings.USERMANAGER_USER_ENABLED": True,
    "libadminsettings.USERMANAGER_USER_PASSWORD": "Password123456"      
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
server = connection.server(host = '127.0.0.1', port = 57412, user = 'Administrator', pw = '')

# ---------------------------------------------
# User Group Methods
# ---------------------------------------------

# Add the User Groups with the appropriate parameters
try:
    print("{} - {}".format("Add new User Groups", user_groups.add_user_group(server, [group1, group2])))
except Exception as err:
    ErrorHandler(err)

# Modify permissions on a User Group
# Ex: Prevent Write access for user group

modify_group = {
    "libadminsettings.USERMANAGER_IO_TAG_WRITE": False,
    "libadminsettings.USERMANAGER_SYSTEM_TAG_WRITE": False,
    "libadminsettings.USERMANAGER_INTERNAL_TAG_WRITE": False
}

try:
    print("{} - {}".format("Modify User Group properties to prevent 'Writes'",user_groups.modify_user_group(server, modify_group, user_group= group1['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)

# Disable and Enable a user groups
try: 
    print("{} - {}".format("Disable User Group",user_groups.disable_user_group(server, group1['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)

try: 
    print("{} - {}".format("Enable User Group",user_groups.enable_user_group(server, group1['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)

# ---------------------------------------------
# User Methods
# ---------------------------------------------

# Add new users with the appropriate parameters
try:
    print("{} - {}".format("Add new Users", users.add_user(server, [user1, user2])))
except Exception as err:
    ErrorHandler(err)

# Modify new user parameters - New Password
modify_pass = {
    "libadminsettings.USERMANAGER_USER_PASSWORD": "NewPassword123"
}

try:
    print("{} - {}".format("Updated a user password", users.modify_user(server,modify_pass, user= user1['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)

# Disable and Enable a user
try:
    print("{} - {}".format("Disable a user", users.disable_user(server, user1['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)
try:
    print("{} - {}".format("Enable a user", users.enable_user(server, user1['common.ALLTYPES_NAME'])))
except Exception as err:
    ErrorHandler(err)