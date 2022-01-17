#syntax=docker/dockerfile:1
FROM gradescope/auto-builds:ubuntu-20.04

RUN  true \
  && python3 -m pip install --upgrade pip setuptools virtualenv \
  && mkdir -p /opt/gradescope-autograding-lib/{src,tests}
COPY . /opt/gradescope-autograding-lib/
RUN  python3 -m pip install /opt/gradescope-autograding-lib/

CMD [ "python3", "/opt/gradescope-autograding-lib/tests/run_tests" ]
