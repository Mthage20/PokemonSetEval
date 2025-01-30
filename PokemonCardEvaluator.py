import streamlit as st
import pandas as pd
import os

# Load the pricecharting data
pricecharting_data = pd.read_csv("pricecharting_data_20250129.csv")

# Set page configuration for the app
st.set_page_config(page_title="Pokémon Card Calculator", layout="wide")


# Sidebar navigation to switch between pages
page = st.sidebar.selectbox("Select a Page", ("Pokémon Card Set Calculator", "Enter Pokémon Set Data"))

# **Pokémon Card Set Calculator Page**
if page == "Pokémon Card Set Calculator":
    st.title("Pokémon Card Set Score Calculator")
    st.write("Evaluate Pokémon card sets based on cost, pull rates, and other metrics.")

    # Load sets data to allow selection

        selected_set_label = st.selectbox("Select a Pokémon Set", list(set_options.keys()))

        # Retrieve the selected set's data
        selected_set = set_options[selected_set_label]
        set_name = selected_set['Set Name']
        release_year = selected_set['Release Year']
        total_cards = selected_set['Total Cards']
        rare_card_value = selected_set['Rare Card Value']

        st.write(f"**Selected Set:** {set_name} (Released: {release_year})")
        st.write(f"Total Cards: {total_cards}, Avg Rare Value: ${rare_card_value:.2f}")

        # Filter pricecharting data based on the selected set
        filtered_data = pricecharting_data[pricecharting_data['console-name'].str.contains(set_name, case=False, na=False)]
        
        # Ensure the 'new-price' column is numeric (coerce any non-numeric values to NaN)
        filtered_data['new-price'] = pd.to_numeric(filtered_data['new-price'], errors='coerce')

        if not filtered_data.empty:
            avg_rare_value = filtered_data['new-price'].mean()
            st.write(f"Average Rare Card Value from Pricecharting Data: ${avg_rare_value:.2f}")
        else:
            st.warning("No data available for the selected set in the Pricecharting dataset.")

        # Input fields for calculation
        cost = st.number_input("Cost of the Set ($)", min_value=10, max_value=1000, value=120, step=10)
        pull_rate = st.slider("Pull Rate (PR): Probability of pulling rare cards", min_value=0.01, max_value=1.0, value=0.1, step=0.01)
        pack_quantity = st.number_input("Number of Packs in Set", min_value=1, max_value=100, value=36, step=1)

        # Function to calculate score
        def calculate_score(cost, hit_value, pull_rate, pack_quantity):
            ev = hit_value * pull_rate
            return (ev * pack_quantity) / cost

        # Function to calculate total value
        def calculate_total_value(pull_rate, hit_value, pack_quantity):
            return pull_rate * hit_value * pack_quantity

        # Calculate when button is clicked
        if st.button("Calculate Score"):
            score = calculate_score(cost, rare_card_value, pull_rate, pack_quantity)
            total_value = calculate_total_value(pull_rate, rare_card_value, pack_quantity)

            # Display results
            st.success(f"📈 Calculated Score: {score:.2f}")
            st.write(f"💰 Total Value of Rare Cards: ${total_value:.2f}")

        # Display filtered Pricecharting data
        if not filtered_data.empty:
            st.write("### Pricecharting Data for Selected Set")
            st.dataframe(filtered_data)


 

