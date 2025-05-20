# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Advanced Tag Groups Test - Test to execute various calls for advanced tags plugin
# parts of the Kepware configuration API

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kepconfig import adv_tags, error, connection
import pytest

# Names to be used for testing
adv_tag_group_name = 'AdvTagGroup1'
adv_tag_group_child = 'AdvTagGroupChild'
adv_tag_child_group_path = f'_advancedtags.{adv_tag_group_name}.{adv_tag_group_child}'

def HTTPErrorHandler(err):
    if err.__class__ is error.KepHTTPError:
        print(err.code)
        print(err.msg)
        print(err.url)
        print(err.hdrs)
        print(err.payload)
    else:
        print('Different Exception Received: {}'.format(err))

def initialize(server: connection.server):
    # Check if the server is TKE or TKS
    if server_type == 'TKE': pytest.skip("Advanced Tags not configurable in {}.".format(server_type), allow_module_level=True)

    try:
        server._config_get(server.url +"/project/_advancedtags")
    except Exception as err:
        pytest.skip("Advanced Tags is not installed", allow_module_level=True)

def complete(server: connection.server):
    pass

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

def test_adv_tag_group_add(server):
    # Add advanced tag group at root
    tag_group_info = [
        {
            "common.ALLTYPES_NAME": adv_tag_group_name
        }
    ]
    assert adv_tags.adv_tag_group.add_tag_group(server, '_advancedtags', tag_group_info)

    # Add advanced tag group as a child
    tag_group_info = [
        {
            "common.ALLTYPES_NAME": adv_tag_group_child
        }
    ]
    assert adv_tags.adv_tag_group.add_tag_group(server, f'_advancedtags.{adv_tag_group_name}', tag_group_info)

def test_adv_tag_group_get(server):
    # Get advanced tag group
    assert type(adv_tags.adv_tag_group.get_tag_group(server, adv_tag_child_group_path)) == dict

    # Get all advanced tag groups at root
    assert type(adv_tags.adv_tag_group.get_all_tag_groups(server, '')) == list

    # Get all advanced tag groups under a parent
    assert type(adv_tags.adv_tag_group.get_all_tag_groups(server, f'_advancedtags.{adv_tag_group_name}')) == list

def test_adv_tag_group_modify(server):
    # Modify advanced tag group
    tag_group_data = {
        "common.ALLTYPES_DESCRIPTION": "Modified advanced tag group"
    }
    assert adv_tags.adv_tag_group.modify_tag_group(server, adv_tag_child_group_path, tag_group_data, force=True)

def test_adv_tag_group_del(server):
    # Delete parent advanced tag group
    assert adv_tags.adv_tag_group.del_tag_group(server, f'_advancedtags.{adv_tag_group_name}')