
class Group:
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
    self._funcs = args

  def __getattr__(self, attr):
    ''' '''
    if any(map(lambda e: not hasattr(e, attr), self._inner)):
      raise AttributeError(attr)
    def _wrapped(*args):
      return list(map(lambda e: getattr(e, attr)(*args), self._inner))
    return _wrapped
