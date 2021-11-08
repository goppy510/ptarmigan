#!/bin/bash

export PATH=/home/$(whoami)/.pyenv/bin:$PATH
eval "$(pyenv init -)"
srcPath=/home/$(whoami)/ptarmigan/src/notify/yamap/moment

/home/$(whoami)/.pyenv/versions/3.10.0/bin/python ${srcPath}/main.py

