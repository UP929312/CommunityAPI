The networth calculations aren't complicated, but are made up from many different data points.
The API will take the compressed GZIP data and decode it into it's different containers.
It will then process each item in the container, which is then also split into 3 different sections, base items, pets, and enchanted books.
It may look for, for example, if the item has a recombobulator 3000, and if it does, increase the value of that item.

**Here's what the code currently does to get the value.\**
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
1. If the item is purchasable from an NPC then:
    If the price of the item from the NPC is less than the BIN, set that as it's base price,
    If the price of the item from the NPC is more than the BIN, set the price to the BIN value.
2. If it's purchasable from the Bazaar, use that price, it's the most accurate.
3. If it's purchasable on the auction house, use the lowest "Buy It Now", this is reasonably accurate.
4. If it's not on either of the above, check Jerry's Price list, it's not always entirely accurate, but has much more items.

Then we calculate some different price points for base items:
- If it's a Theoretical hoe, 1,000,000 for a Mathematical Blueprint, plus the cost of materials to get it to it's tier (e.g. Tier 3)
- If it has hot potato books, add the price of a HPB for each book, and the price of a FPB for each fuming potato book.
- If it's been recombobulated, add the price of a recombobulator 3000 from Bazzar to the value.
- If it's a dungeon item, give the value in essence for each item (and each star), including the price of the Master Stars.
- It it has a reforge stone applied to it, calculate the cost of the reforge stone, as well as the cost to apply it.
- If it has a talisman enrichment, add the price of that enrichment from BIN.
- If it's a Wooden Sword with a "Wood Singularity" added to it, add the price of that item from the BIN.
- If the item is armor and has a skin on it, add the price of that skin from BIN.
- If it has an "Art Of War" book added to it, add the price of that book from the BIN to the value.
- If it has any "Farming for Dummies" books, add them to the value.
- For each enchantment, if it's from the enchantment table, use a base value, if not, if it's not on BIN, try doing 2 of the level below, or 4 of two levels below, etc. This excludes: Compact, Expertise and Cultivating.
- If the item is a drill, add the cost of each upgrade from the BIN to the value.
- If it has scrolls (e.g. on a Hyperion), add the price of all of them to the value.
- If it's got Transmission Tuners, add the value from BIN of each one to the value.
- If it's an Aspect of the Void, and is Ethermerged, add the value of the Etherwarp merger and Conduit to the value.
- If it's a Midas Staff or Sword, add the amount of the winning bid to it.
- If it has gems on it, add the cost of all the gems from bazaar.
- If it has Gemstone chambers, add the cost of each gemstone chamber from BIN.
- If it has gemstone power scrolls, add the cost of the power scrolls from BIN.

For pets:
- Calculate the price of the pet from BIN (for that tier).
- Add the cost of the pet's held item from BIN.
- Add the cost of the pet's skin from BIN.
- We add the amount of pet xp by 0.2, to get it's level's value *(this is partially subjective).
- For Golden Dragons, we calculate the same as above, but each level above 100 is 3x the xp, rather than 0.2 (this is surprisingly accurate)
