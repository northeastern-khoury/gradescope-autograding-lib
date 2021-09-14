
from datetime import datetime

class Assignment:
  ''' '''
  def __init__(self,
               asgnid=None,
               course_id=None,
               title=None,
               release_date=None,
               due_date=None,
               late_due_date=None,
               outline=None,
               total_points=None,
               group_submission=None,
               group_size=None):
    if asgnid is None:
      try:
        asgnid = int(asgnid)
      except Exception as exc:
        raise TypeError("Could not coerce asgnid to int")

    if course_id is not None:
      try:
        course_id = int(course_id)
      except Exception as exc:
        raise TypeError("Could not coerce course_id to int")

    if total_points is not None:
      try:
        total_points = float(total_points)
      except Exception as exc:
        raise TypeError("Could not coerce total_points to float")

    if group_size is not None:
      try:
        group_size = int(group_size)
      except Exception as exc:
        raise TypeError("Could not coerce group_size to int")

    if not isinstance(title, str):
      raise TypeError("title is not a str")
    if not isinstance(release_date, datetime):
      raise TypeError("release_date is not a datetime")
    if not isinstance(due_date, datetime):
      raise TypeError("due_date is not a datetime")
    if late_due_date is not None and not isinstance(late_due_date, datetime):
      raise TypeError("late_due_date is neither None or a datetime")
    if outline is not None and not isinstance(outline, list):
      raise TypeError("outline is neither None nor a list")
    if not isinstance(group_submission, bool):
      raise TypeError("group_submission is not a bool")

    self._id = asgnid
    self._course_id = course_id
    self._title = title
    self._release_date = release_date
    self._due_date = due_date
    self._late_due_date = late_due_date
    self._outline = outline
    self._total_points = total_points
    self._group_submission = group_submission
    self._group_size = group_size

  def encode_json(self):
    ''' '''
    return {
        "id":               self._id,
        "course_id":        self._course_id,
        "title":            self._title,
        "release_date":     self._release_date.isoformat(),
        "due_date":         self._due_date.isoformat(),
        "late_due_date":    self._late_due_date.isoformat(),
        "outline":          self._outline,
        "total_points":     self._total_points,
        "group_submission": self._group_submission,
        "group_size":       self._group_size,
    }

  @staticmethod
  def decode_json(osv):
    ''' '''
    osv["asgnid"] = osv["id"]
    del osv["id"]
    osv["release_date"] = datetime.fromisoformat(osv["release_date"])
    osv["due_date"] = datetime.fromisoformat(osv["due_date"])
    if osv["late_due_date"] is not None:
      osv["late_due_date"] = datetime.fromisoformat(osv["late_due_date"])
    osv["total_points"] = float(osv["total_points"])
    return Assignment(**osv)
