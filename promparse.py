import argparse
import promdisp
import promdat

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

if __name__ == '__main__':
    if args.walltime:
        offset = ""
        if args.offset:
            offset = args.offset
        wall_dat = promdat.wallclock(args.period, args.offset)
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
        promdisp.walltime(wall_dat, unit, sortby, reverse, all)

    elif args.gpu:
        requested = False
        offset = ""
        if args.requested:
            requested = args.requested
        if args.offset:
            offset = args.offset
        gpu_dat = promdat.gpu(args.period, args.requested, args.offset)
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
        promdisp.gpu(gpu_dat, unit, sortby, reverse, all)

    elif args.cpu:
        requested = False
        offset = ""
        if args.requested:
            requested = args.requested
        if args.offset:
            offset = args.offset
        cpu_dat = promdat.cpu(args.period, requested, offset)
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
        promdisp.cpu(cpu_dat, unit, sortby, reverse, all)

    elif args.memory:
        offset = ""
        if args.offset:
            offset = args.offset
        memory_dat = promdat.memory(args.period, offset)
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
        promdisp.memory(memory_dat, unit, sortby, reverse, all)
