
class User:
  '''
  '''
  def __init__(self,
               uid=None,
               email=None,
               name=None,
               sid=None,
               overrides=None):
    if not isinstance(uid, int):
      raise TypeError()
    if not isinstance(email, str):
      raise TypeError()
    if not isinstance(name, str):
      raise TypeError()
    if sid is not None and not isinstance(sid, str):
      raise TypeError()
    if overrides is not None and not isinstance(overrides, dict):
      raise TypeError()

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
        "sid":        self._sid,
        "assignment": self._overrides
    }

  @staticmethod
  def decode_json(osv):
    '''
    '''
    osv["uid"] = osv["id"]
    del osv["id"]
    osv["overrides"] = osv["assignment"]
    del osv["assignment"]
    return User(**osv)
