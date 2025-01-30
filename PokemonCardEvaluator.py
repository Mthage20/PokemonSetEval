import streamlit as st

# Function to calculate the score
def calculate_score(cost, hit_value, pull_rate, pack_quantity):
    ev = hit_value * pull_rate  # Calculate Expected Value
    return (ev * pack_quantity) / cost

# Function to calculate the total value of a set
def calculate_total_value(pull_rate, hit_value, pack_quantity):
    return pull_rate * hit_value * pack_quantity

# Streamlit app
st.title("Pokémon Card Set Score Calculator")
st.write("Evaluate Pokémon card sets based on cost, pull rates, and other metrics.")

# Input fields using sliders
st.header("Set Inputs")
cost = st.slider("Cost (C): Total price of the set ($)", min_value=10, max_value=1000, value=120, step=10)
hit_value = st.slider("Hit Value (HV): Average value of rare cards ($)", min_value=1, max_value=500, value=50, step=1)
pull_rate = st.slider("Pull Rate (PR): Probability of pulling rare cards", min_value=0.01, max_value=1.0, value=0.1, step=0.01)
pack_quantity = st.slider("Pack Quantity (PQ): Number of packs in the set", min_value=1, max_value=100, value=36, step=1)

# Manual/automatic (once I get my api key) input for card market values 
st.header("Manual Input for Card Values")
card_name = st.text_input("Enter Card Name (e.g., Pikachu VMAX)", "")
card_value = st.number_input("Enter the Market Value of this Card ($)", min_value=0.0, value=float(hit_value), step=0.01)


# Calculate the score and total value when the button is clicked
if st.button("Calculate Score"):
    score = calculate_score(cost, card_value, pull_rate, pack_quantity)
    total_value = calculate_total_value(pull_rate, card_value, pack_quantity)
    
    # Display the results
    st.success(f"Calculated Score: {score:.2f}")
    st.write(f"Total Value of Rare Cards: ${total_value:.2f}")

# Show all input values for verification
st.subheader("Input Summary")
st.write(f"Cost: ${cost}, Hit Value: ${card_value}, Pull Rate: {pull_rate}, Packs: {pack_quantity}")
