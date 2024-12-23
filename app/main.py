from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from rich.console import Console
from app.parsers.alertmanager_parser import AlertManagerParser
from app.router.alert_router import AlertRouter, MappingNotFoundError
from app.channels.slack_channel import SlackChannel
from app.formatters.message_formatter import MessageFormatter
from pydantic import ValidationError


app = FastAPI()
console = Console()

# Configuration
routing_rules = {
    "data-engineering": {
        "critical": SlackChannel("webhook_url_1"),
        "warning": SlackChannel("webhook_url_2")
    }
}

parser = AlertManagerParser()
formatter = MessageFormatter()
router = AlertRouter(routing_rules, formatter)

@app.post("/webhook")
async def receive_alert(payload: dict):
    try:
        alerts = parser.parse(payload)
        for alert in alerts:
            await router.route_alert(alert)
        return {"status": "success"}
    except ValidationError as e:
        raise HTTPException(status_code=403, detail="Invalid json with error: "+str(e))
    except MappingNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        console.print_exception(show_locals=True)
        raise HTTPException(status_code=500, detail="Unexpected error: "+str(e))