
from datetime import datetime

from .results import Results


class Submission:
  ''' '''
  def __init__(self,
               submission_time=None,
               score=None,
               results=None):
    if not isinstance(submission_time, datetime):
      raise TypeError()
    if not isinstance(score, float):
      raise TypeError()
    if not isinstance(results, Results):
      raise TypeError()

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
    ''' '''
    osv["submission_time"] = datetime.fromisoformat(osv["submission_time"])
    osv["score"] = float(osv["score"])
    osv["results"] = Results.decode_json(osv["results"])
    return Submission(**osv)
