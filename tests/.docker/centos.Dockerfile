#syntax=docker/dockerfile:1
FROM gradescope/auto-builds:centos

RUN  true \
  && yum install -y bzip2-devel libffi-devel openssl-devel xz-devel zlib-devel \
  && curl https://www.python.org/ftp/python/3.7.11/Python-3.7.11.tgz > /tmp/Python-3.7.11.tgz \
  && tar xzf /tmp/Python-3.7.11.tgz \
  && pushd Python-3.7.11 \
  && ./configure --enable-optimizations \
  && make altinstall \
  && python3.7 -V \
  && popd \
  && rm -rf Python-3.7.11 /tmp/Python-3.7.11 \
  && python3.7 -m pip install --upgrade pip setuptools virtualenv
COPY . /opt/gradescope-autograding-lib/
RUN  python3.7 -m pip install /opt/gradescope-autograding-lib/

CMD [ "python3.7", "/opt/gradescope-autograding-lib/tests/run_tests" ]
