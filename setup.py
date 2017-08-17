from setuptools import setup
import distutils.command.sdist

import setuptools.command.sdist

# Patch setuptools' sdist behaviour with distutils' sdist behaviour
setuptools.command.sdist.sdist.run = distutils.command.sdist.sdist.run

dist = setup(
    # Package name:
    name="dxldomaintoolsservice",

    # Version number:
    version="0.1.0",

    # Requirements
    install_requires=[
        "domaintools_api",
        "dxlbootstrap",
        "dxlclient"
    ],

    # Package author details:
    author="McAfee LLC",

    # License
    license="Apache License 2.0",

    # Keywords
    keywords=['opendxl', 'dxl', 'mcafee', 'service', 'domaintools'],

    # Packages
    packages=[
        "dxldomaintoolsservice",
    ],

    # Details
    url="http://www.mcafee.com/",

    description="DomainTools API DXL Python service library",

    long_description=open('README').read(),

    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
)
