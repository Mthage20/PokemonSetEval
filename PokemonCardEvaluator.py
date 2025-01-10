import streamlit as st

# Function to calculate the score
def calculate_score(cost, hit_value, pull_rate, pack_quantity, resale_liquidity, rarity_factor, variety):
    ev = hit_value * pull_rate  # Calculate Expected Value
    return ((ev * pack_quantity * resale_liquidity * rarity_factor) + variety) / cost

# Streamlit app
st.title("Pokémon Card Set Score Calculator")
st.write("Use the sliders and selectors below to input the data for your Pokémon card set.")

# Input fields for the variables using sliders and selectors
st.header("Set Inputs")
cost = st.slider("Cost (C): Total price of the set ($)", min_value=10, max_value=1000, value=120, step=10)
hit_value = st.slider("Hit Value (HV): Average value of key cards ($)", min_value=1, max_value=500, value=50, step=1)
pull_rate = st.slider("Pull Rate (PR): Probability of pulling a key card", min_value=0.01, max_value=1.0, value=0.1, step=0.01)
pack_quantity = st.slider("Pack Quantity (PQ): Number of packs in the set", min_value=1, max_value=100, value=36, step=1)
resale_liquidity = st.slider("Resale Liquidity (RL): Likelihood of resale", min_value=0.0, max_value=1.0, value=0.9, step=0.05)
rarity_factor = st.slider("Rarity Factor (RF): Multiplier for desirability", min_value=0.5, max_value=3.0, value=1.1, step=0.1)
variety = st.slider("Variety (V): Score for card diversity", min_value=0, max_value=20, value=5, step=1)

# Calculate and display the score when the button is clicked
if st.button("Calculate Score"):
    score = calculate_score(cost, hit_value, pull_rate, pack_quantity, resale_liquidity, rarity_factor, variety)
    st.success(f"Calculated Score: {score:.2f}")

# Optional: Show all input values for verification
st.subheader("Input Summary")
st.write(f"Cost: ${cost}, Hit Value: ${hit_value}, Pull Rate: {pull_rate}, Packs: {pack_quantity}")
st.write(f"Resale Liquidity: {resale_liquidity}, Rarity Factor: {rarity_factor}, Variety: {variety}")
