import re
import json

DEFAULT_ITEM = {"internal_name": "DEFAULT_ITEM", "name":"Default Item",    "stack_size": 1,
                "type": "Default",               "item_group": "Misc",     "rarity": "Common",
                "recombobulated": 0,             "hot_potatoes": 0,        "talisman_enrichment": None,
                "art_of_war": None,              "wood_singularity": None, "skin": None,
                "power_ability_scroll": None,    "gems": {},               "gemstone_chambers": None,
                "enchantments": {},              "reforge": None,          "star_upgrades": 0,
                "farming_for_dummies": 0,        "tuned_transmission": 0,  "ethermerge": False,
                "winning_bid": 0,                "ability_scrolls": [],    "origin_tag": "UNKNOWN",}
                
HOE_MATERIAL_TO_INTERNAL_NAMES = {
    "POTATO": ("POTATO_ITEM", "ENCHANTED_POTATO", "ENCHANTED_BAKED_POTATO"),
    "NETHER_WARTS": ("NETHER_STALK", "ENCHANTED_NETHER_STALK", "MUTANT_NETHER_STALK"),
    "SUGAR_CANE": ("SUGAR_CANE", "ENCHANTED_SUGAR", "ENCHANTED_SUGAR_CANE"),
    "CARROT": ("CARROT_ITEM", "ENCHANTED_CARROT", "ENCHANTED_GOLDEN_CARROT"),
    "WHEAT": ("WHEAT", "ENCHANTED_HAY_BLOCK", "TIGHTLY_TIED_HAY_BALE"),
}


class Item:
    def __init__(self, nbt):
        #print(nbt)

        # Default minecraft items don't have anything special, so just leave them basically
        # It's sometimes: {'id': 5, 'Count': 64, 'Damage': 0}
        #{'id': 160, 'Count': 1, 'tag': {'display': {'Name': ' '}}, 'Damage': 15}
        if "tag" not in nbt or "Lore" not in nbt["tag"].get("display", {}):
            for tag_name, value in DEFAULT_ITEM.items():
                setattr(self, tag_name, value)
            return

        # Generic data            
        tag = nbt['tag']
        extras = tag.get('ExtraAttributes', {})
        display = tag.get('display', {})
        self.internal_name = extras.get('id', None)  # Not sure why some items have no internal_name...
        self.name = re.sub('§.', '', display.get("Name", None))
        self.stack_size = max(0, nbt.get('Count', 1))  # Removes negative stack size
        self.origin_tag = extras.get("originTag", "UNKNOWN")

        # Recomb + HPB
        self.recombobulated = bool(extras.get('rarity_upgrades', False))
        self.hot_potatoes = extras.get('hot_potato_count', 0)

        # Little extras
        self.talisman_enrichment = extras.get("talisman_enrichment", None)
        self.art_of_war = extras.get("art_of_war_count", None)
        self.wood_singularity = extras.get("wood_singularity_count", None)
        self.skin = extras.get("skin", None)
        self.power_ability_scroll = extras.get("power_ability_scroll", None)
        self.gems = extras.get("gems", {})
        self.gemstone_chambers = extras.get("gemstone_slots", None)

        # Unique to tools
        self.enchantments = extras.get('enchantments', {})
        self.reforge = extras.get('modifier', None)
        self.star_upgrades = extras.get("dungeon_item_level", 0)  # Gets number of stars for dungeon items.

        # Parse item name with removed reforges (We can already get the reforges)
        if self.reforge:            
            self.name = self.name.removeprefix(self.reforge.title()+" ")

        # Description parsing for rarity and type
        self.description = display.get('Lore', [])
        self.description[-1] = re.sub('§l§ka', '', self.description[-1])
        # We do this ^ because Hypixel put the changing text before and after special items, which messes with the rarity/type parsing
        self.description_clean = [re.sub('§.', '', line) for line in self.description]

        # Extract rarity and type
        last_desc_row = self.description_clean[-1].split()
        self.rarity = last_desc_row[0] if last_desc_row[0] != "VERY" else "VERY_SPECIAL"
        self.type = last_desc_row[1] if len(last_desc_row) > 1 else None
        
        # self.item_group = Stuff such as:
        #["ACCESSORY", "HELMET", "CHESTPLATE", "LEGGINGS", "BOOTS", "SWORD", "BOW", "AXE", "HOE", "DRILL", "ROD", "PICKAXE", "WEAPON", "GAUNTLET"]
        self.item_group = None
        if self.reforge:
            if "DUNGEON" in last_desc_row:  # Not 100% sure if this is needed, but I'll keep it here
                last_desc_row.remove("DUNGEON")
            self.item_group = last_desc_row[-1]
            if self.item_group == "HATCCESSORY":
                self.item_group = "ACCESSORY"                
        
        if self.internal_name == "PET":
            self.pet_info = json.loads(extras["petInfo"])

        # A little edge case handling, because Hypixel are great...
        if self.reforge is not None:
            if self.reforge == "aote_stone":
                self.reforge = "warped"
            if self.reforge == "jerry_stone":
                self.reforge = "jerry's"

        # Drills
        if self.type == "DRILL": #
            # Not sure why this is lowercase
            self.drill_module_upgrade = extras.get("drill_part_upgrade_module", "").upper() or extras.get("drill_module_upgrade", "").upper()
            self.drill_engine_upgrade = extras.get("drill_part_engine", "").upper()
            self.drill_tank_upgrade =   extras.get("drill_part_fuel_tank", "").upper()
            
            self.has_drill_upgrade = self.drill_module_upgrade or self.drill_engine_upgrade or self.drill_tank_upgrade

        # Hoes
        self.hoe_level, self.hoe_material_list = (None, None)
        if self.type == "HOE" and "THEORETICAL" in self.internal_name:
            hoe_material = "_".join(self.name.split(" ")[1:-1]).upper()  # Turing Sugar Cane Hoe
            if hoe_material != "HOE":  # Remove Mathematical Hoe
                self.hoe_material_list = HOE_MATERIAL_TO_INTERNAL_NAMES[hoe_material]
                self.hoe_level = int(self.internal_name[-1])  # THEORETICAL_HOE_WHEAT_1 -> 1

        # Hoes
        self.farming_for_dummies = extras.get("farming_for_dummies_count", 0)

        # Ender slayer items
        self.tuned_transmission = extras.get('tuned_transmission', 0)

        # Ethermerge
        self.ethermerge = extras.get("ethermerge", False)

        # Winning bid on Midas Staff/Sword
        self.winning_bid = extras.get("winning_bid", 0)

        # For Hyperions
        self.ability_scrolls = extras.get("ability_scroll", None)

    #=========================================================================
        
    def to_dict(self):
        data = {
                "name": self.name,
                "internal_name": self.internal_name,
                "rarity": self.rarity or 'Misc',
                "stack_size": self.stack_size,
                "origin_tag": self.origin_tag,
               }

        if self.type is not None:
            data["type"] = self.type
        if self.item_group is not None:
            data["item_group"] = self.item_group
        if self.type == "DRILL":
            if self.drill_module_upgrade:
                data["drill_module_upgrade"] = self.drill_module_upgrade
            if self.drill_engine_upgrade:
                data["drill_engine_upgrade"] = self.drill_engine_upgrade
            if self.drill_tank_upgrade:
                data["drill_tank_upgrade"] = self.drill_tank_upgrade
                
        if self.type == "HOE":
            data["hoe_level"] = self.hoe_level
            data["hoe_material_list"] = self.hoe_material_list

        if self.recombobulated:
            data["recombobulated"] = True
        if self.hot_potatoes:
            data["hot_potatoes"] = self.hot_potatoes
        if self.reforge is not None:
            data["reforge"] = self.reforge
        if self.star_upgrades:
            data["star_upgrades"] = self.star_upgrades
        if self.talisman_enrichment:
            data["talisman_enrichment"] = self.talisman_enrichment
        if self.art_of_war:
            data["art_of_war"] = True
        if self.wood_singularity:
            data["wood_singularity"] = True
        if self.skin:
            data["skin"] = self.skin
        if self.power_ability_scroll:
            data["power_ability_scroll"] = self.power_ability_scroll
        if self.gems:
            data["gems"] = self.gems
        if self.gemstone_chambers:
            data["gemstone_chambers"] = self.gemstone_chambers
        if self.farming_for_dummies > 0:
            data["farming_for_dummies"] = self.farming_for_dummies
        if self.tuned_transmission:
            data["tuned_transmission"] = self.tuned_transmission
        if self.ethermerge:
            data["ethermerge"] = self.ethermerge
        if self.winning_bid > 0:
            data["winning_bid"] = self.winning_bid
        if self.ability_scrolls:
            data["ability_scrolls"] = self.ability_scrolls

        return data
