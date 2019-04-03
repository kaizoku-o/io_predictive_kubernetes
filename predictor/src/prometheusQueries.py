"""This module serves as a repository of all the queries used by the 
   prometheus and predictor modules.
   Defines queries to get metrics related to CPU, Memory and IO usage
   of the node. 
"""

Queries = {
    # Obtain the memory usage value of a node (in GB) using average of free memory
    #  (Free + cached + Buffer) over the past 24 hours. Multiply the value by 100 
    #  for percentage representation

    "mem" : "100 * (1 - ((avg_over_time(node_memory_MemFree{job='k8s-nodes'}[24h]) + avg_over_time(node_memory_Cached{job='k8s-nodes'}[24h]) + avg_over_time(node_memory_Buffers{job='k8s-nodes'}[24h])) / avg_over_time(node_memory_MemTotal{job='k8s-nodes'}[24h])))",

    # Obtain Instantaneous CPU usage in percentage by subtracting the CPU idle time. All the CPU time except the idle is considered as useful work by the CPU.

    # (avg by (instance)) - take the average for all the CPU instances. For example, if the
    # node has 2 cores, values of cpu0 and cpu1 are considered for average.

    # irate - instant rate. Consider last two data points by looking behind as far as the
    # window specified. Here, it is 5 minutes.

    "cpu" : "100 - (avg by (instance) (irate(node_cpu{job='k8s-nodes',mode='idle'}[5m])) * 100)",

    # Obtain total CPU usage in CPU seconds.
    # Take sum of the all CPU time spent on non-idle, non-iowait and non-guest mode of CPU

    "cpu_non_idle_time_total" : "sum(rate(node_cpu{job='k8s-nodes', mode!='idle', mode!='iowait',mode!~'^(?:guest.*)$'}[5m])) BY (instance)",

    # Obtain current disk IO in terms of number of IO operations performed by a particular disk. Generally, Higher the number of I/O operations executed by the disk, more is the load on I/O than compared to disk with less I/O activity.
    # This is Explicit I/O

    "disk_io_explicit" : "node_disk_io_now{device='xvda',job='k8s-nodes'}",

    # Obtain the rate of major page faults in the node. Major page faults
    # cause IO when loading the pages from disk. This is an Implicit I/O

    "disk_page_faults_rate_implicit" : "rate(node_vmstat_pgmajfault{job='k8s-nodes'}[5m])",

    # Explicilty sums up cached memory, buffered memory and free memory to obtain
    # total free memory in the node. Divide the value by the total memory to get
    # percentage of free memory, subtract the value from 1 to get percent usage memory 
    # and scale to 100.
    # This is similar to mem_utilization_perc_100 except it explicitly gets free memory

    "curr_mem_usage" : "100 * (1 - ((node_memory_MemFree{job='k8s-nodes'} + node_memory_Cached{job='k8s-nodes'} + node_memory_Buffers{job='k8s-nodes'}) / node_memory_MemTotal{job='k8s-nodes'}))",

    # More straight forward approach to determine the memory utilization
    # node_memory_MemAvailable provides the total memory available, divide that
    # by the total memory to get the percentage of available memory. Subtract the
    # value from 1 to obtain the percent memory used

    "mem_utilization_perc": "1 - (node_memory_MemAvailable{job='k8s-nodes'}/node_memory_MemTotal{job='k8s-nodes'})",

    # Same as memutilization query but gets the value in percentage of 100

    "mem_utilization_perc_100" : "100 * (1 - (node_memory_MemAvailable{job='k8s-nodes'}/node_memory_MemTotal{job='k8s-nodes'}))"
}
