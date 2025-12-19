import pandas as pd
import re

print("Welcome to PlayPredictor!")
print("This program predicts the next play (Run or Pass) using 2024 NFL data.\n")

#loading the CSV 
try:
    data = pd.read_csv("2024_plays.csv", encoding="utf-8", on_bad_lines="skip")
except TypeError:
    data = pd.read_csv("2024_plays.csv", encoding="utf-8", error_bad_lines=False)

data.fillna("", inplace=True)


def play_type(description):
    desc = str(description).lower()

    if "pass" in desc:
        return "Pass"
    if "run" in desc:
        return "Run"
    if "kick" in desc or "punt" in desc:
        return "Kick/Punt"
    if "penalty" in desc:
        return "Penalty"

    return "Other"


data["PlayType"] = data["PlayDescription"].apply(play_type)

# basic team tendencies
team_tend = (
    data.groupby(["TeamWithPossession", "PlayType"])
        .size()
        .unstack(fill_value=0)
)

team_tend["Total"] = team_tend.sum(axis=1)
team_tend["RunRatio"] = team_tend["Run"] / team_tend["Total"]
team_tend["PassRatio"] = team_tend["Pass"] / team_tend["Total"]


def predict_play(down, distance, field_pos, time_left, team):
    if team in team_tend.index:
        run_ratio = team_tend.loc[team, "RunRatio"]
        pass_ratio = team_tend.loc[team, "PassRatio"]
    else:
        run_ratio = 0.5
        pass_ratio = 0.5

    run_score = run_ratio
    pass_score = pass_ratio

    # logic
    if down == 1:
        run_score += 0.2
    elif down == 3 and distance > 6:
        pass_score += 0.3
    elif down == 4:
        pass_score += 0.2

    if distance <= 2:
        run_score += 0.15
    elif distance >= 8:
        pass_score += 0.15

    if field_pos > 80:
        run_score += 0.1
    elif field_pos < 30:
        pass_score += 0.1

    if time_left < 2:
        pass_score += 0.25

    prediction = "Pass" if pass_score > run_score else "Run"

    return {
        "Team": team,
        "Down": down,
        "Distance": distance,
        "Field Position": field_pos,
        "Time Left": time_left,
        "Prediction": prediction,
        "Run Score": round(run_score, 2),
        "Pass Score": round(pass_score, 2),
    }


# UI
try:
    team = input("Enter team name (ex: Baltimore Ravens): ").strip()
    down = int(input("Enter down (1-4): "))
    distance = float(input("Enter yards to first down: "))
    field_pos = float(input("Enter field position (0-100, where 100 = opponent goal line): "))
    time_left = float(input("Enter time left in quarter (minutes): "))

    results = predict_play(down, distance, field_pos, time_left, team)

    print("\nPrediction Results:")
    for k, v in results.items():
        print(f"{k}: {v}")

except Exception as e:
    print("Something went wrong.")
    print("Error:", e)
    print("Please check your inputs and try again.")
