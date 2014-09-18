from __future__ import absolute_import

from subprocess import check_output

from ..core import Provider, AutoReply

__all__ = ['simple_shell_instrument', 'simple_shell_command',
           'sensors_command_temp']


class simple_shell_instrument(Provider):
    def __init__(self, name, *args):
        self.name = name
        self.endpoints = {}

    def add_endpoint(self, endpoint):
        self.endpoints[endpoint.name] = endpoint
        endpoint.set_provider(self)

    def list_endpoints(self):
        return self.endpoints.keys()

    def endpoint(self, endpoint):
        if endpoint in self.list_endpoints():
            return self.endpoints[endpoint]

    def send_sync(self, to_send):
        raw_result = None
        if to_send:
            raw_result = check_output(to_send)
        return raw_result


class simple_shell_command(AutoReply):
    def __init__(self, name, on_get=None, on_set=None):
        self.name = name
        self._provider = None
        self._on_get = on_get
        self._on_set = on_set

    def on_get(self):
        result = self._provider.send_sync(self._on_get)
        return result

    def on_set(self, value):
        result = self._provider.send_sync(self._on_set.format(value))
        return result

    def on_config(self):
        raise NotImplementedError

    def provider(self):
        return self._provider

    def set_provider(self, provider):
        self._provider = provider


class sensors_command_temp(AutoReply):
    def __init__(self, name, core=0):  # , on_get='sensors', on_set=None):
        self.name = name
        self._provider = None
        self._on_get = ['sensors']  # on_get
        self._on_set = None  # on_set
        self._core = core

    def on_get(self):
        result = None
        res_lines = self._provider.send_sync(self._on_get).split('\n')
        for line in res_lines:
            if line.startswith('Core {}:'.format(self._core)):
                result = line.split()[2].replace('\xc2\xb0', ' ')
        return result

    def on_set(self, value):
        result = self._provider.send_sync(self._on_set.format(value))
        return result

    def on_config(self):
        raise NotImplementedError

    def provider(self):
        return self._provider

    def set_provider(self, provider):
        self._provider = provider