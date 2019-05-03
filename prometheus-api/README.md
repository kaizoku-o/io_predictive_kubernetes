### Prometheus Utililty Functions

**prometheus.py** (vabongal) provides functions to query prometheus API to get metric data. The metric data request is in the form of prometheus query written in PromQL. The functions take duration parameters to get the metrics in that duration with a specified sampling rate.

#### Prometheus [APIs](https://prometheus.io/docs/prometheus/latest/querying/api/)

* GET /api/v1/query
* GET /api/v1/query_range

#### Functions

*run_query(prometheus_query)*

```(python)
    Get the response of a simple query from prometheus
    Arguments:
        prom_query: Prometheus query
    Returns:
        JSON response of the query results
```

*run_query_range(query, start_range, end_range, step)*

```(python)
    Query prometheus data for a specific range

    Arguments:
        query: Prometheus query
        start_range: range start time in Epoch Timestamp
        end_range: range end time in Epoch Timestamp
        step: Resolution in seconds
    Returns: None
```