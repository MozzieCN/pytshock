import json

import requests

from .cache import Cache
from .exception import *


class Api(object):
    def __init__(self, username: str, password: str, host_ip: str, host_port: str, token_cache: Cache):
        self.token = token_cache.get_token(self.host_ip, self.host_port)
        self.username = username
        self.password = password
        self.host_ip = host_ip
        self.host_port = host_port
        self._cache = token_cache
        self.root_url = 'http://{}:{}'.format(self.host_ip, self.host_port)

    @property
    def current_token(self):
        return self.token
        # if self._is_current_token_valid():
        #     return self.token
        # else:
        #     self.token = self._create_token()
        #     return self.token

    def _create_token(self):
        # print('{}/token/create?username={}&password={}'.format(self.root_url, self.username, self.password))
        response = requests.get(
            '{}/token/create?username={}&password={}'.format(self.root_url, self.username, self.password))
        if response.status_code == 200:
            token_data = json.loads(response.text)
            if token_data.get('status', '403') == '200':
                self.token = token_data.get('token')
                self._cache.save_token(self.host_ip, self.host_port, self.token)
                return
            else:
                raise Exception('Create token error: server return {}'.format(token_data))
        raise Exception('Server return code [{}] error'.format(response.status_code))

    def _is_current_token_valid(self):
        if self.token:
            response = requests.get('{}/tokentest?token={}'.format(self.root_url, self.token))
            if response.status_code == 200:
                token_data = json.loads(response.text)
                if token_data.get('status', '403') == '200':
                    return True
        return False

    def send_request(self, endpoint, data=None, append_token=True, **kwargs):
        data = data or {}
        if append_token:
            if not self.current_token:
                self._create_token()
            data.setdefault('token', self.current_token)
        from urllib.parse import urlencode
        querystring = urlencode(data)
        request_url = '{base_url}{endpoint}?{querystring}'.format(
            base_url=self.root_url,
            endpoint=endpoint,
            querystring=querystring
        )
        response = requests.get(request_url)
        if response.status_code == 200:
            json_data = response.json()

            status = json_data.pop('status', '403')
            if status == '200':
                return json_data
            elif status == '401':
                retry = kwargs.pop('retry', True)
                if retry:
                    self._create_token()
                    self.send_request(endpoint, data, append_token, retry=False)
                else:
                    raise NoPermissionException()
            else:
                retry = kwargs.pop('retry', True)
                if retry:
                    self._create_token()
                    self.send_request(endpoint, data, append_token, retry=False)
                else:
                    raise ParamException()
        else:
            raise ServerException()

    def get(self, url, jsonifty=True):

        real_url = '{}{}?token={}'.format(self.root_url, url, self.current_token)
        response = requests.get(real_url)
        if response.status_code == 200:
            return json.loads(response.text) if jsonifty else response.text
        raise Exception('Server status code not 200. return : {}'.format(response.status_code))
