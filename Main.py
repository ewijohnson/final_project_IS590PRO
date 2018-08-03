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
    """
    This function gets the relevant information on Pokemon encounters and encounter rates from the Bulbapedia
    webpage. Returns poke_rate_dict, a dictionary that contains each Pokemon that can be found in the area and its rate
    of encounter.

    :param location_name:
    :return:
    """

    url = 'https://bulbapedia.bulbagarden.net/wiki/' + location_name
    page = requests.get(url)
    tree = html.fromstring(page.content)

    title = tree.xpath("//h1[@id='firstHeading']/text()")
    print()
    print('----------------------')
    print()
    print('Calculating', title[0], '...')

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

    return poke_rate_dict, title[0]


def singleRunThrough(pokemon_dictionary, outfile, sim_number):
    """
    This function computes one single run through as part of the entire simulation.

    :param pokemon_dictionary:
    :param outfile:
    :param sim_number:
    :return:
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

    print(str(sim_number + 1) + '. ' + 'Total steps:', step_counter, file=outfile)
    print('    ' + 'Pokemon in order of first encounter:', pokemon_encountered, file=outfile)

    return step_counter


def calculateSteps(number_of_sims, poke_dictionary, location_name):
    """
    This function calculates the number of steps by computing x number of single runs.

    :param number_of_sims:
    :param poke_dictionary:
    :param location_name:
    :return:
    """

    file_name = '_'.join(location_name.split())
    with open(file_name + '.txt', 'w') as f:
        print(location_name, file=f)
        all_step_list = []
        for i in range(number_of_sims):
            total_step_counter = singleRunThrough(poke_dictionary, f, i)
            all_step_list.append(total_step_counter)

        bottom_ten, overall_avg, top_ninety, avg_per_poke, minim, maxim, avg_bottom, avg_top = \
            printStats(all_step_list, number_of_sims, poke_dictionary, f)

    return bottom_ten, overall_avg, top_ninety, avg_per_poke, minim, maxim, avg_bottom, avg_top


def printStats(all_steps, sim_number, p_dict, location_file):
    """
    This function calculates and prints all the statistics to separate files.

    :param all_steps:
    :param sim_number:
    :param p_dict:
    :param location_file:
    :return:
    """

    ten_percent = int(sim_number * .1)
    sorted_list = sorted(all_steps)
    top_ninety_percent = sorted_list[-ten_percent]
    avg_top_ninety_percent = round(sum(sorted_list[-ten_percent:]) / len(sorted_list[-ten_percent:]), 2)
    bottom_ten_percent = sorted_list[ten_percent]
    avg_bottom_ten_percent = round(sum(sorted_list[:ten_percent]) / len(sorted_list[:ten_percent]), 2)
    average = round(sum(all_steps) / len(all_steps), 2)
    average_by_pokemon = round(average / len(p_dict), 2)
    maximum = max(all_steps)
    minimum = min(all_steps)

    print('\n', file=location_file)
    print('min steps:', minimum, '  max steps:', maximum, file=location_file)
    print('50%:', average, 'steps', file=location_file)
    print('average steps per pokemon:', average_by_pokemon, file=location_file)

    print('', file=location_file)
    print('top 90%:', top_ninety_percent, '-', maximum, 'steps', file=location_file)
    print('average of top 90%:', avg_top_ninety_percent, 'steps', file=location_file)

    print('', file=location_file)
    print('bottom 10%:', minimum, '-', bottom_ten_percent, 'steps', file=location_file)
    print('average of bottom 10%:', avg_bottom_ten_percent, 'steps', file=location_file)

    return bottom_ten_percent, average, top_ninety_percent, average_by_pokemon, minimum, \
           maximum, avg_bottom_ten_percent, avg_top_ninety_percent


def checkLowestTenth(tenth, lowest_tenth, lowest_tenth_loc, loc):
    if tenth < lowest_tenth:
        lowest_tenth = tenth
        lowest_tenth_loc = loc
    return lowest_tenth, lowest_tenth_loc


def checkHighestNinetieth(ninetieth, highest_ninetieth, highest_ninetieth_loc, loc):
    if ninetieth > highest_ninetieth:
        highest_ninetieth = ninetieth
        highest_ninetieth_loc = loc
    return highest_ninetieth, highest_ninetieth_loc


def main():
    while True:
        number_of_simulations = input('How many iterations of the simulation would you like to run? \nAt least 10000 '
                                          'is suggested. \nEnter the number, or just press "Enter" to quit: ')
        try:
            number_of_simulations = int(number_of_simulations)
        except ValueError:
            if number_of_simulations == '':
                print('Thanks for using this program!')
                quit()
            else:
                print()
                print('Please try again and enter a whole number greater than or equal to 1.')
                print()
                continue

        if number_of_simulations >= 1:
            break
        elif number_of_simulations < 1:
            print()
            print('Please try again and enter a whole number greater than or equal to 1.')
            print()
            continue

    lowest_tenth_percentile = 9999999
    highest_ninetieth_percentile = 0
    lowest_tenth_percentile_location = ''
    highest_ninetieth_percentile_location = ''
    location_averages_dict = {}
    location_averages_by_pokemon_dict = {}
    tenth_percentile_dict = {}
    ninetieth_percentile_dict = {}
    avg_tenth_percentile_dict = {}
    avg_nintieth_percentile_dict = {}

    location_names = ['Kalos_Route_', 'Santalune_Forest', 'Glittering_Cave', 'Connecting_Cave', 'Reflection_Cave',
                      'Terminus_Cave', 'Frost_Cavern', 'Azure_Bay', 'Pokemon_Village', 'Lost_Hotel',
                      'Victory_Road_(Kalos)']

    for location in location_names:
        if location == 'Kalos_Route_':
            for route in range(2, 23):
                route = str(route)
                area = location + route
                poke_dict, title = dataDownload(area)
                tenth_percentile, fiftieth_percentile, ninetieth_percentile, avg_by_num_of_pokemon, minimum_steps, \
                maximum_steps, avg_tenth, avg_nintieth = calculateSteps(number_of_simulations, poke_dict, title)

                lowest_tenth_percentile, lowest_tenth_percentile_location = \
                    checkLowestTenth(tenth_percentile, lowest_tenth_percentile, lowest_tenth_percentile_location, area)

                highest_ninetieth_percentile, highest_ninetieth_percentile_location = \
                    checkHighestNinetieth(ninetieth_percentile, highest_ninetieth_percentile,
                                          highest_ninetieth_percentile_location, area)

                tenth_percentile_dict[area] = (tenth_percentile, (minimum_steps, tenth_percentile))
                ninetieth_percentile_dict[area] = (ninetieth_percentile, (ninetieth_percentile, maximum_steps))

                avg_tenth_percentile_dict[area] = avg_tenth
                avg_nintieth_percentile_dict[area] = avg_nintieth

                location_averages_dict[area] = fiftieth_percentile
                location_averages_by_pokemon_dict[area] = avg_by_num_of_pokemon

        else:
            area = location
            poke_dict, title = dataDownload(area)
            tenth_percentile, fiftieth_percentile, ninetieth_percentile, avg_by_num_of_pokemon, minimum_steps, \
            maximum_steps, avg_tenth, avg_nintieth = calculateSteps(number_of_simulations, poke_dict, title)

            lowest_tenth_percentile, lowest_tenth_percentile_location = \
                checkLowestTenth(tenth_percentile, lowest_tenth_percentile, lowest_tenth_percentile_location, area)

            highest_ninetieth_percentile, highest_ninetieth_percentile_location = \
                checkHighestNinetieth(ninetieth_percentile, highest_ninetieth_percentile,
                                      highest_ninetieth_percentile_location, area)

            tenth_percentile_dict[area] = (tenth_percentile, (minimum_steps, tenth_percentile))
            ninetieth_percentile_dict[area] = (ninetieth_percentile, (ninetieth_percentile, maximum_steps))

            avg_tenth_percentile_dict[area] = avg_tenth
            avg_nintieth_percentile_dict[area] = avg_nintieth

            location_averages_dict[area] = fiftieth_percentile
            location_averages_by_pokemon_dict[area] = avg_by_num_of_pokemon

    with open('Kalos_Aggregate_Statistics.txt', 'w') as file_out:
        print('Aggrgeate Statistics for Kalos, Pokemon X:', file=file_out)
        print('', file=file_out)
        print('Locations sorted by lowest to highest step count, 90th Percentile:', file=file_out)
        for item in sorted(ninetieth_percentile_dict.items(), key=lambda x: x[1][0]):
            print(item[0], 'with', item[1][0], 'steps, and a range of', item[1][1][0], '-', item[1][1][1],
                  'steps', file=file_out)
        print('', file=file_out)
        print('Locations sorted by lowest to highest step count, average of the 90th Percentile:', file=file_out)
        for item in sorted(avg_nintieth_percentile_dict.items(), key=lambda x: x[1]):
            print(item[0], 'with', item[1], 'steps', file=file_out)
        print('', file=file_out)
        print('Locations sorted by lowest to highest step count, 10th Percentile:', file=file_out)
        for item in sorted(tenth_percentile_dict.items(), key=lambda x: x[1][0]):
            print(item[0], 'with', item[1][0], 'steps, and a range of', item[1][1][0], '-', item[1][1][1],
                  'steps', file=file_out)
        print('', file=file_out)
        print('Locations sorted by lowest to highest step count, average of the 10th Percentile:', file=file_out)
        for item in sorted(avg_tenth_percentile_dict.items(), key=lambda x: x[1]):
            print(item[0], 'with', item[1], 'steps', file=file_out)
        print('', file=file_out)
        print('Overall lowest 10th percentile:', lowest_tenth_percentile, 'steps at', lowest_tenth_percentile_location,
              file=file_out)
        print('Overall highest 90th percentile:', highest_ninetieth_percentile, 'steps at',
              highest_ninetieth_percentile_location, file=file_out)
        print('', file=file_out)
        print('Locations sorted by lowest to highest step count, 50th Percentile:', file=file_out)
        for item in sorted(location_averages_dict.items(), key=lambda x: x[1]):
            print(item[0], 'with', item[1], 'steps', file=file_out)
        print('', file=file_out)
        print('Locations sorted by lowest to highest average step count per number of Pokemon:', file=file_out)
        for item in sorted(location_averages_by_pokemon_dict.items(), key=lambda x: x[1]):
            print(item[0], 'with', item[1], 'steps', file=file_out)


if __name__ == '__main__':
    main()
