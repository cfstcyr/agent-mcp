from collections.abc import Callable
from typing import Annotated, Any, Self

from fastapi import Depends, FastAPI, Request


class Container:
    _attr_name: str = "container"
    _services: dict[type, object] = {}

    def setup_app(self, app: FastAPI) -> Self:
        if hasattr(app.state, self._attr_name):
            raise Exception("Container already set up")
        setattr(app.state, self._attr_name, self)
        return self
    
    def register(self, service: object) -> Self:
        if not hasattr(service, "__class__"):
            raise Exception("Service must be a class instance")
        if service.__class__ in self._services:
            raise Exception(f"Service {service.__class__} already registered")
        self._services[service.__class__] = service
        return self
    
    def get[T: object](self, service_type: type[T]) -> T:
        service = self._services.get(service_type)
        if service is None:
            raise Exception(f"Service {service_type} not found in container")
        return service  # type: ignore
    
    @classmethod
    def depends_on[T: object](cls, service_type: type[T]) -> Annotated[T, Callable[[Request], T]]:
        def _get_service(request: Request):
            if not hasattr(request.app.state, cls._attr_name):
                raise Exception("Container not set up")
            container: Self = getattr(request.app.state, cls._attr_name)

            if not isinstance(container, cls):
                raise Exception("Container not set up")

            return container.get(service_type)

        return Depends(_get_service)
