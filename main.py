import urllib.request
import ssl
from bs4 import BeautifulSoup


def parse_ingredients(html):
    trs = html.body.find_all('tr')  # TODO: specify tr of table.ingredients

    for child in trs:
        amount = child.find('td', attrs={'class': 'td-left'}).text.strip().replace(" ", "")
        ingredient = child.find('td', attrs={'class': 'td-right'}).text.strip()
        print(amount + " " + ingredient)


# url = "https://www.chefkoch.de/rezepte/zufallsrezept/"
url = "https://www.chefkoch.de/rezepte/2076041335467470/Hackmuffins.html"
context = ssl._create_unverified_context()
request = urllib.request.urlopen(url, context=context)
response = request.read()

rezeptHtml = response.decode("utf8")
request.close()

rezeptHtml = BeautifulSoup(rezeptHtml, "html.parser")
parse_ingredients(rezeptHtml)
