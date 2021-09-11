from datetime import datetime

from .assignment import Assignment
from .submission import Submission
from .user import User


SUB_UPLOAD = "upload"
SUB_GITHUB = "GitHub"
SUB_BITBUCKET = "Bitbucket"
SUBMISSION_METHODS = [ SUB_UPLOAD, SUB_GITHUB, SUB_BITBUCKET ]


class Metadata:
  ''' '''
  def __init__(self,
               subid=None,
               created_at=None,
               assignment=None,
               submission_method=None,
               users=None,
               previous_submissons=None):
    if subid is None:
      raise TypeError("subid is None")
    if not isinstance(created_at, datetime):
      raise TypeError("created_at is None")
    if not isinstance(assignment, Assignment):
      raise TypeError()
    if submission_method is None:
      raise TypeError("submission_method is None")
    if submission_method not in SUBMISSION_METHODS:
      raise ValueError(f"invalid submission_method \"{submission_method}\";"
                       f"expecting one of: {','.join(SUBMISSION_METHODS)}")
    if not isinstance(users, list):
      raise TypeError("users not a list")
    if not all(map(lambda e: isinstance(e, User), users)):
      raise ValueError("Not all elements in users list User objects")
    if previous_submissons is not None and not isinstance(previous_submissons, list):
      raise TypeError("previous_submissons not a list")

    self._id = int(subid)
    self._created_at = created_at
    self._assignment = assignment
    self._submission_method = submission_method
    self._users = users
    self._previous_submissions = previous_submissons

  @property
  def created_at(self):
    return self._created_at

  @property
  def assignment(self):
    return self._assignment

  @property
  def submission_method(self):
    return self._submission_method

  @property
  def users(self):
    return self._users

  @property
  def previous_submissions(self):
    return self._previous_submissions

  def encode_json(self):
    '''
    '''
    return {
        "id":                   self._id,
        "created_at":           self._created_at.isoformat(),
        "assignment":           self._assignment.encode_json(),
        "submission_method":    self._submission_method,
        "users":                map(User.encode_json, self._users),
        "previous_submissons":  map(Submission.encode_json, self._previous_submissions),
    }

  @staticmethod
  def decode_json(osv):
    '''
    '''
    osv["subid"] = osv["id"]
    del osv["id"]
    osv["created_at"] = datetime.fromisoformat(osv["created_at"])
    osv["assignment"] = Assignment.decode_json(osv["assignment"])
    osv["users"] = list(map(User.decode_json, osv["users"]))
    if "previous_submissons" in osv:
      osv["previous_submissons"] = map(Submission.decode_json, osv["previous_submissons"])
    return Metadata(**osv)
