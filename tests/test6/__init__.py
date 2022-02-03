#!/usr/bin/env python3

import hashlib
import os
import subprocess
from pathlib import Path

import gradescope
from gradescope import Tester
from gradescope.file_util import ChDir, InstructorFiles, Manifest
from gradescope.unix_util import ExecutableFile, Make

def _file_hashes():
  rvd = {}
  for root, _, files in os.walk(gradescope.paths.PATH_CODE):
    root = Path(root)
    for fname in files:
      fpath = root / fname
      with open(fpath, 'rb') as ifp:
        rvd[fpath] = hashlib.sha256(ifp.read()).hexdigest()
  return rvd

MAIN = "./main"
MAIN_C = 'main.c'
NAMES = ["World", "Gradescope", "Tester", "Failure"]

HASHES = _file_hashes()

tester = Tester()
tester.prerequisite(Manifest(MAIN_C))
tester.prerequisite(Make('all', clean_after=True))
tester.prerequisite(ExecutableFile(MAIN))

def _gen_vec(names):
  for name in names:
    yield  {
        "args": (name, ),
        "name": f"Hello, {name}!",
        "max_score": 1,
    }

@tester.testcase(vec=list(_gen_vec(NAMES)))
def test_echo(name):
  expected = f"Hello, {name}!"
  proc = subprocess.Popen([MAIN, name], stdout=subprocess.PIPE)
  out = proc.communicate()[0].decode().strip()
  prc = proc.returncode
  assert prc == 0, f"Executable returned with Error Code {prc}"
  assert out == expected, f"'{out}' != '{expected}'"
  return (1, "Okay!")

def post_test(res):
  def _reg_impl(t, test, score):
    return t.name == test and t.score == score

  for t in res.tests:
    try:
      assert any([_reg_impl(t, 'Hello, World!', 1.0),
                  _reg_impl(t, 'Hello, Gradescope!', 1.0),
                  _reg_impl(t, 'Hello, Tester!', 1.0),
                  _reg_impl(t, 'Hello, Failure!', 0.0),
                ]), t.name
    except AssertionError as exc:
      raise AssertionError(f"Bad out on '{str(exc)}'") from exc
