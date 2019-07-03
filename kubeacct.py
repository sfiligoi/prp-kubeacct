import argparse
import requests

parser = argparse.ArgumentParser(description='print string1 or string2')
parser.add_argument('-p', '--period', required=True)
group = parser.add_mutually_exclusive_group()
group.add_argument('-w', '--walltime', action='store_true')
group.add_argument('-g', '--gpu', action='store_true')
group.add_argument('-c', '--cpu', action='store_true')
group.add_argument('-m', '--memory', action='store_true')
group.add_argument('-n', '--namespace', action='store_true')
parser.add_argument('--all', action='store_true')
parser.add_argument('-s', '--sortby')
parser.add_argument('-u', '--unit')
act = parser.add_mutually_exclusive_group()
act.add_argument('-r', '--reverse', action='store_true') #if included, sorting is reversed
act.add_argument('--requested', action='store_true')
parser.add_argument('-o', '--offset')

args = parser.parse_args()

def wallclock(period):
    query = 'sum(sum_over_time(node_namespace_pod:kube_pod_info:[' + period + ']'
    if args.offset:
        query = query + ' offset ' + args.offset
    query += ')) by (namespace)'
    return requests.get('https://prometheus.nautilus.optiputer.net/api/v1/query?query=' + query).json()

def gpu(period):
    if args.requested:
        query = 'sum(sum_over_time(pod_gpus[' + period + ':1s]'
        if args.offset:
            query = query + ' offset ' + args.offset
        query += ')) by (namespace_name)'
        return requests.get('https://prometheus.nautilus.optiputer.net/api/v1/query?query=' + query).json()
    query = 'sum_over_time(namespace_gpu_utilization[' + period + ':1s]'
    if args.offset:
        query = query + ' offset ' + args.offset
    query += ')'
    return requests.get('https://prometheus.nautilus.optiputer.net/api/v1/query?query=' + query).json()

def cpu(period):
    if args.requested:
        query = 'sum(sum_over_time(kube_pod_container_resource_requests_cpu_cores[' + period + ':1s]'
        if args.offset:
            query = query + ' offset ' + args.offset
        query += ')) by (namespace)'
        return requests.get('https://prometheus.nautilus.optiputer.net/api/v1/query?query=' + query).json()
    query = 'sum(increase(container_cpu_usage_seconds_total[' + period + ':1m]'
    if args.offset:
        query = query + ' offset ' + args.offset
    query += ')/2) by (namespace)'
    return requests.get('https://prometheus.nautilus.optiputer.net/api/v1/query?query=' + query).json()

def memory(period):
    query = 'sum(sum_over_time(namespace:container_memory_usage_bytes:sum[' + period + ':1s]'
    if args.offset:
        query = query + ' offset ' + args.offset
    query += ')) by (namespace)'
    return requests.get('https://prometheus.nautilus.optiputer.net/api/v1/query?query=' + query).json()

if __name__ == '__main__':

    func_one = wallclock(args.period)
    func_two = gpu(args.period)
    func_three = cpu(args.period)
    func_four = memory(args.period)

    if args.walltime:
        values = [] #list of values (wallclock time)
        namespace = []
        name_n_val = []
        dict = func_one["data"]["result"]

        for i in dict:
            namespace.extend(list(list(i.values())[0].values()))
            values.append(list(i.values())[1])

        val = []
        for i in values:
            val.append(float(i[1]))

        div = 1
        if args.unit:
            unit = args.unit
            if unit == "s":
                div = 1
            elif unit == "Ys":
                div = 10**24
            elif unit == "Zs":
                div = 10**21
            elif unit == "Es":
                div = 10**18
            elif unit == "Ps":
                div = 10**15
            elif unit == "Ts":
                div = 10**12
            elif unit == "Gs":
                div = 10**9
            elif unit == "Ms":
                div = 10**6
            elif unit == "ks":
                div = 10**3
        else:
            unit = "s"
            maximum = max(val)
            if maximum/10**24 >= 1000 and maximum/10**24 <= 9999999.9:
                unit = "Ys"
                div = 10**24
            elif maximum/10**21 >= 1000 and maximum/10**21 <= 9999999.9:
                unit = "Zs"
                div = 10**21
            elif maximum/10**18 >= 1000 and maximum/10**18 <= 9999999.9:
                unit = "Es"
                div = 10**18
            elif maximum/10**15 >= 1000 and maximum/10**15 <= 9999999.9:
                unit = "Ps"
                div = 10**15
            elif maximum/10**12 >= 1000 and maximum/10**12 <= 9999999.9:
                unit = "Ts"
                div = 10**12
            elif maximum/10**9 >= 1000 and maximum/10**9 <= 9999999.9:
                unit = "Gs"
                div = 10**9
            elif maximum/10**6 >= 1000 and maximum/10**6 <= 9999999.9:
                unit = "Ms"
                div = 10**6
            elif maximum/10**3 >= 1000 and maximum/10**3 <= 9999999.9:
                unit = "ks"
                div = 10**3

        final_val = []
        for v in val:
            v = round(v/div, 1)
            final_val.append(v)

        for i in range(len(namespace)):
            if args.all:
                name_n_val.append((namespace[i], final_val[i]))
            else:
                if final_val[i] != 0:
                    name_n_val.append((namespace[i], final_val[i]))

        def sorter(e, sortby=0):
            sortby = int(args.sortby)
            return e[sortby]

        reverse_bool = False
        if args.reverse:
            reverse_bool = True

        if args.sortby == "1":
            reverse_bool = not reverse_bool

        name_n_val.sort(key=sorter, reverse=reverse_bool)

        header = [("namespace:", "wallclock time: (" + unit + ")"), ("------------", "---------------")]

        for h in header:
            format = "%-40s %20s"
            n = format%(h)
            print(n)

        for name in name_n_val:
            format = "%-40s %20s"
            n = format%(name)
            print(n)



    elif args.gpu:
        g_namespace = []
        g_values = []
        name_n_val = []
        dict = func_two["data"]["result"]

        for i in dict:
            g_namespace.extend(list(list(i.values())[0].values()))
            g_values.append(list(i.values())[1])


        val = []
        for i in g_values:
            val.append(float(i[1]))

        div = 1
        if args.unit:
            unit = args.unit
            if unit == "s":
                div = 1
            elif unit == "Ys":
                div = 10**24
            elif unit == "Zs":
                div = 10**21
            elif unit == "Es":
                div = 10**18
            elif unit == "Ps":
                div = 10**15
            elif unit == "Ts":
                div = 10**12
            elif unit == "Gs":
                div = 10**9
            elif unit == "Ms":
                div = 10**6
            elif unit == "ks":
                div = 10**3
        else:
            unit = "s"
            maximum = max(val)
            if maximum/10**24 >= 1000 and maximum/10**24 <= 9999999.9:
                unit = "Ys"
                div = 10**24
            elif maximum/10**21 >= 1000 and maximum/10**21 <= 9999999.9:
                unit = "Zs"
                div = 10**21
            elif maximum/10**18 >= 1000 and maximum/10**18 <= 9999999.9:
                unit = "Es"
                div = 10**18
            elif maximum/10**15 >= 1000 and maximum/10**15 <= 9999999.9:
                unit = "Ps"
                div = 10**15
            elif maximum/10**12 >= 1000 and maximum/10**12 <= 9999999.9:
                unit = "Ts"
                div = 10**12
            elif maximum/10**9 >= 1000 and maximum/10**9 <= 9999999.9:
                unit = "Gs"
                div = 10**9
            elif maximum/10**6 >= 1000 and maximum/10**6 <= 9999999.9:
                unit = "Ms"
                div = 10**6
            elif maximum/10**3 >= 1000 and maximum/10**3 <= 9999999.9:
                unit = "ks"
                div = 10**3

        final_val = []
        for v in val:
            v = round(v/div, 1)
            final_val.append(v)

        for i in range(len(g_namespace)):
            if args.all:
                name_n_val.append((g_namespace[i], final_val[i]))
            else:
                if final_val[i] != 0:
                    name_n_val.append((g_namespace[i], final_val[i]))


        def sorter(e, sortby=0):
            sortby = int(args.sortby)
            return e[sortby]

        reverse_bool = False
        if args.reverse:
            reverse_bool = True

        if args.sortby == "1":
            reverse_bool = not reverse_bool

        name_n_val.sort(key=sorter, reverse=reverse_bool)

        header = [("namespace:", "gpu: (" + unit + ")"), ("------------", "------------")]

        for h in header:
            format = "%-40s %20s"
            n = format%(h)
            print(n)

        for name in name_n_val:
            format = "%-40s %20s"
            n = format%(name)
            print(n)



    elif args.cpu:
        c_namespace = []
        c_values = []
        name_n_val = []
        dict = func_three["data"]["result"]

        for i in dict:
            c_namespace.extend(list(list(i.values())[0].values()))
            c_values.append(list(i.values())[1])

        val = []
        for i in c_values:
            val.append(float(i[1]))

        div = 1
        if args.unit:
            unit = args.unit
            if unit == "s":
                div = 1
            elif unit == "Ys":
                div = 10**24
            elif unit == "Zs":
                div = 10**21
            elif unit == "Es":
                div = 10**18
            elif unit == "Ps":
                div = 10**15
            elif unit == "Ts":
                div = 10**12
            elif unit == "Gs":
                div = 10**9
            elif unit == "Ms":
                div = 10**6
            elif unit == "ks":
                div = 10**3
        else:
            unit = "s"
            maximum = max(val)
            if maximum/10**24 >= 1000 and maximum/10**24 <= 9999999.9:
                unit = "Ys"
                div = 10**24
            elif maximum/10**21 >= 1000 and maximum/10**21 <= 9999999.9:
                unit = "Zs"
                div = 10**21
            elif maximum/10**18 >= 1000 and maximum/10**18 <= 9999999.9:
                unit = "Es"
                div = 10**18
            elif maximum/10**15 >= 1000 and maximum/10**15 <= 9999999.9:
                unit = "Ps"
                div = 10**15
            elif maximum/10**12 >= 1000 and maximum/10**12 <= 9999999.9:
                unit = "Ts"
                div = 10**12
            elif maximum/10**9 >= 1000 and maximum/10**9 <= 9999999.9:
                unit = "Gs"
                div = 10**9
            elif maximum/10**6 >= 1000 and maximum/10**6 <= 9999999.9:
                unit = "Ms"
                div = 10**6
            elif maximum/10**3 >= 1000 and maximum/10**3 <= 9999999.9:
                unit = "ks"
                div = 10**3

        final_val = []
        for v in val:
            v = round(v/div, 1)
            final_val.append(v)


        for i in range(len(c_namespace)):
            if args.all:
                name_n_val.append((c_namespace[i], final_val[i]))
            else:
                if final_val[i] != 0:
                    name_n_val.append((c_namespace[i], final_val[i]))


        def sorter(e, sortby=0):
            sortby = int(args.sortby)
            return e[sortby]

        reverse_bool = False
        if args.reverse:
            reverse_bool = True

        if args.sortby == "1":
            reverse_bool = not reverse_bool

        name_n_val.sort(key=sorter, reverse=reverse_bool)

        header = [("namespace:", "cpu: (" + unit + ")"), ("-------------", "-------------")]

        for h in header:
            format = "%-40s %20s"
            n = format%(h)
            print(n)

        for name in name_n_val:
            format = "%-40s %20s"
            n = format%(name)
            print(n)



    elif args.memory:
        m_namespace = []
        m_values = []
        name_n_val = []
        dict = func_four["data"]["result"]

        for i in dict:
            m_namespace.extend(list(list(i.values())[0].values()))
            m_values.append(list(i.values())[1])

        val = []
        for i in m_values:
            val.append(float(i[1]))

        div = 1
        if args.unit:
            unit = args.unit
            if unit == "s":
                div = 1
            elif unit == "Ys":
                div = 10**24
            elif unit == "Zs":
                div = 10**21
            elif unit == "Es":
                div = 10**18
            elif unit == "Ps":
                div = 10**15
            elif unit == "Ts":
                div = 10**12
            elif unit == "Gs":
                div = 10**9
            elif unit == "Ms":
                div = 10**6
            elif unit == "ks":
                div = 10**3
        else:
            unit = "s"
            maximum = max(val)
            if maximum/10**24 >= 1000 and maximum/10**24 <= 9999999.9:
                unit = "Ys"
                div = 10**24
            elif maximum/10**21 >= 1000 and maximum/10**21 <= 9999999.9:
                unit = "Zs"
                div = 10**21
            elif maximum/10**18 >= 1000 and maximum/10**18 <= 9999999.9:
                unit = "Es"
                div = 10**18
            elif maximum/10**15 >= 1000 and maximum/10**15 <= 9999999.9:
                unit = "Ps"
                div = 10**15
            elif maximum/10**12 >= 1000 and maximum/10**12 <= 9999999.9:
                unit = "Ts"
                div = 10**12
            elif maximum/10**9 >= 1000 and maximum/10**9 <= 9999999.9:
                unit = "Gs"
                div = 10**9
            elif maximum/10**6 >= 1000 and maximum/10**6 <= 9999999.9:
                unit = "Ms"
                div = 10**6
            elif maximum/10**3 >= 1000 and maximum/10**3 <= 9999999.9:
                unit = "ks"
                div = 10**3

        final_val = []
        for v in val:
            v = round(v/div, 1)
            final_val.append(v)


        for i in range(len(m_namespace)):
            if args.all:
                name_n_val.append((m_namespace[i], final_val[i]))
            else:
                if final_val[i] != 0:
                    name_n_val.append((m_namespace[i], final_val[i]))

        def sorter(e, sortby=0):
            sortby = int(args.sortby)
            return e[sortby]

        reverse_bool = False
        if args.reverse:
            reverse_bool = True

        if args.sortby == "1":
            reverse_bool = not reverse_bool

        name_n_val.sort(key=sorter, reverse=reverse_bool)

        header = [("namespace:", "memory: (" + unit + ")"), ("------------", "------------")]

        for h in header:
            format = "%-40s %20s"
            n = format%(h)
            print(n)

        for name in name_n_val:
            format = "%-40s %20s"
            n = format%(name)
            print(n)



    else:
        print(args.period)
