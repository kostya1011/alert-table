#! /usr/local/bin/python3


import cloudwatch
from flask import Flask, request, jsonify

app = Flask(__name__)

app.debug = True

client = cloudwatch.CloudwatchClient()


@app.route("/")
def health_check():
    return "The alert-table datasource is healthy."


@app.route("/search", methods=["POST"])
def search():
    return jsonify(
        ["cloudwatch_green", "cloudwatch_red", "cloudwatch_insufficient_data"]
    )


@app.route("/query", methods=["POST"])
def query():
    if request.get_json()["targets"][0]["target"] == "cloudwatch_red":
        alarms = client.getAlarm()
        return table_cloudwatch(alarms)
    elif request.get_json()["targets"][0]["target"] == "cloudwatch_insufficient_data":
        alarms = client.getAlarm(alarm_state="INSUFFICIENT_DATA")
        return table_cloudwatch(alarms)
    elif request.get_json()["targets"][0]["target"] == "cloudwatch_green":
        alarms = client.getAlarm(alarm_state="OK")
        return table_cloudwatch(alarms)


def table_cloudwatch(alarms):
    rows = []
    for alarm in alarms:
        rows.append([alarm["Alarm"], alarm["StateReason"]])
    data = [
        {
            "columns": [
                {"text": "Alert", "type": "string"},
                {"text": "StateReason", "type": "string"},
            ],
            "rows": rows,
            "type": "table",
        }
    ]
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
