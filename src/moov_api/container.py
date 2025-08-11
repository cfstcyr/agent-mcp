from typing import Self

from fastapi import FastAPI, Request


class Container:
    _attr_name: str = "container"
    _services: dict[str, object] = {}

    def setup_app(self, app: FastAPI) -> Self:
        if hasattr(app.state, self._attr_name):
            raise Exception("Container already set up")
        setattr(app.state, self._attr_name, self)
        return self

    def register(self, name: str, service: object) -> Self:
        self._services[name] = service
        return self

    def get(self, name: str):
        if name not in self._services:
            raise Exception(f"Service {name} not registered")
        return self._services[name]

    @classmethod
    def depend_on(cls, name: str):
        def _get_service(request: Request):
            if not hasattr(request.app.state, cls._attr_name):
                raise Exception("Container not set up")
            container: Self = getattr(request.app.state, cls._attr_name)

            if not isinstance(container, cls):
                raise Exception("Container not set up")

            return container.get(name)

        return _get_service
