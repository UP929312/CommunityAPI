# CommunityBot

This is a bot made partially by the community, with the lead dev being Skezza#1139.\
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
- If it has hot potato books, add the price of a HPB for each book, and the price of a FPB for each fuming potato book.
- If it's been recombobulated, add the price of a recombobulator 3000 to the value.
- If it's a dungeon item, give the rough value in essence for each item (and each star).
- It it has a reforge stone applied to it, calculate the cost of the reforge stone, as well as the cost to apply it.
- If it has a talisman enrichment, add the price of that enrichment.
- For each enchantment, add the cost of the enchanted book from BIN to the item.
- And if there's more than one item, e.g. a stack of enchanted diamond blocks, it multiplies the value by the amount of items.
