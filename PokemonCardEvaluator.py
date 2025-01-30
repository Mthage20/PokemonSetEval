import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(page_title="Pokémon Card Calculator", layout="wide")

def load_card_data():
    try:
        # Attempt to load user's CSV with multiple encoding attempts
        try:
            df = pd.read_csv("pricecharting_data_20250129.csv")
        except UnicodeDecodeError:
            df = pd.read_csv("pricecharting_data_20250129.csv", encoding='latin1')
            
        # Validate required columns
        required_columns = ['console-name', 'new-price', 'product-name', 'release-date']
        if not all(col in df.columns for col in required_columns):
            st.error("CSV is missing required columns. Using sample data.")
            raise FileNotFoundError
            
    except FileNotFoundError:
        # Generate realistic sample data
        st.warning("Using sample data. Upload your CSV for accurate results.")
        sample_data = {
            'console-name': ['Base Set', 'Jungle', 'Fossil', 'Base Set 2', 'Team Rocket'],
            'new-price': [450.50, 120.30, 95.80, 380.00, 75.40],
            'product-name': ['Charizard', 'Pikachu', 'Blastoise', 'Venusaur', 'Dark Charizard'],
            'release-date': ['1999-01-01', '1999-06-01', '2000-01-01', '2000-05-01', '2001-03-15'],
            'loose-price': [320.00, 80.50, 65.30, 275.00, 50.20],
            'graded-price': [1200.00, 450.00, 680.00, 950.00, 350.00]
        }
        df = pd.DataFrame(sample_data)
    
    # Enhanced price cleaning with debug
    price_columns = [col for col in df.columns if '-price' in col]
    
    for col in price_columns:
        if df[col].dtype == 'object':
            # Remove all non-numeric characters except decimals
            df[col] = df[col].astype(str).str.replace(r'[^\d.]', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Date handling with validation
    df['release-date'] = pd.to_datetime(df['release-date'], errors='coerce')
    df = df[df['release-date'].notna()]  # Filter out invalid dates
    df['Release Year'] = df['release-date'].dt.year
    
    # Debug output
    st.session_state.raw_data = df.copy()
    
    # Group with enhanced aggregation
    grouped = df.groupby('console-name').agg(
        Total_Cards=('product-name', 'count'),
        Avg_Value=('new-price', lambda x: round(x.mean(), 2)),
        Value_Std_Dev=('new-price', lambda x: round(x.std(), 2)),
        Total_Value=('new-price', 'sum'),
        Release_Year=('Release Year', 'first')
    ).reset_index()
    
    return grouped.rename(columns={'console-name': 'Set Name'})

def calculate_final_scores(card_data):
    # Ensure numeric stability
    for col in ['Total Value', 'Avg Value', 'Value Std Dev']:
        card_data[col] = card_data[col].fillna(0)
    
    # Weighted calculations with validation
    card_data['Highest Potential Value'] = (
        (card_data['Total Value'] * 0.40) + 
        (card_data['Avg Value'] * 0.30) + 
        (card_data['Value Std Dev'] * 0.30)
    ).round(2)
    
    card_data['Safest Set to Rip'] = (
        (card_data['Value Std Dev'] * 0.50) + 
        (card_data['Avg Value'] * 0.30) + 
        (card_data['Total Value'] * 0.20)
    ).round(2)
    
    card_data['Best Balanced Set'] = (
        (card_data['Total Value'] * 0.30) + 
        (card_data['Avg Value'] * 0.30) + 
        (card_data['Value Std Dev'] * 0.40)
    ).round(2)
    
    return card_data

def main():
    card_data = load_card_data()
    card_data = calculate_final_scores(card_data)
    
    st.title("Pokémon Card Set Analyzer")
    st.write("Compare Pokémon card sets based on market data")
    
    # Debug section
    with st.expander("Debug Data Preview"):
        st.write("Raw Data Sample:", st.session_state.raw_data.head())
        st.write("Processed Data:", card_data)
        st.write("Numeric Columns Summary:", card_data.describe())

    # Rest of your existing display code...
    # [Keep the leaderboards and comparison sections unchanged from previous version]

if __name__ == "__main__":
    main()