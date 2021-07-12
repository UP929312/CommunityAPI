~DUNGEON_EXPERIENCE = (
    50, 75, 110, 160, 230, 330, 470, 670, 950, 1340,
    1890, 2665, 3760, 5260, 7380, 10300, 14400, 20000, 27600, 38000,
    52500, 71500, 97000, 132000, 180000, 243000, 328000, 445000, 600000, 800000,
    1065000, 1410000, 1900000, 2500000, 3300000, 4300000, 5600000, 7200000, 9200000, 12000000,
    15000000, 19000000, 24000000, 30000000, 38000000, 48000000, 60000000, 75000000, 93000000, 116250000
)

LEVEL_50_EXP = 569809640

DUNGEON_WEIGHTS = {
    "CATACOMBS": 0.0002149604615,
    "HEALER": 0.0000045254834,
    "MAGE": 0.0000045254834,
    "BERSERK": 0.0000045254834,
    "ARCHER": 0.0000045254834,
    "TANK": 0.0000045254834,
}


#type, function, exponent, divider
#  TAMING(SkyBlockSkill.TAMING, SkillsResponse::getTaming, 1.14744, 441379);


#https://github.com/Senither/Hypixel-Skyblock-Assistant/blob/master/app/src/main/java/com/senither/hypixel/statistics/weight/DungeonWeight.java

'''
 public Weight calculateTotalWeight() {
        if (!hasData()) {
            return new Weight(0D, 0D);
        }

        double weight = 0D;
        double overflow = 0D;

        for (DungeonWeight value : DungeonWeight.values()) {
            Weight dungeonWeight = value.getCalculatorFromDungeon(this).calculateWeight();

            weight += dungeonWeight.getWeight();
            overflow += dungeonWeight.getOverflow();
        }

        return new Weight(weight, overflow);
    }
    '''
