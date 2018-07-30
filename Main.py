from lxml import html
import requests
import random

# Shows data and Pokemon for Pokemon X - steps will be the same but Pokemon will be different for Pokemon Y

# Excludes Horde Encounters, Rock Smash, Rustling Bush, Surfing, Fishing, Ceiling

# Combines rates for all environments per location, as the player will not necessarily stay within one type - they will
#   freely move around all areas per location

# All areas work:
# Route 2-22, Santalune Forest, Glittering Cave, Connecting Cave, Reflection Cave, Terminus Cave, Frost Cavern,
#   Azure Bay, Pokemon Village, Lost Hotel, Victory Road



def dataDownload(location_name):
    """This function gets the relevant information on Pokemon encounters and encounter rates from the Bulbapedia
    webpage that lists this information."""


    url = 'https://bulbapedia.bulbagarden.net/wiki/' + location_name
    page = requests.get(url)
    tree = html.fromstring(page.content)

    title = tree.xpath("//h1[@id='firstHeading']/text()")
    print()
    print('----------------------')
    print()
    print(title[0])



    # Excludes all Pokemon after the 'Horde Encounter' banner in the tables, extracts all preceding Pokemon, environment
    #   types, and rates of encounter.

    pokemon = tree.xpath("//tr[@style='text-align:center;']/th/a/span[text()='X']/../../../td/table/tr/td/a/span/text()"
                         "[following::th/a[@title='Horde Encounter']]")

    # Need to manually remove the final three Pokemon for Victory Road because of horrible XML
    if location_name == 'Victory_Road_(Kalos)':
        pokemon = pokemon[:-3]

    # Only used for some cases, will be empty otherwise if there are no Swamp Pokemon
    swamp_pokemon = tree.xpath("//tr[@style='text-align:center;']/th/a/span[text()='X']/../../../td/table/tr/td/a/span/"
                               "text()[preceding::th/a/span[text()='Swamp']]")

    # This is added for Route 19, where the XML for the Swamp Pokemon is different than other webpages
    if not swamp_pokemon:
        swamp_pokemon = tree.xpath("//tr[@style='text-align:center;']/th/a/span[text()='X']/../../../td/table/tr/td/a/"
                                   "span/text()[preceding::th[@style='background: #BDA595; color: #573118']]")
    # This is added for cases where there are no Horde Encounters, and therefore the first XPath won't return results
    if not pokemon:
        pokemon = tree.xpath("//tr[@style='text-align:center;']/th/a/span[text()='X']/../../../td/table/tr/td/a/span/"
                                 "text()")


    rates = tree.xpath("//tr[@style='text-align:center;']/th/a/span[text()='X']/../../../td[@colspan='4']/text()")

    # As with swamp_pokemon, only used if there are Swamp Pokemon
    swamp_rates = tree.xpath("//tr[@style='text-align:center;']/th/a/span[text()='X']/../../../td[@colspan='4']/text()"
                             "[preceding::th/a/span[text()='Swamp']]")

    # For Route 19 again, where the Swamp XML is different:
    if not swamp_rates:
        swamp_rates = tree.xpath("//tr[@style='text-align:center;']/th/a/span[text()='X']/../../../td[@colspan='4']/"
                                 "text()[preceding::th[@style='background: #BDA595; color: #573118']]")


    cleaned_pokemon_list = []

    for i, environment in enumerate(pokemon):

        if environment in ['Fishing', 'Surfing', 'Ceiling', 'Rock\xa0Smash', 'Rustling bush', 'Shaking trash cans']:

            del pokemon[i-1]

    if swamp_pokemon:
        for i, environment in enumerate(swamp_pokemon):

            if environment in ['Fishing', 'Surfing', 'Ceiling', 'Rock\xa0Smash', 'Rustling bush', 'Shaking trash cans']:
                del swamp_pokemon[i - 1]




    for environment in pokemon:
        if environment not in ['Surfing', 'Fishing', 'Grass', 'Yellow flowers', 'Red flowers', 'Purple flowers',
                               'Tall grass', 'Cave', 'Ceiling', 'Rock\xa0Smash', 'Terrain', 'Dirt', 'Swamp', 'Snow',
                               'Rustling bush', 'Shaking trash cans']:
            cleaned_pokemon_list.append(environment)

    cleaned_swamp_pokemon_list = []
    if swamp_pokemon:
        for environment in swamp_pokemon:
            if environment not in ['Surfing', 'Fishing', 'Grass', 'Yellow flowers', 'Red flowers', 'Purple flowers',
                                   'Tall grass', 'Cave', 'Ceiling', 'Rock\xa0Smash', 'Terrain', 'Dirt', 'Swamp', 'Snow',
                                   'Rustling bush', 'Shaking trash cans']:
                cleaned_swamp_pokemon_list.append(environment)


    poke_rate_dict = {}


    poke_counter = 0

    for rate in rates:
        rate = (rate.strip().strip('%'))
        try:
            rate = int(rate)


        except ValueError:
            pass

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

    if swamp_pokemon:

        poke_counter = 0

        for rate in swamp_rates:
            rate = (rate.strip().strip('%'))
            try:
                rate = int(rate)


            except ValueError:
                pass

            # This accounts for different 'variations' of the same Pokemon that have different encounter rates.
            #   All variations of a Pokemon are considered to be the same Pokemon, as supported by the game (one
            #   'Pokedex' (an in-game Pokemon database) entry per Pokemon, including all variations).
            try:
                poke_rate_dict[(cleaned_swamp_pokemon_list[poke_counter])] += rate
            except IndexError:
                pass
            except KeyError:
                poke_rate_dict[(cleaned_swamp_pokemon_list[poke_counter])] = rate
            poke_counter += 1


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


location_names = ['Kalos_Route_', 'Santalune_Forest', 'Glittering_Cave', 'Connecting_Cave', 'Reflection_Cave',
                  'Terminus_Cave', 'Frost_Cavern', 'Azure_Bay', 'Pokemon_Village', 'Lost_Hotel', 'Victory_Road_(Kalos)']

print()
print('Kalos Route 1 has no wild Pokemon.')

for location in location_names:
    if location == 'Kalos_Route_':
        for route in range(2, 23):
            route = str(route)
            area = location + route
            poke_dict = dataDownload(area)

            print(poke_dict)

            # This part repeats
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
            maximum = max(all_step_list)
            minimum = min(all_step_list)
            print()
            print('overall average:', average, 'max:', maximum, 'min:', minimum)
            print('average steps per pokemon:', average / len(poke_dict))


    else:
        area = location
        poke_dict = dataDownload(area)

        print(poke_dict)

        # This part repeats
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
        maximum = max(all_step_list)
        minimum = min(all_step_list)
        print()
        print('overall average:', average, 'max:', maximum, 'min:', minimum)
        print('average steps per pokemon:', average / len(poke_dict))
