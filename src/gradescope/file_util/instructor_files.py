
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

    if src is None:
      src = paths.PATH_INSTRUCTOR_FILES
    elif not isinstance(src, (str, Path)):
      raise TypeError
    if dst is None:
      dst = paths.PATH_CODE
    elif not isinstance(dst, (str, Path)):
      raise TypeError

    self._cleanup = cleanup
    self._src = Path(src)
    self._dst = Path(dst)
    self._root_dirs = []
    self._root_files = []

  def exec(self):
    # print(f"InstructorFiles.exec(src={self._src}, dst={self._dst})")
    for src_root, dirs, files in os.walk(self._src):
      dst_root = Path(re.sub(f'^{self._src}', str(self._dst), src_root))
      src_root = Path(src_root)
      for fdir in dirs:
        os.makedirs(dst_root / fdir)
        if src_root == self._src:
          self._root_dirs.append(dst_root / fdir)
      for file in files:
        shutil.copyfile(src_root / file, dst_root / file)
        self._root_files.append(dst_root / file)
    return self._do_cleanup

  def _do_cleanup(self):
    if self._cleanup:
      for fdir in self._root_dirs:
        shutil.rmtree(fdir)
      for file in self._root_files:
        os.remove(file)
