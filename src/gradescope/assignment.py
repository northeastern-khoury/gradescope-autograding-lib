
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
    if asgnid is None and not isinstance(asgnid, int):
      raise TypeError()
    if not isinstance(course_id, int):
      raise TypeError()
    if not isinstance(title, str):
      raise TypeError()
    if not isinstance(release_date, datetime):
      raise TypeError()
    if not isinstance(due_date, datetime):
      raise TypeError()
    if late_due_date is not None and not isinstance(late_due_date, datetime):
      raise TypeError()
    if outline is not None and not isinstance(outline, list):
      raise TypeError()
    if not isinstance(total_points, int) and not isinstance(total_points, float):
      raise TypeError()
    if not isinstance(group_submission, bool):
      raise TypeError()
    if group_size is not None and not isinstance(group_size, int):
      raise TypeError()

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
