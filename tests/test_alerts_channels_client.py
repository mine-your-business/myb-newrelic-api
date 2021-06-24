import pytest
# from newrelic import NewRelicAlertsChannelsApi


# TODO - This needs tests!
@pytest.fixture(scope='module')
def client():
    return None
    # return NewRelicAlertsChannelsApi(api_key)


@pytest.mark.usefixtures('client')
class TestClient(object):

    def test(self, client):
        # TODO!
        assert True
