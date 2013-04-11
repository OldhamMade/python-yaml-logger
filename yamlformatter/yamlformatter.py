import datetime
import logging
import re

from yaml import dump, safe_dump
try:
    from yaml import CDumper as Dumper, CSafeDumper as SafeDumper
except ImportError:
    from yaml import Dumper, SafeDumper

# skip natural LogRecord attributes
# http://docs.python.org/library/logging.html#logrecord-attributes
RESERVED_ATTRS = (
    'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
    'funcName', 'levelname', 'levelno', 'lineno', 'module',
    'msecs', 'message', 'msg', 'name', 'pathname', 'process',
    'processName', 'relativeCreated', 'thread', 'threadName',
    )

RESERVED_ATTR_HASH = dict(zip(RESERVED_ATTRS, RESERVED_ATTRS))


def merge_record_extra(record, target, reserved=RESERVED_ATTR_HASH):
    """
    Merges extra attributes from LogRecord object into target dictionary

    :param record: logging.LogRecord
    :param target: dict to update
    :param reserved: dict or list with reserved keys to skip
    """
    for key, value in record.__dict__.iteritems():
        #this allows to have numeric keys
        if (key not in reserved
            and not (hasattr(key,"startswith") and key.startswith('_'))
            ):
            target[key] = value
    return target


class YAMLFormatter(logging.Formatter):

    default_fields = [
        'asctime',
        'created',
        'levelname',
        'message',
        'name',
        ]

    def __init__(self, *args, **kwargs):
        logging.Formatter.__init__(self, *args, **kwargs)
        self._required_fields = self.parse()
        self._required_fields += self.default_fields
        self._skip_fields = dict(zip(self._required_fields,
                                     self._required_fields))
        self._skip_fields.update(RESERVED_ATTR_HASH)


    def parse(self):
        """Parses format string looking for substitutions"""
        standard_formatters = re.compile(r'\((.+?)\)', re.IGNORECASE)
        return standard_formatters.findall(self._fmt)


    def format(self, record):
        """Formats a log record and serializes to YAML"""
        extras = {}
        if isinstance(record.msg, dict):
            extras = record.msg
            record.message = None
        else:
            record.message = record.getMessage()

        # only format time if needed
        if "asctime" in self._required_fields:
            record.asctime = self.formatTime(record, self.datefmt)

        log_record = {}

        for field in self._required_fields:
            try:
                log_record[field] = record.__dict__[field]
            except KeyError:
                pass

        log_record.update(extras)
        merge_record_extra(record, log_record)#, reserved=self._skip_fields)

        #return dump([log_record,], Dumper=Dumper, default_flow_style=False, allow_unicode=True)
        return safe_dump([log_record,], default_flow_style=False, allow_unicode=True)
