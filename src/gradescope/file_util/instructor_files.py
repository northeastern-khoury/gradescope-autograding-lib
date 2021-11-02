
import re
import os
import shutil

from pathlib import Path

from .. import paths
from ..prereq import Prereq


class InstructorFiles(Prereq):
  __name__ = "InstructorFiles"

  def __init__(self,  cleanup=False, src=None, dst=None, **kwargs):
    super().__init__(**kwargs)

    if isinstance(src, str):
      src = Path(src)
    elif src is not None and not isinstance(src, Path):
      raise TypeError(f"src is not one of (None, str, Path): {type(src)}")
    if isinstance(dst, str):
      dst = Path(dst)
    elif dst is not None and not isinstance(dst, Path):
      raise TypeError(f"dst is not one of (None, str, Path): {type(dst)}")

    self._cleanup = cleanup
    self._src = src
    self._dst = dst
    self._root_dirs = []
    self._root_files = []

  def _do_cleanup(self):
    for fdir in self._root_dirs:
      shutil.rmtree(fdir)
    for file in self._root_files:
      os.remove(file)

  def exec(self):
    # print(f"InstructorFiles.exec(src={self._src}, dst={self._dst})")
    if self._src is None:
      self._src = paths.PATH_INSTRUCTOR_FILES
    if self._dst is None:
      self._dst = Path(os.getcwd())

    for src_root, dirs, files in os.walk(self._src):
      dst_root = Path(re.sub(f'^{self._src}', str(self._dst), src_root))
      src_root = Path(src_root)
      for fdir in dirs:
        if not (dst_root / fdir).is_dir():
          os.makedirs(dst_root / fdir)
        if src_root == self._src:
          self._root_dirs.append(dst_root / fdir)
      for file in files:
        shutil.copyfile(src_root / file, dst_root / file)
        if src_root == self._src:
          self._root_files.append(dst_root / file)
    return self._do_cleanup
