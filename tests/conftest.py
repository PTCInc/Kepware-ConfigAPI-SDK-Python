import pytest
import kepconfig

@pytest.fixture(scope="module")
def kepware_server():
    return kepconfig.connection.server(host = 'localhost', port = 57412, user = 'Administrator', pw = '', https = False)