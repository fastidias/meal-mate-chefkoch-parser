import urllib.request
import ssl
from bs4 import BeautifulSoup
import json
import time
import re

def parse_rezept(url):
    context = ssl._create_unverified_context()
    request = urllib.request.urlopen(url, context=context)
    response = request.read()

    rezeptHtml = response.decode("utf8")
    request.close()

    rezeptHtml = BeautifulSoup(rezeptHtml, "html.parser")

    try:
        return {
            "title": parse_title(rezeptHtml),
            "ingredients": parse_ingredients(rezeptHtml),
            "source": request.geturl()
        }
    except NameError:
        print(request.geturl())

    return {}

def parse_ingredients(html):
    tbodies = html.body.find_all('tbody')  # TODO: specify tr of table.ingredients
    ingredients = []

    for tbody in tbodies:
        trs = tbody.find_all('tr')
        for child in trs:
            amount = child.find('td', attrs={'class': 'td-left'}).text.strip().replace(" ", "")
            match = re.match(r"(\d+)(\D+)", amount)
            if match:
                quantity = match.group(1)
                unit = match.group(2)            
            name = child.find('td', attrs={'class': 'td-right'}).text.strip()
            ingredients.append({"name": name, "quantity": quantity, "unit": unit})

    return ingredients

def parse_title(html):
    title = html.body.find_all('h1')
    return title[0].contents[0]

url = "https://www.chefkoch.de/rezepte/zufallsrezept/"

rezepte = []
for i in range(10):
    time.sleep(0.5)
    rezepte.append(parse_rezept(url))

with open("rezepte.json", "w", encoding='utf-8') as text_file:
    text_file.write(json.dumps(rezepte, ensure_ascii=False, indent=4))
