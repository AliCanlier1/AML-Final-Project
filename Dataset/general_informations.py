import json
import requests
from bs4 import BeautifulSoup


def get_general_stats(url, teamName):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    p_elements = soup.find_all("p")
    firstElement = p_elements[0].text.strip().split('\n')
    winRatioElement = firstElement[1].strip().split('-')
    winRatio = int(round(int(winRatioElement[0]) / (
            int(winRatioElement[0]) + int(winRatioElement[1]) + int(winRatioElement[2].replace(",", ""))), 2) * 100)
    order = int(firstElement[4].strip()[:-2])
    secondElement = p_elements[2].text.strip().split('\n')
    goalRatioElement = float(secondElement[0].split(" (")[1].replace(" per game), ", ""))
    goalCondedeElement = float(secondElement[1].split(" (")[1].replace(" per game),", ""))
    result = {
        "team_name": teamName,
        "general_informations": [
            {
                "Win Ratio": winRatio,
                "Standing": order,
                "Goal Ratio": goalRatioElement,
                "Goal Against Ratio": goalCondedeElement
            }
        ]
    }
    return result


def main():
    urls = [
        ("https://fbref.com/en/squads/18bb7c10/Arsenal-Stats", "Arsenal"),
        ("https://fbref.com/en/squads/822bd0ba/Liverpool-Stats", "Liverpool"),
        ("https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats", "Manchester City"),
        ("https://fbref.com/en/squads/19538871/Manchester-United-Stats", "Manchester United"),
        ("https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats", "Chelsea"),
        ("https://fbref.com/en/squads/8602292d/Aston-Villa-Stats", "Aston Villa"),
        ("https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats", "Tottenham Hotspur"),
        ("https://fbref.com/en/squads/b2b47a98/Newcastle-United-Stats", "Newcastle United"),
        ("https://fbref.com/en/squads/7c21e445/West-Ham-United-Stats", "West Ham United"),
        ("https://fbref.com/en/squads/d07537b9/Brighton-and-Hove-Albion-Stats", "Brighton & Hove Albion"),
        ("https://fbref.com/en/squads/4ba7cbea/Bournemouth-Stats", "Bournemouth"),
        ("https://fbref.com/en/squads/47c64c55/Crystal-Palace-Stats", "Crystal Palace"),
        ("https://fbref.com/en/squads/8cec06e1/Wolverhampton-Wanderers-Stats", "Wolverhampton"),
        ("https://fbref.com/en/squads/fd962109/Fulham-Stats", "Fulham"),
        ("https://fbref.com/en/squads/d3fd31cc/Everton-Stats", "Everton"),
        ("https://fbref.com/en/squads/cd051869/Brentford-Stats", "Brentford"),
        ("https://fbref.com/en/squads/e4a775cb/Nottingham-Forest-Stats", "Nottingham Forest"),
        ("https://fbref.com/en/squads/e297cd13/Luton-Town-Stats", "Luton Town"),
        ("https://fbref.com/en/squads/943e8050/Burnley-Stats", "Burnley Town"),
        ("https://fbref.com/en/squads/1df6b87e/Sheffield-United-Stats", "Sheffield United")
    ]
    all_results = []
    for url in urls:
        result = get_general_stats(url[0], url[1])
        all_results.append(result)

    with open("data/general_informations.json", "w") as file:
      json.dump(all_results, file, indent=4)


if __name__ == "__main__":
    main()
