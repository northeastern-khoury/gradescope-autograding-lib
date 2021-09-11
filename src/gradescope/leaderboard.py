
ORDER_ASCENDING = "asc"
ORDER_DESCENDING = "desc"

class _LeaderboardElem:
  ''' '''

  def __init__(self,
               value=None,
               order=ORDER_DESCENDING):
    if not isinstance(order, str):
      raise TypeError()
    if order not in (ORDER_ASCENDING, ORDER_DESCENDING):
      raise ValueError()
    self._value = value
    self._order = order

  @property
  def order(self):
    ''' '''
    return self._order

  @order.setter
  def order(self, val):
    ''' '''
    if not isinstance(val, str):
      raise TypeError()
    if val not in (ORDER_ASCENDING, ORDER_DESCENDING):
      raise TypeError()
    self._order = val

  @property
  def value(self):
    ''' '''
    return self._value

  @value.setter
  def value(self, val):
    self._value = val

class Leaderboard:
  ''' '''

  def __init__(self):
    self._elems = {}

  def __len__(self):
    return len(self._elems)

  def __getitem__(self, key):
    return self._elems[key]

  def __setitem__(self, key, val):
    if key not in self._elems:
      self._elems[key] = _LeaderboardElem()
    self._elems[key].value = val

  def __delitem__(self, key):
    del self._elems[key]

  def __contains__(self, key):
    return key in self._elems

  def encode_json(self):
    ''' '''
    def _make_json_elem(key, val):
      elm = {
          "name": key,
          "value": val.value,
      }
      if val.order != ORDER_DESCENDING:
        elm["order"] = val.order
      return elm
    return map(_make_json_elem, self._elems.items())

  @staticmethod
  def decode_json(osv):
    ''' '''
    if not isinstance(osv, list):
      raise TypeError()
    lbrd = Leaderboard()
    for obj in osv:
      lbrd[obj["name"]] = obj["value"]
      if "order" in obj:
        lbrd[obj["name"]].order = obj["order"]
    return lbrd
