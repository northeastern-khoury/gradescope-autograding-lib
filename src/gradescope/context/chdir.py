
import os

from pathlib import Path

class ChDir:
  def __init__(self, fdir):
    if not isinstance(fdir, (str, Path)):
      raise TypeError
    fdir = Path(fdir)
    if not fdir.is_dir():
      raise RuntimeError

    self._path = fdir
    self._cwd = None

  @property
  def path(self):
    return self._path

  def __enter__(self):
    # print(f"ChDir({self._path}).__enter__")
    self._cwd = os.getcwd()
    os.chdir(self._path)

  def __exit__(self, exc_type, exc_val, exc_tb):
    # print(f"ChDir({self._path}).__exit__")
    os.chdir(self._cwd)
    self._cwd = None
