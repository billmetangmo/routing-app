# AlertManager Router

A Python FastAPI service that routes AlertManager alerts to different channels based on team and severity.

## Features

- Receives webhook alerts from AlertManager
- Routes alerts to specific Slack channels based on team and severity
- Customizable message formatting
- Extensible channel system (currently supports Slack)
- Input validation using Pydantic models

## Requirements

- Python 3.13+
- Dependencies listed in [requirements.txt](requirements.txt):
  - FastAPI
  - Uvicorn
  - Pydantic
  - aiohttp
  - pytest
  - pytest-asyncio
  - httpx

## Installation

1. Clone the repository
2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration

The routing rules are configured in main.py.
Example configuration:

```
routing_rules = {
    "data-engineering": {
        "critical": SlackChannel("webhook_url_1"),
        "warning": SlackChannel("webhook_url_2")
    }
}
```

## Usage

1. Start the server:

```bash
fastapi dev app/main.py
```

2. Send alerts to the webhook endpoint:

```bash
POST http://localhost:8000/webhook
```

Example of valid payload:

```
{
  "status": "failed",
  "receiver": "airflow-alerts",
  "alerts": [
    {
      "status": "failed",
      "labels": {
        "alertname": "AirflowJobFailure",
        "job": "airflow",
        "severity": "critical",
        "instance": "airflow-instance-01",
        "team": "data-engineering",
        "task_id": "example_task",
        "dag_id": "example_dag"
      },
      "annotations": {
        "summary": "Airflow job has failed",
        "description": "The Airflow job 'example_task' in DAG 'example_dag' has failed.",
        "runbook": "https://yourcompany.runbooks/airflow-job-failure"
      }
    }
  ]
}
```

## Project structure

```
app/
├── channels/         # Channel implementations (Slack, etc.)
├── formatters/       # Message formatting
├── models/          # Pydantic models
├── parsers/         # Alert parsing
├── router/          # Alert routing logic
└── main.py          # FastAPI application
```

## Testing

Run the test suite using pytest:

```
pytest tests/
```
