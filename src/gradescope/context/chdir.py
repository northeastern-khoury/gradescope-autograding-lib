
import os

from pathlib import Path

class ChDir:
  def __init__(self, fdir):
    if not isinstance(fdir, (str, Path)):
      raise TypeError(f"Given directory is neither a string or a Path: {type(fdir)}")
    fdir = Path(fdir)
    if not fdir.is_dir():
      raise RuntimeError(f"No such dir `{fdir}`; we see: {os.listdir()}")

    self._path = fdir
    self._cwd = None

  @property
  def path(self):
    return self._path

  def __enter__(self):
    self._cwd = os.getcwd()
    os.chdir(self._path)

  def __exit__(self, exc_type, exc_val, exc_tb):
    os.chdir(self._cwd)
    self._cwd = None
