#!/usr/bin/env python3

import hashlib
import os
import subprocess
import time

import gradescope
from gradescope import Tester
from gradescope.file_util import ChDir, InstructorFiles, Manifest
from gradescope.unix_util import ExecutableFile, Make
from gradescope.leaderboard.orders import ORDER_DESCENDING

MAIN = "./main"
MAIN_C = 'main.c'
NAMES = ["World", "Gradescope", "Tester", "Failure"]

tester = Tester()
tester.prerequisite(Manifest(MAIN_C))
tester.prerequisite(Make('all', clean_after=True))
tester.prerequisite(ExecutableFile(MAIN))

tester.no_tests()

@tester.leaderboard(name="runtime", order=ORDER_DESCENDING)
def get_runtime():
  name = "World"
  expected = f"Hello, {name}!"

  start_time = time.monotonic()
  proc = subprocess.Popen([MAIN, name], stdout=subprocess.PIPE)
  out = proc.communicate()[0].decode().strip()
  end_time = time.monotonic()

  prc = proc.returncode
  assert prc == 0, f"Executable returned with Error Code {prc}"
  assert out == expected, f"'{out}' != '{expected}'"
  return end_time - start_time

def post_test(res):
  assert res.leaderboard["runtime"] is not None, "Missing runtime object in leaderboard"
