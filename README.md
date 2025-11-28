# FFXIV-Crossbreed-Helper
A program to help with crossbreeding seeds in Final Fantasy XIV

This program was created after a friend of mine asked for a tool to help her with making Thavnairian Onion Seeds.
DISCLAIMER: The whole program was written in python and was not optimized for speed! Runtimes of ~2 minutes per function may occur (if its longer than that, it *might* be an error).
It also has a pretty basic design, if enough people want it prettier, I'll try my best to prettify it!
The program is split into three functions:

## Part 1: Create list of steps from seeds in inventory to target seed(s)

Say you want to create a specific seed (e.g. Tavnairian Onion Seeds) and you have an inventory full of other seeds you gathered/found/bought previously, and you want to know which seeds you'd have to
gather/cross to get to your target seed. This function will give you the shortest way from your inventory to your target seed, or, if there are multiple ways,
a list of them. Also, if you're not afraid to gather some more seeds yourself, there's a checkbox which switches the function.
With the checkbox on, the program will check if any seed that is produced by crossbreeding can instead be gathered. This reduces the amount of steps needed, but you do need a high level
of Botanist for some of the seeds (or other requirements, like Grand Company Rank and Seals, Allied Seals, etc.).
Beware that gathering a seed is in itself one step.

## Part 2: Create list of seeds that can be made from seeds in your inventory in X steps

If you don't know what you want to do with all of the seeds you gathered, this function can tell you all the seeds that can be made from your inventory seeds in a certain amount of steps.
As with the first function, you can choose if you want the program to account for all the seeds that can be gathered in the wild/bought/otherwise obtained.

## Part 3: For any seed, create a list of gatherable seeds that produce that seed

If you want to produce a certain seed but don't know where to start, this program can tell you where! When you input a seed, you get a list of seeds that can be gathered/obtained otherwise, from which you can then
make the seed in question.
ANOTHER DISCLAIMER: This particular function will only give you a very limited number of options, compared to the actual amount. If this function were to work as first intended, it would very quickly
either reach recursion depth or the list would be at least half a gigabyte (!) big. Thus, I went for the more conservative approach. Just because the program only outputs one "option list" for a seed, that
doesn't mean that there aren't others!

## How to Install:
- go to releases
- download the .zip file
- unpack it in the location of your choosing
- Run the .exe file

If you have any suggestions or criticisms or if you find any bugs, feel free to contact me or create an issue!
Also, tell others about this program! I hope to help as many people as possible, even if its with something as "banal" as this^^ If you think my work is worth money, please feel free to donate some on ko-fi.com/nick75 <3

- nick75

# NEW FEATURES! by kgetech:

## A Quit Button:
- Added a quit button to the program (Oooh, fancy!).

## Export and Import Options:
- Added export and import buttons for "Shortest Path" Inventory and Targets.
- Added export and import button for "What Can You Make?" Inventory.
- These save to sh_inventory.csv, sh_targets.csv and all_inventory.csv 
  respectively.
- TODO: Lots of code duplication, refactoring would be nice if we wanted to 
  extend or expand this project.
- Other Notes: I think nick75 did a great job with this project, and I 
  think we could easily expand/extend this project if we do some 
  re-arranging of the code.