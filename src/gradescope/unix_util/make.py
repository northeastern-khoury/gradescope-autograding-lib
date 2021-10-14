
import subprocess
import traceback

from ..prereq import Prereq, PrereqError

from ..visibility import VISIBLE


class Make(Prereq):
  ''' '''
  __name__ = "Make"

  def __init__(self, *args, clean_after=False, **kwargs):
    super().__init__(**kwargs)

    self._args = list(args)
    self._clean_after = clean_after

  @staticmethod
  def _call(*args, stderr=subprocess.DEVNULL):
    args = list(args)
    args.insert(0, 'make')

    make = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=stderr)
    out = make.communicate()[0].decode()
    return (out, make.returncode)

  def exec(self):
    # print(f"Make.exec({self._args}){{{os.listdir()}}}")
    try:
      out, ret = Make._call(*self._args, stderr=subprocess.STDOUT)
    except OSError as exc:
      output = "Make failed with exit code -1"
      raise PrereqError(output) from exc
    else:
      print(out)
      if ret != 0:
        output = f"Make failed with exit code {ret}"
        raise PrereqError(output, stdout=out, stdout_visibility=VISIBLE)

  def __exit__(self, exc_type, exc_val, exc_tb):
    # print(f"Make.__exit__(type={exc_type}, val={exc_val}, tb=...)")
    if exc_val is None and self._clean_after:
      try:
        Make._call("clean")
      except:
        traceback.print_exc()
