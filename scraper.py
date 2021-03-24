from bs4 import BeautifulSoup
import requests, os


def scrape_football():

    try:
        livescore_html = requests.get('https://www.livescores.com/soccer/serbia/super-liga/fixtures/all/')
    except Exception as e:
        return print('An error occured as: ', e)

    parsed_markup = BeautifulSoup(livescore_html.text, 'html.parser')

    scores = {}

    for element in parsed_markup.find_all("div", "row-gray"):

        match_name_element = element.find(attrs={"class": "scorelink"})

        if match_name_element is not None:

            match_name = match_name_element.get('href').split('/')[4]
            home_team_score = element.find("div", "sco").get_text().split("-")[0].strip()
            away_team_score = element.find("div", "sco").get_text().split("-")[1].strip()
            home_team = match_name.split('-vs-')[0]
            away_team = match_name.split('-vs-')[1]
            match_name = home_team + ' vs ' + away_team
            scores[match_name] = (home_team_score, away_team_score)
        else:
            home_team = ' '.join(element.find("div", "tright").get_text().strip().split(" "))
            away_team = ' '.join(element.find(attrs={"class": "ply name"}).get_text().strip().split(" "))

            home_team_score = element.find("div", "sco").get_text().split("-")[0].strip()
            away_team_score = element.find("div", "sco").get_text().split("-")[1].strip()

            match_name = home_team + ' vs ' + away_team
            scores[match_name] = (home_team_score, away_team_score)

    return scores

def scrape_basketball():

    try:
        livescore_html = requests.get('https://www.livescores.com/basketball/ncaa/')
    except Exception as e:
        return print('An error occured as: ', e)

    parsed_markup = BeautifulSoup(livescore_html.text, 'html.parser')

    scores = {}



    for element in parsed_markup.find_all("div", "row-group row-group-wide"):

        divs = element.find_all("div", "row-gray even")

        if not divs:
            divs = element.find_all("div", "row-gray")

        home_team_score = divs[0].find("div", "sco3").get_text()
        away_team_score = divs[1].find("div", "sco3").get_text()
        home_team = divs[0].find("div", "bas-ply").get_text()
        away_team = divs[1].find("div", "bas-ply").get_text()

        print(home_team, home_team_score, away_team_score, away_team)


    return scores