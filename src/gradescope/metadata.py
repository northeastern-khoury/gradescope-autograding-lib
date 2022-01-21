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
               assignment_id=None,
               submission_method=None,
               users=None,
               previous_submissions=None):
    if subid is None:
      raise TypeError("subid is None")
    if not isinstance(subid, int):
      raise TypeError("subid not an integer")

    if not isinstance(created_at, datetime):
      raise TypeError("created_at is None")

    if not isinstance(assignment, Assignment):
      raise TypeError("assignment not an Assignment")

    if assignment_id is not None and not isinstance(assignment_id, int):
      raise TypeError("assignment_id not None or an int")

    if submission_method is None:
      raise TypeError("submission_method is None")
    if submission_method not in SUBMISSION_METHODS:
      raise ValueError(f"invalid submission_method \"{submission_method}\";"
                       f"expecting one of: {','.join(SUBMISSION_METHODS)}")

    if users is None:
      users = []
    elif not isinstance(users, list):
      raise TypeError("users not a list")
    elif not all(map(lambda e: isinstance(e, User), users)):
      raise ValueError("Not all elements in users list User objects")

    if previous_submissions is None:
      previous_submissions = []
    elif not isinstance(previous_submissions, list):
      raise TypeError("previous_submissions not a list")

    self._id = subid
    self._created_at = created_at
    self._assignment = assignment
    self._assignment_id = assignment_id
    self._submission_method = submission_method
    self._users = users
    self._previous_submissions = previous_submissions

  @property
  def created_at(self):
    return self._created_at

  @property
  def assignment(self):
    return self._assignment

  @property
  def assignment_id(self):
    return self._assignment_id

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
        "assignment_id":        self._assignment_id,
        "submission_method":    self._submission_method,
        "users":                list(map(User.encode_json, self._users)),
        "previous_submissons":  list(map(Submission.encode_json, self._previous_submissions)),
    }

  @staticmethod
  def decode_json(osv):
    ''' decode_json: U(dict, None) -> U(Metadata, None)
    '''
    if osv is None:
      return None
    osv["subid"] = int(osv["id"])
    del osv["id"]
    osv["created_at"] = datetime.fromisoformat(osv["created_at"])
    if "assignment_id" in osv and osv["assignment_id"] is not None:
      osv["assignment_id"] = int(osv["assignment_id"])
    osv["assignment"] = Assignment.decode_json(osv["assignment"])
    osv["users"] = list(map(User.decode_json, osv["users"]))
    if "previous_submissions" in osv:
      if osv["previous_submissions"] is not None:
        osv["previous_submissions"] = list(map(Submission.decode_json, osv["previous_submissions"]))
    return Metadata(**osv)
