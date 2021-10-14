
from .abc import Testcase

class FunctionTestcase(Testcase):
  def __init__(self, func, args=None, **kwargs):
    super().__init__(**kwargs)
    if not callable(func):
      raise ValueError(f"Given a non-function object: {func}")

    self._func = func
    self._args = args

  def exec(self):
    if self._args is None:
      return self._func()
    return self._func(*self._args)
