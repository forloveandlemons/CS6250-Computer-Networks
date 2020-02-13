#!/usr/bin/env python
from argparse import ArgumentParser
import sys
import os
import termcolor as T
from subprocess import Popen, PIPE
import re

parser = ArgumentParser("Connect to a mininet node and run a command")
parser.add_argument('--node',
                    help="The node's name (e.g., h1, h2, etc.)")
parser.add_argument('--list', action="store_true", default=False,
                    help="List all running nodes.")
parser.add_argument('--cmd', default='ifconfig',
                    nargs="+",
                    help="Command to run inside node.")

FLAGS = parser.parse_args()
node_pat = re.compile('.*bash .* mininet:(.*)')


def list_nodes(do_print=False):
    cmd = 'ps aux'
    proc = Popen(cmd.split(), stdout=PIPE)
    out, err = proc.communicate()
    # Mapping from name to pid.
    ret = {}
    for line in out.split('\n'):
        match = node_pat.match(line)
        if not match:
            continue
        name = match.group(1)
        pid = line.split()[1]
        if do_print:
            print "name: %6s, pid: %6s" % (name, pid)
        ret[name] = pid
    return ret


def main():
    if FLAGS.list:
        list_nodes(do_print=True)
        return

    if not FLAGS.node:
        parser.print_help()
        return

    pid_by_name = list_nodes()
    pid = pid_by_name.get(FLAGS.node)
    if pid is None:
        print "node `%s' not found" % (FLAGS.node)
        sys.exit(1)

    cmd = ' '.join(FLAGS.cmd)
    os.system("mnexec -a %s %s" % (pid, cmd))


if __name__ == '__main__':
    main()

