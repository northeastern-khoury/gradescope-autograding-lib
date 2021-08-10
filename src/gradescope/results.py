

import json

from warnings import warn

from .leaderboard import Leaderboard
from .visibility import HIDDEN, VISIBLE

class Results:
  ''' class Results
      <TBD>
  '''

  def __init__(self, #pylint:disable=R0913
               score=None,
               execution_time=None,
               output=None,
               visibility=VISIBLE,
               stdout_visibility=HIDDEN,
               tests=None,
               leaderboard=None,
               extra_data=None,
               **kwargs,
              ):

    if tests is None:
      tests = []
    else:
      tests = tests.copy()
    if leaderboard is None:
      leaderboard = Leaderboard()
    elif isinstance(leaderboard, Leaderboard):
      leaderboard = leaderboard.copy()
    else:
      raise ValueError("leaderboard not a Leaderboard")
    if extra_data is None:
      extra_data = {}

    if len(kwargs) > 0:
      warn(f"Unknown arg keys: {kwargs.keys()}")

    self._score = score
    self._execution_time = execution_time
    self._output = output
    self._visibility = visibility
    self._stdout_visibility = stdout_visibility
    self._extra_data = extra_data

  def __getitem__(self, name):
    if name in self._extra_data:
      return self._extra_data[name]
    raise AttributeError(f"No item in Result data with key: {name}")

  def __setitem__(self, name, val):
    self._extra_data[name] = val

  def encode_json(self):
    '''
    '''
    s_map = {}
    if self._score is not None:
      s_map["score"] = self._score
    return s_map

  @staticmethod
  def decode_json(osv):
    '''
    '''
    return Results(**json.loads(osv))
