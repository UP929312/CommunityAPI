import re


class Item:
    def __init__(self, nbt, slot_number):
        self.__nbt__ = nbt

        #print(nbt)

        # Generic data
        tag = nbt['tag']  # No idea why this fails for a very small number of people... If I use get, the whole thing breaks
        extras = tag.get('ExtraAttributes', {})
        display = tag.get('display', {})
        self.internal_name = extras.get('id', None)  # Not sure why some items have no internal_name...
        self.name = re.sub('§.', '', display.get("Name", None))
        self.stack_size = self.__nbt__.get('Count', 1)
            
        self.recombobulated = 1 if extras.get('rarity_upgrades', False) else 0
        self.hot_potatos = extras.get('hot_potato_count', 0)

        # Unique to tools
        self.enchantments = extras.get('enchantments', {})
        self.reforge = extras.get('modifier', None)
        self.star_upgrades = extras.get("dungeon_item_level", 0)  # Gets number of stars for dungeon items.

        # Little extras
        self.talisman_enrichment = extras.get("talisman_enrichment", None)
        self.art_of_war = extras.get("art_of_war_count", None)
        self.wood_singularity = extras.get("wood_singularity_count", None)

        # Hoes
        self.farming_for_dummies = extras.get("farming_for_dummies_count", 0)
        self.mined_crops = extras.get("mined_crops", 0)
        self.farmed_cultivating = extras.get("farmed_cultivating", 0)

        # Description parsing for rarity and type
        self.description = display.get('Lore', [])
        self.description[-1] = re.sub('§l§ka', '', self.description[-1])
        # We do this because Hypixel put the changing text before and after special items, which messes with the rarity/type parsing
        self.description_clean = [re.sub('§.', '', line) for line in self.description]

        # Extract rarity and type
        last_desc_row = self.description_clean[-1].split()
        self.rarity = last_desc_row[0] if last_desc_row[0] != "VERY" else "VERY_SPECIAL"
        self.type = last_desc_row[1] if len(last_desc_row) > 1 else None

        # self.item_group = Stuff such as "ARMOR", "SWORD", "ROD", "ACCESSORY
        self.item_group = None
        if self.reforge:
            if "DUNGEON" in last_desc_row:
                last_desc_row.remove("DUNGEON")
            self.item_group = last_desc_row[-1]
        
        # Parse item name with removed reforges (We can already get the reforges)
        if self.reforge is not None:
            for reforge in ['Strong ', 'Shaded ', 'Withered ', 'Fabled ', 'Unreal ', 'Unpleasant ', 'Precise ', 'Blessed ', 'Forceful ', 'Ancient ', 'Renowned ', 'Submerged ', 'Light ', 'Necrotic ', 'Wise ', 'Loving ', 'Pure ', 'Fierce ', 'Candied ', 'Treacherous ', 'Dirty ', 'Smart ', 'Heroic ', 'Fast ', 'Titanic ', 'Sharp ', 'Rapid ', 'Awkward ', 'Fine ', 'Heavy ', 'Fair ', 'Odd ', 'Gentle ', 'Neat ', 'Hasty ', 'Spicy ', 'Rich ', 'Clean ']:
                self.name = self.name.removeprefix(reforge)       

        # A little edge case handling, because Hypixel are great...
        if self.reforge is not None:
            if self.reforge == "aote_stone":
                self.reforge = "warped"
            if self.reforge == "jerry_stone":
                self.reforge = "jerry's"

        # Drills
        if self.type == "DRILL":
            self.drill_module_upgrade = extras.get("drill_part_upgrade_module", "").upper()  # Not sure why this is lowercase
            self.drill_engine_upgrade = extras.get("drill_part_engine", "").upper()
            self.drill_tank_upgrade = extras.get("drill_part_fuel_tank", "").upper()

        # Hoes
        self.hoe_level, self.hoe_material = (None, None)
        if self.type == "HOE" and "THEORETICAL" in self.internal_name:
            self.material = "_".join(self.name.split(" ")[1:-1]).upper()  # Turing Sugar Cane Hoe
            self.hoe_level = self.internal_name[-1]  # THEORETICAL_HOE_WHEAT_1 -> 1

        # For Hyperions
        self.ability_scrolls = extras.get("ability_scroll", None)

        # Livid Fragments
        self.livid_fragments = 8 if self.internal_name is not None and self.internal_name.startswith("STARRED") else 0 # STARRED = 8 LIVID_FRAGMENTS
        
    def __str__(self):
        return self.internal_name

    def __repr__(self):
        list_of_elems = [f"{self.name} ({self.internal_name})"]
        list_of_elems.append(f"Rarity: {self.rarity if self.rarity is not None else 'Misc'}")
        if self.type is not None:
            list_of_elems.append(f"Type: {self.type}")
        if self.item_group is not None:
            list_of_elems.append(f"Group: {self.item_group}")
        if self.type == "DRILL":
            if self.drill_module_upgrade:
                list_of_elems.append(f"Drill module: {self.drill_module_upgrade}")
            if self.drill_engine_upgrade:
                list_of_elems.append(f"Drill engine: {self.drill_engine_upgrade}")
            if self.drill_tank_upgrade:
                list_of_elems.append(f"Drill tank: {self.drill_tank_upgrade}")
        if self.type == "HOE":
            list_of_elems.append(f"Level: {self.hoe_level}, Type: {self.hoe_material}")
        if self.stack_size > 1:
            list_of_elems.append(f"Amount: {self.stack_size}")
        if self.recombobulated:
            list_of_elems.append(f"+Recombobulated")
        if self.hot_potatos:
            list_of_elems.append(f"{self.hot_potatos} Hot Potatos")
        if self.reforge is not None:
            list_of_elems.append(f"Reforge: {self.reforge}")
        if self.star_upgrades:
            list_of_elems.append(f"Stars: {self.star_upgrades}")
        if self.talisman_enrichment:
            list_of_elems.append(f"Enrichment: {self.talisman_enrichment}")
        if self.art_of_war:
            list_of_elems.append("+Art of War")
        if self.wood_singularity:
            list_of_elems.append("+Wood Singularity")
        if self.farming_for_dummies > 0:
            list_of_elems.append(f"{self.farming_for_dummies} Farming for Dummies")
        if self.mined_crops:
            list_of_elems.append(f"{self.mined_crops} mined crops")
        if self.farmed_cultivating:
            list_of_elems.append(f"{self.farmed_cultivating} farmed cultivating")
        if self.livid_fragments:
            list_of_elems.append(f"{self.livid_fragments} livid fragments")
        
        return ", ".join(list_of_elems)
