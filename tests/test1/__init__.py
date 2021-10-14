#!/usr/bin/env python3

from gradescope import Tester

tester = Tester()

@tester.prerequisite()
def dummy_prereq():
  return

@tester.testcase()
def dummy_test():
  return (1.0, 'no-op')
