from accessory_list import talisman_upgrades

dupes = []

for key, value in talisman_upgrades.items():
    dupes.append(key)
    for v2 in value:
        dupes.append(v2)

all_accessories = list(set(dupes))

[all_accessories.remove(key) for key in talisman_upgrades.keys()]

print(all_accessories)
