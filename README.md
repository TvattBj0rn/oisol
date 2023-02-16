
# WardB0t

WardB0t is a discord bot designed to alleviate mental charges about Foxhole bases. Every base can consume up to 2 ressources hourly, and when you are the owner of several bases, it becomes hard to keep track of every base status, until they start to decay. 

## Modules

- **Stats module**: This module aims to make the retrivial of wiki information simpler. Right now, it can only get the statistics from tanks but will be able to get features for all vehicles in the future.
- **Bases module**: This module is base managing tool. It allows people to get current status of gsup/bsup stockpile and consumption from a base without having to connect in game. As of right now, the module is not working properly and needs an update.

## Tech

- [Python](https://www.python.org/) - the best language that ever existed;
- [Discord.py](https://discordpy.readthedocs.io/en/stable/) - python based discord API module;
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) - Python library used for scarping.

## Current Available commands

The prefix used for this bot is `$`, but the commands are hybrid so `/` also works.

- `fstats tank_name`: this command allow the user to get stats of a specific tank.


## Planned features

The features below are not ordered by priority. These are just ideas that I might add later on the future, even though some are more likely than other.

- Add a kit system: the bot take a JSON file from the discord interface and add it to a kit list. The kit list would be accessible from a command `!kit` and a specific kit would be accessible using `!kit [kit name]`.
- Add a wiki parsing system using word recognition (e.g. `!info falchion` would get the infos of a falchion tank, `!info wt` would get info about watch towers, ...).
- A logi order system. This would work for example on frontline bases, as well as backlines factories. Using the command `!logi_order` would start an interaction with the bot, to define what is needed, the amount needed and the place to deliver.
- A complete rework of the bot interaction. Currently, users interact with the bot using commands. The idea would be for example to have a reaction system for some commands such as the `base_add_stockpile`.
- An implementation of the Foxhole War API to discord, allowing to target specifics regions and get more infos.
- An operation planner. This would allow to set a specific target, a time and to pick what members are joining the OP using the discord reactions system.
