# encoding: utf-8

'''🧠 LabCAS Infosphere: the information API for the Laboratory Catalog and Archive Service'''

import importlib.resources


PACKAGE_NAME = __name__
__version__ = VERSION = importlib.resources.files(__name__).joinpath('VERSION.txt').read_text().strip()
