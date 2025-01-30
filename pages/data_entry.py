import streamlit as st

st.set_page_config(page_title="Enter Pokémon Set Data", layout="wide")

st.title("Enter Pokémon Set Data")
st.write("Manually input Pokémon card set details.")

# Form for Data Entry
with st.form("set_data"):
    set_name = st.text_input("Set Name", "")
    release_year = st.number_input("Release Year", min_value=1996, max_value=2025, value=2024, step=1)
    total_cards = st.number_input("Total Cards in Set", min_value=1, max_value=1000, value=200, step=1)
    rare_card_value = st.number_input("Avg Value of Rare Cards ($)", min_value=0.0, value=10.0, step=0.01)
    
    submit_button = st.form_submit_button("Save Data")

if submit_button:
    st.success(f"Saved Data for {set_name} (Released: {release_year})")
