
import os

from pathlib import Path

from ..prereq import Prereq


class ChDir(Prereq):
  def __init__(self, fdir, **kwargs):
    super().__init__(**kwargs)
    if not isinstance(fdir, (str, Path)):
      raise TypeError(f"Given directory is neither a string or a Path: {type(fdir)}")
    self._path = Path(fdir)
    self._cwd = None

  @property
  def path(self):
    return self._path

  def _do_cleanup(self):
    os.chdir(self._cwd)
    self._cwd = None

  def exec(self):
    if not self._path.is_dir():
      raise RuntimeError(f"No such dir `{self._path}`; we see: {os.listdir()}")
    self._cwd = os.getcwd()
    os.chdir(self._path)
    return self._do_cleanup
