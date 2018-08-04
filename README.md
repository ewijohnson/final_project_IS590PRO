# Number of Steps to Encounter All Unique Pokemon by Location: Pokemon X

## Team Member(s): 
Eric Johnson

# Monte Carlo Simulation Scenario & Purpose:
This simulation looks at the Pokemon video games, specifically Pokemon X. It will determine the minimum, maximum, and overall average number of steps (along with other statistics) it takes for the player to encounter at least one of every Pokemon that can be found in each location by walking. This will exclude Pokemon encountered in the following ways: Surfing, Fishing, Horde Encounters, Rock Smash, Rustling Bush, and Ceiling. It will include all locations in Pokemon X: Routes 2-22 (Route 1 has no wild Pokemon), Santalune Forest, Glittering Cave, Connecting Cave, Reflection Cave, Terminus Cave, Frost Cavern, Azure Bay, Pokemon Village, Lost Hotel, and Victory Road. After data on each location has been gathered, statistics from the game as a whole will be calculated.

The simulation looks at all environment types within each location as a whole: so for example, on Route 4 where Pokemon can be found in Yellow Flowers and Red Flowers, the rates for each Pokemon are calculated by combining the Yellow and Red Flowers. This is done because it is assumed that each player generally walks around in all environment types while looking for Pokemon rather than restricting themselves to a single environment type.  

Some background for anyone not familiar with the Pokemon games: in the games, when your player walks in certain areas (such as grass, caves, or water) in each location, there is a chance for an encounter with a random wild Pokemon after a random number of steps. The Pokemon and the chance of their encounters differ by each clearly defined location. Each location will be calculated and simulated separately (e.g., 100,000 trials for Route 2, 100,000 for Route 3, etc.). 

For example, in Route 1, Pokemon A has a 12.5% chance of being encountered, Pokemon B has a 50% chance, and Pokemon C has an 37.5% chance. What is the minimum, maximum, and overall average number of steps the player must take to encounter all three Pokemon at least once? 

## Simulation's variables of uncertainty
1. Number of steps between wild Pokemon encounters (a range of 1-31)**
2. Percent chance of encountering each Pokemon in a location (pulled from pages at bulbapedia.bulbagarden.net)

** Initial data gathered from source 1 at the bottom, and then corroborated through personal testing for Pokemon X

## Hypothesis or hypotheses before running the simulation:
Before running this program, I believed that the average number of steps to encounter Pokemon would be based off of the number of Pokemon in each area, and therefore while the rates per location may differ, if the rates are divided by the total number of Pokemon in that area, they will average out to be similar. This turned out to be false, as the averages by number of Pokemon ranged from 35.32 steps on Route 13 to 77.08 steps in Frost Cavern (and a slight outlier of 414.8 steps on Route 17, which will be discussed in the following section).  

## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)
Looking at data on the lowest 10th percentiles, the overall average, and the highest 90th percentiles, each location is generally pretty much in the same place. Routes 13 and 9 are consistently at the lowest step count end, while Route 22 and Santalune Forest are consistently at the highest step count end. 

There seems to be no real correlation between step count and location in the game. Route 22 is one of the final areas in the game, and it is consistently ranked at the high end, yet Santalune Forest is also consistently ranked at the high end, and it is the second location that is discovered in the game. Route 2, the first location, is generally on the lower-middle side, while Routes 9 and 13, mid-game, are at the very bottom (lowest) step count end. 

Route 17 seems to be a bit of an outlier, even after running 100,000 simulations. This is because Route 17 has one Pokemon that has an encounter rate of 1%. This is the lowest encounter rate in the entire game (the next lowest is 5%), and because of this, it skews the high end of the data to relatively enormous numbers. The maximum step count for Route 17 is 20,497, while the next highest is only 4816 steps. However, this does not affect the lowest 10th percentile, as the minimum can still be as low as the other locations, which is why Route 17 is in the middle for any calculations involving the 10th percentile, yet is always at the far top end for any overall averages or 90th percentile statistics. 

Besides Route 17, the rest of the step counts for all locations gradually increase when looking at the rest of the data, even though there is no correlation between which locations increase and their location in the sequence of playing the game. To look at one example, the overall average step count incrementally increases from 105.97 steps at Route 13 to 735.63 steps at Route 22 (and then jumps to 1659.2 steps at Route 17). The upper cutoff of the 10th percentile step count increases from 44 steps at Route 9 to 377 steps at Route 22 (and note that for the 10th percentile, Route 17 is not an outlier, for reasons discussed previously). 

For the 10th percentile data, the locations were sorted by the upper limit of the 10th percentile rather than the minimum value. This was done to attempt to standardize the results, as the minimum can in some cases be much lower than the rest of the values (the minimum, like the maximum, can often be outliers when compared to the rest of the data). This was similarly done with the 90th percentile data, with the bottom cutoff for the 90th percentile being used to rank the locations, rather than the absolute maximum value. 

The average of the 10th and 90th percentiles were also calculated, to see how far the data tends to skew in one direction, if at all. For one example, the 10th percentile of Route 22 ranges from 104-377 steps, yet the average of the 10th percentile is 316.92. This shows that much more of the data is closer to the 10th percentile upper limit than to the absolute minimum (further providing evidence that the minimum values can often be outliers). 

The range of step counts for each location was also calculated, to see how much variation there can be in each location. As expected, Route 17 had the largest range of 20,482 steps (15-20,497). Second from the top was Frost Cavern with a range of 4802 steps (39-4841), followed closely by Santalune Forest at 4720 steps (87-4807). Route 13 had the smallest range, a value of 953 steps (4-957). Interestingly, while Route 13 and Route 9 were nearly always at the low end for all calculations, here, Route 9 had a much larger range than Route 13, and was fourth from the bottom instead of the expected second, with a range of 1337 steps (4-1341).  

Overall, this data can come in useful if a player is unsure of how much longer to search for certain Pokemon in various areas of Kalos in Pokemon X. In 90% of cases, all Pokemon in an area will have been encountered once by the step count at the 90th percentile cutoff, and only 10% of the time will it take more steps than that. 

## Instructions on how to use the program:
Run program normally using Python. Enter the number of simulations you'd like to run when prompted. Output will be in text files. 
Program took about 6 minutes to run on my machine when number of simulations was 100,000, so it may be slower on other machines.
Program was fast (a minute or two at the most) when only doing 10,000 simulations and the results were nearly identical. 

The program will create a series of output files, one for each location and one aggregate statistics file. 

The Location files contain data on each of the runs, and **AT THE BOTTOM THERE ARE BRIEF AGGREGATE STATISTICS FOR THAT LOCATION ONLY**.
Because of size limits, the Location files uploaded here are for 10,000 simulations, while the aggregate statistics file is for data gathered from 100,000 simulations. While a few numbers may be slightly different, overall the results are nearly identical.

The aggregate statistics file contains data from looking at all locations together, comparing and ranking the locations by various statistical methods. 


## All Sources Used:
1. https://ssl-forum-files.fobby.net/forum_attachments/0029/3387/Pokemon_Statistics_nice.pdf
"Player Speed vs. Wild Pokémon Encounter Frequency in Pokémon SoulSilver"

2. bulbapedia.bulbagarden.net, all pages on Pokemon X routes/locations (Kalos):
bulbapedia.bulbagarden.net/wiki/Kalos_Route_2, 
bulbapedia.bulbagarden.net/wiki/Kalos_Route_3,
...etc.









 
