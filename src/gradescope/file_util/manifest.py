
import os

from ..prereq import Prereq, PrereqError

class Manifest(Prereq):
  ''' '''
  __name__ = "Manifest"

  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

    self._manifest = args

  def exec(self):
    # print(f"Manifest.exec({self._manifest})")
    missing = list(filter((lambda fname: not os.path.isfile(fname)), self._manifest))
    if len(missing) > 0:
      list_missing = ', '.join(map(lambda e: f"'{e}'", missing))
      output = f"Your submission appears to be missing the files {list_missing}\n" \
               f"We see: {os.listdir()}"
      raise PrereqError(output)
