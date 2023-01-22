#!python3

import argparse
import logging
from common.logfile import LogfileProcessor
from common.event import EventProcessor, LogbackListener
# from notify import Notifiers, CSVNotify, LogbackNotify
from Module.ucpath_queue import I280Queue
from common.util import LogHelper, Module

log = logging.getLogger('logger')

parser = argparse.ArgumentParser('Log analyze and report')
parser.add_argument(
    '--d', action='store_true', help='Show debugging messages"')
parser.add_argument(
    '--csv', action='store_true',
    help='Write audit data for each module to csv files')
parser.add_argument('--logfile', help='Log file to parse', required=True)
parser.add_argument('--instance', help='Instance name', required=True)
parser.add_argument('--hostname', help='Host name', required=True)

args = parser.parse_args()

processor = EventProcessor(log)
processor.register_listener(LogbackListener(log))

# if args.csv:
#     # add the CSV notifier if requested.
#     notifiers.add_notifier(CSVNotify())

# List of modules

modules: list[Module] = [I280Queue(processor, log)]

debug_level = logging.DEBUG if args.d else logging.INFO

LogHelper.initialize_console_logging(log, debug_level)

log.info('Starting')
app = LogfileProcessor(modules, log)
app.from_file(args.logfile, args.instance, args.hostname)
app.log_stats(processor)





