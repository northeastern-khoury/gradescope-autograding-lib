
import json
import time

from .leaderboard import Leaderboard

from .. import paths
from ..grade import Grade
from ..json import JSONEncoder
from ..prereq import Prereq
from ..visibility import HIDDEN, VISIBLE, VISIBILITIES


class _ResultTimer(Prereq):
  def __init__(self, target, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._res = target

  def exec(self):
    self._res.start_time()
    return self._res.end_time

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
               extra_data=None
              ):
    if score is not None:
      try:
        score = float(score)
      except Exception as exc:
        raise TypeError("score is none of None, an int, or a float") from exc
    if execution_time is not None:
      try:
        execution_time = int(execution_time)
      except Exception as exc:
        raise TypeError("execution_time is none of None, an int, or a float") from exc
    if not (output is None or isinstance(output, str)):
      raise TypeError("output is neither None nor a str")

    if visibility is not None:
      if not isinstance(visibility, str):
        raise TypeError("Visibility tag is neither None nor a string")
      if visibility not in VISIBILITIES:
        raise ValueError(f"Unknown visibility tag for 'visibility': \"{visibility}\"")

    if stdout_visibility is not None:
      if not isinstance(stdout_visibility, str):
        raise TypeError("Stdout visibility tag is neither None nor a string")
      if stdout_visibility not in VISIBILITIES:
        raise ValueError(f"Unknown visibility tag for 'stdout_visibility': \"{visibility}\"")

    if tests is None:
      tests = []
    elif isinstance(tests, list):
      tests = tests.copy()
    else:
      raise TypeError("tests is neither None nor a list")

    if leaderboard is not None and not isinstance(leaderboard, Leaderboard):
      raise TypeError("leaderboard is neither a Leaderboard or None")

    if extra_data is None:
      extra_data = {}
    elif not isinstance(extra_data, dict):
      raise TypeError("extra_data is neitehr None nor a dict")

    self._extra_data        = extra_data.copy()
    self._execution_time    = execution_time
    self._leaderboard       = leaderboard
    self._output            = output
    self._score             = score
    self._stdout_visibility = stdout_visibility
    self._tests             = tests
    self._visibility        = visibility

    self._start_time        = None

  @property
  def tests(self):
    return self._tests

  @property
  def leaderboard(self):
    if self._leaderboard is None:
      self._leaderboard = Leaderboard()
    return self._leaderboard

  @property
  def timer_context(self):
    return _ResultTimer(self)

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
    if self._start_time is None:
      raise RuntimeError("start_time() not yet called!")
    self._execution_time = time.time() - self._start_time
    self._start_time = None

  def add_tests(self, res):
    if not isinstance(res, list):
      if hasattr(res, '__iter__'):
        res = list(res)
      else:
        res = [ res ]
    if any(map(lambda g: not isinstance(g, Grade), res)):
      raise TypeError("res is not a Result or Iterable of Results")
    self._tests += res

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
    if self._visibility is not None:
      s_obj["visibility"] = self._visibility
    if self._stdout_visibility is not None:
      s_obj["stdout_visibility"] = self._stdout_visibility
    if len(self._extra_data) > 0:
      s_obj["extra_data"] = self._extra_data
    if self._tests is not None:
      s_obj["tests"] = self._tests
    if self._leaderboard is not None and len(self._leaderboard) > 0:
      s_obj["leaderboard"] = self._leaderboard

    return s_obj

  def save(self):
    ''' save : self -> None
        EFFECT: Writes this object as a json object to drive at .paths.PATH_RESULTS
    '''
    with open(paths.PATH_RESULTS, 'w') as rfp:
      json.dump(self, rfp, cls=JSONEncoder)

  @staticmethod
  def decode_json(osv):
    ''' decode_json: U(dict, None) -> U(Results, None)
    '''
    if osv is None:
      return None
    if "leaderboard" in osv:
      objs = osv["leaderboard"]
      osv["leaderboard"] = Leaderboard()
      for val in objs:
        key = val["name"]
        if "value" not in val:
          raise ValueError("Missing mandatory")
        osv["leaderboard"][key] = val["value"]
        if "order" in val:
          osv["leaderboard"][key].order = val["order"]
    return Results(**osv)
