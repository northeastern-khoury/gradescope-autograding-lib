#!/usr/bin/env python3

import gradescope
from gradescope import Tester
from gradescope.file_util import Manifest
from gradescope.unix_util import ExecutableFile, Make

tester = Tester()
tester.prerequisite(Manifest('main.c'))
tester.prerequisite(Make('all', clean_after=True))
tester.prerequisite(ExecutableFile('main'))
tester.no_tests()
