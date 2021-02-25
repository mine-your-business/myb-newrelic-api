import requests
import json
from enum import Enum
from urllib.parse import urlencode

class NewRelicAlertsChannelsApi:

    def __init__(
            self, 
            api_key, 
            api_url='https://api.newrelic.com', 
            verbose=False
    ):
        self._api_key = api_key
        self._api_url = api_url
        self._verbose = verbose

    def _request(self, method, url, headers={}, body=None, params=None):
        api_url = self._api_url + url

        if self._verbose:
            print(method, api_url)

        headers['Api-Key'] = self._api_key
        headers['Accept'] = 'application/json'

        s = requests.Session()
        response = s.request(method, api_url, data=body, params=params, headers=headers)

        if response.status_code >= 200 and response.status_code < 300:
            return response.json()
        elif response.content:
            raise Exception(str(response.status_code) + ': ' + response.reason + ': ' + str(response.content))
        else:
            raise Exception(str(response.status_code) + ': ' + response.reason)


    def list_channels(self):
        return self._request(
            'GET', 
            '/v2/alerts_channels.json'
        )
        
    # channel_type must be a string matching one of the following:
    # 
    #   User
    #   Email
    #   OpsGenie
    #   PagerDuty
    #   Slack
    #   VictorOps
    #   Webhook
    #   xMatters
    #
    def create_channel(self, name, channel_type, configuration):
        headers = {
            'Content-Type': 'application/json'
        }
        body = {
            'channel': {
                'name': name,
                'type': channel_type,
                'configuration': configuration
            }
        }
        return self._request(
            'POST', 
            '/v2/alerts_channels.json',
            headers=headers,
            body=json.dumps(body)
        )

    def delete_channel(self, channel_id):
        return self._request(
            'DELETE', 
            f'/v2/alerts_channels/{channel_id}.json'
        )

    def update_channel_association(self, channel_id, policy_id):
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            'channel_ids': channel_id,
            'policy_id': policy_id
        }
        return self._request(
            'PUT', 
            '/v2/alerts_policy_channels.json',
            headers=headers,
            params=urlencode(params, True)
        )
    
    def delete_channel_association(self, channel_id, policy_id):
        params = {
            'channel_id': channel_id,
            'policy_id': policy_id
        }
        return self._request(
            'DELETE', 
            f'/v2/alerts_policy_channels.json',
            params=urlencode(params, True)
        )
