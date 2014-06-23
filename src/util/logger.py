'''

'''
import datetime, inspect, os, sys, logging
import logging.handlers

class ConsoleLogFormatter(logging.Formatter):
    converter=datetime.datetime.fromtimestamp
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s.%03d" % (t, record.msecs)
        return s


def init_logging(file_path='test.log', log_level=logging.DEBUG):
    file_hdlr = logging.handlers.RotatingFileHandler(file_path, backupCount=50)
    file_hdlr.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s;%(module)s;%(funcName)-10s;'
                                  '%(lineno)d;%(levelname)s;%(message)s')
    file_hdlr.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(log_level)
    formatter = ConsoleLogFormatter('%(asctime)s;'
                                  '%(levelname)-5s %(message)s',
                                  "%H:%M:%S.%f")
    console.setFormatter(formatter)

    # add the handler to the root logger
    my_log = logging.getLogger()
    my_log.setLevel(logging.DEBUG)
    my_log.addHandler(console)
    my_log.addHandler(file_hdlr)
    return my_log

logger = init_logging('./log/all.log', logging.DEBUG)

