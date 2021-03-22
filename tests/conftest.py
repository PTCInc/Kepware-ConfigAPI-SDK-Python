# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# Pytest config file

import pytest
import kepconfig

@pytest.fixture(scope="module")
def kepware_server():
    return kepconfig.connection.server(host = 'localhost', port = 57412, user = 'Administrator', pw = '', https = False)
    # return kepconfig.connection.server(host = 'localhost', port = 57413, user = 'Administrator', pw = 'Kepware400400400', https = False)