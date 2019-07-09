import argparse
import kubedata
import kubedisplay

parser = argparse.ArgumentParser(description='displays kubernetes data queried from prometheus')
parser.add_argument('-p', '--period', required=True)
group = parser.add_mutually_exclusive_group()
group.add_argument('-w', '--walltime', action='store_true')
group.add_argument('-g', '--gpu', action='store_true')
group.add_argument('-c', '--cpu', action='store_true')
group.add_argument('-m', '--memory', action='store_true')
parser.add_argument('--all', action='store_true')
parser.add_argument('-s', '--sortby')
parser.add_argument('-o', '--offset')
act = parser.add_mutually_exclusive_group()
act.add_argument('-r', '--reverse', action='store_true') #if included, sorting is reversed
act.add_argument('--requested', action='store_true')
act.add_argument('-u', '--unit')
args = parser.parse_args()

if __name__ == '__main__':
    if args.walltime:
        offset = ""
        if args.offset:
            offset = args.offset
        wall_dat = kubedata.wallclock(args.period, args.offset)
        unit = ""
        sortby = ""
        reverse = False
        all = False
        if args.unit:
            unit = args.unit
        if args.sortby:
            sortby = args.sortby
        if args.reverse:
            reverse = True
        if args.all:
            all = True
        kubedisplay.walltime(wall_dat, sortby, unit, reverse, all)

    elif args.gpu:
        requested = False
        offset = ""
        if args.requested:
            requested = args.requested
        if args.offset:
            offset = args.offset
        gpu_dat = kubedata.gpu(args.period, args.requested, args.offset)
        unit = ""
        sortby = ""
        reverse = False
        all = False
        if args.unit:
            unit = args.unit
        if args.sortby:
            sortby = args.sortby
        if args.reverse:
            reverse = True
        if args.all:
            all = True
        kubedisplay.gpu(gpu_dat, sortby, unit, reverse, all)

    elif args.cpu:
        requested = False
        offset = ""
        if args.requested:
            requested = args.requested
        if args.offset:
            offset = args.offset
        cpu_dat = kubedata.cpu(args.period, requested, offset)
        unit = ""
        sortby = ""
        reverse = False
        all = False
        if args.unit:
            unit = args.unit
        if args.sortby:
            sortby = args.sortby
        if args.reverse:
            reverse = True
        if args.all:
            all = True
        kubedisplay.cpu(cpu_dat, sortby, unit, reverse, all)

    elif args.memory:
        offset = ""
        if args.offset:
            offset = args.offset
        memory_dat = kubedata.memory(args.period, offset)
        unit = ""
        sortby = ""
        reverse = False
        all = False
        if args.unit:
            unit = args.unit
        if args.sortby:
            sortby = args.sortby
        if args.reverse:
            reverse = True
        if args.all:
            all = True
        kubedisplay.memory(memory_dat, sortby, unit, reverse, all)
