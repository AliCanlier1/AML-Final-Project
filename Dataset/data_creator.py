import json
import csv

all_teams_scores_fixtures = "data/teams_scores_fixtures.json"
general_informations = "data/general_informations.json"
miscellaneous_stats = "data/miscellaneous_stats.json"
passing_stats = "data/passing_stats.json"
shooting_stats = "data/shooting_stats.json"

with open(all_teams_scores_fixtures, 'r') as f:
    all_teams_scores = json.load(f)
with open(general_informations, 'r') as f:
    general_information = json.load(f)
with open(miscellaneous_stats, 'r') as f:
    miscellaneous = json.load(f)
with open(passing_stats, 'r') as f:
    passing = json.load(f)
with open(shooting_stats, 'r') as f:
    shooting = json.load(f)

combined_data = []

for team, matches in all_teams_scores.items():
    print(team)
    for match in matches:
        opponentTeam = match["Opponent"]
        opponentTeamFormation = None
        opponentTeamLastMatchResult = -2
        matchResult: -1
        homeTeamLastMatchResult = -2

        if match["Result"] == "W":
            matchResult = 1
        if match["Result"] == "D":
            matchResult = 0
        if match["Result"] == "L":
            matchResult = -1

        for ht_match in reversed(all_teams_scores.get(team, [])):
            if ht_match["Round"] < match["Round"]:
                homeTeamLastMatchResult = ht_match["Result"]
                if homeTeamLastMatchResult == "W":
                    homeTeamLastMatchResult = 1
                if homeTeamLastMatchResult == "D":
                    homeTeamLastMatchResult = 0
                if homeTeamLastMatchResult == "L":
                    homeTeamLastMatchResult = -1
        attendance = 0
        if(match["Attendance"] != ""):
            attendance = match["Attendance"].replace(',', '')
            attendance = int(attendance)


        for op_match in reversed(all_teams_scores.get(opponentTeam, [])):
            if op_match["Round"] < match["Round"]:
                opponentTeamLastMatchResult = op_match["Result"]
                if opponentTeamLastMatchResult == "W":
                    opponentTeamLastMatchResult = 1
                if opponentTeamLastMatchResult == "D":
                    opponentTeamLastMatchResult = 0
                if opponentTeamLastMatchResult == "L":
                    opponentTeamLastMatchResult = -1
            if op_match["Round"] == match["Round"]:
                opponentTeamFormation = op_match["Formation"]
        currentMatch = {
            "Team1WinRate": int(general_information[team]["Win Ratio"]),
            "Team1GoalsScored": int(match["GoalsScored"]),
            "Team1LastMatchResult": int(homeTeamLastMatchResult),
            "Team2WinRate": int(general_information[opponentTeam]["Win Ratio"]),
            "Team1GoalRatio": float(general_information[team]["Goal Ratio"]),
            "Team2GoalRatio": float(general_information[opponentTeam]["Goal Ratio"]),
            "Team1GoalAgainstRatio": float(general_information[team]["Goal Against Ratio"]),
            "Team2GoalAgainstRatio": float(general_information[opponentTeam]["Goal Against Ratio"]),
            "Team2GoalsScored": int(match["GoalsConceded"]),
            "Team2LastMatchResult": int(opponentTeamLastMatchResult),
            "Team1LeagueRanking": int(general_information[team]["Standing"]),
            "Team2LeagueRanking": int(general_information[opponentTeam]["Standing"]),
            "Attendance": attendance,
            "MatchStadium": match["Venue"],
            "Team1Formation": match["Formation"],
            "Team2Formation": opponentTeamFormation,
            "Team1SuccessfulPassPercentage": float(passing[team]),
            "Team2SuccessfulPassPercentage": float(passing[opponentTeam]),
            "Team1ShootRatio": float(shooting[team]),
            "Team2ShootRatio": float(shooting[opponentTeam]),
            "Team1YellowCardNumber": int(miscellaneous[team]["yellow_card_number"]),
            "Team2YellowCardNumber": int(miscellaneous[opponentTeam]["yellow_card_number"]),
            "Team1RedCardNumber": int(miscellaneous[team]["red_card_number"]),
            "Team2RedCardNumber": int(miscellaneous[opponentTeam]["red_card_number"]),
            "Team1OffsideNumber": int(miscellaneous[team]["offsides_number"]),
            "Team2OffsideNumber": int(miscellaneous[opponentTeam]["offsides_number"]),
            "Team1OffsidePerMatch": round(float(miscellaneous[team]["offsides_per_match"]), 2),
            "Team2OffsidePerMatch": round(float(miscellaneous[opponentTeam]["offsides_per_match"]), 2),
            "Result": matchResult,
        }
        combined_data.append(currentMatch)

csv_file_path = 'dataset.csv'

fieldnames = combined_data[0].keys()

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(combined_data)
