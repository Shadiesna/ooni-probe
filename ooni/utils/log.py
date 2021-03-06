# -*- encoding: utf-8 -*-
#
# :authors: Arturo Filastò
# :licence: see LICENSE

import sys
import os
import traceback
import logging

from twisted.python import log as txlog
from twisted.python.failure import Failure
from twisted.python.logfile import DailyLogFile

from ooni.utils import otime
from ooni import config

## Get rid of the annoying "No route found for
## IPv6 destination warnings":
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

def start(logfile=None, application_name="ooniprobe"):
    daily_logfile = None

    if not logfile:
        logfile = config.basic.logfile

    log_folder = os.path.dirname(logfile)
    log_filename = os.path.basename(logfile)

    daily_logfile = DailyLogFile(log_filename, log_folder)

    txlog.msg("Starting %s on %s (%s UTC)" %  (application_name, otime.prettyDateNow(),
                                                 otime.utcPrettyDateNow()))
    logging.basicConfig()
    python_logging = txlog.PythonLoggingObserver(application_name)

    if config.advanced.debug:
        python_logging.logger.setLevel(logging.DEBUG)
    else:
        python_logging.logger.setLevel(logging.INFO)

    txlog.startLoggingWithObserver(python_logging.emit)

    txlog.addObserver(txlog.FileLogObserver(daily_logfile).emit)

def stop():
    txlog.msg("Stopping OONI")

def msg(msg, *arg, **kw):
    txlog.msg(msg, logLevel=logging.INFO, *arg, **kw)

def debug(msg, *arg, **kw):
    txlog.msg(msg, logLevel=logging.DEBUG, *arg, **kw)

def err(msg, *arg, **kw):
    txlog.err("Error: " + str(msg), logLevel=logging.ERROR, *arg, **kw)

def exception(error):
    """
    Error can either be an error message to print to stdout and to the logfile
    or it can be a twisted.python.failure.Failure instance.
    """
    if isinstance(error, Failure):
        error.printTraceback()
    else:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)

class LoggerFactory(object):
    """
    This is a logger factory to be used by oonib
    """
    def __init__(self, options):
        pass

    def start(self, application):
        # XXX parametrize this
        start('/tmp/oonib.log', "OONIB")

    def stop(self):
        txlog.msg("Stopping OONIB")

