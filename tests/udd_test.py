# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# UDD Test - Test to exersice all UDD Profile Library related features

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kepconfig
from kepconfig import error, connectivity
import kepconfig.connectivity.udd.profile as uddprofile
import time
import datetime
import pytest


# Channel and Device name to be used
profile1 = {
        "common.ALLTYPES_NAME": "Profile1",
        "common.ALLTYPES_DESCRIPTION": "",
        "libudcommon.LIBUDCOMMON_PROFILE_JAVASCRIPT": "function onProfileLoad () {return {version: \"2.0\", mode: \"Client\"};}\nfunction onValidateTag (info) {}\nfunction onTagsRequest (info) {}\nfunction onData (info) {}\n"
    }
profile2 = {
        "common.ALLTYPES_NAME": "Profile2",
        "common.ALLTYPES_DESCRIPTION": "",
        "libudcommon.LIBUDCOMMON_PROFILE_JAVASCRIPT": "function onProfileLoad () {return {version: \"2.0\", mode: \"Client\"};}\nfunction onValidateTag (info) {}\nfunction onTagsRequest (info) {}\nfunction onData (info) {}\n"
    }

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


def initialize(server: kepconfig.connection.server):
    if server_type == 'TKE': pytest.skip("UDD not configurable in {}.".format(server_type), allow_module_level=True)
    
    try:
        server._config_get(server.url +"/doc/drivers/Universal Device/channels")
    except Exception as err:
        pytest.skip("UDD Driver is not installed", allow_module_level=True)

def complete(server):
    try:
        profiles_list = uddprofile.get_all_profiles(server)
        [uddprofile.del_profile(server, g['common.ALLTYPES_NAME']) for g in profiles_list]
    except Exception as err:
            ErrorHandler(err)

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

# 
# MAIN TEST SET
# 


def test_profile_add(server: kepconfig.connection.server):
    # Add profile
    assert uddprofile.add_profile(server, profile1)

    # Add multi profiles with one failure
    assert type(uddprofile.add_profile(server, [profile1, profile2])) == list

def test_profile_get(server: kepconfig.connection.server):
    # Get All Profiles
    assert type(uddprofile.get_all_profiles(server)) == list

    # Get All Profiles - alternate
    assert type(uddprofile.get_profile(server)) == list

    # Get one profile
    assert type(uddprofile.get_profile(server, profile1['common.ALLTYPES_NAME'])) == dict


def test_profile_modify(server: kepconfig.connection.server):
    # Modify Profile
    profile1['common.ALLTYPES_DESCRIPTION'] = 'Test Change'
    assert uddprofile.modify_profile(server, profile1)

    # Modify Profile with name parameter
    change = {'common.ALLTYPES_DESCRIPTION':'Test Change'}
    assert uddprofile.modify_profile(server, change, profile1['common.ALLTYPES_NAME'], force=True)

def test_profile_delete(server: kepconfig.connection.server):
    # Modify Profile
    assert uddprofile.del_profile(server, profile1['common.ALLTYPES_NAME'])