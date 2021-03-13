from asyncio import gather
from typing import List

from aiohttp import web
from applipy import Config
from applipy_http import (
    Context,
    Endpoint,
)

from applipy_healthcheck.healthchecker import HealthChecker


class HealthCheckEndpoint(Endpoint):

    _checkers: List[HealthChecker]
    _verbose: bool

    def __init__(self, checkers: List[HealthChecker], config: Config) -> None:
        self._checkers = checkers
        self._verbose = config.get('healthcheck.verbose', False)

    async def get(self, request: web.Request, context: Context) -> web.StreamResponse:

        statuses = await gather(*(c.check() for c in self._checkers))
        ok = all(ok for ok, _ in statuses)
        body = 'OK' if ok else 'BAD'
        if self._verbose:
            body += '\n---\n'
            body += '\n'.join(c.__class__.__name__ + ': ' + msg for c, (_, msg) in zip(self._checkers, statuses))
        return web.Response(body=body)

    def path(self) -> str:
        return '/health'
