import re


class Item:
    def __init__(self, nbt, slot_number):
        self.__nbt__ = nbt
	
        tag = nbt['tag']
        extras = tag.get('ExtraAttributes', {})
        display = tag.get('display', {})
        self.internal_name = extras.get('id', None)

        self.description = display.get('Lore', [])
        self.description_clean = [re.sub('§.', '', line) for line in self.description]

        self.recombobulated = 1 if extras.get('rarity_upgrades', False) else 0
        self.hot_potatos = extras.get('hot_potato_count', 0)
        self.stack_size = self.__nbt__.get('Count', 1)

        self.enchantments = extras.get('enchantments', {})
        self.reforge = extras.get('modifier', None)
        self.star_upgrades = display.get('Name', "").count("✪")

        if self.description_clean:
            rarity_type = self.description_clean[-1].split()
            self.rarity = rarity_type[0].lower()
            self.type = rarity_type[1].lower() if len(rarity_type) > 1 else None

        item_name = re.sub('§.', '', display.get("Name", None))
       
        for reforge in ['strong', 'shaded', 'withered', 'fabled', 'unreal', 'unpleasant', 'precise', 'blessed', 'forceful', 'ancient', 'renowned', 'submerged', 'light', 'necrotic', 'wise', 'loving', 'pure', 'fierce', 'candied', 'treacherous', 'dirty']:
            if item_name.startswith(reforge.capitalize()+" "):
                item_name = item_name[len(reforge+" "):]
        self.name = item_name

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return self.internal_name
