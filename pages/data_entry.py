import streamlit as st
import pandas as pd

# File name for storing data
csv_file = "sets.csv"

# Load existing data (if the file exists)
try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Set Name", "Release Year", "Total Cards", "Rare Card Value"])

st.title("Enter Pokémon Set Data")

# Form for Data Entry
with st.form("set_data"):
    set_name = st.text_input("Set Name", "")
    release_year = st.number_input("Release Year", min_value=1996, max_value=2025, value=2024, step=1)
    total_cards = st.number_input("Total Cards in Set", min_value=1, max_value=1000, value=200, step=1)
    rare_card_value = st.number_input("Avg Value of Rare Cards ($)", min_value=0.0, value=10.0, step=0.01)

    submit_button = st.form_submit_button("Save Data")

# Save data when the form is submitted
if submit_button:
    new_data = pd.DataFrame([[set_name, release_year, total_cards, rare_card_value]],
                            columns=["Set Name", "Release Year", "Total Cards", "Rare Card Value"])
    df = pd.concat([df, new_data], ignore_index=True)  # Append new data
    df.to_csv(csv_file, index=False)  # Save back to CSV
    st.success(f"Saved Data for {set_name} (Released: {release_year})")

# Display all saved sets
st.header("Saved Sets")
st.dataframe(df)
