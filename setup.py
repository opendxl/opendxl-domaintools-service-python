from setuptools import setup
import distutils.command.sdist

import setuptools.command.sdist

# Patch setuptools' sdist behaviour with distutils' sdist behaviour
setuptools.command.sdist.sdist.run = distutils.command.sdist.sdist.run

VERSION = __import__('dxldomaintoolsservice').get_version()

dist = setup(
    # Package name:
    name="dxldomaintoolsservice",

    # Version number:
    version=VERSION,

    # Requirements
    install_requires=[
        "domaintools_api",
        "dxlbootstrap",
        "dxlclient"
    ],

    # Package author details:
    author="",

    # License
    license="",

    # Keywords
    keywords=[],

    # Packages
    packages=[
        "dxldomaintoolsservice",
    ],

    # Details
    url="",

    description="",

    long_description=open('README').read(),

    classifiers=[
        "Programming Language :: Python"
    ],
)
