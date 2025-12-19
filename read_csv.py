import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os

# read csv 2024_plays
try:
    data = pd.read_csv("2024_plays.csv", encoding="utf-8", on_bad_lines="skip")
except TypeError:
    data = pd.read_csv("2024_plays.csv", encoding="utf-8", error_bad_lines=False)

data.fillna("", inplace=True)

# get yards
def find_yards(text):
    text = str(text)
    m = re.search(r"(-?\d+)\s*Yard", text, re.IGNORECASE)
    if m:
        return int(m.group(1))
    else:
        return 0

data["Yards"] = data["PlayOutcome"].apply(find_yards)
data.loc[data["Yards"] == 0, "Yards"] = data["PlayDescription"].apply(find_yards)

# get play type
def play_type(text):
    text = str(text).lower()
    if "pass" in text:
        return "Pass"
    elif "run" in text:
        return "Run"
    elif "penalty" in text:
        return "Penalty"
    elif "kick" in text or "punt" in text:
        return "Kick/Punt"
    else:
        return "Other"

data["PlayType"] = data["PlayDescription"].apply(play_type)

# average yards
avg_yards = data.groupby("TeamWithPossession")["Yards"].mean()
total_yards = data.groupby("TeamWithPossession")["Yards"].sum()
median_yards = data.groupby("TeamWithPossession")["Yards"].median()
play_count = data["TeamWithPossession"].value_counts()

summary = pd.DataFrame({
    "Total Plays": play_count,
    "Total Yards": total_yards,
    "Average Yards": avg_yards,
    "Median Yards": median_yards
})

summary = summary.sort_values(by="Total Yards", ascending=False)
summary.to_csv("2024_summary.csv")
print("Saved summary to 2024_summary.csv")

# play type avg
type_avg = data.groupby("PlayType")["Yards"].mean().sort_values(ascending=False)

# week info
data["WeekNumber"] = data["Week"].str.extract(r"(\d+)").astype(float)
weekly = data.groupby(["WeekNumber", "TeamWithPossession"])["Yards"].mean().reset_index()
weekly.to_csv("2024_visual_data.csv", index=False)
print("Saved visualization data to 2024_visual_data.csv")

# make plots folder in VS Code 
if not os.path.exists("plots"):
    os.mkdir("plots")

# plot 1
plt.figure(figsize=(10, 6))
avg_yards.sort_values(ascending=False).plot(kind="bar", color="skyblue", label="Average")
median_yards.sort_values(ascending=False).plot(kind="bar", color="orange", alpha=0.6, label="Median")
plt.title("Average vs Median Yards per Team")
plt.xlabel("Team")
plt.ylabel("Yards")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("plots/avg_vs_median_yards.png")
plt.close()

# plot 2
plt.figure(figsize=(8, 5))
type_avg.plot(kind="bar", color="green")
plt.title("Average Yards by Play Type")
plt.xlabel("Play Type")
plt.ylabel("Average Yards")
plt.tight_layout()
plt.savefig("plots/avg_yards_playtype.png")
plt.close()

# plot 3
plt.figure(figsize=(10, 6))
sns.heatmap(summary[["Total Plays", "Total Yards", "Average Yards", "Median Yards"]],
            cmap="coolwarm", annot=True, fmt=".1f")
plt.title("Team Performance Heatmap")
plt.tight_layout()
plt.savefig("plots/team_heatmap.png")
plt.close()

# plot 4
top_teams = summary.head(5).index
plt.figure(figsize=(10, 6))
for team in top_teams:
    d = weekly[weekly["TeamWithPossession"] == team]
    plt.plot(d["WeekNumber"], d["Yards"], marker="o", label=team)
plt.title("Average Yards per Week (Top 5 Teams)")
plt.xlabel("Week")
plt.ylabel("Average Yards")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/weekly_yards_top5.png")
plt.close()

# plot 5
league = data.groupby("WeekNumber")["Yards"].mean()
plt.figure(figsize=(10, 5))
plt.plot(league.index, league.values, marker="o", color="purple")
plt.title("League-Wide Average Yards per Week")
plt.xlabel("Week")
plt.ylabel("Average Yards per Play")
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/league_yards_trend.png")
plt.close()

print("All plots saved in plots folder!")

