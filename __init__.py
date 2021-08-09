''' Util Lib holding gradescope class types
'''

import os

from .grade import Grade
from .json import JSONEncoder
from .metadata import Metadata
from .results import Results
from .testcaseabc import Testcase
from .tester import PrereqError, Tester
from .visibility import VISIBLE, AFTER_DUE, AFTER_PUBLISH, HIDDEN

PATH_CODE = "/autograder/submission"
PATH_METADATA = "/autograder/submission_metadata.json"
