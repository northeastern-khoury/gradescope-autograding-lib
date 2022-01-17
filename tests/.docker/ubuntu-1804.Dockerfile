#syntax=docker/dockerfile:1
FROM gradescope/auto-builds:ubuntu-18.04

RUN  true \
  && apt-get update \
  && apt-get install -y python3.7 \
  && python3.7 -m pip install --upgrade pip setuptools virtualenv \
  && mkdir -p /opt/gradescope-autograding-lib/{src,tests}
COPY . /opt/gradescope-autograding-lib/
RUN  python3.7 -m pip install /opt/gradescope-autograding-lib/

CMD [ "python3.7", "/opt/gradescope-autograding-lib/tests/run_tests" ]
