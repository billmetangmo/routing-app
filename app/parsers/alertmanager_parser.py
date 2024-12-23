from typing import List
from app.models.alert import AlertManagerPayload, AlertDetail

class AlertManagerParser:
    def parse(self, payload: dict) -> List[AlertDetail]:
        alert_payload = AlertManagerPayload.model_validate(payload)
        return alert_payload.alerts