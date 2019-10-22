#!/usr/bin/env bash
# --------------------------------------
# To start the game
# Step 1: Start the docker
#        run-docker.sh

# Step 2: go to dir
#        cd /battleship-ai

# Step 3: run this script
#         ./run-game.sh
# --------------------------------------

# once the docker bash prompt appears
# - - - - - - - - - - - - - - - - - -
cd src

# R U N    T H E    G A M E  E N G I N E
python game.py


# jupyter notebook --ip=0.0.0.0 --port 8888 --no-browser --allow-root