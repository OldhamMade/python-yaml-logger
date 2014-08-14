import sys
if sys.version_info < (2, 6):
    print(sys.stderr, "{}: need Python 2.6 or later.".format(sys.argv[0]))
    print(sys.stderror, "Your python is {}".format(sys.version))
    sys.exit(1)

from setuptools import setup, find_packages

execfile('yamlformatter/__version__.py')

setup(
    name = "python-yaml-logger",
    version = __version__,
    url = "http://github.com/OldhamMade/python-yaml-logger",
    license = "MIT",
    description = "YAML formatter for the standard Python logging module",
    author = "Phillip B Oldham",
    author_email = "phillip.oldham@gmail.com",
    packages = find_packages(exclude="specs"),
    #use_2to3 = True,
    install_requires = [
        'setuptools',
        'PyYAML',
        ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: System :: Logging',
    ]
)
