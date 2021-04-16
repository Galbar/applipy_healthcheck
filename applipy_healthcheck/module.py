from applipy import Module, Config
from applipy_inject import with_names
from applipy_http import Api, Endpoint, HttpModule, PathFormatter
from applipy_healthcheck.endpoint import HealthCheckEndpoint


class HealthCheckModule(Module):

    def __init__(self, config: Config) -> None:
        self._config = config.get('healthcheck', Config({}))

    def configure(self, bind, register) -> None:
        bind(Endpoint, HealthCheckEndpoint, name='healthcheck')
        bind(PathFormatter, name='healthcheck')
        bind(with_names(Api, 'healthcheck'),
             name=self._config.get('server_name', None))

    @classmethod
    def depends_on(cls):
        return HttpModule,
