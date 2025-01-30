import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(page_title="Pokémon Card Calculator", layout="wide")

def load_card_data():
    try:
        # Attempt to load user's CSV
        df = pd.read_csv("pricecharting_data_20250129.csv")
        
        # Validate required columns
        required_columns = ['console-name', 'new-price', 'product-name', 'release-date']
        if not all(col in df.columns for col in required_columns):
            st.error("CSV is missing required columns. Using sample data.")
            raise FileNotFoundError  # Force fallback to sample data
            
    except FileNotFoundError:
        # Generate sample data if CSV is missing
        st.warning("Using sample data. Upload your CSV for accurate results.")
        sample_data = {
            'console-name': ['Base Set', 'Jungle', 'Fossil'],
            'new-price': [100.50, 75.30, 60.80],
            'product-name': ['Charizard', 'Pikachu', 'Blastoise'],
            'release-date': ['1999-01-01', '1999-06-01', '2000-01-01']
        }
        df = pd.DataFrame(sample_data)
    
    # Continue with existing processing code...
    price_columns = ["new-price"]  # Simplified for example
    for col in price_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df['release-date'] = pd.to_datetime(df['release-date'], errors='coerce')
    grouped = df.groupby('console-name').agg(
        Total_Cards=('product-name', 'count'),
        Avg_Value=('new-price', 'mean'),
        Value_Std_Dev=('new-price', 'std'),
        Total_Value=('new-price', 'sum'),
        Release_Year=('release-date', lambda x: x.dt.year.mode()[0])
    ).reset_index()
    
    return grouped.rename(columns={'console-name': 'Set Name'})

def calculate_final_scores(card_data):
    if card_data.empty:
        return card_data

    card_data['Highest Potential Value'] = (
        (card_data['Total Value'] * 0.40) +
        (card_data['Avg Value'] * 0.30) +
        (card_data['Value Std Dev'] * 0.30)
    )

    card_data['Safest Set to Rip'] = (
        (card_data['Value Std Dev'] * 0.50) +
        (card_data['Avg Value'] * 0.30) +
        (card_data['Total Value'] * 0.20)
    )

    card_data['Best Balanced Set'] = (
        (card_data['Total Value'] * 0.30) +
        (card_data['Avg Value'] * 0.30) +
        (card_data['Value Std Dev'] * 0.40)
    )

    # Check for NaN values in calculations
    st.write("📈 Score Calculation Debug:", card_data.describe())

    return card_data

def main():
    st.title("Pokémon Card Set Analyzer")
    st.write("Compare Pokémon card sets based on market data")

    card_data = load_card_data()

    # Ensure data is not empty before calculations
    if card_data.empty:
        st.error("❌ No data loaded. Please check the CSV file and ensure it has the required columns.")
        return

    card_data = calculate_final_scores(card_data)

    # Force display of full data
    st.subheader("📜 Full Processed Data")
    st.dataframe(card_data, use_container_width=True)

    if not card_data.empty:
        # Leaderboards Section
        st.subheader("🏆 Set Leaderboards")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**💰 Highest Potential Value**")
            high_potential = card_data.sort_values('Highest Potential Value', ascending=False).head(10)
            st.dataframe(high_potential[['Set Name', 'Highest Potential Value', 'Avg Value', 'Total Value']], use_container_width=True)

        with col2:
            st.markdown("**🛡️ Safest Set to Rip**")
            safest = card_data.sort_values('Safest Set to Rip', ascending=False).head(10)
            st.dataframe(safest[['Set Name', 'Safest Set to Rip', 'Value Std Dev', 'Avg Value']], use_container_width=True)

        with col3:
            st.markdown("**⚖️ Best Balanced Set**")
            balanced = card_data.sort_values('Best Balanced Set', ascending=False).head(10)
            st.dataframe(balanced[['Set Name', 'Best Balanced Set', 'Total Value', 'Avg Value']], use_container_width=True)

        # Debugging: Check if leaderboard tables are actually sorted correctly
        st.write("🔍 Debug: Highest Potential Value Ranking Preview", card_data[['Set Name', 'Highest Potential Value']].sort_values('Highest Potential Value', ascending=False).head(5))

        # Comparison Section
        st.divider()
        st.subheader("🔬 Set Comparison")

        selected_sets = st.multiselect(
            "Select sets to compare",
            options=card_data['Set Name'].unique(),
            default=card_data['Set Name'].head(3).tolist()
        )

        if selected_sets:
            comparison_data = card_data[card_data['Set Name'].isin(selected_sets)]
            st.dataframe(comparison_data.set_index('Set Name'), use_container_width=True)

if __name__ == "__main__":
    main()
