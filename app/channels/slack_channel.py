from app.channels.base_channel import BaseChannel
from app.models.alert import AlertManagerPayload

class SlackChannel(BaseChannel):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    async def send_message(self, alert: AlertManagerPayload, formatted_message: str) -> bool:
        print(f"Sending message to Slack: {formatted_message}")
        return True