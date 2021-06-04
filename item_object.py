import re


class Item:
    def __init__(self, nbt, slot_number):
        self.__nbt__ = nbt

        #print(nbt)
	
        tag = nbt['tag']
        extras = tag.get('ExtraAttributes', {})
        display = tag.get('display', {})
        self.internal_name = extras.get('id', None)
        self.name = re.sub('§.', '', display.get("Name", None))
        self.stack_size = self.__nbt__.get('Count', 1)

        self.recombobulated = 1 if extras.get('rarity_upgrades', False) else 0
        self.hot_potatos = extras.get('hot_potato_count', 0)
        
        self.enchantments = extras.get('enchantments', {})
        self.reforge = extras.get('modifier', None)
        self.star_upgrades = display.get('Name', "").count("✪")
        self.talisman_enrichment = extras.get("talisman_enrichment", None)

        # Description parsing for rarity and type
        self.description = display.get('Lore', [])
        self.description[-1] = re.sub('§l§ka', '', self.description[-1])
        # We do this because Hypixel put the changing text before and after special items, which messes with the rarity/type parsing
        self.description_clean = [re.sub('§.', '', line) for line in self.description]

        # Extract rarity and type
        last_desc_row = self.description_clean[-1].split()
        self.rarity = last_desc_row[0].upper()
        self.type = last_desc_row[1].lower() if len(last_desc_row) > 1 else None

        # self.item_group = Stuff such as "ARMOR", "SWORD", "ROD", "ACCESSORY
        self.item_group = None
        if self.reforge:
            if "DUNGEON" in last_desc_row:
                last_desc_row.remove("DUNGEON")
            self.item_group = last_desc_row[-1]
        
        # Parse item name with removed reforges (We can already get the reforges)
        for reforge in ['strong', 'shaded', 'withered', 'fabled', 'unreal', 'unpleasant', 'precise', 'blessed', 'forceful', 'ancient', 'renowned', 'submerged', 'light', 'necrotic', 'wise', 'loving', 'pure', 'fierce', 'candied', 'treacherous', 'dirty']:
            if self.name.startswith(reforge.capitalize()+" "):
                self.name = self.name[len(reforge+" "):]

        # A little edge case handling, because Hypixel are great...
        if self.reforge is not None:
            if self.reforge.lower() == "aote_stone":
                self.reforge = "warped"
            if self.reforge.lower() == "jerry_stone":
                self.reforge = "jerry's"

        if self.reforge == "odd_sword":
            print(nbt)

    def __str__(self):
        return self.internal_name

    def __repr__(self):
        return f"{self.name} ({self.internal_name}), Amount: {self.stack_size}, Recommed: {self.recombobulated}, HPB: {self.hot_potatos}, Reforge: {self.reforge}, Stars: {self.star_upgrades} talisman enrichment: {self.talisman_enrichment}"
