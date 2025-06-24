# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Note: The code within this file was created in total or in part
#  with the use of AI tools.

# Advanced Tag Groups Test - Test to execute various calls for advanced tags plugin
# parts of the Kepware configuration API

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kepconfig import adv_tags, error, connection, connectivity
import pytest

adv_tag_list_avail  = []

# Names to be used for testing
adv_tag_group_name = 'AdvTagGroup1'
adv_tag_group_child = 'AdvTagGroupChild'
adv_tag_child_group_path = f'_advancedtags.{adv_tag_group_name}.{adv_tag_group_child}'

sim_ch_name = 'SimulatedDevice'
sim_dev_name = 'SimulatedDevice'
sim_tag_name = 'tag1'

avg_tag_name = 'AvgTag1'
avg_tag_data = [
        {
            "common.ALLTYPES_NAME": avg_tag_name,
            "common.ALLTYPES_DESCRIPTION": "",
            "advanced_tags.ENABLED": True,
            "advanced_tags.AVERAGE_TAG": "_System._Time_Hour",
            "advanced_tags.DATATYPE": 9,
            "advanced_tags.RUN_TAG": "_System._Time_Second"
        }
    ]

derived_tag_name = 'DerivedTag1'
derived_tag_data = [
    {
        "common.ALLTYPES_NAME": derived_tag_name,
        "common.ALLTYPES_DESCRIPTION": "",
        "advanced_tags.ENABLED": True,
        "advanced_tags.DERIVED_EXPRESSION": "20.00 + 100.00",
        "advanced_tags.DATATYPE": 9,
    }
]

complex_tag_name = 'ComplexTag1'
complex_tag_data = [
    {
        "common.ALLTYPES_NAME": complex_tag_name,
        "common.ALLTYPES_DESCRIPTION": "",
        "advanced_tags.ENABLED": True,
    }
]

cumulative_tag_name = 'CumulativeTag1'
cumulative_tag_data = [
    {
        "common.ALLTYPES_NAME": cumulative_tag_name,
        "common.ALLTYPES_DESCRIPTION": "",
        "advanced_tags.ENABLED": True,
        "advanced_tags.CUMULATIVE_TAG": "_System._Time_Hour",
    }
]

minimum_tag_name = 'MinimumTag1'
minimum_tag_data = [
    {
        "common.ALLTYPES_NAME": minimum_tag_name,
        "common.ALLTYPES_DESCRIPTION": "",
        "advanced_tags.ENABLED": True,
        "advanced_tags.MINIMUM_TAG": "_System._Time_Hour",
        "advanced_tags.RUN_TAG": "_System._Time_Second"
    }
]

maximum_tag_name = 'MaximumTag1'
maximum_tag_data = [
    {
        "common.ALLTYPES_NAME": maximum_tag_name,
        "common.ALLTYPES_DESCRIPTION": "",
        "advanced_tags.ENABLED": True,
        "advanced_tags.MAXIMUM_TAG": "_System._Time_Hour",
        "advanced_tags.RUN_TAG": "_System._Time_Second"
    }
]

link_tag_name = 'LinkTag1'
link_tag_data = [
    {
        "common.ALLTYPES_NAME": link_tag_name,
        "common.ALLTYPES_DESCRIPTION": "",
        "advanced_tags.ENABLED": True,
        "advanced_tags.LINK_INPUT_TAG": "_System._Time_Hour",
        "advanced_tags.LINK_OUTPUT_TAG": f"{sim_ch_name}.{sim_dev_name}.{sim_tag_name}",
    }
]

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
    
    # Create simulated device for testing
    sim_device = {
        "common.ALLTYPES_NAME": sim_ch_name,
        "servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator",
        "devices": [
            {
                "common.ALLTYPES_NAME": sim_dev_name,
                "servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Simulator",
                "tags": [
                    {
                        "common.ALLTYPES_NAME": sim_tag_name,
                        "servermain.TAG_ADDRESS": "K0"
                    }
                ],
            }
        ]
    }
    try:
        connectivity.channel.add_channel(server, sim_device)
    except Exception as err:
        HTTPErrorHandler(err)
        return False
    return True


def complete(server: connection.server):
    # Remove advanced tag group and all tags created during the test
    children = server._config_get(server.url +"/project/_advancedtags?content=children").payload
    for key, obj_list in children.items():
        if key == 'average_tags':
            for obj in obj_list:
                avg_tag_path = f'_advancedtags.{obj["name"]}'
                adv_tags.average_tags.del_average_tag(server, avg_tag_path)
        elif key == 'derived_tags':
            for obj in obj_list:
                derived_tag_path = f'_advancedtags.{obj["name"]}'
                adv_tags.derived_tags.del_derived_tag(server, derived_tag_path)
        elif key == 'complex_tags':
            for obj in obj_list:
                complex_tag_path = f'_advancedtags.{obj["name"]}'
                adv_tags.complex_tags.del_complex_tag(server, complex_tag_path)
        elif key == 'cumulative_tags':
            for obj in obj_list:
                cumulative_tag_path = f'_advancedtags.{obj["name"]}'
                adv_tags.cumulative_tags.del_cumulative_tag(server, cumulative_tag_path)
        elif key == 'minimum_tags':
            for obj in obj_list:
                minimum_tag_path = f'_advancedtags.{obj["name"]}'
                adv_tags.min_tags.del_minimum_tag(server, minimum_tag_path)
        elif key == 'maximum_tags':
            for obj in obj_list:
                maximum_tag_path = f'_advancedtags.{obj["name"]}'
                adv_tags.max_tags.del_maximum_tag(server, maximum_tag_path)
        elif key == 'link_tags':
            for obj in obj_list:
                link_tag_path = f'_advancedtags.{obj["name"]}'
                adv_tags.link_tags.del_link_tag(server, link_tag_path)
    
    # Delete all Channels
    try:
        ch_left = connectivity.channel.get_all_channels(server)
        for x in ch_left:
            print(connectivity.channel.del_channel(server,x['common.ALLTYPES_NAME']))
    except Exception as err:
        HTTPErrorHandler(err)

@pytest.fixture(scope="module")
def server(kepware_server):
    server = kepware_server[0]
    global server_type
    server_type = kepware_server[1]
    
    # Initialize any configuration before testing in module
    if not initialize(server):
        pytest.fail("Simulation Device creation failed")

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

def test_average_tag_add(server):
    # Add an average tag to the root advanced tag plug-in
    assert adv_tags.average_tags.add_average_tag(server, f'_advancedtags', avg_tag_data)
    testTag = {
            "common.ALLTYPES_NAME": "newAvgTag",
            "common.ALLTYPES_DESCRIPTION": "",
            "advanced_tags.ENABLED": True,
            "advanced_tags.AVERAGE_TAG": "_System._Time_Hour",
            "advanced_tags.DATATYPE": 9,
            "advanced_tags.RUN_TAG": "_System._Time_Second"
        }
    avg_tag_data.append(testTag)

    # Add an average tag to the advanced tag group
    assert adv_tags.average_tags.add_average_tag(server, f'_advancedtags.{adv_tag_group_name}', avg_tag_data)

def test_average_tag_get(server):
    # Get the average tag
    avg_tag_path = f'_advancedtags.{adv_tag_group_name}.{avg_tag_name}'
    result = adv_tags.average_tags.get_average_tag(server, avg_tag_path)
    assert type(result) == dict
    assert result.get("common.ALLTYPES_NAME") == avg_tag_name

def test_average_tag_modify(server):
    # Modify the average tag
    avg_tag_path = f'_advancedtags.{adv_tag_group_name}.{avg_tag_name}'
    avg_tag_data = {
        "common.ALLTYPES_DESCRIPTION": "Modified average tag"
    }
    assert adv_tags.average_tags.modify_average_tag(server, avg_tag_path, avg_tag_data, force=True)

def test_average_tag_get_all(server):
    # Get all average tags under the group
    result = adv_tags.average_tags.get_all_average_tags(server, f'_advancedtags.{adv_tag_group_name}')
    assert type(result) == list
    assert any(tag.get("common.ALLTYPES_NAME") == avg_tag_name for tag in result)

def test_average_tag_del(server):
    # Delete the average tag
    avg_tag_path = f'_advancedtags.{adv_tag_group_name}.{avg_tag_name}'
    assert adv_tags.average_tags.del_average_tag(server, avg_tag_path)

def test_derived_tag_add(server):
    # Add a derived tag to the root advanced tag plug-in
    assert adv_tags.derived_tags.add_derived_tag(server, f'_advancedtags', derived_tag_data)

    testTag = {
        "common.ALLTYPES_NAME": "newDerivedTag",
        "common.ALLTYPES_DESCRIPTION": "",
        "advanced_tags.ENABLED": True,
        "advanced_tags.DERIVED_EXPRESSION": "20.00 + 100.00",
        "advanced_tags.DATATYPE": 9,
    }
    derived_tag_data.append(testTag)
    # Add a derived tag to the advanced tag group
    assert adv_tags.derived_tags.add_derived_tag(server, f'_advancedtags.{adv_tag_group_name}', derived_tag_data)

def test_derived_tag_get(server):
    # Get the derived tag
    derived_tag_path = f'_advancedtags.{adv_tag_group_name}.{derived_tag_name}'
    result = adv_tags.derived_tags.get_derived_tag(server, derived_tag_path)
    assert type(result) == dict
    assert result.get("common.ALLTYPES_NAME") == derived_tag_name

def test_derived_tag_modify(server):
    # Modify the derived tag
    derived_tag_path = f'_advancedtags.{adv_tag_group_name}.{derived_tag_name}'
    tag_data = {
        "common.ALLTYPES_DESCRIPTION": "Modified derived tag"
    }
    assert adv_tags.derived_tags.modify_derived_tag(server, derived_tag_path, tag_data, force=True)

def test_derived_tag_get_all(server):
    # Get all derived tags under the group
    result = adv_tags.derived_tags.get_all_derived_tags(server, f'_advancedtags.{adv_tag_group_name}')
    assert type(result) == list
    assert any(tag.get("common.ALLTYPES_NAME") == derived_tag_name for tag in result)

def test_derived_tag_del(server):
    # Delete the derived tag
    derived_tag_path = f'_advancedtags.{adv_tag_group_name}.{derived_tag_name}'
    assert adv_tags.derived_tags.del_derived_tag(server, derived_tag_path)

def test_complex_tag_add(server):
    # Add a complex tag to the root advanced tag plug-in
    assert adv_tags.complex_tags.add_complex_tag(server, f'_advancedtags', complex_tag_data)

    testTag = {
        "common.ALLTYPES_NAME": "newComplexTag",
        "common.ALLTYPES_DESCRIPTION": "",
        "advanced_tags.ENABLED": True,
    }
    complex_tag_data.append(testTag)
    # Add a complex tag to the advanced tag group
    assert adv_tags.complex_tags.add_complex_tag(server, f'_advancedtags.{adv_tag_group_name}', complex_tag_data)

def test_complex_tag_get(server):
    # Get the complex tag
    complex_tag_path = f'_advancedtags.{adv_tag_group_name}.{complex_tag_name}'
    result = adv_tags.complex_tags.get_complex_tag(server, complex_tag_path)
    assert type(result) == dict
    assert result.get("common.ALLTYPES_NAME") == complex_tag_name

def test_complex_tag_modify(server):
    # Modify the complex tag
    complex_tag_path = f'_advancedtags.{adv_tag_group_name}.{complex_tag_name}'
    tag_data = {
        "common.ALLTYPES_DESCRIPTION": "Modified complex tag"
    }
    assert adv_tags.complex_tags.modify_complex_tag(server, complex_tag_path, tag_data, force=True)

def test_complex_tag_get_all(server):
    # Get all complex tags under the group
    result = adv_tags.complex_tags.get_all_complex_tags(server, f'_advancedtags.{adv_tag_group_name}')
    assert type(result) == list
    assert any(tag.get("common.ALLTYPES_NAME") == complex_tag_name for tag in result)

def test_complex_tag_del(server):
    # Delete the complex tag
    complex_tag_path = f'_advancedtags.{adv_tag_group_name}.{complex_tag_name}'
    assert adv_tags.complex_tags.del_complex_tag(server, complex_tag_path)

def test_cumulative_tag_add(server):
    # Add a cumulative tag to the root advanced tag plug-in
    assert adv_tags.cumulative_tags.add_cumulative_tag(server, f'_advancedtags', cumulative_tag_data)

    testTag = {
        "common.ALLTYPES_NAME": "newCumulativeTag",
        "common.ALLTYPES_DESCRIPTION": "",
        "advanced_tags.ENABLED": True,
        "advanced_tags.CUMULATIVE_TAG": "_System._Time_Hour",
    }
    cumulative_tag_data.append(testTag)
    # Add a cumulative tag to the advanced tag group
    assert adv_tags.cumulative_tags.add_cumulative_tag(server, f'_advancedtags.{adv_tag_group_name}', cumulative_tag_data)

def test_cumulative_tag_get(server):
    # Get the cumulative tag
    cumulative_tag_path = f'_advancedtags.{adv_tag_group_name}.{cumulative_tag_name}'
    result = adv_tags.cumulative_tags.get_cumulative_tag(server, cumulative_tag_path)
    assert type(result) == dict
    assert result.get("common.ALLTYPES_NAME") == cumulative_tag_name

def test_cumulative_tag_modify(server):
    # Modify the cumulative tag
    cumulative_tag_path = f'_advancedtags.{adv_tag_group_name}.{cumulative_tag_name}'
    tag_data = {
        "common.ALLTYPES_DESCRIPTION": "Modified cumulative tag"
    }
    assert adv_tags.cumulative_tags.modify_cumulative_tag(server, cumulative_tag_path, tag_data, force=True)

def test_cumulative_tag_get_all(server):
    # Get all cumulative tags under the group
    result = adv_tags.cumulative_tags.get_all_cumulative_tags(server, f'_advancedtags.{adv_tag_group_name}')
    assert type(result) == list
    assert any(tag.get("common.ALLTYPES_NAME") == cumulative_tag_name for tag in result)

def test_cumulative_tag_del(server):
    # Delete the cumulative tag
    cumulative_tag_path = f'_advancedtags.{adv_tag_group_name}.{cumulative_tag_name}'
    assert adv_tags.cumulative_tags.del_cumulative_tag(server, cumulative_tag_path)

def test_minimum_tag_add(server):
    # Add a minimum tag to the root advanced tag plug-in
    assert adv_tags.min_tags.add_minimum_tag(server, f'_advancedtags', minimum_tag_data)

    testTag = {
        "common.ALLTYPES_NAME": "newMinimumTag",
        "common.ALLTYPES_DESCRIPTION": "",
        "advanced_tags.ENABLED": True,
        "advanced_tags.MINIMUM_TAG": "_System._Time_Hour",
        "advanced_tags.RUN_TAG": "_System._Time_Second"
    }
    minimum_tag_data.append(testTag)
    # Add a minimum tag to the advanced tag group
    assert adv_tags.min_tags.add_minimum_tag(server, f'_advancedtags.{adv_tag_group_name}', minimum_tag_data)

def test_minimum_tag_get(server):
    # Get the minimum tag
    minimum_tag_path = f'_advancedtags.{adv_tag_group_name}.{minimum_tag_name}'
    result = adv_tags.min_tags.get_minimum_tag(server, minimum_tag_path)
    assert type(result) == dict
    assert result.get("common.ALLTYPES_NAME") == minimum_tag_name

def test_minimum_tag_modify(server):
    # Modify the minimum tag
    minimum_tag_path = f'_advancedtags.{adv_tag_group_name}.{minimum_tag_name}'
    tag_data = {
        "common.ALLTYPES_DESCRIPTION": "Modified minimum tag"
    }
    assert adv_tags.min_tags.modify_minimum_tag(server, minimum_tag_path, tag_data, force=True)

def test_minimum_tag_get_all(server):
    # Get all minimum tags under the group
    result = adv_tags.min_tags.get_all_minimum_tags(server, f'_advancedtags.{adv_tag_group_name}')
    assert type(result) == list
    assert any(tag.get("common.ALLTYPES_NAME") == minimum_tag_name for tag in result)

def test_minimum_tag_del(server):
    # Delete the minimum tag
    minimum_tag_path = f'_advancedtags.{adv_tag_group_name}.{minimum_tag_name}'
    assert adv_tags.min_tags.del_minimum_tag(server, minimum_tag_path)

def test_maximum_tag_add(server):
    # Add a maximum tag to the root advanced tag plug-in
    assert adv_tags.max_tags.add_maximum_tag(server, f'_advancedtags', maximum_tag_data)

    testTag = {
        "common.ALLTYPES_NAME": "newMaximumTag",
        "common.ALLTYPES_DESCRIPTION": "",
        "advanced_tags.ENABLED": True,
        "advanced_tags.MAXIMUM_TAG": "_System._Time_Hour",
        "advanced_tags.RUN_TAG": "_System._Time_Second"
    }
    maximum_tag_data.append(testTag)
    # Add a maximum tag to the advanced tag group
    assert adv_tags.max_tags.add_maximum_tag(server, f'_advancedtags.{adv_tag_group_name}', maximum_tag_data)

def test_maximum_tag_get(server):
    # Get the maximum tag
    maximum_tag_path = f'_advancedtags.{adv_tag_group_name}.{maximum_tag_name}'
    result = adv_tags.max_tags.get_maximum_tag(server, maximum_tag_path)
    assert type(result) == dict
    assert result.get("common.ALLTYPES_NAME") == maximum_tag_name

def test_maximum_tag_modify(server):
    # Modify the maximum tag
    maximum_tag_path = f'_advancedtags.{adv_tag_group_name}.{maximum_tag_name}'
    tag_data = {
        "common.ALLTYPES_DESCRIPTION": "Modified maximum tag"
    }
    assert adv_tags.max_tags.modify_maximum_tag(server, maximum_tag_path, tag_data, force=True)

def test_maximum_tag_get_all(server):
    # Get all maximum tags under the group
    result = adv_tags.max_tags.get_all_maximum_tags(server, f'_advancedtags.{adv_tag_group_name}')
    assert type(result) == list
    assert any(tag.get("common.ALLTYPES_NAME") == maximum_tag_name for tag in result)

def test_maximum_tag_del(server):
    # Delete the maximum tag
    maximum_tag_path = f'_advancedtags.{adv_tag_group_name}.{maximum_tag_name}'
    assert adv_tags.max_tags.del_maximum_tag(server, maximum_tag_path)

def test_link_tag_add(server):
    # Add a link tag to the root advanced tag plug-in
    assert adv_tags.link_tags.add_link_tag(server, f'_advancedtags', link_tag_data)

    testTag = {
        "common.ALLTYPES_NAME": "newLinkTag",
        "common.ALLTYPES_DESCRIPTION": "",
        "advanced_tags.ENABLED": True,
        "advanced_tags.LINK_INPUT_TAG": "_System._Time_Hour",
        "advanced_tags.LINK_OUTPUT_TAG": f"{sim_ch_name}.{sim_dev_name}.{sim_tag_name}",
    }
    link_tag_data.append(testTag)
    # Add a link tag to the advanced tag group
    assert adv_tags.link_tags.add_link_tag(server, f'_advancedtags.{adv_tag_group_name}', link_tag_data)

def test_link_tag_get(server):
    # Get the link tag
    link_tag_path = f'_advancedtags.{adv_tag_group_name}.{link_tag_name}'
    result = adv_tags.link_tags.get_link_tag(server, link_tag_path)
    assert type(result) == dict
    assert result.get("common.ALLTYPES_NAME") == link_tag_name

def test_link_tag_modify(server):
    # Modify the link tag
    link_tag_path = f'_advancedtags.{adv_tag_group_name}.{link_tag_name}'
    tag_data = {
        "common.ALLTYPES_DESCRIPTION": "Modified link tag"
    }
    assert adv_tags.link_tags.modify_link_tag(server, link_tag_path, tag_data, force=True)

def test_link_tag_get_all(server):
    # Get all link tags under the group
    result = adv_tags.link_tags.get_all_link_tags(server, f'_advancedtags.{adv_tag_group_name}')
    assert type(result) == list
    assert any(tag.get("common.ALLTYPES_NAME") == link_tag_name for tag in result)

def test_link_tag_del(server):
    # Delete the link tag
    link_tag_path = f'_advancedtags.{adv_tag_group_name}.{link_tag_name}'
    assert adv_tags.link_tags.del_link_tag(server, link_tag_path)

def test_adv_tag_group_del(server):
    # Delete parent advanced tag group
    assert adv_tags.adv_tag_group.del_tag_group(server, f'_advancedtags.{adv_tag_group_name}')

