from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum

class AlertStatus(str, Enum):
    FAILED = "failed"
    RESOLVED = "resolved"

class Labels(BaseModel):
    alertname: str
    job: str
    severity: str
    instance: str
    team: str
    task_id: str
    dag_id: str

class Annotations(BaseModel):
    summary: str
    description: str
    runbook: HttpUrl

class AlertDetail(BaseModel):
    status: AlertStatus
    labels: Labels
    annotations: Annotations
    startsAt: datetime
    endsAt: datetime
    generatorURL: HttpUrl

class GroupLabels(BaseModel):
    alertname: str

class AlertManagerPayload(BaseModel):
    status: AlertStatus
    receiver: str
    alerts: List[AlertDetail]
    groupLabels: GroupLabels