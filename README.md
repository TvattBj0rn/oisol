
# WardB0t

Companion bot for the FCF foxhole regiment ! 

## Modules

- **Registre**: This module allows us to keep track of the enlisted players in the regiment, allowing us to see for how long a player has been in the regiment.
- **Stockpile**: This module a stockpile viewer tool. It allows people to add and view stockpiles on an embedded list.

## Tech

- [Python](https://www.python.org/) - the best language that ever existed;
- [Discord.py](https://discordpy.readthedocs.io/en/stable/) - python based discord API module;

## Current Available commands

The prefix used for this bot is `$`, but the commands are hybrid so `/` also works.


## Planned features

The features below are not ordered by priority. These are just ideas that I might add later on the future, even though some are more likely than other.

- Add a wiki parsing system using word recognition (e.g. `!info falchion` would get the infos of a falchion tank, `!info wt` would get info about watch towers, ...). (done but deleted due to it not being used)

- An implementation of the Foxhole War API to discord, allowing to target specifics regions and get more infos. (Currently working on it)

- A logi order system. This would work for example on frontline bases, as well as backlines factories. Using the command `!logi_order` would start an interaction with the bot, to define what is needed, the amount needed and the place to deliver.
- An operation planner. This would allow to set a specific target, a time and to pick what members are joining the OP using the discord reactions system.
