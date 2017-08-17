from __future__ import absolute_import

from .app import DomainToolsService

import pkg_resources

__version__ = pkg_resources.require("dxldomaintoolsservice")[0].version

def get_version():
    """
    Returns the version of the package

    :return: The version of the package
    """
    return __version__
