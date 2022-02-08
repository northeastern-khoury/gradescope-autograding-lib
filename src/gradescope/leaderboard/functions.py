
from .abc import LeaderboardEntryFactory
from .orders import ORDER_ASCENDING, ORDER_DESCENDING

class LbEntryFunction(LeaderboardEntryFactory):
  ''' '''

  def __init__(self,
               func,
               args=None,
               name=None,
               order=ORDER_ASCENDING,
               **kwargs):
    super().__init__(**kwargs)
    if not isinstance(name, str):
      raise TypeError("name is not a str")
    if order not in (ORDER_ASCENDING, ORDER_DESCENDING):
      raise ValueError("order item invalid: "
                      f"\"{order}\" not in {(ORDER_ASCENDING, ORDER_DESCENDING)}")

    if not callable(func):
      raise ValueError(f"Given a non-function object: {func}")
    if args is None:
      args = ()

    self.__name__ = name
    self._order = order
    self._func = func
    self._args = args

  def exec(self, res):
    ''' self -> None
        Produce this LeaderboardEntry and add it to the given Results object
    '''
    res.leaderboard[self.__name__] = self._func(*self._args)
    res.leaderboard[self.__name__].order = self._order
