
import os
import stat

from ..prereq import Prereq, PrereqError

class ExecutableFile(Prereq):
  __name__ = "ExecutableFile"

  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
    self._elfs = list(args)

  def exec(self):
    for elf in self._elfs:
      if not os.path.isfile(elf):
        raise PrereqError(f"Missing build object {elf}; build failed?")
      perms = os.stat(elf).st_mode
      os.chmod(elf, perms | stat.S_IEXEC)
