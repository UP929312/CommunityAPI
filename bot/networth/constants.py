page_names = ["main", "inventory", "accessories", "ender_chest", "armor", "equipment", "wardrobe", "storage", "pets", "misc"]

# Item descriptive icons

MISSING = "<:missing:854823285825208372>"

PRICE_SOURCE = "<:price_source:854752333299974174>"
RECOMBOBULATOR = "<:recombobulator:854750106376339477>"
ART_OF_WAR = "<:art_of_war:854750132721811466>"
HOT_POTATO_BOOK = "<:hot_potatos:854753109305065482>"
TALISMAN_ENRICHMENT = "<:talisman_enrichment:855013601232551966>"
ENCHANTMENTS = "<:enchantments:854756289010728970>"
REGULAR_STARS = "<:regular_stars:854752631741480990>"
MASTER_STARS = "<:master_stars:854750116066230323>"
SKIN = "<:armor_skin:867793856245006358>"
POWER_ABILITY_SCROLL = "<:power_ability_scroll:1035458856949653504>"
GEMS = "<:gemstone:1035458879523393557>"
GEMSTONE_CHAMBERS = "<:gemstone_chamber:1041792988319330305>"
GEMSTONE_POWER_SCROLL = "<:gemstone_power_scroll:1035458882425847838>"
REFORGE = "<:reforge:854750152048246824>"
TRANSMISSIONS = "<:transmission_tuner:856491122736758814>"
ETHERMERGE = "<:ethermerge:856616140246351892>"
WINNING_BID = "<:winning_bid:856491169750712320>"
DYE = "<:dye:1035458871742959648>"

PET_ITEM = "<:pet_item:854768366014169129>"
PET_SKIN = "<:pet_skin:854768054424305684>"
LEVEL = "<:level:854767687623639080>"

# PAGES ICONS

MAIN = "<:main:854797453223657505>"
INVENTORY = "<:inventory:854797467726643210>"
ENDER_CHEST = "<:ender_chest:854797443321036830>"
ACCESSORES = "<:belt:1035458861596938270>"
WARDROBE = "<:wardrobe:854797516078972928>"

STORAGE = "<:storage:854797494830628884>"
#VAULT = "<:vault:854841046151331900>"
EQUIPMENT = "<:belt:985209099354538014>"
ARMOUR = "<:armor:855021791391383562>"
PETS = "<:pets:854797481132032090>"
MISC = "<:misc:854801277489774613>"

PAGE_TO_EMOJI: dict[str, str] = {
    "main": MAIN,
    "inventory": INVENTORY,
    "ender_chest": ENDER_CHEST,
    "accessories": ACCESSORES,
    "wardrobe": WARDROBE,
    "storage": STORAGE,
    "equipment": EQUIPMENT,
    "armor": ARMOUR,
    "pets": PETS,
    "misc": MISC,
}

PAGES = list(PAGE_TO_EMOJI.keys())
EMOJI_LIST = list(PAGE_TO_EMOJI.values())

PAGE_TO_IMAGE = {
    "main": "https://cdn.discordapp.com/emojis/854797453223657505.png?v=1",
    "inventory": "https://cdn.discordapp.com/emojis/854797467726643210.png?v=1",
    "ender_chest": "https://cdn.discordapp.com/emojis/854797443321036830.png?v=1",
    "accessories": "https://cdn.discordapp.com/emojis/854797427420823572.png?v=1",
    "wardrobe": "https://cdn.discordapp.com/emojis/854797516078972928.png?v=1",

    "storage": "https://cdn.discordapp.com/emojis/854797494830628884.png?v=1",
    #"vault": "https://cdn.discordapp.com/emojis/854841046151331900.png?v=1",
    "equipment": "https://cdn.discordapp.com/emojis/985209099354538014.png?v=1",
    "armor": "https://cdn.discordapp.com/emojis/855021791391383562.png?v=1",
    "pets": "https://cdn.discordapp.com/emojis/854797481132032090.png?v=1",
    "misc": "https://cdn.discordapp.com/emojis/854801277489774613.png?v=1",
} 
