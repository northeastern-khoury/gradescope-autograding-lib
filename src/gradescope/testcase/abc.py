
from abc import ABC, abstractmethod

from ..grade import Grade
from ..visibility import VISIBLE, VISIBILITIES

class Testcase(ABC):
  '''
  '''

  def __init__(self,
               name=None,
               number=None,
               max_score=0.0,
               visibility=VISIBLE,
               extra_credit=False,
              ):
    if name is not None and not isinstance(name, str):
      raise ValueError
    if isinstance(max_score, int):
      max_score = float(max_score)
    elif max_score is not None and not isinstance(max_score, float):
      raise TypeError()
    if visibility not in VISIBILITIES:
      raise ValueError("visibility item invalid: "
                       f"\"{visibility}\" not in {VISIBILITIES}")

    self.__name__ = name

    self._number = number
    self._max_score = max_score
    self._visibility = visibility
    self._extra_credit = extra_credit

  @abstractmethod
  def exec(self, res):
    ''' self -> float x U(None, str)
        Abstract Method
        Raises: NotImplementedError if not overridden
        Run this Testcase and produce a grade
    '''
    raise NotImplementedError('Missing Method Override?')

  def _run(self, res):
    ''' self -> Grade
        Grade this Testcase
    '''
    try:
      self.exec(res)
    except AssertionError as exc:
      res.add_tests(Grade(
          score=0,
          max_score=self._max_score,
          name=self.__name__,
          number=self._number,
          output=str(exc),
          tags=None,
          visibility=self._visibility,
          extra_data=None,
      ))
