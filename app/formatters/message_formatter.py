from app.models.alert import AlertDetail

class MessageFormatter:
    def format_alert(self, alert: AlertDetail) -> str:
        return (
            f"*{alert.labels.alertname}*: {alert.annotations.summary} \n"
            f"Severity: {alert.labels.severity}\n"
            f"Description: {alert.annotations.description}\n"
            f"Runbook: {alert.annotations.runbook}"
        )