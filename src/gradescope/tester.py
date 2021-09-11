
import json
import os
import traceback

from .metadata import Metadata
from .paths import PATH_METADATA, PATH_CODE
from .results import Results
from .testcaseabc import Testcase
from .visibility import VISIBLE, HIDDEN, VISIBILITIES


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

  def exec(self, max_score=None):
    if self._args is None:
      return self._func()
    return self._func(*self._args)

class _FunctionPrereq(_FunctionTestcase):
  def __init__(self, func, optional=False, **kwargs):
    super().__init__(func, **kwargs)

    self._optional = optional

  def exec(self, **kwargs):
    try:
      super().exec(**kwargs)
    except PrereqError as exc:
      if self._optional:
        #TODO: Logging of some form
        pass
      else:
        raise exc

class Tester:
  ''' docstring for Tester '''

  @staticmethod
  def _load_metadata(path):
    with open(path, 'r') as mfp:
      return Metadata.decode_json(json.load(mfp))

  def __init__(self, maintainer=None, metadata=None):
    if maintainer is None:
      maintainer = "Course Staff"
    if metadata is None:
      metadata = PATH_METADATA

    self._maintainer = maintainer
    self._metadata = Tester._load_metadata(metadata)
    self._prerequisites = []
    self._testcases = []
    self._failed = False

  @property
  def metadata(self):
    ''' '''
    if self._metadata is not None:
      return self._metadata
    raise ValueError()

  @property
  def failed(self):
    return self._failed

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
    cwd = os.getcwd()
    try:
      os.chdir(PATH_CODE)
      for prereq in self._prerequisites:
        try:
          prereq.exec()
        except PrereqError as exc:
          self._failed = True
          return Results(score=0,
                         output="".join(exc.args),
                         visibility=exc.visibility,
                        )
        except AssertionError as exc:
          self._failed = True
          traceback.print_exc()
          return Results(score=0,
                         output=str(exc),
                         visibility=VISIBLE,
                         stdout_visibility=HIDDEN,
                        )

      res = Results()
      res.start_time()
      for test in self._testcases:
        res.add_test(test.grade())
      res.end_time()
      return res
    except:
      self._failed = True
      traceback.print_exc()
      return Results(score=0,
                     output="An internal error has occurred. " +
                            "Please reach out to " +
                            self._maintainer +
                            " for assistance.",
                     stdout_visibility=HIDDEN,
                    )
    finally:
      os.chdir(cwd)
