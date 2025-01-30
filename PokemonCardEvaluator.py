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

# ... (previous imports and setup remain the same)

def main():
    card_data = load_card_data()
    card_data = calculate_final_scores(card_data)
    
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
            
            # Identify top performers for each category
            crown_categories = {
                'Highest Potential Value': comparison_data['Highest Potential Value'].idxmax(),
                'Safest Set to Rip': comparison_data['Safest Set to Rip'].idxmax(),
                'Best Balanced Set': comparison_data['Best Balanced Set'].idxmax()
            }
            
            # Display comparison metrics
            st.subheader("Set Comparison")
            
            # Create metrics table with crowns
            comparison_table = comparison_data[[
                'Set Name', 'Release Year', 'Total Cards',
                'Avg Value', 'Value Std Dev', 'Total Value',
                'Highest Potential Value', 'Safest Set to Rip', 'Best Balanced Set'
            ]].copy()
            
            # Add crown emoji to top performers
            for category, idx in crown_categories.items():
                comparison_table.loc[idx, category] = f"👑 {comparison_table.loc[idx, category]:.2f}"

            # Format currency columns
            currency_cols = ['Avg Value', 'Value Std Dev', 'Total Value']
            comparison_table[currency_cols] = comparison_table[currency_cols].applymap(
                lambda x: f"${x:,.2f}" if pd.notnull(x) else "N/A"
            )
            
            # Format crown categories with currency
            crown_currency_cols = ['Highest Potential Value', 'Safest Set to Rip', 'Best Balanced Set']
            comparison_table[crown_currency_cols] = comparison_table[crown_currency_cols].applymap(
                lambda x: f"${float(x.replace('👑 ','')):,.2f}" if '👑' in str(x) else f"${x:,.2f}"
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
                    "Total Value": "Total Set Value",
                    "Highest Potential Value": "Highest Potential Value",
                    "Safest Set to Rip": "Safest Set to Rip",
                    "Best Balanced Set": "Best Balanced Set"
                }
            )
            
            # Add visual separation
            st.divider()
            
            # Detailed individual set view with crowns
            st.subheader("Set Details")
            cols = st.columns(len(selected_sets))
            
            for i, (_, row) in enumerate(comparison_data.iterrows()):
                with cols[i]:
                    st.markdown(f"**{row['Set Name']}**")
                    
                    # Create crown indicators
                    crowns = []
                    for category in crown_categories:
                        if crown_categories[category] == row.name:
                            crowns.append(f"🏆 {category}")
                    
                    if crowns:
                        st.markdown("**Awards:** " + " | ".join(crowns))
                    
                    st.metric("Release Year", row['Release Year'])
                    st.metric("Total Cards", row['Total Cards'])
                    st.metric("Average Value", f"${row['Avg Value']:,.2f}")
                    st.metric("Value Std Dev", f"${row['Value Std Dev']:,.2f}")
                    st.metric("Total Set Value", f"${row['Total Value']:,.2f}")
                    st.metric("Highest Potential Value", 
                             f"${row['Highest Potential Value']:,.2f}",
                             help="👑 Crowned set" if crown_categories['Highest Potential Value'] == row.name else "")
                    st.metric("Safest Set to Rip", 
                             f"${row['Safest Set to Rip']:,.2f}",
                             help="👑 Crowned set" if crown_categories['Safest Set to Rip'] == row.name else "")
                    st.metric("Best Balanced Set", 
                             f"${row['Best Balanced Set']:,.2f}",
                             help="👑 Crowned set" if crown_categories['Best Balanced Set'] == row.name else "")

        else:
            st.warning("Please select at least one set to compare")

    else:
        st.warning("No card data available. Please check your data source.")

if __name__ == "__main__":
    main()