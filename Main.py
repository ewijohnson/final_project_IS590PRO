from lxml import html
import requests
import random

# Fine for now:
# Route 2, 3, 6, Santalune Forest

# Places with Issues:
#   Route 4, 22, Glittering Cave(different rates in red vs purple flowers, three colors of Flabebe,
#       different locations)
#   Route 5, 7-21, Connecting Cave, Reflection Cave, Azure Bay, Lost Hotel, Terminus Cave, Frost Cavern,
#       Pokemon Village, Victory Road same as R 5 (IndexError) - two slightly different reasons though(one with 'rate'
#       one with join)


def dataDownload():
    """This function gets the relevant information on Pokemon encounters and encounter rates from the Bulbapedia
    webpage that lists this information."""

    url = 'https://bulbapedia.bulbagarden.net/wiki/Kalos_Route_2'
    page = requests.get(url)
    tree = html.fromstring(page.content)

    title = tree.xpath("//h1[@id='firstHeading']/text()")
    print(title[0])


    pokemon = tree.xpath("//tr[@style='text-align:center;']/th/a/span[text()='X']/../../../td/table/tr/td/a/span/text()")

    rates = tree.xpath("//tr[@style='text-align:center;']/th/a/span[text()='X']/../../../td[@colspan='4']/text()")

    # for poke in pokemon:
    #     if poke in ['Surfing', 'Fishing']:
    #         pokemon.remove(poke)



    print(pokemon)

    combined_pokemon_list = []
    # Combines Pokemon name with environment type
    for i in range(0, len(pokemon), 2):
        combined_pokemon = pokemon[i] + '-' + pokemon[i + 1]
        combined_pokemon_list.append(combined_pokemon)

    print(combined_pokemon_list)
    poke_rate_dict = {}
    poke_counter = 0

    for rate in rates:
        rate = (rate.strip().strip('%'))
        try:
            rate = int(rate)
        except ValueError:
            pass
        poke_rate_dict[(combined_pokemon_list[poke_counter])] = rate
        poke_counter += 1

    for pokemon in combined_pokemon_list:
        if 'Fishing' in pokemon:
            del poke_rate_dict[pokemon]
        elif 'Surfing' in pokemon:
            del poke_rate_dict[pokemon]
        elif 'Horde Encounter' in pokemon:
            del poke_rate_dict[pokemon]
        elif 'Rustling bush' in pokemon:
            del poke_rate_dict[pokemon]

    print(poke_rate_dict)

    return poke_rate_dict



def monteCarloSimulation(pokemon_dictionary):
    """This runs through one run of the simulation. This is the part of the program that must be repeated in order to
    make it a Monte Carlo simulation.
    Doctests will go here.
    """

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

#print(poke_dict)

all_step_list = []
for i in range(10000):
    total_step_counter = monteCarloSimulation(poke_dict)
    all_step_list.append(total_step_counter)

average = sum(all_step_list) / len(all_step_list)
max = max(all_step_list)
min = min(all_step_list)
print('average:', average, 'max:', max, 'min:', min)
print('average steps per pokemon:', average/len(poke_dict))
