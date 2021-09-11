
class User:
  '''
  '''
  def __init__(self,
               uid=None,
               email=None,
               name=None):
    if not isinstance(uid, str):
      raise TypeError()
    if not isinstance(email, str):
      raise TypeError()
    if not isinstance(name, str):
      raise TypeError()

    self._id = uid
    self._email = email
    self._name = name

  @property
  def id(self):
    return self._id

  @property
  def email(self):
    return self._email

  @property
  def name(self):
    return self._name

  def encode_json(self):
    '''
    '''
    return {
        "id": self._id,
        "email": self._email,
        "name": self._name,
    }

  @staticmethod
  def decode_json(osv):
    '''
    '''
    osv["uid"] = osv["id"]
    del osv["id"]
    return User(**osv)
