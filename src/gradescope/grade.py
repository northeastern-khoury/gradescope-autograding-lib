
from warnings import warn

from .visibility import VISIBLE, VISIBILITIES

class Grade: #pylint:disable=R0902
  ''' class Grade
      <TBD>
  '''

  def __init__(self, #pylint:disable=R0913
               score=None,
               max_score=None,
               name=None,
               number=None,
               output=None,
               tags=None,
               visibility=VISIBLE,
               extra_data=None,
              ):
    if score is not None:
      try:
        score = float(score)
      except Exception as exc:
        raise TypeError() from exc

    if max_score is not None:
      try:
        max_score = float(max_score)
      except Exception as exc:
        raise TypeError() from exc

    if name is not None and not isinstance(name, str):
      raise TypeError("name is neiter None nor a str")
    if tags is None:
      tags = []
    if not isinstance(visibility, str):
      raise TypeError("visibility is not a str")
    if visibility not in VISIBILITIES:
      raise ValueError("visibility item invalid: "
                       f"\"{visibility}\" not in {VISIBILITIES}")
    if extra_data is None:
      extra_data = {}

    self._score = score
    self._max_score = max_score
    self._name = name
    self._number = number
    self._output = output
    self._tags = set(tags)
    self._visibility = visibility
    self._extra_data = extra_data

  def __repr__(self):
    msg  = '\''
    msg += self._name if self._name else "(?)"
    msg += f"[{self._number}]" if self._number else ""
    msg += ": "
    msg += f"{self._score}/{self._max_score}"
    msg += '\''
    return msg

  def __getitem__(self, key):
    if key in self._extra_data:
      return self._extra_data[key]
    raise KeyError(f"No extra data with key \"{key}\"")

  def __setitem__(self, name, val):
    self._extra_data[name] = val

  @property
  def name(self):
    ''' self -> U(str, None)
        Get the name of the current Grade object
    '''
    return self._name

  @property
  def score(self):
    ''' self -> U(float, None)
        Get the Grade's current score
    '''
    return self._score

  @score.setter
  def score(self, score):
    ''' self x float -> None
        Raises: TypeError if score not float
                UserWarning if warnings enabled and score > max_score
        Validate and store the current score
    '''
    if not isinstance(score, (int, float)):
      raise TypeError("Score type not int or float")
    self._score = score
    if score > self._max_score:
      warn(f"Assigned score for {self._name} greater than max"
           f"({score:.2d} > {self._max_score}")

  @property
  def output(self):
    ''' self -> str
        Return the current output
    '''
    return self._output

  @output.setter
  def output(self, output):
    ''' self x str -> None
        Raises: TypeError if score is not str
        Stores the new output
    '''
    self._output = output

  @property
  def max_score(self):
    ''' self -> float
        Get the max score for this Grade
    '''
    return self._max_score

  @max_score.setter
  def max_score(self, max_score):
    ''' self x float -> None
        Raises: TypeError if max_score not float
        Validate and store the current max_score
    '''
    if not isinstance(max_score, (int, float)):
      raise TypeError("Score type not int or float")
    self._max_score = max_score

  def encode_json(self):
    ''' self -> dict
        Local lib JSONEncoder hook
        Returns a JSON-lib compatible dict representation of this Grade
    '''
    s_map = {}
    if self._score is not None:
      s_map["score"] = self._score
    if self._max_score is not None:
      s_map["max_score"] = self._max_score
    if self._name is not None:
      s_map["name"] = self._name
    if self._number is not None:
      s_map["number"] = self._number
    if self._output is not None:
      s_map["output"] = self._output
    if len(self._tags) > 0:
      s_map["tags"] = list(self._tags)
    s_map["visibility"] = self._visibility
    if len(self._extra_data) > 0:
      s_map["extra_data"] = self._extra_data
    return s_map

  @staticmethod
  def decode_json(osv):
    ''' decode_json: U(dict, None) -> U(Grade, None)
    '''
    if osv is None:
      return None
    return Grade(osv)
