import pytest
# from newrelic import NewRelicInsightsApi


# TODO - This needs tests!
@pytest.fixture(scope='module')
def client():
    return None
    # return NewRelicInsightsApi(account_id, api_key)


@pytest.mark.usefixtures('client')
class TestClient(object):

    def test(self, client):
        # TODO!
        assert True
