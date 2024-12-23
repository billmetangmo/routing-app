from app.models.alert import AlertDetail, Labels, Annotations
from app.formatters.message_formatter import MessageFormatter
from datetime import datetime
from pydantic import HttpUrl

def test_format_alert():
    formatter = MessageFormatter()
    alert = AlertDetail(
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
    formatted_message = formatter.format_alert(alert)
    assert "*AirflowJobFailure*" in formatted_message
    assert "Severity: critical" in formatted_message
    assert "Description: The Airflow job 'example_task' in DAG 'example_dag' has failed." in formatted_message
    assert "Runbook: https://yourcompany.runbooks/airflow-job-failure" in formatted_message