from data.constants.collector import fetch_prices

def update_price_lists(data) -> dict:
    print("Updating prices!")
    
    data.BAZAAR, data.LOWEST_BIN, data.PRICES = fetch_prices()
    data.BAZAAR["ENDER_PEARL"] = 100
    data.BAZAAR["ENCHANTED_CARROT"] = 1000
    # For overrides
    for item, hard_price in [("RUNE", 5), ("WISHING_COMPASS", 1000), ("PLUMBER_SPONGE", 100), ("ICE_HUNK", 100),]:
        data.LOWEST_BIN[item] = hard_price
    # Price backups
    for item, hard_price in [("SCATHA;2", 250_000_000),("SCATHA;3", 500_000_000), ("SCATHA;4", 1_000_000_000 ), ("GAME_ANNIHILATOR", 2_500_000_000), ("GAME_BREAKER", 1_000_000_000), ]:
        if item not in data.LOWEST_BIN:
            data.LOWEST_BIN[item] = hard_price

    return data
