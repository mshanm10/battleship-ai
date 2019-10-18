#!/usr/bin/env bash

docker build -t battleship-ai .

docker run -it --rm \
-v /Users/muthu/dev/project/battleship-ai:/battleship-ai \
battleship-ai bin/bash

# cd battleship-ai/src && python game.py


