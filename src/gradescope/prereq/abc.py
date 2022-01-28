
from abc import abstractmethod
from contextlib import AbstractContextManager

from .error import PrereqError


class Prereq(AbstractContextManager):
  '''
  '''

  def __init__(self, optional=False):
    if not isinstance(optional, bool):
      raise TypeError()

    self._optional = optional
    self._cleanup = None

  @abstractmethod
  def exec(self):
    ''' exec: Self -> U(None, F())
        

        Raises: Not Implemented Error if not Overridden
    '''
    raise NotImplementedError('Missing Method Override?')

  def dispatch(self, res, stack):
    self._res = res
    stack.enter_context(self)

  def __enter__(self):
    '''
    '''
    try:
      self._cleanup = self.exec()
    except PrereqError as exc:
      if not self._optional:
        raise exc
      res.add_tests(Grade(
          score=0,
          max_score=0,
          name=self.__name__,
          output=f"{exc}:\n\n{exc.stdout}",
          tags=None,
          visibility=exc.visibility,
          extra_data=None,
      ))
    return self

  def __exit__(self, exc_type, exc_cal, exc_tb):
    if exc_type is None and self._cleanup is not None:
      self._cleanup()
    self.res = None
