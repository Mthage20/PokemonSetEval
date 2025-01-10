import streamlit as st

# Function to calculate the score
def calculate_score(cost, hit_value, pull_rate, pack_quantity, resale_liquidity, rarity_factor, variety):
    ev = hit_value * pull_rate  # Calculate Expected Value
    return ((ev * pack_quantity * resale_liquidity * rarity_factor) + variety) / cost

# Streamlit app
st.title("Pokémon Card Set Score Calculator")
st.write("Use this tool to evaluate the value of different Pokémon card sets based on cost, hit value, pull rate, and more.")

# Input fields for the variables
cost = st.number_input("Cost (C): Total price of the set", value=120.0, min_value=0.0)
hit_value = st.number_input("Hit Value (HV): Average value of key cards", value=50.0, min_value=0.0)
pull_rate = st.number_input("Pull Rate (PR): Probability of pulling a key card (e.g., 0.1 for 1 in 10)", value=0.1, min_value=0.0, max_value=1.0)
pack_quantity = st.number_input("Pack Quantity (PQ): Number of packs in the set", value=36, min_value=1)
resale_liquidity = st.number_input("Resale Liquidity (RL): Likelihood of resale (0.0 to 1.0)", value=0.9, min_value=0.0, max_value=1.0)
rarity_factor = st.number_input("Rarity Factor (RF): Multiplier for desirability", value=1.1, min_value=0.0)
variety = st.number_input("Variety (V): Score for card diversity in the set", value=5.0, min_value=0.0)

# Calculate and display the score when the button is clicked
if st.button("Calculate Score"):
    score = calculate_score(cost, hit_value, pull_rate, pack_quantity, resale_liquidity, rarity_factor, variety)
    st.success(f"Calculated Score: {score:.2f}")
else:
    st.write("Fill out the inputs above and click 'Calculate Score' to evaluate.")

