import requests
from bs4 import BeautifulSoup

URL = "http://alexandrovroman.pythonanywhere.com/"


def has_connect() -> bool:
    try:
        return requests.get(URL).status_code == 200
    except requests.exceptions.ConnectionError:
        return False


def top(n: int) -> list:
    response = requests.get(f"{URL}top/{n}/")
    if response.status_code != 200:
        return []
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", class_="cwdtable")
    rows = table.find("tbody").find_all("tr")
    matrix = [[cell.text for cell in row.find_all("td")[1:]] for row in rows]
    return matrix


def add_record(nick: str, time: int) -> None:
    json = {"nick": nick, "time": time}
    requests.post(f"{URL}add/", json=json)
