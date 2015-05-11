#!/bin/bash
if [ $# -eq 0 ]
  then
    docker build --no-cache=true -f dockerflix.us -t trick77/dockerflix .
  else
    docker build --no-cache=true -f dockerflix.$1 -t trick77/dockerflix .
fi
