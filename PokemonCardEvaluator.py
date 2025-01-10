
# Define a function to calculate the score
def calculate_score(cost, hit_value, pull_rate, pack_quantity, resale_liquidity, rarity_factor, variety):
    # Calculate Expected Value (EV)
    ev = hit_value * pull_rate
    # Calculate the final score
    score = ((ev * pack_quantity * resale_liquidity * rarity_factor) + variety) / cost
    return score

# Data: Example Pokémon sets
sets = [
    {
        "name": "Set A",
        "cost": 120,
        "hit_value": 50,
        "pull_rate": 0.10,
        "pack_quantity": 36,
        "resale_liquidity": 0.9,
        "rarity_factor": 1.1,
        "variety": 5,
    },
    {
        "name": "Set B",
        "cost": 100,
        "hit_value": 40,
        "pull_rate": 0.08,
        "pack_quantity": 30,
        "resale_liquidity": 0.8,
        "rarity_factor": 1.2,
        "variety": 7,
    },
]

# Calculate and display scores for each set
for set_data in sets:
    score = calculate_score(
        set_data["cost"],
        set_data["hit_value"],
        set_data["pull_rate"],
        set_data["pack_quantity"],
        set_data["resale_liquidity"],
        set_data["rarity_factor"],
        set_data["variety"],
    )
    print(f"Set: {set_data['name']}, Score: {score:.2f}")
