from abc import ABC, abstractmethod
from app.models.alert import AlertManagerPayload

class BaseChannel(ABC):
    @abstractmethod
    async def send_message(self, alert: AlertManagerPayload, formatted_message: str) -> bool:
        pass