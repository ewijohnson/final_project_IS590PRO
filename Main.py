from lxml import html
import requests
import random

# Shows data and Pokemon for Pokemon X - steps will be the same but Pokemon will be different for Pokemon Y

# Excludes Horde Encounters, Rock Smash, Rustling Bush, Surfing, Fishing, Ceiling

# Combines rates for all environments per location, as the player will not necessarily stay within one type - they will
#   freely move around all areas per location

# Fine for now:
# Route 2-9, 22, Santalune Forest, Glittering Cave, Connecting Cave, Reflection Cave, Terminus Cave, Frost Cavern

# Places with Issues:
#   Route 10-21, Azure Bay, Lost Hotel
#       Pokemon Village, Victory Road same as R 5 (IndexError) - two slightly different reasons though(one with 'rate'
#       one with join)


def dataDownload():
    """This function gets the relevant information on Pokemon encounters and encounter rates from the Bulbapedia
    webpage that lists this information."""

    url = 'https://bulbapedia.bulbagarden.net/wiki/Frost_Cavern'
    page = requests.get(url)
    tree = html.fromstring(page.content)

    title = tree.xpath("//h1[@id='firstHeading']/text()")
    print(title[0])

    # Excludes all Pokemon after the 'Horde Encounter' banner in the tables, extracts all preceding Pokemon, environment
    #   types, and rates of encounter.
    pokemon = tree.xpath("//tr[@style='text-align:center;']/th/a/span[text()='X']/../../../td/table/tr/td/a/span/text()"
                         "[following::th/a[@title='Horde Encounter']]")
    print('pokemon1', pokemon)
    if not pokemon:
        pokemon = tree.xpath("//tr[@style='text-align:center;']/th/a/span[text()='X']/../../../td/table/tr/td/a/span/"
                             "text()")

    rates = tree.xpath("//tr[@style='text-align:center;']/th/a/span[text()='X']/../../../td[@colspan='4']/text()")

    cleaned_pokemon_list = []
    print('@@@@@@@', pokemon)
    for i, environment in enumerate(pokemon):

        if environment in ['Fishing', 'Surfing', 'Ceiling', 'Rock\xa0Smash']:

            del pokemon[i-1]




    print('!!!!!!!', pokemon)

    for environment in pokemon:
        if environment not in ['Surfing', 'Fishing', 'Grass', 'Yellow flowers', 'Red flowers', 'Purple flowers',
                               'Tall grass', 'Cave', 'Ceiling', 'Rock\xa0Smash']:
            cleaned_pokemon_list.append(environment)


    # combined_pokemon_list = []
    # # Combines Pokemon name with environment type
    # for i in range(0, len(pokemon), 2):
    #     combined_pokemon = pokemon[i] + '-' + pokemon[i + 1]
    #     combined_pokemon_list.append(combined_pokemon)


    poke_rate_dict = {}
    poke_counter = 0

    print('^^^^', cleaned_pokemon_list)
    print('&&&', rates)
    for rate in rates:
        rate = (rate.strip().strip('%'))
        try:
            rate = int(rate)
        # This stops the calculations when the Horde Encounters start
        except ValueError:
            break
        print('***', rate)
        # This accounts for different 'variations' of the same Pokemon that have different encounter rates.
        #   All variations of a Pokemon are considered to be the same Pokemon, as supported by the game (one
        #   'Pokedex' (an in-game Pokemon database) entry per Pokemon, including all variations).
        try:
            poke_rate_dict[(cleaned_pokemon_list[poke_counter])] += rate
        except IndexError:
            pass
        except KeyError:
            poke_rate_dict[(cleaned_pokemon_list[poke_counter])] = rate
        poke_counter += 1

    # for pokemon in combined_pokemon_list:
    #     if 'Fishing' in pokemon:
    #         del poke_rate_dict[pokemon]
    #     elif 'Surfing' in pokemon:
    #         del poke_rate_dict[pokemon]
    #     elif 'Horde Encounter' in pokemon:
    #         del poke_rate_dict[pokemon]
    #     elif 'Rustling bush' in pokemon:
    #         del poke_rate_dict[pokemon]

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

    #print(step_counter, pokemon_encountered)
    return step_counter


poke_dict = dataDownload()

print(poke_dict)

number_of_simulations = 10000
ten_percent = int(number_of_simulations * .1)

all_step_list = []
for i in range(number_of_simulations):
    total_step_counter = monteCarloSimulation(poke_dict)
    all_step_list.append(total_step_counter)

sorted_list = sorted(all_step_list)
top_ninety_percent = sorted_list[-ten_percent]
max_ten_percent = sum(sorted_list[-ten_percent:]) / len(sorted_list[-ten_percent:])
print()
print('top 90%:', top_ninety_percent, 'steps')
print('average of top 90%:', max_ten_percent, 'steps')

average = sum(all_step_list) / len(all_step_list)
max = max(all_step_list)
min = min(all_step_list)
print()
print('overall average:', average, 'max:', max, 'min:', min)
print('average steps per pokemon:', average/len(poke_dict))

