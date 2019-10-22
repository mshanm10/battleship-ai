# Battleship-AI

### Gaming Engine
Written in python and is dockerized. So, you can run it easily
as long as you have docker installed.

1. run-docker.sh
2. below commands should be run inside docker prompt
3. cd /battleship-ai
4. run-game.sh (to play the game)
5. run-notebook.sh (to view data-preparation & model training details) 

Players
1. Manual
2. Random Player (take random shots)
3. AI Player (use col_classifier and row_classifier models) 
to take next shot

AI Models
1. used XGBoost algorithm

Prediction Flow:
1. Input: current training grid , previous attack coordinate,
and status
2. Col classifier first predict column (one of [A,B,C,D,E])
3. Row classifier use all input above and col classifier's 
predicted col to predict row (one of [1,2,3,4,5])

Issues:
1. Training and testing accuracy was great but preformance
when playing game was poor.
2. It got stuck predicting same column over and over again

Next Steps:
1. Wanted to try CNN model or reinforcement learning algorithm
2. Try one hot encoding for each targeting grid position