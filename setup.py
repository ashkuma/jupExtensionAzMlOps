import os
import re
from codecs import open
from setuptools import setup, find_packages


NAME = "AZMLDEMO"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["PyGithub"
]

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'License :: OSI Approved :: MIT License',
]


# Version extraction inspired from 'requests'
with open(os.path.join('.', 'version.py'), 'r') as fd:
    VERSION = re.search(r'^VERSION\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)
    print(VERSION)

setup(
    name=NAME,
    version=VERSION,
    description="Extension for ML ops",
    long_description=" No description for now",
    license='MIT',
    author="Microsoft",
    author_email="VSTS_Social@microsoft.com",
    url=" ",
    classifiers=CLASSIFIERS,
    package_data={},
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
    include_package_data=True,
    install_requires=REQUIRES
)