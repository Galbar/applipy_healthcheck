from typing import (
    Optional,
    Tuple,
)


class HealthChecker:

    async def check(self) -> Tuple[bool, Optional[str]]:
        raise NotImplementedError()
