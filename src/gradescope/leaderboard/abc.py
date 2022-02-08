
from abc import ABC, abstractmethod

class LeaderboardEntryFactory(ABC):
  ''' '''
  def __init__(self):
    pass

  @abstractmethod
  def exec(self, res):
    ''' self -> None
        Abstract Method
        Raises: NotImplementedError if not overridden
        Run this EntryFactory and add it to res
    '''
    raise NotImplementedError('Missing Method Override?')
