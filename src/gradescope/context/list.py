
class ListContext:
  def __init__(self, managers):
    if not isinstance(managers, list):
      raise TypeError

    self._managers = managers.copy()
    self._ctx = []

  def __enter__(self):
    for manager in self._managers:
      manager.__enter__()
      self._ctx.append(manager)

  def __exit__(self, exc_type, exc_val, exc_tb):
    while len(self._ctx) > 0:
      self._ctx.pop().__exit__(exc_type, exc_val, exc_tb)
