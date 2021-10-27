
from abc import ABC, abstractmethod

class Testcase(ABC):
  '''
  '''

  def __init__(self):
    pass

  @abstractmethod
  def exec(self, res):
    ''' self -> float x U(None, str)
        Abstract Method
        Raises: NotImplementedError if not overridden
        Run this Testcase and produce a grade
    '''
    raise NotImplementedError('Missing Method Override?')
