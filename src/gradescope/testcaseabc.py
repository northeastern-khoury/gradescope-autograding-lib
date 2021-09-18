
from abc import ABC, abstractmethod

from .grade import Grade
from .visibility import VISIBLE, VISIBILITIES

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

    self._name = name
    self._number = number
    self._max_score = max_score
    self._visibility = visibility
    self._extra_credit = extra_credit

  @property
  def name(self):
    return self._name

  @abstractmethod
  def exec(self, max_score=None):
    ''' self x (float)max_score -> float x U(None, str)
        Abstract Method
        Raises: NotImplementedError if not overridden
        Run this Grade and produce a grade
    '''
    raise NotImplementedError('Missing Method Override?')

  def grade(self):
    ''' self -> Grade
        Grade this test case
    '''
    pct, output = self.exec(max_score=self._max_score)
    return Grade(
        score=pct * self._max_score,
        max_score=(0 if self._extra_credit else self._max_score),
        name=self._name,
        number=self._number,
        output=output,
        tags=None,
        visibility=self._visibility,
        extra_data=None,
      )
