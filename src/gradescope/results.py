
import json
import time

from .grade import Grade
from .json import JSONEncoder
from .leaderboard import Leaderboard
from .paths import PATH_RESULTS
from .visibility import HIDDEN, VISIBLE, VISIBILITIES

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
              ):
    if not (score is None or isinstance(score, (int, float))):
      raise TypeError()
    if not (execution_time is None or isinstance(execution_time, int)):
      raise TypeError()
    if not (output is None or isinstance(output, str)):
      raise TypeError()

    if not (visibility is None or isinstance(visibility, str)):
      raise TypeError()
    if visibility not in VISIBILITIES:
      raise ValueError()

    if not (stdout_visibility is None or isinstance(stdout_visibility, str)):
      raise TypeError()
    if stdout_visibility not in VISIBILITIES:
      raise ValueError()

    if tests is None:
      tests = []
    elif isinstance(tests, list):
      tests = tests.copy()
    else:
      raise TypeError()

    if leaderboard is None:
      leaderboard = Leaderboard()
    elif isinstance(leaderboard, Leaderboard):
      leaderboard = leaderboard.copy()
    else:
      raise TypeError("leaderboard not a Leaderboard")

    if extra_data is None:
      extra_data = {}
    elif not isinstance(extra_data, dict):
      raise TypeError()

    if len(kwargs) > 0:
      warn(f"Unknown arg keys: {kwargs.keys()}")

    self._execution_time    = execution_time
    self._extra_data        = extra_data.copy()
    self._output            = output
    self._score             = score
    self._start_time        = None
    self._stdout_visibility = stdout_visibility
    self._tests             = tests
    self._visibility        = visibility

  @property
  def leaderboard(self):
    return self._leaderboard

  def __getitem__(self, name):
    if name in self._extra_data:
      return self._extra_data[name]
    raise AttributeError(f"No item in Result data with key: {name}")

  def __setitem__(self, name, val):
    self._extra_data[name] = val

  def start_time(self):
    if self._start_time is not None:
      raise RuntimeError("start_time() already called!")
    self._start_time = time.time()

  def end_time(self):
    if self._start_time is not None:
      raise RuntimeError("start_time() not yet called!")
    self._execution_time = time.time() - self._start_time
    self._start_time = None

  def add_test(self, res):
    if not isinstance(res, Grade):
      raise TypeError()
    self._tests.append(res)

  def encode_json(self):
    '''
    '''
    s_obj = {}

    if self._score is not None:
      s_obj["score"] = self._score
    if self._execution_time is not None:
      s_obj["execution_time"] = self._execution_time
    if self._output is not None:
      s_obj["output"] = self._output
    if self._tests is not None:
      s_obj["tests"] = self._tests
    if len(self._extra_data) > 0:
      s_obj["extra_data"] = self._extra_data

    return s_obj

  def save(self):
    ''' save : self -> None
        EFFECT: Writes this object as a json object to drive at .paths.PATH_RESULTS
    '''
    with open(PATH_RESULTS, 'w') as rfp:
      json.dump(self, rfp, cls=JSONEncoder)

  @staticmethod
  def decode_json(osv):
    '''
    '''
    return Results(**osv)
