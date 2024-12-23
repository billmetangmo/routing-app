import pytest
from app.router.alert_router import AlertRouter, MappingNotFoundError
from app.channels.slack_channel import SlackChannel
from app.formatters.message_formatter import MessageFormatter
from app.models.alert import AlertDetail, Labels, Annotations
from datetime import datetime
from pydantic import HttpUrl

@pytest.fixture
def valid_alert():
    return AlertDetail(
        status="failed",
        labels=Labels(
            alertname="AirflowJobFailure",
            job="airflow",
            severity="critical",
            instance="airflow-instance-01",
            team="data-engineering",
            task_id="example_task",
            dag_id="example_dag"
        ),
        annotations=Annotations(
            summary="Airflow job has failed",
            description="The Airflow job 'example_task' in DAG 'example_dag' has failed.",
            runbook=HttpUrl("https://yourcompany.runbooks/airflow-job-failure")
        ),
        startsAt=datetime(2024, 12, 5, 17, 0, 0),
        endsAt=datetime(1, 1, 1, 0, 0, 0),
        generatorURL=HttpUrl("http://prometheus.example.com/graph?g0.expr=rate%28airflow_task_failures%5B5m%5D%29+%3E+0&g0.tab=1")
    )

@pytest.fixture
def invalid_alert():
    return AlertDetail(
        status="failed",
        labels=Labels(
            alertname="AirflowJobFailure",
            job="airflow",
            severity="critical",
            instance="airflow-instance-01",
            team="devops",
            task_id="example_task",
            dag_id="example_dag"
        ),
        annotations=Annotations(
            summary="Airflow job has failed",
            description="The Airflow job 'example_task' in DAG 'example_dag' has failed.",
            runbook=HttpUrl("https://yourcompany.runbooks/airflow-job-failure")
        ),
        startsAt=datetime(2024, 12, 5, 17, 0, 0),
        endsAt=datetime(1, 1, 1, 0, 0, 0),
        generatorURL=HttpUrl("http://prometheus.example.com/graph?g0.expr=rate%28airflow_task_failures%5B5m%5D%29+%3E+0&g0.tab=1")
    )

@pytest.fixture
def router():
    routing_rules = {
        "data-engineering": {
            "critical": SlackChannel("webhook_url_1"),
            "warning": SlackChannel("webhook_url_2")
        }
    }
    formatter = MessageFormatter()
    return AlertRouter(routing_rules, formatter)

@pytest.mark.asyncio

async def test_valid_team(router, valid_alert):
    result = await router.route_alert(valid_alert)
    assert result is True

@pytest.mark.asyncio

async def test_invalid_team(router, invalid_alert):
    with pytest.raises(MappingNotFoundError):
        await router.route_alert(invalid_alert)