
from abc import ABC, abstractmethod

from .error import PrereqError


class Prereq(ABC):
  '''
  '''

  def __init__(self, optional=False):
    if not isinstance(optional, bool):
      raise TypeError()

    self._optional = optional
    self._cleanup = None

  @abstractmethod
  def exec(self):
    '''
    '''
    raise NotImplementedError('Missing Method Override?')

  def __enter__(self):
    '''
    '''
    try:
      self._cleanup = self.exec()
    except PrereqError as exc:
      if self._optional:
        #TODO: Logging of some form
        pass
      else:
        raise exc
    return self

  def __exit__(self, exc_type, exc_cal, exc_tb):
    if exc_type is None and self._cleanup is not None:
      self._cleanup()
