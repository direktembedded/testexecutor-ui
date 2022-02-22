import os
te_current_path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(te_current_path, 'VERSION')) as version_file:
    VERSION = version_file.read().strip()

__version__ = VERSION
