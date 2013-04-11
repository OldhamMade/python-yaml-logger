import os
import sys
import logging

try:
    from io import BytesIO as StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

sys.path.insert(0, os.path.abspath('../yamlformatter'))
import yamlformatter


class YAMLFormatterSpec(unittest.TestCase):
    '''YAML Formatter Spec'''

    def setUp(self):
        self.default_fields = [
            'asctime',
            'created',
            'levelname',
            'message',
            'name',
            ]

        self.logger = logging.getLogger('logformatting-test')
        self.logger.setLevel(logging.DEBUG)
        self.buffer = StringIO()

        self.logHandler = logging.StreamHandler(self.buffer)
        self.logger.addHandler(self.logHandler)


    def it_should_handle_simple_log_messages(self):
        formatter = yamlformatter.YAMLFormatter()
        self.logHandler.setFormatter(formatter)

        self.logger.info("test message")
        for record in load(self.buffer.getvalue()):
            self.assertEqual(set(self.default_fields), set(record.keys()))


    def it_should_support_custom_formats(self):
        supported_keys = [
            'asctime',
            'created',
            'filename',
            'funcName',
            'levelname',
            'levelno',
            'lineno',
            'module',
            'msecs',
            'message',
            'name',
            'pathname',
            'process',
            'processName',
            'relativeCreated',
            'thread',
            'threadName'
        ]

        log_format = lambda x : ['%({0:s})'.format(i) for i in x]
        custom_format = ' '.join(log_format(supported_keys))

        formatter = yamlformatter.YAMLFormatter(custom_format)
        print custom_format
        self.logHandler.setFormatter(formatter)

        self.logger.info("test message")

        for record in load(self.buffer.getvalue()):
            self.assertEqual(set(supported_keys), set(record.keys()))


    def it_should_ignore_unknown_formats(self):
        formatter = yamlformatter.YAMLFormatter('%(unknown_key)s %(message)s')

        self.logHandler.setFormatter(formatter)

        try:
            self.logger.info("test message")
            for record in load(self.buffer.getvalue()):
                self.assertEqual(
                    set(self.default_fields),
                    set(record.keys())
                    )
        except:
            raise Exception('logging should succeed')


    def it_should_log_python_dictionaries(self):
        formatter = yamlformatter.YAMLFormatter()

        self.logHandler.setFormatter(formatter)

        test_data = {
            "text": "testing logging",
            "num": 1,
            5: "9",
            "nested": {
                "more": "data"
                }
            }

        self.logger.info(test_data)

        result = self.buffer.getvalue()

        for record in load(self.buffer.getvalue()):
            self.assertEqual(
                set(self.default_fields + test_data.keys()),
                set(record.keys())
                )
            self.assertEqual(
                record['nested']['more'],
                'data'
                )


    def it_should_log_extra_data(self):
        formatter = yamlformatter.YAMLFormatter()

        self.logHandler.setFormatter(formatter)

        test_data = {
            "text": "testing logging",
            "num": 1,
            5: "9",
            "nested": {
                "more": "data"
                }
            }

        self.logger.info('test message', extra=test_data)

        for record in load(self.buffer.getvalue()):
            self.assertEqual(
                set(self.default_fields + test_data.keys()),
                set(record.keys()+['message',])
                )
            self.assertEqual(
                record['nested']['more'],
                'data'
                )

    def it_should_log_multiple_messages(self):
        formatter = yamlformatter.YAMLFormatter()

        self.logHandler.setFormatter(formatter)

        for i in range(10):
            self.logger.info('message %d' % i)

        print self.buffer.getvalue()

        results = load(self.buffer.getvalue())

        self.assertEqual(len(results), 10)
        for record in results:
            self.assertEqual(
                set(self.default_fields),
                set(record.keys())
                )
