
from .abc import Prereq


class FunctionPrereq(Prereq):
  def __init__(self, func, args=None, **kwargs):
    super().__init__(**kwargs)

    self._func = func
    self._args = args

  def exec(self):
    if self._args is None:
      self._func()
    else:
      self._func(*self._args)
