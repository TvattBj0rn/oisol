# WardB0t

WardB0t is a discord bot designed to alleviate mental charges about Foxhole bases. Every base can consume up to 2 ressources hourly, and when you are the owner of several bases, it becomes hard to keep track of every base status, until they start to decay. 

## Features

- Create a base on the bot
- Set stockpile and hourly consumption for any base
- Automatic saving each time an edit action is completed
- Calculation of time left for each resource for each base
- Automatic alerts when the stockpile reach a threshold of left time

## Tech

- [Python](https://www.python.org/) - the best language that ever existed
- [Discordpy](https://discordpy.readthedocs.io/en/stable/) - python based discord API module

## Current Available commands

The prefix used for this bot is `!`.

- `base_new [base name]` - this command create a new base, the name can have space in it. Keep in mind that every parameter you give to the bot after base_new will be considered as part of the base name.
- `base_del [base name]` - this command delete a base currently existing. The naming works as in the base_new command.
- `base_status [base name]` - this command give the status of a specific base.
- `base_list` - this command list every base currently existing within the bot saved data.
- `base_consumption [ressource_type] [hourly_consumption] [base name]` - this command will set the hourly consumption of either `bsup` or `gsup` of a specific base (naming works as commands before).
- `base_set_stockpile [ressource_type] [stock] [base name]` - this command set the stockpile of a specific base to a specific amount.
- `base_add_stockpile [ressource_type] [stock] [base name]` - this command work as the `base_set_stockpile` but instead of replacing the stockpile value, it will add to the stock (either in crate are in units).

## Current background tasks
The background tasks are not accessible from the bot command interface but are instead task that continuously repeat while the bot is online.

- `update_stockpile` - every hour, the bot will applied a consumption rate on the stockpile. If the result of the division of the stockpile by the consumption rate get below a certain threshold (currently 5h), it will send an alert every hour until the stockpile is ressuplied.

## Planned features

The features below are not ordered by priority. These are just ideas that I might add later on the future, even though some are more likely than other.

- Add a kit system: the bot take a JSON file from the discord interface and add it to a kit list. The kit list would be accessible from a command `!kit` and a specific kit would be accessible using `!kit [kit name]`.
- Add a wiki parsing system using word recognition (e.g. `!info falchion` would get the infos of a falchion tank, `!info wt` would get info about watch towers, ...).
- A logi order system. This would work for example on frontline bases, as well as backlines factories. Using the command `!logi_order` would start an interaction with the bot, to define what is needed, the amount needed and the place to deliver.
- A complete rework of the bot interaction. Currently, users interact with the bot using commands. The idea would be for example to have a reaction system for some commands such as the `base_add_stockpile`.
- An implementation of the Foxhole War API to discord, allowing to target specifics regions and get more infos (If a regiment is focusing on Viper Pit for example, they do not really care about what happens in Westgate. However, what happens in Marban Hollow would be of bigger interest to the regiment.
- An operation planner. This would allow to set a specific target, a time and to pick what members are joining the OP using the discord reactions system.
