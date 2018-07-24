from lxml import html
import requests

url = 'https://bulbapedia.bulbagarden.net/wiki/Kalos_Route_2'
page = requests.get(url)
tree = html.fromstring(page.content)

title = tree.xpath("//h1[@id='firstHeading']/text()")
print(title[0])


pokemon = tree.xpath("//tr[@style='text-align:center;']/th/a/span[text()='X']/../../../td/table/tr/td/a/span[text() != 'Grass']/text()")

rates = tree.xpath("//tr[@style='text-align:center;']/th/a/span[text()='X']/../../../td[@colspan='4']/text()")

# print(pokemon)

poke_rate_dict = {}
poke_counter = 0

for rate in rates:
    rate = (rate.strip().strip('%'))
    rate = int(rate)
    poke_rate_dict[(pokemon[poke_counter])] = rate
    poke_counter += 1

print(poke_rate_dict)
