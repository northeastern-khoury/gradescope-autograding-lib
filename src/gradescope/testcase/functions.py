
import sys

from .abc import Testcase

from ..grade import Grade
from ..visibility import VISIBLE, VISIBILITIES


class FunctionTestcase(Testcase):
  def __init__(self,
               func,
               args=None,
               **kwargs):
    super().__init__(**kwargs)
    self._func = func
    self._args = args

  def exec(self, res):
    ''' self -> Grade
        Grade this Testcase
    '''
    try:
      pct, output = self._func() if self._args is None else self._func(*self._args)
    except AssertionError as exc:
      pct, output = 0.0, str(exc)
    except Exception as exc:
      sys.stdout.write(str(exc).encode())
      pct, output = 0.0, f"Inner exception on testcase {self.__name__}. Please reach out to course staff for assistance"
    finally:
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
