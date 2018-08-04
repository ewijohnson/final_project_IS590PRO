from lxml import html
import requests
import random
import pandas as pd

# Shows data and Pokemon for Pokemon X - steps will be the same but Pokemon will be different for Pokemon Y

# Excludes Horde Encounters, Rock Smash, Rustling Bush, Surfing, Fishing, Ceiling

# Combines rates for all environments per location, as the player will not necessarily stay within one type - they will
#   freely move around all areas per location


def dataDownload(location_name):
    """
    This function gets the relevant information on Pokemon encounters and encounter rates from the Bulbapedia
    webpage. The XPath is set up to handle different formats and data on the different webpages that are read. If used
    for other Pokemon games with other parts of the website, it will probably need to be checked and likely adjusted to
    account for other XML instances.

    :param location_name: a string that fills in the end of the webpage URL
    :return: poke_rate_dict: a dict that contains the names of the wild Pokemon in the location that match the test
    criteria as described (no surfing, no horde encounters, etc.) and the rates of encounter for each of those Pokemon
    :return: title[0]: the name of the location directly extracted from the webpage

    >>> location_name = 'Kalos_Route_2'
    >>> dataDownload(location_name)
    <BLANKLINE>
    ----------------------
    <BLANKLINE>
    Calculating Kalos Route 2 ...
    ({'Weedle': 11, 'Pidgey': 14, 'Zigzagoon': 15, 'Fletchling': 20, 'Bunnelby': 20, 'Scatterbug': 20}, 'Kalos Route 2')
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

    # Need to manually remove the final three Pokemon for Victory Road because of webpage XML
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

    # This extracts the rates of encounter for all Pokemon from the webpage
    rates = tree.xpath("//tr[@style='text-align:center;']/th/a/span[text()='X']/../../../td[@colspan='4']/text()")

    # As with swamp_pokemon, only used if there are Swamp Pokemon rates to extract, otherwise will return empty
    swamp_rates = tree.xpath("//tr[@style='text-align:center;']/th/a/span[text()='X']/../../../td[@colspan='4']/text()"
                             "[preceding::th/a/span[text()='Swamp']]")

    # For Route 19 again, where the Swamp XML is different:
    if not swamp_rates:
        swamp_rates = tree.xpath("//tr[@style='text-align:center;']/th/a/span[text()='X']/../../../td[@colspan='4']/"
                                 "text()[preceding::th[@style='background: #BDA595; color: #573118']]")

    # Sets up empty dictionary that will soon contain all relevant Pokemon and the associated rates of encounter
    poke_rate_dict = {}

    # Cleans up extracted Pokemon/environment data and adds them to a dictionary with associated rates of encounter
    pokemon = removePokemon(pokemon)
    cleaned_pokemon_list = removeEnvironmentType(pokemon)
    poke_rate_dict = createDict(poke_rate_dict, cleaned_pokemon_list, rates)

    # Repeats the above steps if there are Pokemon in the swamp_pokemon list, combines them into the same dict
    if swamp_pokemon:
        swamp_pokemon = removePokemon(swamp_pokemon)
        cleaned_swamp_pokemon_list = removeEnvironmentType(swamp_pokemon)
        poke_rate_dict = createDict(poke_rate_dict, cleaned_swamp_pokemon_list, swamp_rates)

    return poke_rate_dict, title[0]


def removePokemon(full_pokemon_list):
    """
    This function removes Pokemon that are not being tested for, based on the environment where they are found.

    :param full_pokemon_list: list of Pokemon and environments that was extracted from the webpage
    :return: full_pokemon_list: the same list, with any necessary Pokemon removed

    >>> full_pokemon_list = ['Geodude', 'Grass', 'Magikarp', 'Fishing', 'Tentacool', 'Surfing']
    >>> removePokemon(full_pokemon_list)
    ['Geodude', 'Grass', 'Fishing', 'Surfing']
    """

    # List of environment/terrain types that are not being tested for
    remove_environment_list = ['Fishing', 'Surfing', 'Ceiling', 'Rock\xa0Smash', 'Rustling bush', 'Shaking trash cans']

    for i, environment in enumerate(full_pokemon_list):
        if environment in remove_environment_list:
            del full_pokemon_list[i-1]

    return full_pokemon_list


def removeEnvironmentType(pokemon_removed_list):
    """
    This function takes the reduced list of Pokemon returned by removePokemon(), and removes the names of all
    environment types, leaving a list of just the relevant Pokemon to be tested. It 'removes' these names by appending
    the ones being kept to a new list.

    :param pokemon_removed_list: list of Pokemon with some removed from removePokemon() function
    :return: just_pokemon: list of only the relevant Pokemon, and all environment type names removed

    >>> pokemon_removed_list = ['Geodude', 'Grass', 'Fishing', 'Surfing']
    >>> removeEnvironmentType(pokemon_removed_list)
    ['Geodude']
    """

    # List of all environments to be removed from each Pokemon list before the main simulation
    all_environment_list = ['Surfing', 'Fishing', 'Grass', 'Yellow flowers', 'Red flowers', 'Purple flowers',
                            'Tall grass', 'Cave', 'Ceiling', 'Rock\xa0Smash', 'Terrain', 'Dirt', 'Swamp', 'Snow',
                            'Rustling bush', 'Shaking trash cans']
    just_pokemon = []
    for poke_or_environ in pokemon_removed_list:
        if poke_or_environ not in all_environment_list:
            just_pokemon.append(poke_or_environ)

    return just_pokemon


def createDict(pokemon_dict, pokemon_list, encounter_rates):
    """
    This function creates a dictionary associating each Pokemon with its rate of encounter. If there are Pokemon in the
    swamp_pokemon list, it will effectively combine that list with the other Pokemon list, into a single dictionary.

    :param pokemon_dict: dictionary of Pokemon and their encounter rates
    :param pokemon_list: list of relevant Pokemon after it has been cleaned
    :param encounter_rates: list of encounter rates for relevant Pokemon
    :return: pokemon_dict: now with more key-value pairs of Pokemon:Encounter Rates

    >>> pokemon_dict = {}
    >>> pokemon_list = ['Bulbasaur', 'Hoothoot', 'Caterpie']
    >>> encounter_rates = [' 50%\\n', ' 25%\\n', ' 25%\\n']
    >>> createDict(pokemon_dict, pokemon_list, encounter_rates)
    {'Bulbasaur': 50, 'Hoothoot': 25, 'Caterpie': 25}
    """

    poke_counter = 0
    for rate in encounter_rates:
        rate = (rate.strip().strip('%'))
        try:
            rate = int(rate)
        except ValueError:
            pass
        # This accounts for different 'variations' of the same Pokemon that have different encounter rates, such as
        #   different colors of one Pokemon. All variations of a Pokemon are considered to be the same Pokemon, as
        #   supported by the game (one 'Pokedex' (an in-game Pokemon database) entry per Pokemon, including all
        #   variations).
        try:
            pokemon_dict[(pokemon_list[poke_counter])] += rate
        except IndexError:
            pass
        except KeyError:
            pokemon_dict[(pokemon_list[poke_counter])] = rate
        poke_counter += 1

    return pokemon_dict


def singleRunThrough(pokemon_dictionary, outfile, sim_number):
    """
    This function computes one single run through as part of the entire simulation. It calculates one potential outcome
    for encountering all unique Pokemon in a location based off of the data extracted via XPath earlier. This function
    is repeated over and over again to create the Monte Carlo simulation.

    :param pokemon_dictionary: a dict compiled from the earlier function dataDownload() that contains the correct wild
    Pokemon along with their encounter rates
    :param outfile: the file that the data is printed to, this is passed through a couple functions so different parts
    of the data for each location can be added to the correct, single file
    :param sim_number: the number of iterations that the program is running for. It is passed into this function so that
    in the outfile, each line of a single run through can be numbered directly in the file for easier reading
    :return: step_counter: the number of steps that it took to encounter all unique Pokemon in the location

    >>> pokemon_dictionary = {'Zubat': 40, 'Geodude': 20, 'Oddish': 40}
    >>> outfile = open('Kalos_Route_100.txt', 'w')
    >>> sim_number = 10
    >>> a = singleRunThrough(pokemon_dictionary, outfile, sim_number)

    The variable 'a' that is returned represents a random integer. Because it is random, there is not a good way to
    include it in the doctests. To see possible outcomes for this function, delete everything to the left of and
    including the equal sign. This will cause the doctest to fail but will provide example outputs for this function.
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
    print('    ' + 'Pokemon by order of first encounter:', pokemon_encountered, file=outfile)

    return step_counter


def calculateSteps(number_of_sims, poke_dictionary, location_name):
    """
    This function loops through the singleRunThrough() function number_of_sims times. This combined effect will create a
    Monte Carlo simulation by getting the step count and adding the step count from each run through to the
    all_step_list list. It calls the printStats() function that takes the all_step_series and runs various statistical
    methods on it.

    :param number_of_sims: the number of iterations the simulation will run, input by the user in main()
    :param poke_dictionary: the dict that contains all available wild Pokemon and their rates of encounter
    :param location_name: the name of current location
    :return: all_step_series: pandas Series that contains all the step counts for one location
    :return: bottom_ten: Series of the 10th percentile of all_step_series
    :return: top_ninety: Series of the 90th percentile of all_step_series
    :return: avg_per_poke: average steps divided by number of Pokemon in that location

    >>> number_of_sims = 10
    >>> poke_dictionary = {'Zubat': 40, 'Geodude': 20, 'Oddish': 40}
    >>> location_name = 'Kalos_Route_100'
    >>> a, b, c, d = calculateSteps(number_of_sims, poke_dictionary, location_name)

    The variables a, b, c, d represent random values. a, b, and c are pandas Series will random values. d is a random
    integer that represents the average steps divided by the number of Pokemon in that location. To see some example
    outputs, the equals sign and anything to the left can be deleted; then when doctests are run, they will fail but
    show possible random outputs.
    """

    file_name = '_'.join(location_name.split())
    with open(file_name + '.txt', 'w') as f:
        print(location_name, file=f)
        all_step_list = []
        for i in range(number_of_sims):
            total_step_counter = singleRunThrough(poke_dictionary, f, i)
            all_step_list.append(total_step_counter)

        all_step_series = pd.Series(all_step_list)

        all_step_series, bottom_ten, top_ninety, avg_per_poke = printStats(all_step_series, number_of_sims,
                                                                           poke_dictionary, f)

    return all_step_series, bottom_ten, top_ninety, avg_per_poke


def printStats(all_steps, sim_number, p_dict, location_file):
    """
    This function calculates and prints all the statistics to separate files. As with the calculateSteps() function, it
    returns a large number of variables in order to better modularize the program. This was a decision that was made so
    that the program as a whole could be more readable and more easily understood.

    :param all_steps: pandas Series that contains all the steps counts for one location
    :param sim_number: the number of times the simulation was done
    :param p_dict: the dictionary that contains the available wild Pokemon and their encounter rates
    :param location_file: the name of the location
    :return: all_steps: pandas Series that contains all the step counts for one location
    :return: bottom_ten_percent: Series of the 10th percentile of all_steps
    :return: top_ninety_percent: Series of the 90th percentile of all_steps
    :return: average_by_pokemon: average steps divided by number of Pokemon in that location

    >>> all_steps = pd.Series([132, 144, 670, 490, 40, 566, 765, 334, 423, 537])
    >>> sim_number = 10
    >>> p_dict = {'Zubat': 40, 'Geodude': 20, 'Oddish': 40}
    >>> location_file = open('Kalos_Route_100.txt', 'w')
    >>> printStats(all_steps, sim_number, p_dict, location_file)
    (0    132
    1    144
    2    670
    3    490
    4     40
    5    566
    6    765
    7    334
    8    423
    9    537
    dtype: int64, 4    40
    dtype: int64, 6    765
    dtype: int64, 136.7)
    """

    ten_percent = int(sim_number * .1)
    sorted_steps = all_steps.sort_values()
    top_ninety_percent = sorted_steps.iloc[-ten_percent:]
    avg_top_ninety_percent = round(top_ninety_percent.mean(), 2)
    bottom_ten_percent = sorted_steps.iloc[:ten_percent]
    avg_bottom_ten_percent = round(bottom_ten_percent.mean(), 2)
    average = round(all_steps.mean(), 2)
    average_by_pokemon = round(average / len(p_dict), 2)

    print('\n', file=location_file)
    print('min steps:', all_steps.min(), '  max steps:', all_steps.max(), file=location_file)
    print('mean steps:', average, file=location_file)
    print('average steps per pokemon:', average_by_pokemon, file=location_file)

    print('', file=location_file)
    print('top 90%:', top_ninety_percent.min(), '-', all_steps.max(), 'steps', file=location_file)
    print('average of top 90%:', avg_top_ninety_percent, 'steps', file=location_file)

    print('', file=location_file)
    print('bottom 10%:', all_steps.min(), '-', bottom_ten_percent.max(), 'steps', file=location_file)
    print('average of bottom 10%:', avg_bottom_ten_percent, 'steps', file=location_file)

    return all_steps, bottom_ten_percent, top_ninety_percent, average_by_pokemon


def createPercentileDict(percentile_dict, location, percentile_data):
    """
    Creates dictionaries of minimum and maximum values by location to define percentile boundaries

    :param percentile_dict: dictionary that contains data on a percentile (10th, 90th, etc.) associated with locations
    :param location: location name to be used as dictionary key
    :param percentile_data: pandas Series that contains data on percentile (10th, 90th, etc.)
    :return: percentile_dict: after adding another key-value pair of location and data

    >>> percentile_dict = {}
    >>> location = 'Kalos_Route_100'
    >>> percentile_data = pd.Series([132, 144, 670, 490, 40, 566, 765, 334, 423, 537])
    >>> createPercentileDict(percentile_dict, location, percentile_data)
    {'Kalos_Route_100': (40, 765)}
    """
    percentile_dict[location] = (percentile_data.min(), percentile_data.max())
    return percentile_dict


def createAveragePercentileDict(percentile_dict, location, percentile_data):
    """
    Creates dictionaries of mean values by location of a given data set (percentiles, all steps, etc.)

    :param percentile_dict: dictionary that contains data on a percentile (10th, 90th, etc.) associated with locations
    :param location: location name to be used as dictionary key
    :param percentile_data: pandas Series that contains data on percentile (10th, 90th, all data, etc.)
    :return: percentile_dict: after adding another key-value pair of location and data

    >>> percentile_dict = {}
    >>> location = 'Kalos_Route_100'
    >>> percentile_data = pd.Series([132, 144, 670, 490, 40, 566, 765, 334, 423, 537])
    >>> createAveragePercentileDict(percentile_dict, location, percentile_data)
    {'Kalos_Route_100': 410.1}
    """
    percentile_dict[location] = percentile_data.mean()
    return percentile_dict


def createRangeDict(percentile_dict, location, percentile_data):
    """
    Creates dictionaries of range values, including the min and max values, by location for a set of data

    :param percentile_dict: dictionary that contains data on a percentile (10th, 90th, etc.) associated with locations
    :param location: location name to be used as dictionary key
    :param percentile_data: pandas Series that contains data on percentile (10th, 90th, all data, etc.)
    :return: percentile_dict: after adding another key-value pair of location and data

    >>> percentile_dict = {}
    >>> location = 'Kalos_Route_100'
    >>> percentile_data = pd.Series([132, 144, 670, 490, 40, 566, 765, 334, 423, 537])
    >>> createRangeDict(percentile_dict, location, percentile_data)
    {'Kalos_Route_100': (725, 40, 765)}
    """

    percentile_dict[location] = ((percentile_data.max())-(percentile_data.min()), percentile_data.min(),
                                 percentile_data.max())
    return percentile_dict


def main():
    while True:
        number_of_simulations = input('How many iterations per location would you like to run? \nAt least 10000 is '
                                      'suggested. \nEnter the number, or just press "Enter" to quit: ')
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

    print()
    print('Preparing for first data download ...')

    # Sets up empty dictionaries
    tenth_percentile_dict = {}
    ninetieth_percentile_dict = {}
    avg_tenth_percentile_dict = {}
    avg_ninetieth_percentile_dict = {}
    location_averages_dict = {}
    location_minmax_dict = {}
    location_averages_by_pokemon_dict = {}

    location_names = ['Kalos_Route_', 'Santalune_Forest', 'Glittering_Cave', 'Connecting_Cave', 'Reflection_Cave',
                      'Terminus_Cave', 'Frost_Cavern', 'Azure_Bay', 'Pokemon_Village', 'Lost_Hotel',
                      'Victory_Road_(Kalos)']

    for location in location_names:
        if location == 'Kalos_Route_':
            for route in range(2, 23):
                route = str(route)
                area = location + route
                poke_dict, title = dataDownload(area)
                all_step_data, tenth_percentile, ninetieth_percentile, avg_by_num_of_pokemon = calculateSteps(
                    number_of_simulations, poke_dict, title)

                tenth_percentile_dict = createPercentileDict(tenth_percentile_dict, area, tenth_percentile)
                ninetieth_percentile_dict = createPercentileDict(ninetieth_percentile_dict, area, ninetieth_percentile)

                avg_tenth_percentile_dict = createAveragePercentileDict(avg_tenth_percentile_dict, area,
                                                                        tenth_percentile)
                avg_ninetieth_percentile_dict = createAveragePercentileDict(avg_ninetieth_percentile_dict, area,
                                                                            ninetieth_percentile)

                location_averages_dict = createAveragePercentileDict(location_averages_dict, area, all_step_data)

                location_minmax_dict = createRangeDict(location_minmax_dict, area, all_step_data)

                location_averages_by_pokemon_dict[area] = avg_by_num_of_pokemon

        # For all other locations that aren't a Route
        else:
            area = location
            poke_dict, title = dataDownload(area)
            all_step_data, tenth_percentile, ninetieth_percentile, avg_by_num_of_pokemon = calculateSteps(
                number_of_simulations, poke_dict, title)

            tenth_percentile_dict = createPercentileDict(tenth_percentile_dict, area, tenth_percentile)
            ninetieth_percentile_dict = createPercentileDict(ninetieth_percentile_dict, area, ninetieth_percentile)

            avg_tenth_percentile_dict = createAveragePercentileDict(avg_tenth_percentile_dict, area, tenth_percentile)
            avg_ninetieth_percentile_dict = createAveragePercentileDict(avg_ninetieth_percentile_dict, area,
                                                                        ninetieth_percentile)

            location_averages_dict = createAveragePercentileDict(location_averages_dict, area, all_step_data)

            location_minmax_dict = createRangeDict(location_minmax_dict, area, all_step_data)

            location_averages_by_pokemon_dict[area] = avg_by_num_of_pokemon

    # Prints off all aggregate statistics to separate file
    with open('Kalos_Aggregate_Statistics.txt', 'w') as file_out:
        print('Aggregate Statistics for Kalos, Pokemon X:', file=file_out)
        print('How many steps does it take to encounter each unique type of Pokemon a minimum of one time in each '
              'location?', file=file_out)
        print('Note: This only includes land-based, single Pokemon encounters, of all combined terrain types per '
              'location.', file=file_out)
        print('', file=file_out)
        print('Locations sorted by lowest to highest step count, 90th Percentile:', file=file_out)
        for item in sorted(ninetieth_percentile_dict.items(), key=lambda x: x[1][0]):
            print(item[0], 'with', item[1][0], 'steps, and a range of', item[1][0], '-', item[1][1],
                  'steps', file=file_out)
        print('', file=file_out)
        print('Locations sorted by lowest to highest step count, average of the 90th Percentile:', file=file_out)
        for item in sorted(avg_ninetieth_percentile_dict.items(), key=lambda x: x[1]):
            print(item[0], 'with', item[1], 'steps', file=file_out)
        print('', file=file_out)
        print('Locations sorted by lowest to highest step count, 10th Percentile:', file=file_out)
        for item in sorted(tenth_percentile_dict.items(), key=lambda x: x[1][1]):
            print(item[0], 'with', item[1][1], 'steps, and a range of', item[1][0], '-', item[1][1],
                  'steps', file=file_out)
        print('', file=file_out)
        print('Locations sorted by lowest to highest step count, average of the 10th Percentile:', file=file_out)
        for item in sorted(avg_tenth_percentile_dict.items(), key=lambda x: x[1]):
            print(item[0], 'with', item[1], 'steps', file=file_out)
        print('', file=file_out)
        print('Locations sorted by lowest to highest step count, 50th Percentile:', file=file_out)
        for item in sorted(location_averages_dict.items(), key=lambda x: x[1]):
            print(item[0], 'with', item[1], 'steps', file=file_out)
        print('', file=file_out)
        print('Locations sorted by smallest to largest range of step count values:', file=file_out)
        for item in sorted(location_minmax_dict.items(), key=lambda x: x[1][0]):
            print(item[0], 'with a range of', item[1][0], 'steps, ranging from', item[1][1], '-', item[1][2], 'steps',
                  file=file_out)
        print('', file=file_out)
        print('Locations sorted by lowest to highest average step count per number of Pokemon:', file=file_out)
        for item in sorted(location_averages_by_pokemon_dict.items(), key=lambda x: x[1]):
            print(item[0], 'with', item[1], 'steps per Pokemon', file=file_out)


if __name__ == '__main__':
    main()
