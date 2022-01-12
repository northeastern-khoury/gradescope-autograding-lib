#!/usr/bin/env python3

import subprocess

import gradescope
from gradescope import Tester
from gradescope.file_util import ChDir, InstructorFiles, Manifest
from gradescope.unix_util import ExecutableFile, Make


MAIN = "./main"
MANIFEST = [ 'main.c' ]
NAMES = ["World", "Gradescope", "Tester", "Failure"]

tester = Tester(skip_instructor_files=True)
tester.prerequisite(ChDir('sub_dir'))
tester.prerequisite(InstructorFiles(cleanup=True))
tester.prerequisite(Manifest(*MANIFEST))
tester.prerequisite(Make('all', clean_after=True))
tester.prerequisite(ExecutableFile('main'))

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
  out = proc.communicate()[0]
  rc = proc.returncode
  if rc != 0:
    return (0, f"Executable returned with Error Code {rc}")
  if out.strip() != expected:
    return (0, f"'{out}' != '{expected}'")
  return (1, "Okay!")

def post_test():
  assert 
