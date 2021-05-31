# CommunityBot

This is a bot made partially by the community, with the lead dev being Skezza#1139.\
This bot will remain open source, and provide fun information about your profile, such as it's value.\
Anyone can make a pull request, and it'll be reviewed and possibly added.\
If you make good suggestions, you'll be invited into a special community-bot-dev channel, where we can further discuss ideas.

Here's what the code currently does to get the value.\
It gets a collection of items, from your:
Accessory bag\
Inventory\
Ender chest\
Currently equiped armor\
Wardrobe\
Personal vault\
Storage\
Pets

With these (excluding pets), it will do the following:\
If it's purchasable on the auction house, get the lowest BIN with the same internal ID. (If it's not use Jerry The Price Checker's price list)\

If it has hot potato books, add 10,000 for each hot potato book, and 100,000 for each fuming potato book.\
If it's been recombobulated, add 5,000,000 to the value.\
If it's a dungeon item, give the rough value in essence for each item (and each star).\
If it's a warped aspect of the end, add 10 million if it's epic, add 5 million if it's not.\
For each level 6 enchantment, add 500k, for each level 7 and above enchantment, add 1 million.\
And if there's more than one item, e.g. a stack of enchanted diamond blocks, it multiplies the value by the amount of items.
