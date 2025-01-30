    import streamlit as st
    import pandas as pd
    import os

    # Set page configuration for the app
    st.set_page_config(page_title="Pokémon Card Calculator", layout="wide")

    def load_card_data():
        # Load the CSV data
        df = pd.read_csv("pricecharting_data_20250129.csv")
        
        # Clean price columns
        price_columns = [
            "loose-price", "cib-price", "new-price", "graded-price",
            "box-only-price", "manual-only-price", "bgs-10-price",
            "condition-17-price", "condition-18-price"
        ]
        
        for col in price_columns:
            df[col] = df[col].replace('[\$,]', '', regex=True).astype(float)
        
        # Handle date conversion
        df['release-date'] = pd.to_datetime(df['release-date'], errors='coerce')
        df = df.dropna(subset=['release-date'])
        
        # Extract release year
        df['Release Year'] = df['release-date'].dt.year
        
        # Group by set and calculate metrics
        grouped = df.groupby('console-name').agg({
            'product-name': 'count',
            'new-price': ['mean', 'std', 'sum'],
            'Release Year': 'first'
        }).reset_index()
        
        # Flatten columns
        grouped.columns = ['Set Name', 'Total Cards', 
                        'Avg Value', 'Value Std Dev', 'Total Value',
                        'Release Year']
        
        return grouped

    def calculate_final_scores(card_data):
        # Calculate final scores for each category
        card_data['Highest Potential Value'] = (card_data['Total Value'] * 0.40) + (card_data['Avg Value'] * 0.30) + (card_data['Value Std Dev'] * 0.30)
        card_data['Safest Set to Rip'] = (card_data['Value Std Dev'] * 0.50) + (card_data['Avg Value'] * 0.30) + (card_data['Total Value'] * 0.20)
        card_data['Best Balanced Set'] = (card_data['Total Value'] * 0.30) + (card_data['Avg Value'] * 0.30) + (card_data['Value Std Dev'] * 0.40)
        
        return card_data

def main():
    card_data = load_card_data()
    card_data = calculate_final_scores(card_data)
    
    st.title("Pokémon Card Set Analyzer")
    st.write("Compare Pokémon card sets based on market data")

    if not card_data.empty:
        # ... (keep the existing comparison section code the same)

        # New Leaderboards Section
        st.divider()
        st.subheader("Set Leaderboards")
        
        # Create three columns for the leaderboards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Highest Potential Value**")
            high_potential = card_data.sort_values('Highest Potential Value', ascending=False).head(10)
            high_potential = high_potential[['Set Name', 'Highest Potential Value', 'Avg Value', 'Total Value']]
            st.dataframe(
                high_potential.style.format({
                    'Highest Potential Value': '${:,.2f}',
                    'Avg Value': '${:,.2f}',
                    'Total Value': '${:,.2f}'
                }),
                height=400,
                hide_index=True,
                use_container_width=True
            )
        
        with col2:
            st.markdown("**Safest Set to Rip**")
            safest = card_data.sort_values('Safest Set to Rip', ascending=False).head(10)
            safest = safest[['Set Name', 'Safest Set to Rip', 'Value Std Dev', 'Avg Value']]
            st.dataframe(
                safest.style.format({
                    'Safest Set to Rip': '${:,.2f}',
                    'Value Std Dev': '${:,.2f}',
                    'Avg Value': '${:,.2f}'
                }),
                height=400,
                hide_index=True,
                use_container_width=True
            )
        
        with col3:
            st.markdown("**Best Balanced Set**")
            balanced = card_data.sort_values('Best Balanced Set', ascending=False).head(10)
            balanced = balanced[['Set Name', 'Best Balanced Set', 'Total Value', 'Avg Value']]
            st.dataframe(
                balanced.style.format({
                    'Best Balanced Set': '${:,.2f}',
                    'Total Value': '${:,.2f}',
                    'Avg Value': '${:,.2f}'
                }),
                height=400,
                hide_index=True,
                use_container_width=True
            )

    else:
        st.warning("No card data available. Please check your data source.")

if __name__ == "__main__":
    main()