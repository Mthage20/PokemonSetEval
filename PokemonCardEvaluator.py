import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(page_title="Pokémon Card Calculator", layout="wide")

def load_card_data():
    try:
        # Load CSV file
        df = pd.read_csv("pricecharting_data_20250129.csv")
        st.write("✅ CSV Loaded Successfully")

        # Check available columns
        st.write("Columns in dataset:", df.columns.tolist())

        # Define price columns
        price_columns = [
            "loose-price", "cib-price", "new-price", "graded-price",
            "box-only-price", "manual-only-price", "bgs-10-price",
            "condition-17-price", "condition-18-price"
        ]

        # Clean price columns
        for col in price_columns:
            if col in df.columns:
                df[col] = df[col].replace('[\$,]', '', regex=True)
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            else:
                st.warning(f"⚠️ Column '{col}' not found in dataset")

        # Handle release dates
        if 'release-date' in df.columns:
            df['release-date'] = pd.to_datetime(df['release-date'], errors='coerce')
            df = df.dropna(subset=['release-date'])
            df['Release Year'] = df['release-date'].dt.year
        else:
            st.warning("⚠️ 'release-date' column missing!")

        # Ensure 'console-name' exists
        if 'console-name' not in df.columns:
            st.error("❌ 'console-name' column is missing! Data aggregation will fail.")
            return pd.DataFrame()

        # Group by set name and aggregate values
        grouped = df.groupby('console-name').agg(
            Total_Cards=('product-name', 'count'),
            Avg_Value=('new-price', 'mean'),
            Value_Std_Dev=('new-price', 'std'),
            Total_Value=('new-price', 'sum'),
            Release_Year=('Release Year', 'first')
        ).reset_index()

        # Rename columns
        grouped = grouped.rename(columns={
            'console-name': 'Set Name',
            'Total_Cards': 'Total Cards',
            'Avg_Value': 'Avg Value',
            'Value_Std_Dev': 'Value Std Dev',
            'Total_Value': 'Total Value',
            'Release_Year': 'Release Year'
        })

        st.write("📊 Aggregated Data Preview:", grouped.head())

        return grouped

    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return pd.DataFrame()

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

    # Check for NaN values in the leaderboard calculations
    st.write("📈 Score Calculation Stats:", card_data.describe())

    return card_data

def main():
    card_data = load_card_data()

    # Ensure data is not empty before calculations
    if card_data.empty:
        st.error("❌ No data loaded. Please check the CSV file and ensure it has the required columns.")
        return

    card_data = calculate_final_scores(card_data)

    st.title("Pokémon Card Set Analyzer")
    st.write("Compare Pokémon card sets based on market data")

    if not card_data.empty:
        # Leaderboards Section
        st.subheader("Set Leaderboards")
        
        # Debugging: Check sorted values
        st.write("🔍 Debug: Highest Potential Value Ranking Preview", card_data[['Set Name', 'Highest Potential Value']].sort_values('Highest Potential Value', ascending=False).head(5))

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**🏆 Highest Potential Value**")
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
