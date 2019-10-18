import pandas as pd

print("Battleship Game Started.")
tg = pd.DataFrame([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]], columns=['A', 'B', 'C', 'D', 'E'], index=[1,2,3,4,5])
player_a = {
    "ocean_grid": [],
    "targeting_grid": []
}
player_b = {
    "ocean_grid": [],
    "targeting_grid": []
}
print("Your Targeting Grid (Player A)")
print(tg)
move = input("Player A (your move):")
print(move)
