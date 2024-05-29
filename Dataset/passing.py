import requests
from bs4 import BeautifulSoup
import json

def scrape_passing_completion_percentage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the last row in the tfoot element
        tfoot = soup.find('tfoot')
        if tfoot:
            last_row = tfoot.find('tr')
            if last_row:
                # Find the cell with passes_pct
                passes_pct_cell = last_row.find('td', {'data-stat': 'passes_pct'})
                if passes_pct_cell:
                    # Extract the text content of the cell
                    passes_pct = passes_pct_cell.text.strip()
                    return passes_pct

        # If we couldn't find the passes_pct value
        return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request to {url}: {e}")
        return None

    except Exception as e:
        print(f"An error occurred while scraping data from {url}: {e}")
        return None

def scrape_teams_passing_stats(team_urls):
    teams_data = []

    for url, team_name in team_urls:
        passes_pct = scrape_passing_completion_percentage(url)
        if passes_pct is not None:
            team_data = {
                "team_name": team_name,
                "passes_pct": passes_pct
            }
            teams_data.append(team_data)
        else:
            print(f"Passing completion percentage not found for {team_name}")

    return teams_data

def save_teams_passing_stats_json(teams_data):

    filepath = "data/passing_stats.json"
    with open(filepath, 'w') as json_file:
        json.dump(teams_data, json_file, indent=4)


if __name__ == "__main__":
    team_urls = [
        ("https://fbref.com/en/squads/822bd0ba/2023-2024/matchlogs/all_comps/passing/Liverpool-Match-Logs-All-Competitions", "Liverpool"),
        ("https://fbref.com/en/squads/18bb7c10/2023-2024/matchlogs/all_comps/passing/Arsenal-Match-Logs-All-Competitions", "Arsenal"),
        ("https://fbref.com/en/squads/8602292d/2023-2024/matchlogs/all_comps/passing/Aston-Villa-Match-Logs-All-Competitions", "Aston Villa"),
        ("https://fbref.com/en/squads/b8fd03ef/2023-2024/matchlogs/all_comps/passing/Manchester-City-Match-Logs-All-Competitions", "Manchester City"),
        ("https://fbref.com/en/squads/361ca564/2023-2024/matchlogs/all_comps/passing/Tottenham-Hotspur-Match-Logs-All-Competitions", "Tottenham Hotspur"),
        ("https://fbref.com/en/squads/19538871/2023-2024/matchlogs/all_comps/passing/Manchester-United-Match-Logs-All-Competitions", "Manchester United"),
        ("https://fbref.com/en/squads/7c21e445/2023-2024/matchlogs/all_comps/passing/West-Ham-United-Match-Logs-All-Competitions", "West Ham United"),
        ("https://fbref.com/en/squads/d07537b9/2023-2024/matchlogs/all_comps/passing/Brighton-and-Hove-Albion-Match-Logs-All-Competitions", "Brighton and Hove Albion"),
        ("https://fbref.com/en/squads/8cec06e1/2023-2024/matchlogs/all_comps/passing/Wolverhampton-Wanderers-Match-Logs-All-Competitions", "Wolverhampton Wanderers"),
        ("https://fbref.com/en/squads/b2b47a98/2023-2024/matchlogs/all_comps/passing/Newcastle-United-Match-Logs-All-Competitions", "Newcastle United"),
        ("https://fbref.com/en/squads/cff3d9bb/2023-2024/matchlogs/all_comps/passing/Chelsea-Match-Logs-All-Competitions", "Chelsea"),
        ("https://fbref.com/en/squads/fd962109/2023-2024/matchlogs/all_comps/passing/Fulham-Match-Logs-All-Competitions", "Fulham"),
        ("https://fbref.com/en/squads/4ba7cbea/2023-2024/matchlogs/all_comps/passing/Bournemouth-Match-Logs-All-Competitions", "Bournemouth"),
        ("https://fbref.com/en/squads/47c64c55/2023-2024/matchlogs/all_comps/passing/Crystal-Palace-Match-Logs-All-Competitions", "Crystal Palace"),
        ("https://fbref.com/en/squads/cd051869/2023-2024/matchlogs/all_comps/passing/Brentford-Match-Logs-All-Competitions", "Brentford"),
        ("https://fbref.com/en/squads/d3fd31cc/2023-2024/matchlogs/all_comps/passing/Everton-Match-Logs-All-Competitions", "Everton"),
        ("https://fbref.com/en/squads/e297cd13/2023-2024/matchlogs/all_comps/passing/Luton-Town-Match-Logs-All-Competitions", "Luton Town"),
        ("https://fbref.com/en/squads/e4a775cb/2023-2024/matchlogs/all_comps/passing/Nottingham-Forest-Match-Logs-All-Competitions", "Nottingham Forest"),
        ("https://fbref.com/en/squads/943e8050/2023-2024/matchlogs/all_comps/passing/Burnley-Match-Logs-All-Competitions", "Burnley"),
        ("https://fbref.com/en/squads/1df6b87e/2023-2024/matchlogs/all_comps/passing/Sheffield-United-Match-Logs-All-Competitions", "Sheffield United")
        # Add more team URLs as needed
    ]

    teams_data = scrape_teams_passing_stats(team_urls)
    save_teams_passing_stats_json(teams_data)