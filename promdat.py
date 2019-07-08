import requests

def wallclock(period, offset=""):
    query = 'sum(sum_over_time(node_namespace_pod:kube_pod_info:[' + period + ']'
    if offset:
        query = query + ' offset ' + offset
    query += ')) by (namespace)'
    return requests.get('https://prometheus.nautilus.optiputer.net/api/v1/query?query=' + query).json()


def gpu(period, requested=False, offset=""):
    if requested:
        query = 'sum(sum_over_time(pod_gpus[' + period + ':1s]'
        if offset:
            query = query + ' offset ' + offset
        query += ')) by (namespace_name)'
        return requests.get('https://prometheus.nautilus.optiputer.net/api/v1/query?query=' + query).json()
    query = 'sum_over_time(namespace_gpu_utilization[' + period + ':1s]'
    if offset:
        query = query + ' offset ' + offset
    query += ')'
    return requests.get('https://prometheus.nautilus.optiputer.net/api/v1/query?query=' + query).json()


def cpu(period, requested=False, offset=""):
    if requested:
        query = 'sum(sum_over_time(kube_pod_container_resource_requests_cpu_cores[' + period + ':1s]'
        if offset:
            query = query + ' offset ' + offset
        query += ')) by (namespace)'
        return requests.get('https://prometheus.nautilus.optiputer.net/api/v1/query?query=' + query).json()
    query = 'sum(increase(container_cpu_usage_seconds_total[' + period + ':1m]'
    if offset:
        query = query + ' offset ' + offset
    query += ')/2) by (namespace)'
    return requests.get('https://prometheus.nautilus.optiputer.net/api/v1/query?query=' + query).json()


def memory(period, offset=""):
    query = 'sum(sum_over_time(namespace:container_memory_usage_bytes:sum[' + period + ':1s]'
    if offset:
        query = query + ' offset ' + offset
    query += ')) by (namespace)'
    return requests.get('https://prometheus.nautilus.optiputer.net/api/v1/query?query=' + query).json()
