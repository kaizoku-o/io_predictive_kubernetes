Queries = {
    "mem" : "100 * (1 - ((avg_over_time(node_memory_MemFree[24h]) + avg_over_time(node_memory_Cached[24h]) + avg_over_time(node_memory_Buffers[24h])) / avg_over_time(node_memory_MemTotal[24h])))",

    "cpu" : "100 - (avg by (instance) (irate(node_cpu{job='k8s-nodes',mode='idle'}[5m])) * 100)",

    "cpunonidle" : "sum(rate(node_cpu{mode!='idle',mode!='iowait',mode!~'^(?:guest.*)$'}[5m])) BY (instance)",

    "diskio" : "node_disk_io_now{device='xvda'}"
}
