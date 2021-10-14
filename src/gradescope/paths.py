
import os

from pathlib import Path


# Default Paths
ROOT_PATH             = Path('/autograder')
PATH_CODE             = ROOT_PATH / 'submission'
PATH_INSTRUCTOR_FILES = ROOT_PATH / 'instructor_files'
PATH_RESULTS          = ROOT_PATH / 'results' / 'results.json'
PATH_METADATA         = ROOT_PATH / 'submission_metadata.json'

# Load Paths from ENV
def reload():
  ''' reload: None -> None
      AFFECT: changes the values of all PATH variables
  '''
  global ROOT_PATH, PATH_CODE, PATH_INSTRUCTOR_FILES, PATH_RESULTS, PATH_METADATA #pylint:disable=W0603
  ROOT_PATH             = Path(os.getenv('AUTOGRADER_ROOT',
                                         str(ROOT_PATH)))
  PATH_CODE             = Path(os.getenv('PATH_CODE',
                                         str(ROOT_PATH / 'submission')))
  PATH_INSTRUCTOR_FILES = Path(os.getenv('PATH_INSTRUCTOR_FILES',
                                         str(ROOT_PATH / 'instructor_files')))
  PATH_RESULTS          = Path(os.getenv('PATH_RESULTS',
                                         str(ROOT_PATH / 'results' / 'results.json')))
  PATH_METADATA         = Path(os.getenv('PATH_METADATA',
                                         str(ROOT_PATH / 'submission_metadata.json')))

# Load on first startup
reload()
