#!/usr/bin/env bash

docker build -t battleship-ai .

docker run -it --rm \
-v /Users/muthu/dev/project/battleship-ai:/battleship-ai \
-p 8888:8888 \
battleship-ai bin/bash

# cd battleship-ai/src

# R U N    T H E    G A M E  E N G I N E
# python game.py


# jupyter notebook --ip=0.0.0.0 --port 8888 --no-browser --allow-root