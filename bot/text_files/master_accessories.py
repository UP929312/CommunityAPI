def get_master_accessories():
    import os, json
    from accessory_list import talisman_upgrades

    from pathlib import Path
    parent_dir = str(os.path.abspath('..'))

    tier_colors = {
        "§f": "common",
        "§a": "uncommon",
        "§9": "rare",
        "§5": "epic",
        "§6": "legendary",
        "§d": "mythic",
        "§4": "supreme",
        "§c": "special",
        "§c": "very special",
    }

    MASTER_ACCESSORIES = []
    UPGRADEABLE_ACCESSORIES = talisman_upgrades.keys()

    for item in os.listdir(parent_dir+'/items'):
        with open(parent_dir+"/items/"+item, encoding="utf-8") as file:
            json_data = json.load(file)
        if item.rstrip(".json") in UPGRADEABLE_ACCESSORIES:
            continue
        lore_line = [x for x in json_data["lore"] if "ACCESSORY" in x]
        if lore_line:
            desc_line = lore_line[0]
            rarity = tier_colors[desc_line[:2]].upper()
            
            name = json_data["displayname"]
            for symbol in ["Â", "§5", "§6", "§9", "§f", "§a", "§d", "♪ "]:
                name = name.replace(symbol, "")
                
            wiki_link = json_data.get("info", ["No Wiki Link Exists for this item yet!",])[0]
            MASTER_ACCESSORIES.append((item.rstrip(".json"), name, rarity, wiki_link))
            
    return MASTER_ACCESSORIES

#print(get_master_accessories())

MASTER_ACCESSORIES = [('ARTIFACT_POTION_AFFINITY', 'Potion Affinity Artifact', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Potion_Affinity_Artifact'), ('AUTO_RECOMBOBULATOR', 'Auto Recombobulator', 'LEGENDARY', 'https://hypixel-skyblock.fandom.com/wiki/Auto_Recombobulator'), ('BAT_ARTIFACT', 'Bat Artifact', 'LEGENDARY', 'https://hypixel-skyblock.fandom.com/wiki/Bat_Artifact'), ('BAT_PERSON_ARTIFACT', 'Bat Person Artifact', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Bat_Person_Artifact'), ('BEASTMASTER_CREST_LEGENDARY', 'Beastmaster Crest', 'LEGENDARY', 'https://hypixel-skyblock.fandom.com/wiki/Beastmaster_Crest'), ('BITS_TALISMAN', 'Bits Talisman', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Bits_Talisman'), ('BLOOD_GOD_CREST', 'Blood God Crest', 'COMMON', 'https://hypixel-skyblock.fandom.com/wiki/Blood_God_Crest'), ('CAMPFIRE_TALISMAN_29', 'Campfire God Badge', 'LEGENDARY', 'https://hypixel-skyblock.fandom.com/wiki/Campfire_Badge'), ('CANDY_RELIC', 'Candy Relic', 'LEGENDARY', 'https://hypixel-skyblock.fandom.com/wiki/Candy_Relic'), ('CATACOMBS_EXPERT_RING', 'Catacombs Expert Ring', 'EPIC', 'https://hypixel-skyblock.fandom.com/wiki/Catacombs_Expert_Ring'), ('CHEETAH_TALISMAN', 'Cheetah Talisman', 'EPIC', 'https://hypixel-skyblock.fandom.com/wiki/Cheetah_Talisman'), ('COIN_TALISMAN', 'Talisman of Coins', 'COMMON', 'https://hypixel-skyblock.fandom.com/wiki/Talisman_of_Coins'), ('DANTE_TALISMAN', 'Dante Talisman', 'COMMON', 'https://hypixel-skyblock.fandom.com/wiki/Dante_Talisman'), ('DAY_CRYSTAL', 'Day Crystal', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Day_Crystal'), ('DEVOUR_RING', 'Devour Ring', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Devour_Ring'), ('EMERALD_RING', 'Emerald Ring', 'UNCOMMON', 'https://hypixel-skyblock.fandom.com/wiki/Emerald_Ring'), ('ENDER_RELIC', 'Ender Relic', 'LEGENDARY', 'https://hypixel-skyblock.fandom.com/wiki/Ender_Relic'), ('ETERNAL_HOOF', 'Eternal Hoof', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Eternal_Hoof'), ('EXPERIENCE_ARTIFACT', 'Experience Artifact', 'EPIC', 'https://hypixel-skyblock.fandom.com/wiki/Experience_Artifact'), ('FARMER_ORB', 'Farmer Orb', 'UNCOMMON', 'https://hypixel-skyblock.fandom.com/wiki/Farmer_Orb'), ('FARMING_TALISMAN', 'Farming Talisman', 'COMMON', 'https://hypixel-skyblock.fandom.com/wiki/Farming_Talisman'), ('FEATHER_ARTIFACT', 'Feather Artifact', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Feather_Artifact'), ('FIRE_TALISMAN', 'Fire Talisman', 'COMMON', 'https://hypixel-skyblock.fandom.com/wiki/Fire_Talisman'), ('FISH_AFFINITY_TALISMAN', 'Fish Affinity Talisman', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Fish_Affinity_Talisman'), ('FROZEN_CHICKEN', 'Frozen Chicken', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Frozen_Chicken'), ('GRAVITY_TALISMAN', 'Gravity Talisman', 'UNCOMMON', 'https://hypixel-skyblock.fandom.com/wiki/Gravity_Talisman'), ('HANDY_BLOOD_CHALICE', 'Handy Blood Chalice', 'COMMON', 'https://hypixel-skyblock.fandom.com/wiki/Handy_Blood_Chalice'), ('HASTE_RING', 'Haste Ring', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Haste_Ring'), ('HEALING_RING', 'Healing Ring', 'UNCOMMON', 'https://hypixel-skyblock.fandom.com/wiki/Healing_Ring'), ('HEGEMONY_ARTIFACT', 'Hegemony Artifact', 'LEGENDARY', 'https://hypixel-skyblock.fandom.com/wiki/Hegemony_Artifact'), ('HUNTER_RING', 'Hunter Ring', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Hunter_Ring'), ('INTIMIDATION_ARTIFACT', 'Intimidation Artifact', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Intimidation_Artifact'), ('JERRY_TALISMAN_GOLDEN', 'Golden Jerry Artifact', 'LEGENDARY', 'https://hypixel-skyblock.fandom.com/wiki/Golden_Jerry_Artifact'), ('JUNGLE_AMULET', 'Jungle Amulet', 'UNCOMMON', 'No Wiki Link Exists for this item yet!'), ('KING_TALISMAN', 'King Talisman', 'COMMON', 'https://hypixel-skyblock.fandom.com/wiki/King_Talisman'), ('LAVA_TALISMAN', 'Lava Talisman', 'UNCOMMON', 'https://hypixel-skyblock.fandom.com/wiki/Lava_Talisman'), ('MAGNETIC_TALISMAN', 'Magnetic Talisman', 'UNCOMMON', 'https://hypixel-skyblock.fandom.com/wiki/Magnetic_Talisman'), ('MASTER_SKULL_TIER_7', 'Master Skull - Tier 7', 'LEGENDARY', 'https://hypixel-skyblock.fandom.com/wiki/Master_Skull'), ('MELODY_HAIR', "Melody's Hair ♫", 'EPIC', "https://hypixel-skyblock.fandom.com/wiki/Melody's_Hair"), ('MINERAL_TALISMAN', 'Mineral Talisman', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Mineral_Talisman'), ('MINE_TALISMAN', 'Mine Affinity Talisman', 'COMMON', 'https://hypixel-skyblock.fandom.com/wiki/Mine_Affinity_Talisman'), ('NEW_YEAR_CAKE_BAG', 'New Year Cake Bag', 'UNCOMMON', 'https://hypixel-skyblock.fandom.com/wiki/New_Year_Cake_Bag'), ('NIGHT_CRYSTAL', 'Night Crystal', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Night_Crystal'), ('NIGHT_VISION_CHARM', 'Night Vision Charm', 'COMMON', 'https://hypixel-skyblock.fandom.com/wiki/Night_Vision_Charm'), ('PERSONAL_COMPACTOR_7000', 'Personal Compactor 7000', 'LEGENDARY', 'https://hypixel-skyblock.fandom.com/wiki/Personal_Compactor_7000'), ('PERSONAL_DELETOR_7000', 'Personal Deletor 7000', 'LEGENDARY', 'https://hypixel-skyblock.fandom.com/wiki/Personal_Deletor_7000'), ('PIGGY_BANK', 'Piggy Bank', 'UNCOMMON', 'https://hypixel-skyblock.fandom.com/wiki/Piggy_Bank'), ('PIGS_FOOT', "Pig's Foot", 'RARE', "https://hypixel-skyblock.fandom.com/wiki/Pig's_Foot"), ('POCKET_ESPRESSO_MACHINE', 'Pocket Espresso Machine', 'COMMON', 'https://hypixel-skyblock.fandom.com/wiki/Pocket_Espresso_Machine'), ('POTATO_TALISMAN', 'Potato Talisman', 'COMMON', 'https://hypixel-skyblock.fandom.com/wiki/Potato_Talisman'), ('POWER_ARTIFACT', 'Artifact of Power', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Artifact_of_Power'), ('POWER_RING', 'Ring of Power', 'UNCOMMON', 'https://hypixel-skyblock.fandom.com/wiki/Ring_of_Power'), ('POWER_TALISMAN', 'Talisman of Power', 'COMMON', 'https://hypixel-skyblock.fandom.com/wiki/Talisman_of_Power'), ('RAZOR_SHARP_SHARK_TOOTH_NECKLACE', 'Razor-sharp Shark Tooth Necklace', 'LEGENDARY', 'https://hypixel-skyblock.fandom.com/wiki/Razor-sharp_Shark_Tooth_Necklace'), ('REAPER_ORB', 'Reaper Orb', 'LEGENDARY', 'https://hypixel-skyblock.fandom.com/wiki/Reaper_Orb'), ('RED_CLAW_ARTIFACT', 'Red Claw Artifact', 'EPIC', 'https://hypixel-skyblock.fandom.com/wiki/Red_Claw_Artifact'), ('SCARF_GRIMOIRE', "Scarf's Grimoire", 'LEGENDARY', "https://hypixel-skyblock.fandom.com/wiki/Scarf's_Grimoire"), ('SCAVENGER_TALISMAN', 'Scavenger Talisman', 'COMMON', 'https://hypixel-skyblock.fandom.com/wiki/Scavenger_Talisman'), ('SEAL_OF_THE_FAMILY', 'Seal of the Family', 'EPIC', 'https://hypixel-skyblock.fandom.com/wiki/Seal_of_the_Family'), ('SEA_CREATURE_ARTIFACT', 'Sea Creature Artifact', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Sea_Creature_Artifact'), ('SKELETON_TALISMAN', 'Skeleton Talisman', 'COMMON', 'https://hypixel-skyblock.fandom.com/wiki/Skeleton_Talisman'), ('SOULFLOW_SUPERCELL', 'Soulflow Supercell', 'EPIC', 'https://hypixel-skyblock.fandom.com/wiki/Soulflow_Supercell'), ('SPEED_ARTIFACT', 'Speed Artifact', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Speed_Artifact'), ('SPIDER_ARTIFACT', 'Spider Artifact', 'EPIC', 'https://hypixel-skyblock.fandom.com/wiki/Spider_Artifact'), ('SPIKED_ATROCITY', 'Spiked Atrocity', 'EPIC', 'https://hypixel-skyblock.fandom.com/wiki/Spiked_Atrocity'), ('SURVIVOR_CUBE', 'Survivor Cube', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Survivor_Cube'), ('TARANTULA_TALISMAN', 'Tarantula Talisman', 'EPIC', 'https://hypixel-skyblock.fandom.com/wiki/Tarantula_Talisman'), ('TITANIUM_RELIC', 'Titanium Relic', 'LEGENDARY', 'https://hypixel-skyblock.fandom.com/wiki/Titanium_Relic'), ('TREASURE_ARTIFACT', 'Treasure Artifact', 'LEGENDARY', 'https://hypixel-skyblock.fandom.com/wiki/Treasure_Artifact'), ('VACCINE_TALISMAN', 'Vaccine Talisman', 'COMMON', 'https://hypixel-skyblock.fandom.com/wiki/Vaccine_Talisman'), ('VILLAGE_TALISMAN', 'Village Affinity Talisman', 'COMMON', 'https://hypixel-skyblock.fandom.com/wiki/Village_Affinity_Talisman'), ('WEDDING_RING_9', 'Legendary Ring of Love', 'LEGENDARY', 'https://hypixel-skyblock.fandom.com/wiki/Ring_of_Love'), ('WITHER_RELIC', 'Wither Relic', 'LEGENDARY', 'https://hypixel-skyblock.fandom.com/wiki/Wither_Relic'), ('WOLF_PAW', 'Wolf Paw', 'UNCOMMON', 'https://hypixel-skyblock.fandom.com/wiki/Wolf_Paw'), ('WOLF_RING', 'Wolf Ring', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Wolf_Ring'), ('WOOD_TALISMAN', 'Wood Affinity Talisman', 'UNCOMMON', 'https://hypixel-skyblock.fandom.com/wiki/Wood_Affinity_Talisman'), ('ZOMBIE_ARTIFACT', 'Zombie Artifact', 'RARE', 'https://hypixel-skyblock.fandom.com/wiki/Zombie_Artifact')]


