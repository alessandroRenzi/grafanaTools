# ============================================================================================
# COSTRUTTORE REGOLE LIVENESS & HTTP RESPONSE CODE (JMX)
# ============================================================================================

def build_liveness_payload(client, folder_uid, datasource_uid):
    target_url = f"https://{client}.datalitecloud.it/{client}/jsp/debug.jsp"
    return {
        "title": f"{client} http response",
        "ruleGroup": "liveness",
        "folderUID": folder_uid,
        "condition": "D",
        "noDataState": "NoData",
        "execErrState": "Error",
        "for": "1m",
        "labels": {
            "client": client,
            "type": "liveness"
        },
        "annotations": {
            "summary": f"Il client {client} non risponde alla verifica di liveness"
        },
        "data": [
            {
                "refId": "A",
                "queryType": "",
                "relativeTimeRange": {"from": 300, "to": 0},
                "datasourceUid": datasource_uid,
                "model": {
                    "adhocFilters": [],
                    "alias": "",
                    "datasource": {"type": "influxdb", "uid": datasource_uid},
                    "groupBy": [
                        {"params": ["$__interval"], "type": "time"},
                        {"params": ["null"], "type": "fill"}
                    ],
                    "hide": False,
                    "intervalMs": 1000,
                    "maxDataPoints": 43200,
                    "measurement": "http_response",
                    "orderByTime": "ASC",
                    "policy": "one_week",
                    "query": "",
                    "refId": "A",
                    "resultFormat": "time_series",
                    "select": [[
                        {"params": ["http_response_code"], "type": "field"},
                        {"params": [], "type": "last"}
                    ]],
                    "slimit": "",
                    "tags": [{
                        "key": "server::tag",
                        "operator": "=",
                        "value": target_url
                    }],
                    "tz": ""
                }
            },
            {
                "refId": "D",
                "queryType": "",
                "relativeTimeRange": {"from": 600, "to": 0},
                "datasourceUid": "__expr__",
                "model": {
                    "conditions": [{
                        "evaluator": {"params": [399, 0], "type": "gt"},
                        "operator": {"type": "and"},
                        "query": {"params": ["A"]},
                        "reducer": {"params": [], "type": "last"},
                        "type": "query"
                    }],
                    "datasource": {"name": "Expression", "type": "__expr__", "uid": "__expr__"},
                    "expression": "",
                    "intervalMs": 1000,
                    "maxDataPoints": 43200,
                    "refId": "D",
                    "type": "classic_conditions"
                }
            }
        ]
    }

def build_liveness_error_code_payload(client, folder_uid, datasource_uid):
    target_url = f"https://{client}.datalitecloud.it/{client}/jsp/debug.jsp"
    return {
        "title": f"{client} https response code",
        "folderUID": folder_uid,
        "ruleGroup": "liveness",
        "condition": "D",
        "noDataState": "NoData",
        "execErrState": "Error",
        "for": "1m",
        "labels": {
            "client": client,
            "type": "liveness"
        },
        "annotations": {
            "summary": f"Il client {client} risponde con errore (Codice: {{{{ $values.B.Value }}}})"
        },
        "data": [
            {
                "refId": "B",
                "queryType": "",
                "relativeTimeRange": {"from": 21600, "to": 0},
                "datasourceUid": datasource_uid,
                "model": {
                    "adhocFilters": [],
                    "alias": "",
                    "datasource": {
                        "type": "influxdb",
                        "uid": datasource_uid
                    },
                    "groupBy": [
                        {"params": ["$__interval"], "type": "time"},
                        {"params": ["null"], "type": "fill"}
                    ],
                    "hide": False,
                    "intervalMs": 1000,
                    "limit": "",
                    "maxDataPoints": 43200,
                    "measurement": "http_response",
                    "orderByTime": "ASC",
                    "policy": "one_week",
                    "query": "",
                    "refId": "B",
                    "resultFormat": "time_series",
                    "select": [
                        [
                            {"params": ["result_code"], "type": "field"},
                            {"params": [], "type": "last"}
                        ]
                    ],
                    "slimit": "",
                    "tags": [
                        {
                            "key": "server::tag",
                            "operator": "=",
                            "value": target_url
                        }
                    ],
                    "tz": ""
                }
            },
            {
                "refId": "D",
                "queryType": "",
                "relativeTimeRange": {"from": 600, "to": 0},
                "datasourceUid": "__expr__",
                "model": {
                    "conditions": [
                        {
                            "evaluator": {"params": [0, 0], "type": "gt"},
                            "operator": {"type": "and"},
                            "query": {"params": ["B"]},
                            "reducer": {"params": [], "type": "last"},
                            "type": "query"
                        }
                    ],
                    "datasource": {
                        "name": "Expression",
                        "type": "__expr__",
                        "uid": "__expr__"
                    },
                    "expression": "",
                    "intervalMs": 1000,
                    "maxDataPoints": 43200,
                    "refId": "D",
                    "type": "classic_conditions"
                }
            }
        ]
    }