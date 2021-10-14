
import json
import traceback

from . import paths

from .context import ChDir, ListContext
from .file_util import InstructorFiles
from .group import Group
from .metadata import Metadata
from .prereq import FunctionPrereq, Prereq, PrereqError
from .results import Results
from .testcase import FunctionTestcase
from .visibility import VISIBLE, HIDDEN


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
      metadata = paths.PATH_METADATA

    self._maintainer = maintainer
    self._metadata = Tester._load_metadata(metadata)
    self._prerequisites = []
    self._testcases = []
    self._callable_map = {}
    self._failed = False

    if paths.PATH_INSTRUCTOR_FILES.is_dir():
      self.prerequisite(InstructorFiles(cleanup=True))

  def __str__(self):
    return " ".join(["Tester{{",
                     f"maintainer: '{self._maintainer}',",
                     f"names: [{', '.join(self._callable_map.keys())}],",
                     f"prereqs: [{', '.join(map(str, self._prerequisites))}],"
                     f"testcases: [{', '.join(map(str, self._testcases))}],",
                     f"failed? {self._failed}",
                     "}}"])

  def __getattr__(self, k):
    if k.startswith('__') or k not in self._callable_map:
      raise AttributeError(f"'Tester' object has no attribute '{k}'")
    return self._callable_map[k]

  @property
  def metadata(self):
    ''' '''
    if self._metadata is not None:
      return self._metadata
    raise ValueError()

  @property
  def failed(self):
    return self._failed

  def _new_callable(self, target, hook=(lambda e: e)):
    def _inner(func):
      if hasattr(func, '__name__'):
        name = func.__name__
        if name == "<lambda>":
          name += f" {hex(id(func))}"
      elif hasattr(func, '__str__'):
        name = str(func)
      else:
        name = hex(id(func))
      if name in self._callable_map:
        raise ValueError(f"Namespace Collision: {name}")
      grdr = hook(func)
      target.append(grdr)
      self._callable_map[name] = grdr
      return grdr
    return _inner

  def prerequisite(self, *args, **kwargs):
    ''' '''
    def _hook(func):
      if not isinstance(func, Prereq):
        if not callable(func):
          raise TypeError
        func = FunctionPrereq(func, **kwargs)
      return func
    inner = self._new_callable(self._prerequisites, hook=_hook)
    if len(args) == 0:
      return inner
    return inner(*args)

  def testcase(self, *args, vec=None, **kwargs):
    ''' '''
    func = self._new_callable(self._testcases,
                              hook=lambda f: FunctionTestcase(f, **kwargs))
    if vec is not None:
      if len(kwargs) > 0:
        raise ValueError("Joint use of Vec with single spec def")
      func =  self._new_callable(self._testcases,
                                 hook=lambda f: Group( *(FunctionTestcase(f, **spec) for spec in vec) ))
    if len(args) == 0:
      return func
    return func(*args)

  def no_tests(self):
    ''' no_tests : None -> None
        Signal to the Tester that no tests will be executed
    '''
    if len(self._testcases) > 0:
      raise RuntimeError("Testcases already configured!")
    self._testcases.append(FunctionTestcase(lambda: (0.0, "Okay")))

  def _handle_exec_failure(self,
                           output,
                           exc=None,
                           stdout=None,
                           stdout_visibility=HIDDEN,
                           visibility=VISIBLE,
                          ):
    ''' Helper function for exec to simplify exception handling '''
    self._failed = True
    if stdout is not None:
      print(stdout)
    if exc is not None:
      print("\n\n===== DEBUG TRACE FOR COURSE STAFF =====")
      traceback.print_exception(type(exc), exc, exc.__traceback__)
    return Results(score=0,
                   output=output,
                   visibility=visibility,
                   stdout_visibility=stdout_visibility,
                  )

  def exec(self):
    ''' exec : Self -> U(None, Results)
        #TODO
    '''
    if len(self._testcases) == 0:
      raise RuntimeError("No testcases configured?")

    context = self._prerequisites.copy()
    context.insert(0, ChDir(paths.PATH_CODE))
    try:
      with ListContext(context):
        res = Results()
        res.start_time()
        for test in self._testcases:
          res.add_tests(test.grade())
        res.end_time()
        return res
    except PrereqError as exc:
      return self._handle_exec_failure("".join(exc.args),
                                       stdout=exc.stdout,
                                       visibility=exc.visibility,
                                       stdout_visibility=exc.stdout_visibility,
                                      )
    except AssertionError as exc:
      return self._handle_exec_failure(str(exc),
                                       exc=exc)
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
