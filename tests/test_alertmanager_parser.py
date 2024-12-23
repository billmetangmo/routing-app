import pytest
from app.parsers.alertmanager_parser import AlertManagerParser
from pydantic import ValidationError


@pytest.fixture
def parser():
    return AlertManagerParser()

@pytest.fixture
def valid_payload():
    return {
        "status": "failed",
        "receiver": "airflow-alerts",
        "alerts": [
            {
                "status": "failed",
                "labels": {
                    "alertname": "AirflowJobFailure",
                    "job": "airflow",
                    "instance": "airflow-instance-01",
                    "team": "data-engineering",
                    "severity": "critical",
                    "task_id": "example_task",
                    "dag_id": "example_dag"
                },
                "annotations": {
                    "summary": "Airflow job has failed",
                    "description": "The Airflow job 'example_task' in DAG 'example_dag' has failed.",
                    "runbook": "https://yourcompany.runbooks/airflow-job-failure"
                },
                "startsAt": "2024-12-05T17:00:00Z",
                "endsAt": "0001-01-01T00:00:00Z",
                "generatorURL": "http://prometheus.example.com/graph?g0.expr=rate%28airflow_task_failures%5B5m%5D%29+%3E+0&g0.tab=1"
            }
        ],
        "groupLabels": {
            "alertname": "AirflowJobFailure"
        }
    }

@pytest.fixture
def invalid_payload():
    return  {
        "receiver": "airflow-alerts",
        "alerts": []
    }

def test_parse_valid_payload(parser,valid_payload):
    alerts = parser.parse(valid_payload)
    assert len(alerts) == 1
    alert = alerts[0]
    assert alert.status == "failed"
    assert alert.labels.alertname == "AirflowJobFailure"
    assert alert.labels.job == "airflow"
    assert alert.labels.task_id == "example_task"
    assert alert.annotations.summary == "Airflow job has failed"
    assert alert.annotations.description.startswith("The Airflow job")
    assert alert.startsAt.isoformat() == "2024-12-05T17:00:00+00:00"
    assert alert.endsAt.year == 1


def test_parse_invalid_payload(parser,invalid_payload):
    with pytest.raises(ValidationError):
        parser.parse(invalid_payload)