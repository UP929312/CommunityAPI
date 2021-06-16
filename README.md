# CommunityBot &middot; ![version](https://img.shields.io/badge/Version-0.8.0-brightgreen.svg?style=flat-square) ![license](https://img.shields.io/badge/License-MIT-brightgreen.svg?style=flat-square) [![Discord](https://img.shields.io/discord/571681282652766208.svg?style=flat-square&logo=discord&label=HypixelSkyblock&colorA=7289DA&colorB=2C2F33)](https://discord.gg/HypixelSkyblock)

This is a bot made partially by the community, with the lead dev being Skezza#1139.\
Special mention to Mega_Pi for the research and knowledge on a lot of the content!\
This bot will remain open source, and provide fun information about your profile, such as it's value.\
Anyone can make a pull request, and it'll be reviewed and possibly added.\
If you make good suggestions, you'll be invited into a special community-bot-dev channel, where we can further discuss ideas.

Here's what the code currently does to get the value.\
It gets a collection of items, from your:
- Accessory bag
- Inventory
- Ender chest
- Currently equipped armor
- Wardrobe
- Personal vault
- Storage
- Pets

With these (excluding pets), it will do the following:
1. If it's purchasable from the Bazaar, use that price, it's the most accurate.
2. If it's purchasable on the auction house, buy the lowest Buy It Now item, this is quite accurate.
3. If it's not on either of these, check Jerry's list, it's not always entirely accurate, but has much more items.

Then we calculate some extras for base items:
- If it's a theoretical hoe, 1,000,000 for a mathematical blueprint, plus the cost of materials to get it to it's tier (e.g. tier 3)
- If it has hot potato books, add the price of a HPB for each book, and the price of a FPB for each fuming potato book.
- If it's been recombobulated, add the price of a recombobulator 3000 to the value.
- If it's a dungeon item, give the rough value in essence for each item (and each star), including the price of the Master Stars.
- It it has a reforge stone applied to it, calculate the cost of the reforge stone, as well as the cost to apply it.
- If it has a talisman enrichment, add the price of that enrichment from BIN.
- If it's a Wooden Sword with a "Wood Singularity" added to it, add the price of that item from the BIN.
- If it has an "Art Of War" book added to it, add the price of that book from the BIN to the value.
- For each enchantment, if it's not on BIN, try doing 2 of the level below, or 4 of two levels below, etc.
- If the item is a drill, add the cost of each upgrade from the BIN to the value.
- If it has scrolls (e.g. on a Hyperion), add the price of all of them to the value.
- ~~If it's got livid fragments applied to it, add those 8 to the value.~~ Currently disabled.
- And if there's more than one item, e.g. a stack of enchanted diamond blocks, it multiplies the value by the amount of items.

For pets:
- Calculate the price of the pet from BIN (average for that tier)
- Add the cost of the pet's held item from BIN
- Add the cost of the pet's skin from BIN
- We add the amount of pet xp by 0.2, to get it's level's value (this is partially subjective)
