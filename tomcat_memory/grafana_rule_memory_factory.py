# ============================================================================================
# COSTRUTTORE REGOLE TOMCAT MEMORY (JMX)
# ============================================================================================

def build_tomcat_memory_payload(client, host_tag, folder_uid, datasource_uid, threshold=80):

    def make_jmx_query(ref_id, instance_tag, type_instance_tag):
        return {
            "refId": ref_id,
            "queryType": "",
            "relativeTimeRange": {"from": 600, "to": 0},
            "datasourceUid": datasource_uid,
            "model": {
                "alias": ref_id,
                "datasource": {"type": "influxdb", "uid": datasource_uid},
                "groupBy": [
                    {"params": ["$__interval"], "type": "time"},
                    {"params": ["null"], "type": "fill"}
                ],
                "hide": False,
                "intervalMs": 1000,
                "maxDataPoints": 43200,
                "measurement": "FastJMX_value",
                "orderByTime": "ASC",
                "policy": "one_week",
                "query": f'SELECT mean("value") FROM "autogen"."FastJMX_value" WHERE ("host" = \'{host_tag}\' AND "instance"::tag = \'{instance_tag}\' AND "type_instance"::tag = \'{type_instance_tag}\') AND $timeFilter GROUP BY time($__interval) fill(null)',
                "rawQuery": False,
                "refId": ref_id,
                "resultFormat": "time_series",
                "select": [[{"params": ["value"], "type": "field"}, {"params": [], "type": "mean"}]],
                "tags": [
                    {"key": "host", "operator": "=", "value": host_tag},
                    {"condition": "AND", "key": "instance::tag", "operator": "=", "value": instance_tag},
                    {"condition": "AND", "key": "type_instance::tag", "operator": "=", "value": type_instance_tag}
                ]
            }
        }

    def make_reducer(ref_id, target_expression):
        return {
            "refId": ref_id,
            "queryType": "",
            "relativeTimeRange": {"from": 600, "to": 0},
            "datasourceUid": "__expr__",
            "model": {
                "conditions": [{
                    "evaluator": {"params": [0, 0], "type": "gt"},
                    "operator": {"type": "and"},
                    "query": {"params": []},
                    "reducer": {"params": [], "type": "avg"},
                    "type": "query"
                }],
                "datasource": {"name": "Expression", "type": "__expr__", "uid": "__expr__"},
                "expression": target_expression,
                "intervalMs": 1000,
                "maxDataPoints": 43200,
                "reducer": "max",
                "refId": ref_id,
                "settings": {"mode": "replaceNN", "replaceWithValue": 0},
                "type": "reduce"
            }
        }

    return {
        "title": f"{client} - Tomcat Memory",
        "ruleGroup": "Memory",
        "folderUID": folder_uid,
        "condition": "Limite",
        "noDataState": "OK",
        "execErrState": "Error",
        "for": "30s",
        "labels": {
            "client": client,
            "type": "tomcat"
        },
        "annotations": {
            "summary": "Percentuale memoria di cui è stata effettuata la commit ({{ $values.Percentage.Value }}%) al limite.\nPuò causare un errore di out of memory"
        },
        "data": [
            make_jmx_query("heapCommitted", "memory-heap", "committed"),
            make_jmx_query("heapMax", "memory-heap", "max"),
            make_jmx_query("nonHeapCommitted", "memory-nonheap", "committed"),
            make_jmx_query("nonHeapMax", "memory-nonheap", "max"),
            make_reducer("redHeapCommitted", "heapCommitted"),
            make_reducer("redHeapMax", "heapMax"),
            make_reducer("redNonHeapCommitted", "nonHeapCommitted"),
            make_reducer("redNonHeapMax", "nonHeapMax"),
            {
                "refId": "Percentage",
                "queryType": "",
                "relativeTimeRange": {"from": 600, "to": 0},
                "datasourceUid": "__expr__",
                "model": {
                    "conditions": [{
                        "evaluator": {"params": [0, 0], "type": "gt"},
                        "operator": {"type": "and"},
                        "query": {"params": []},
                        "reducer": {"params": [], "type": "avg"},
                        "type": "query"
                    }],
                    "datasource": {"name": "Expression", "type": "__expr__", "uid": "__expr__"},
                    "expression": "100*(($redHeapCommitted+$redNonHeapCommitted)/($redHeapMax+$redNonHeapMax))",
                    "hide": False,
                    "intervalMs": 1000,
                    "maxDataPoints": 43200,
                    "refId": "Percentage",
                    "type": "math"
                }
            },
            {
                "refId": "Limite",
                "queryType": "",
                "relativeTimeRange": {"from": 600, "to": 0},
                "datasourceUid": "__expr__",
                "model": {
                    "conditions": [{
                        "evaluator": {"params": [threshold, 0], "type": "gt"},
                        "operator": {"type": "and"},
                        "query": {"params": []},
                        "reducer": {"params": [], "type": "avg"},
                        "type": "query"
                    }],
                    "datasource": {"name": "Expression", "type": "__expr__", "uid": "__expr__"},
                    "expression": "Percentage",
                    "intervalMs": 1000,
                    "maxDataPoints": 43200,
                    "refId": "Limite",
                    "type": "threshold"
                }
            }
        ]
    }