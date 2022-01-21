
from datetime import datetime

from .results import Results


class Submission:
  ''' '''
  def __init__(self,
               submission_time=None,
               score=None,
               results=None):
    try:
      score = float(score)
    except Exception as exc:
      raise TypeError("score could not be coerced to float") from exc
    if not isinstance(submission_time, datetime):
      raise TypeError("submission_time not a datetime")
    if results is not None and not isinstance(results, Results):
      raise TypeError("results is not a Results object")

    self._submission_time = submission_time
    self._score = score
    self._results = results

  def encode_json(self):
    ''' '''
    return {
        "submission_time":  self._submission_time.isoformat(),
        "score":            self._score,
        "results":          list(map(Results.encode_json, self._results)),
    }

  @staticmethod
  def decode_json(osv):
    ''' decode_json: U(dict, None) -> U(Submission, None)
    '''
    if osv is None:
      return None
    osv["submission_time"] = datetime.fromisoformat(osv["submission_time"])
    osv["score"] = float(osv["score"])
    osv["results"] = Results.decode_json(osv["results"])
    return Submission(**osv)
