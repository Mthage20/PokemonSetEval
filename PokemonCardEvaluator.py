import streamlit as st

st.set_page_config(page_title="Pokémon Card Calculator", layout="wide")

st.title("Pokémon Card Set Score Calculator")
st.write("Evaluate Pokémon card sets based on cost, pull rates, and other metrics.")

# Navigation
st.page_link("data_entry.py", label="Go to Data Entry", icon="📊")

# Main Page Content
st.header("Set Inputs")
cost = st.slider("Cost (C): Total price of the set ($)", min_value=10, max_value=1000, value=120, step=10)
hit_value = st.slider("Hit Value (HV): Average value of rare cards ($)", min_value=1, max_value=500, value=50, step=1)
pull_rate = st.slider("Pull Rate (PR): Probability of pulling rare cards", min_value=0.01, max_value=1.0, value=0.1, step=0.01)
pack_quantity = st.slider("Pack Quantity (PQ): Number of packs in the set", min_value=1, max_value=100, value=36, step=1)

# Calculate score
def calculate_score(cost, hit_value, pull_rate, pack_quantity):
    ev = hit_value * pull_rate
    return (ev * pack_quantity) / cost

if st.button("Calculate Score"):
    score = calculate_score(cost, hit_value, pull_rate, pack_quantity)
    st.success(f"Calculated Score: {score:.2f}")
