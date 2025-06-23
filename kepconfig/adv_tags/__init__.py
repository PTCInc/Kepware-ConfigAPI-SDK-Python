# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. and/or all its affiliates. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

r"""`adv_tags` module provides support for Kepware's Advanced Tags plug-in 
specific objects within the Kepware Configuration API
"""

from . import adv_tag_group, average_tags, derived_tags, complex_tags, cumulative_tags, min_tags, max_tags, link_tags
ADV_TAGS_ROOT = '/project/_advancedtags'

def adv_tag_path_split(path: str, *, isItem=False) -> dict:
    '''Used to split the standard Kepware address decimal notation into a dict that contains the 
    advanced tag path components.

    :param path: standard Kepware address in decimal notation ("_advancedtags.tg1.tg2.tg3")
    :return: dict that contains the "adv_tag_root" and "tag_path"
    :rtype: dict

    Ex: path = "_advancedtags.tg1.tg2.tg3"

    return = {'adv_tag_root': '_advancedtags', 'tag_path': ['tg1','tg2','tg3']}

    Ex: path = "_advancedtags.ch1.dev1"

    return = {'adv_tag_root': '_advancedtags', 'tag_path': ['ch1','dev1']}
    '''
    path_list = path.split('.', 2)
    path_obj = {}
    for x in range(0, len(path_list)):
        if x == 0:
            path_obj['adv_tag_root'] = path_list[0]
        elif x == 1:
            if isItem:
                path_obj['tag_path'] = path_list[1:-1]
                path_obj['item'] = path_list[-1]
            else:
                path_obj['tag_path'] = path_list[1:]
    return path_obj

def _create_adv_tags_base_url(base_url, path_obj):
    '''Creates url object for the "path_obj" which provides the adv tags tag group structure of Kepware's project tree. Used 
    to build a part of Kepware Configuration API URL structure
    
    Returns the advanced tag group specific url when a value is passed as the tag group name.
    '''
    url = base_url + ADV_TAGS_ROOT
    url += adv_tag_group._create_adv_tags_group_url(path_obj)

    return url