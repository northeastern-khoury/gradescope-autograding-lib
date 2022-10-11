
class User:
  '''
  '''
  def __init__(self,
               uid=None,
               email=None,
               name=None,
               sections=None,
               sid=None,
               overrides=None,
               **kwargs):
    if len(kwargs) > 0:
      print(f"WARN: Got unexpected kwargs: {', '.join(kwargs.keys())}")

    if sections is None:
      sections = []
    try:
      uid = int(uid)
    except Exception as exc:
      raise TypeError("UID could not be coerced to int") from exc

    if not isinstance(email, str):
      raise TypeError("Email is not a str")
    if not isinstance(name, str):
      raise TypeError("Name is not a str")
    if not isinstance(sections, list) and all(map(lambda e: isinstance(e, str), sections)):
      raise TypeError("Sections is not list<str>")
    if sid is not None and not isinstance(sid, str):
      raise TypeError("SID is neither None or a str")
    if overrides is not None and not isinstance(overrides, dict):
      raise TypeError("overrides is neither None or a dict")

    self._id = uid
    self._email = email
    self._name = name
    self._sid = sid
    self._overrides = overrides

  @property
  def id(self):
    return self._id

  @property
  def email(self):
    return self._email

  @property
  def name(self):
    return self._name

  @property
  def sections(self):
    return ro(self._sections)

  @property
  def sid(self):
    return self._sid

  @property
  def overrides(self):
    return self._overrides

  def encode_json(self):
    '''
    '''
    return {
        "id":         self._id,
        "email":      self._email,
        "name":       self._name,
        "sections":   self._sections,
        "sid":        self._sid,
        "assignment": self._overrides
    }

  @staticmethod
  def decode_json(osv):
    ''' decode_json: U(dict, None) -> U(User, None)
    '''
    if osv is None:
      return None
    osv["uid"] = osv["id"]
    del osv["id"]
    osv["overrides"] = osv["assignment"]
    del osv["assignment"]
    return User(**osv)
