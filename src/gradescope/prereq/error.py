
from ..visibility import HIDDEN, VISIBLE, VISIBILITIES

class PrereqError(RuntimeError):
  def __init__(self, *args, stdout=None, visibility=VISIBLE, stdout_visibility=HIDDEN, **kwargs):
    super().__init__(*args, **kwargs)

    if visibility not in VISIBILITIES:
      raise ValueError(f"Unknown visibility \"{visibility}\" for key 'visibility'")
    if stdout_visibility not in VISIBILITIES:
      raise ValueError(f"Unknown visibility \"{stdout_visibility}\" for key 'visibility'")

    self._stdout = str(stdout)
    self._stdout_visibility = stdout_visibility
    self._visibility = visibility

  @property
  def stdout(self):
    return self._stdout

  @property
  def visibility(self):
    return self._visibility

  @property
  def stdout_visibility(self):
    return self._stdout_visibility
