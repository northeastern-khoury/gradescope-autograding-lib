#!/usr/bin/env python3

import hashlib
import os
import subprocess
from pathlib import Path

import gradescope
from gradescope import Tester
from gradescope.file_util import ChDir, InstructorFiles, Manifest
from gradescope.grade import Grade
from gradescope.testcase import Testcase
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

class ExTestcase(Testcase):
  def __init__(self, *names):
    super().__init__()
    assert all(map(lambda s: isinstance(s, str), names))
    self._names = names

  @staticmethod
  def _test_echo(name):
    expected = f"Hello, {name}!"
    proc = subprocess.Popen([MAIN, name], stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    rc = proc.returncode
    if rc != 0:
      return Grade(score=0, max_score=1,
                   output=f"Executable returned with Error Code {rc}")
    if out.strip() != expected:
      return Grade(score=0, max_score=1, output=f"'{out}' != '{expected}'")
    return Grade(score=1, max_score=1, output="Okay!")

  def exec(self, res):
    res.add_tests(ExTestcase._test_echo(fname) for fname in self._names)

HASHES = _file_hashes()

tester = Tester()
tester.prerequisite(Manifest(MAIN_C))
tester.prerequisite(Make('all', clean_after=True))
tester.prerequisite(ExecutableFile(MAIN))
tester.testcase(ExTestcase("World", "Gradescope", "Tester", "Failure"))

def post_test(_res):
  seen = []
  new_hashes = _file_hashes()
  for fname in HASHES:
    seen.append(fname)
    if fname not in new_hashes:
      raise AssertionError(f"File '{fname}' deleted after Tester.exec")
    if HASHES[fname] != new_hashes[fname]:
      raise AssertionError(f"File '{fname}' different after Tester.exec "
                            f"(Hash was: {HASHES[fname]}; now: {new_hashes[fname]}")
  for fname in new_hashes:
    if fname not in seen:
      raise AssertionError(f"File '{fname}' not present before Tester.exec but present after")
