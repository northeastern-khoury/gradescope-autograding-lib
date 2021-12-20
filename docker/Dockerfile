#syntax=docker/dockerfile:1
FROM gradescope/auto-builds:ubuntu-20.04

RUN true \
 && ln -fs /usr/share/zoneinfo/GMT0 /etc/localtime \
 && apt-get update \
 && apt-get dist-upgrade -y \
 && apt-get install -y build-essential clang git golang jq libssl-dev llvm nodejs openjdk-13-jdk python3 python3-pip rustc valgrind

ARG LIB_VERSION=main
ARG LIB_REFRESH=0

RUN --mount=type=secret,id=deploy_token true \
 && DEPLOY_TOKEN=`cat /run/secrets/deploy_token` \
 && python3 -m pip install git+https://northeasten-khoury:$DEPLOY_TOKEN@github.com/northeastern-khoury/gradescope-autograding-lib@$LIB_VERSION
