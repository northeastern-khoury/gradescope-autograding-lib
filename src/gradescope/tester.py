
from .paths import PATH_METADATA
from .results import Results
from .testcaseabc import Testcase
from .visibility import VISIBLE


class PrereqError(RuntimeError):
  def __init__(self, *args, visibility=VISIBLE, **kwargs):
    super().__init__(*args, **kwargs)
    self._visibility = visibility

  @property
  def visibility(self):
    return self._visibility

class _FunctionTestcase(Testcase):
  def __init__(self, func, args=None, **kwargs):
    super().__init__(**kwargs)
    if not callable(func):
      raise ValueError(f"Given a non-function object: {func}")

    self._func = func
    self._args = args

  def exec(self, _max_score=None):
    self._func(*self._args)

class _FunctionPrereq(_FunctionTestcase):
  def __init__(self, func, optional=False, **kwargs):
    super().__init__(func, **kwargs)

    self._optional = optional

  def exec(self, **kwargs):
    try:
      super.exec(**kwargs)
    except PrereqError as exc:
      if self._optional:
        #TODO
        pass
      else:
        raise exc

class Tester:
  ''' docstring for Tester '''

  @staticmethod
  def _load_metadata(path):
    with open(path, 'r') as mfp:
      pass

  def __init__(self):
    self._metadata = Tester._load_metadata(PATH_METADATA)
    self._prerequisites = []
    self._testcases = []

  @property
  def metadata(self):
    ''' '''
    if self._metadata is not None:
      return self._metadata
    raise ValueError()

  def prerequisite(self, **kwargs):
    ''' '''
    def _inner(func):
      prq = _FunctionPrereq(func, **kwargs)
      self._prerequisites.append(prq)
      return func
    return _inner

  def testcase(self, vec=None, args=None, **kwargs):
    ''' '''
    def _inner(func):
      raise RuntimeError("Unreachable")
    if vec is not None:
      if len(kwargs) > 0 or args is not None:
        raise ValueError("Joint use of Vec with single spec def")
      def _inner(func):
        for spec in vec:
          grdr = _FunctionTestcase(func, **spec)
          self._testcases.append(grdr)
        return func
    else:
      def _inner(func):
        grdr = _FunctionTestcase(func, args=args, **kwargs)
        self._testcases.append(grdr)
        return func
    return _inner

  def exec(self):
    ''' '''
    try:
      for prereq in self._prerequisites:
        try:
          prereq.exec()
        except PrereqError as exc:
          return Results(score=0,
                         output="".join(exc.args),
                         visibility=exc.visibility,
                        )
        except AssertionError as exc:
          return Results(
                        )

      res = Results()
      for test in self._testcases:
        try:
          pass
        except Exception as exc:
          raise
      return res
    finally:
      self._metadata = None
