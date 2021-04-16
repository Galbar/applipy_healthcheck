[![pipeline status](https://gitlab.com/applipy/applipy_healthcheck/badges/master/pipeline.svg)](https://gitlab.com/applipy/applipy_healthcheck/-/pipelines?scope=branches&ref=master)
[![coverage report](https://gitlab.com/applipy/applipy_healthcheck/badges/master/coverage.svg)](https://gitlab.com/applipy/applipy_healthcheck/-/graphs/master/charts)
[![PyPI Status](https://img.shields.io/pypi/status/applipy-healthcheck.svg)](https://pypi.org/project/applipy-healthcheck/)
[![PyPI Version](https://img.shields.io/pypi/v/applipy-healthcheck.svg)](https://pypi.org/project/applipy-healthcheck/)
[![PyPI Python](https://img.shields.io/pypi/pyversions/applipy-healthcheck.svg)](https://pypi.org/project/applipy-healthcheck/)
[![PyPI License](https://img.shields.io/pypi/l/applipy-healthcheck.svg)](https://pypi.org/project/applipy-healthcheck/)
[![PyPI Format](https://img.shields.io/pypi/format/applipy-healthcheck.svg)](https://pypi.org/project/applipy-healthcheck/)

# Applipy HealthCheck Metrics

    pip install applipy_healthcheck

Exposes the health status of the applipy application through an HTTP endpoint with path `/health`.

## Usage

Add the `applipy_healthcheck.HealthCheckModule` to your application. Optionally,
define through which http server to expose the `/health` endpoint, if no name
is given it defaults to the anonymous server:

```yaml
# dev.yaml

app:
    name: demo
    modules:
        - applipy_healthcheck.HealthCheckModule

http.servers:
- name: internal
  host: 0.0.0.0
  port: 8080

healthcheck.server_name: internal
```

To run this test just install `applipy_healthcheck` and `pyyaml` and run the applipy application:

```bash
pip install applipy_healthcheck pyyaml
python -m applipy
```

You can now query [http://0.0.0.0:8080/health](http://0.0.0.0:8080/health)
and you should see `OK` being returned.

## Custom health checks

`applipy_healthcheck` exposes the `HealthChecker` interface. You can implement
your own and the health check endpoint will use it to determine the health of
the system.

### Example

#### Full healthcheck module config

All keys and their default values:

```yaml
healthcheck:
  server_name: null
  verbose: false
```

#### Usage with custom HealthChecker

```python
# mymodule.py

from applipy import Module
from applipy_healthcheck import HealthChecker


class MyHealthChecker(HealthChecker):

    async def check(self):
        is_healthy = True
        status_message = 'All OK'
        return is_healthy, status_message


class MyModule(Module):
    def configure(self, bind, register):
        bind(HealthChecker, MyHealthChecker)

    @classmethod
    def depends_on(cls):
        return HealthCheckModule,
```

```yaml
# dev.yaml

app:
  name: test
  modules: [mymodule.MyModule]

http.servers:
- host: 0.0.0.0
  port: 8080
```
