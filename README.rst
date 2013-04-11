python-yaml-logger
==================

|travis_status|_

Overview
--------
``python-yaml-logger`` is a formatter for the standard Python logging module designed to allow formatting log data as YAML_. Using YAML allow for both human- and machine-readable log files, and allows developers to quickly parse and make better use of log data.


Installation
------------

Manual installation::

  $ wget http://github.com/wewriteapps/python-yaml-logger/archive/master.tar.gz -O- | tar zx
  $ cd python-yaml-logger-master
  $ python setup.py install


Usage
-----

::

   import logging
   import yamllogger

   logger = logging.getLogger()
   logHandler = logging.FileHandler('my.yamllog')
   formatter = yamllogger.YAMLFormatter()
   logHandler.setFormatter(formatter)
   logger.addHandler(logHandler)


Example output
--------------

::

   - asctime: 2013-04-10 15:39:26,014
     created: 1365604766.014612
     levelname: INFO
     message: test message
     name: logger_name

.. _YAML: http://en.wikipedia.org/wiki/YAML
.. |travis_status| image:: https://secure.travis-ci.org/wewriteapps/python-yaml-logger.png
.. _travis_status: https://secure.travis-ci.org/wewriteapps/python-yaml-logger
