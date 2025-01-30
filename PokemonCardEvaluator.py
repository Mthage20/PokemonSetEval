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

def main():
    card_data = load_card_data()
    
    st.title("Pokémon Card Set Analyzer")
    st.write("Compare Pokémon card sets based on market data")

    if not card_data.empty:
        # Multi-select for set comparison
        selected_sets = st.multiselect(
            "Select sets to compare",
            options=card_data['Set Name'].unique(),
            default=[card_data['Set Name'].iloc[0]]
        )
        
        if selected_sets:
            # Filter selected sets
            comparison_data = card_data[card_data['Set Name'].isin(selected_sets)]
            
            # Display comparison metrics
            st.subheader("Set Comparison")
            
            # Create metrics table
            comparison_table = comparison_data[[
                'Set Name', 'Release Year', 'Total Cards',
                'Avg Value', 'Value Std Dev', 'Total Value'
            ]].copy()
            
            # Format currency columns
            currency_cols = ['Avg Value', 'Value Std Dev', 'Total Value']
            comparison_table[currency_cols] = comparison_table[currency_cols].applymap(
                lambda x: f"${x:,.2f}" if pd.notnull(x) else "N/A"
            )
            
            # Display as table with index removed
            st.dataframe(
                comparison_table.set_index('Set Name'),
                use_container_width=True,
                column_config={
                    "Release Year": "Release Year",
                    "Total Cards": "Total Cards",
                    "Avg Value": "Average Value",
                    "Value Std Dev": "Value Std Dev",
                    "Total Value": "Total Set Value"
                }
            )
            
            # Add visual separation
            st.divider()
            
            # Detailed individual set view
            st.subheader("Set Details")
            cols = st.columns(len(selected_sets))
            
            for i, (_, row) in enumerate(comparison_data.iterrows()):
                with cols[i]:
                    st.markdown(f"**{row['Set Name']}**")
                    st.metric("Release Year", row['Release Year'])
                    st.metric("Total Cards", row['Total Cards'])
                    st.metric("Average Value", f"${row['Avg Value']:,.2f}")
                    st.metric("Value Std Dev", f"${row['Value Std Dev']:,.2f}")
                    st.metric("Total Set Value", f"${row['Total Value']:,.2f}")

        else:
            st.warning("Please select at least one set to compare")

    else:
        st.warning("No card data available. Please check your data source.")

if __name__ == "__main__":
    main()