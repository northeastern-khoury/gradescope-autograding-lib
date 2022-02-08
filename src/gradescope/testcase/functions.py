
from .abc import Testcase

from ..grade import Grade

class FunctionTestcase(Testcase):
  def __init__(self,
               func,
               args=None,
               **kwargs):
    super().__init__(**kwargs)

    if not callable(func):
      raise ValueError(f"Given a non-function object: {func}")
    if args is not None and not hasattr(args, '__iter__'):
      raise ValueError(f"Given a non-array args list: {type(args)}")
    if args is None:
      args = ()

    self._func = func
    self._args = args

  def exec(self, res):
    ''' self -> None
        Grade this Testcase
    '''
    pct, output = self._func(*self._args)
    res.add_tests(Grade(
        score=pct * self._max_score,
        max_score=(0 if self._extra_credit else self._max_score),
        name=self.__name__,
        number=self._number,
        output=output,
        tags=None,
        visibility=self._visibility,
        extra_data=None,
    ))
