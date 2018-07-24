from lxml import html
import requests
import random

def dataDownload():
    """This function gets the relevant information on Pokemon encounters and encounter rates from the Bulbapedia
    webpage that lists this information."""

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

    return poke_rate_dict



def monteCarloSimulation(pokemon_dictionary):
    """This runs through one run of the simulation. This is the part of the program that must be repeated in order to
    make it a Monte Carlo simulation."""

    number_of_pokemon = len(pokemon_dictionary)

    # Creates the weighted list of all possible Pokemon encounters
    random_choice_poke_list = []
    for key in pokemon_dictionary:
        random_choice_poke_list += [key] * (pokemon_dictionary[key])

    step_counter = 0
    pokemon_encountered = []


    while len(pokemon_encountered) < number_of_pokemon:

        # The range of steps before the next Pokemon encounter
        steps = random.randint(1, 32)
        # Random Pokemon that is encountered, chosen from the weighted list
        poke_choice = random.choice(random_choice_poke_list)

        step_counter += steps
        if poke_choice not in pokemon_encountered:
            pokemon_encountered.append(poke_choice)

    print(step_counter, pokemon_encountered)
    return step_counter


poke_dict = dataDownload()

# print(poke_dict)

all_step_list = []
for i in range(100000):
    total_step_counter = monteCarloSimulation(poke_dict)
    all_step_list.append(total_step_counter)

average = sum(all_step_list) / len(all_step_list)
max = max(all_step_list)
min = min(all_step_list)
print(average, max, min)
