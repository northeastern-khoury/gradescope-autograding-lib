
from .abc import Testcase

from ..grade import Grade
from ..visibility import VISIBLE, VISIBILITIES


class FunctionTestcase(Testcase):
  def __init__(self,
               func,
               args=None,
               name=None,
               number=None,
               max_score=0.0,
               visibility=VISIBLE,
               extra_credit=False,
               **kwargs):
    super().__init__(**kwargs)
    if name is not None and not isinstance(name, str):
      raise ValueError
    if isinstance(max_score, int):
      max_score = float(max_score)
    elif max_score is not None and not isinstance(max_score, float):
      raise TypeError()
    if visibility not in VISIBILITIES:
      raise ValueError("visibility item invalid: "
                       f"\"{visibility}\" not in {VISIBILITIES}")

    if not callable(func):
      raise ValueError(f"Given a non-function object: {func}")

    self.__name__ = name

    self._number = number
    self._max_score = max_score
    self._visibility = visibility
    self._extra_credit = extra_credit

    self._func = func
    self._args = args

  def exec(self, res):
    ''' self -> Grade
        Grade this Testcase
    '''
    pct, output = self._func() if self._args is None else self._func(*self._args)
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
