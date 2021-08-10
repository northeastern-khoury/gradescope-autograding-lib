
import json

class JSONEncoder(json.JSONEncoder):
  ''' class JSONEncoder
      inherits json.JSONEncoder
      overrides json.JSONEncoder::default
      For lib-local classes, checks if it has an encoding func (`encode_json`)
      If so, performs json encoding on the output of that function
      Otherwise, behaves as super-class
  '''
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def default(self, o):
    encode = getattr(o, "encode_json", None)
    if callable(encode):
      return encode()
    return o
