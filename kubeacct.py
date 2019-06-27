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
act = parser.add_mutually_exclusive_group()
act.add_argument('-r', '--reverse', action='store_true')
args = parser.parse_args()

def wallclock(period):
        return requests.get('https://prometheus.nautilus.optiputer.net/api/v1/query?query=sum(node_namespace_pod:kube_pod_info:) by (namespace)').json()


def gpu(period):
    return requests.get('https://prometheus.nautilus.optiputer.net/api/v1/query?query=increase(namespace_gpu_utilization[' + period + '])').json()

def cpu(period):
    return requests.get('https://prometheus.nautilus.optiputer.net/api/v1/query?query=increase(namespace_name:kube_pod_container_resource_requests_cpu_cores:sum[' + period + '])').json()

def memory(period):
    return requests.get('https://prometheus.nautilus.optiputer.net/api/v1/query?query=increase(namespace:container_memory_usage_bytes:sum[' + period + '])').json()

if __name__ == '__main__':

    func_one = wallclock(args.period)
    func_two = gpu(args.period)
    func_three = cpu(args.period)
    func_four = memory(args.period)

    if args.walltime:
        values = [] #list of values (wallclock time)
        namespace = []
        header = [("namespace:", "wallclock time:"), ("------------", "---------------")]

        for h in header:
            format = "%-65s %20s"
            n = format%(h)
            print(n)

        name_n_val = []
        dict = func_one["data"]["result"]

        for i in dict:
            namespace.extend(list(list(i.values())[0].values()))
            values.append(list(i.values())[1])

        for i in range(len(namespace)):
            if args.all:
                name_n_val.append((namespace[i], round(float(values[i][1]), 1)))
            else:
                if float(values[i][1]) != 0:
                    name_n_val.append((namespace[i], round(float(values[i][1]), 1)))

        def sorter(e, sortby=0):
            sortby = int(args.sortby)
            return e[sortby]

        reverse_bool = False
        if args.reverse:
            reverse_bool = True

        if args.sortby == "1":
            reverse_bool = not reverse_bool

        name_n_val.sort(key=sorter, reverse=reverse_bool)

        for name in name_n_val:
            format = "%-65s %20s"
            n = format%(name)
            print(n)



    elif args.gpu:
        g_namespace = []
        g_values = []
        header = [("namespace:", "gpu:"), ("------------", "------------")]

        for h in header:
            format = "%-65s %20s"
            n = format%(h)
            print(n)

        name_n_val = []
        dict = func_two["data"]["result"]

        for i in dict:
            g_namespace.extend(list(list(i.values())[0].values()))
            g_values.append(list(i.values())[1])

        for i in range(len(g_namespace)):
            if args.all:
                name_n_val.append((g_namespace[i], round(float(g_values[i][1]), 1)))
            else:
                if float(g_values[i][1]) != 0:
                    name_n_val.append((g_namespace[i], round(float(g_values[i][1]), 1)))

        def sorter(e, sortby=0):
            sortby = int(args.sortby)
            return e[sortby]

        reverse_bool = False
        if args.reverse:
            reverse_bool = True

        if args.sortby == "1":
            reverse_bool = not reverse_bool

        name_n_val.sort(key=sorter, reverse=reverse_bool)

        for name in name_n_val:
            format = "%-65s %20s"
            n = format%(name)
            print(n)



    elif args.cpu:
        c_namespace = []
        c_values = []
        header = [("namespace:", "cpu:"), ("-------------", "-------------")]
        for h in header:
            format = "%-65s %20s"
            n = format%(h)
            print(n)

        name_n_val = []
        dict = func_three["data"]["result"]

        for i in dict:
            c_namespace.extend(list(list(i.values())[0].values()))
            c_values.append(list(i.values())[1])

        for i in range(len(c_namespace)):
            if args.all:
                name_n_val.append((c_namespace[i], round(float(c_values[i][1]), 1)))
            else:
                if float(c_values[i][1]) != 0:
                    name_n_val.append((c_namespace[i], round(float(c_values[i][1]), 1)))

        def sorter(e, sortby=0):
            sortby = int(args.sortby)
            return e[sortby]

        reverse_bool = False
        if args.reverse:
            reverse_bool = True

        if args.sortby == "1":
            reverse_bool = not reverse_bool

        name_n_val.sort(key=sorter, reverse=reverse_bool)

        for name in name_n_val:
            format = "%-65s %20s"
            n = format%(name)
            print(n)



    elif args.memory:
        m_namespace = []
        m_values = []
        header = [("namespace:", "memory:"), ("------------", "------------")]

        for h in header:
            format = "%-65s %20s"
            n = format%(h)
            print(n)

        name_n_val = []
        dict = func_four["data"]["result"]

        for i in dict:
            m_namespace.extend(list(list(i.values())[0].values()))
            m_values.append(list(i.values())[1])
        for i in range(len(m_namespace)):

            if args.all:
                name_n_val.append((m_namespace[i], round(float(m_values[i][1]), 1)))
            else:
                if float(m_values[i][1]) != 0:
                    name_n_val.append((m_namespace[i], round(float(m_values[i][1]), 1)))

        def sorter(e, sortby=0):
            sortby = int(args.sortby)
            return e[sortby]

        reverse_bool = False
        if args.reverse:
            reverse_bool = True

        if args.sortby == "1":
            reverse_bool = not reverse_bool

        name_n_val.sort(key=sorter, reverse=reverse_bool)

        for name in name_n_val:
            format = "%-65s %20s"
            n = format%(name)
            print(n)



    else:
        print(args.period)
