import requests
import gzip, json
import copy

# NRQL Query Example: "SELECT count(*) FROM Transaction SINCE 1 minute ago"
class NewRelicInsightsApi:

    def __init__(
            self, 
            account_id, 
            api_key, 
            query_api_url='https://insights-api.newrelic.com', 
            insert_api_url='https://insights-collector.newrelic.com',
            verbose=False
    ):
        self.account_id = account_id
        self._api_key = api_key
        self._query_api_url = query_api_url
        self._insert_api_url = insert_api_url
        self._verbose = verbose

    def _request(self, method, api_url, path, headers, body=None, params=None):
        url = api_url + path

        if self._verbose:
            print(method, url)

        s = requests.Session()
        response = s.request(method, url, data=body, params=params, headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.content:
            raise Exception(str(response.status_code) + ": " + response.reason + ": " + str(response.content))
        else:
            raise Exception(str(response.status_code) + ": " + response.reason)


    def query(self, nrql_query):
        params = {
            'nrql': nrql_query
        }
        headers = {
            'Accept': 'application/json',
            'X-Query-Key': self._api_key
        }
        return self._request(
            'GET', 
            self._query_api_url, 
            f'/v1/accounts/{self.account_id}/query', 
            headers, 
            params=params
        )
        
    def insert_event(self, event_type, event, flatten=False, join_lists=False):
        return self.insert_events(event_type, [event])

    def insert_events(self, event_type, events, flatten=False, join_lists=False):
        headers = {
            'Content-Type': 'application/json',
            'X-Insert-Key': self._api_key,
            'Content-Encoding': 'gzip'
        }
        payload = []
        for event in events:
            if flatten:
                event = self._flatten_dict(event, join_lists=join_lists)
            event_dict = event if type(event) == dict else event.__dict__ if hasattr(event, '__dict__') else None
            if event_dict:
                payload_event = event_dict.copy()
                payload_event['eventType'] = event_type
                payload.append(payload_event)

        body = gzip.compress(str.encode(json.dumps(payload), 'utf-8'))
        return self._request(
            'POST', 
            self._insert_api_url, 
            f'/v1/accounts/{self.account_id}/events', 
            headers, 
            body=body
        )

    def _flatten_dict(self, dict_to_flatten, parent_key='', separator='_', join_lists=False):
        items = []
        for key, value in dict_to_flatten.items():
            new_key = parent_key + separator + key if parent_key else key
            if isinstance(value, collections.MutableMapping):
                items.extend(self._flatten_dict(value, new_key, separator, join_lists).items())
            elif join_lists and isinstance(value, list) and len(value) > 0 and not isinstance(value[0], collections.MutableMapping):
                items.append((new_key, ','.join(value)))
            else:
                items.append((new_key, value))
        return dict(items)
       