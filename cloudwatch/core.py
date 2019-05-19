import boto3
from json import loads


class CloudwatchClient:
    def __init__(self):
        self.client = boto3.client("cloudwatch")

    def getAlarm(self, alarm_state="ALARM"):
        alarm_list = []
        alarm_list_json = []
        response = self.client.describe_alarms(StateValue=alarm_state)
        alarm_list_json += response["MetricAlarms"]
        while response.get("NextToken", False):
            response = self.client.describe_alarms(
                StateValue=alarm_state, NextToken=response["NextToken"]
            )
            alarm_list_json += response["MetricAlarms"]
        for alarm in alarm_list_json:
            alarm_list.append(
                dict({"Alarm": alarm["AlarmName"], "StateReason": alarm["StateReason"]})
            )
        return alarm_list
