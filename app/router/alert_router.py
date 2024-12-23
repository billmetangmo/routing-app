from typing import Dict, Type
from app.channels.base_channel import BaseChannel
from app.models.alert import AlertDetail
from app.formatters.message_formatter import MessageFormatter

class MappingNotFoundError(ValueError):
    def __init__(self, team: str, severity: str):
        self.message = f"No mapping found for team '{team}' and severity '{severity}'"
        super().__init__(self.message)

class AlertRouter:
    def __init__(self, routing_rules: Dict[str, Dict[str, BaseChannel]],
                 formatter: MessageFormatter):
        self.routing_rules = routing_rules
        self.formatter = formatter

    async def route_alert(self, alert: AlertDetail) -> bool:
        team = alert.labels.team
        severity = alert.labels.severity

        if team not in self.routing_rules or severity not in self.routing_rules[team]:
            raise MappingNotFoundError(team, severity)

        channel = self.routing_rules[team][severity]
        formatted_message = self.formatter.format_alert(alert)

        return await channel.send_message(alert, formatted_message)