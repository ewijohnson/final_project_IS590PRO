# Title: 

## Team Member(s): 
Eric Johnson

# Monte Carlo Simulation Scenario & Purpose:
This simulation will be looking at the Pokemon video games, specifically Pokemon X. It will determine the minimum, maximum, and overall average number of steps it takes for the player to encounter at least one of every Pokemon that can be found in each location by walking. This will exclude Pokemon encountered in the following ways: Surfing, Fishing, Horde Encounters, Rock Smash, Rustling Bush, and Ceiling. It will include all locations in Pokemon X: Routes 2-22 (Route 1 has no wild Pokemon), Santalune Forest, Glittering Cave, Connecting Cave, Reflection Cave, Terminus Cave, Frost Cavern, Azure Bay, Pokemon Village, Lost Hotel, and Victory Road. 

The simulation looks at all environment types within each location as a whole: so for example, on Route 4 where Pokemon can be found in Yellow Flowers and Red Flowers, the rates for each Pokemon are calculated by combining the Yellow and Red Flowers. This is done because it is assumed that each player generally walks around in all environment types while looking for Pokemon rather than restricting themselves to a single environment type.  

Some background for anyone not familiar with the Pokemon games: in the games, when your player walks in certain areas (such as grass, caves, or water) in each location, there is a chance for an encounter with a random wild Pokemon after a random number of steps. The Pokemon and the chance of their encounters differ by each clearly defined location. Each location will be calculated and simulated separately (e.g., 100,000 trials for Route 2, 100,000 for Route 3, etc.). 

For example, in Route 1, Pokemon A has a 12.5% chance of being encountered, Pokemon B has a 50% chance, and Pokemon C has an 37.5% chance. What is the minimum, maximum, and overall average number of steps the player must take to encounter all three Pokemon at least once? 

## Simulation's variables of uncertainty
1. Number of steps between wild Pokemon encounters (a range of 1-31)
2. Percent chance of encountering each Pokemon in a location (pulled from pages at bulbapedia.bulbagarden.net)

## Hypothesis or hypotheses before running the simulation:
Before running this program, I believed that the average number of steps to encounter Pokemon would be based off of the number of Pokemon in each area, and therefore while the rates per location may differ, if the rates are divided by the total number of Pokemon in that area, they will average out to be similar. 

## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)
After running the initial simulation, I added the calculation to see if the average number of steps per Pokemon for each area was similar. Upon running the simulation again, I saw that it was not. One location, Route 17, had an unusually higher than average step count, and this is because one Pokemon there has an encounter chance of only 1% - much lower than any other Pokemon.

Generally speaking, many of the overall average step counts are in the 400-600 step range, with the minimum usually around 40-70 and the maximum somewhere in the low thousands. Many of the highest numbers are somewhat outliers, however, as when the top 90% is calculated, it usually begins around 700-800.

## Instructions on how to use the program:
Run program normally. Enter the number of simulations you'd like to run when prompted. Output will be in text files. 
Program took a few minutes to run on my machine when number of simulations was 100,000.

## All Sources Used:
bulbapedia.bulbagarden.net, all pages on Pokemon X routes/locations (Kalos):
bulbapedia.bulbagarden.net/wiki/Kalos_Route_2
bulbapedia.bulbagarden.net/wiki/Kalos_Route_3
...etc.









 
