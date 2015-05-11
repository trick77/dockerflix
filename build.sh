#!/bin/bash
if [ $# -eq 0 ]
  then
    docker build -f dockerflix.us -t trick77/dockerflix .
  else
    docker build -f dockerflix.$1 -t trick77/dockerflix . 
fi
