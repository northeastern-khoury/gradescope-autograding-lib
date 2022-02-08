''' Util Lib holding gradescope class types
'''

import os

from .assignment import Assignment
from .grade import Grade
from .json import JSONEncoder
from .metadata import Metadata
from .results import Results
from .tester import Tester
from .user import User
from .visibility import VISIBLE, AFTER_DUE, AFTER_PUBLISH, HIDDEN

if bool(os.environ.get('DEBUG', False)):
  print(f"tester.py init: {os.getcwd()}")
