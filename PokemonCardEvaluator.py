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
        # Multi-select for set comparison
        selected_sets = st.multiselect(
            "Select sets to compare",
            options=card_data['Set Name'].unique(),
            default=[card_data['Set Name'].iloc[0]]
        )
        
        if selected_sets:
            # Reset index for reliable row identification
            comparison_data = card_data[card_data['Set Name'].isin(selected_sets)].reset_index(drop=True)
            
            # Debug: Show raw data
            st.write("Debug - Comparison Data:", comparison_data)
            
            # Identify top performers with error handling
            crown_categories = {}
            try:
                crown_categories = {
                    'Highest Potential Value': comparison_data['Highest Potential Value'].idxmax(),
                    'Safest Set to Rip': comparison_data['Safest Set to Rip'].idxmax(),
                    'Best Balanced Set': comparison_data['Best Balanced Set'].idxmax()
                }
            except ValueError as e:
                st.error(f"Error calculating crowns: {e}. Check if all score columns contain numeric values.")
            
            st.subheader("Set Comparison")
            
            # Create display dataframe with formatted numbers
            display_df = comparison_data.copy()
            
            # Format currency columns first
            currency_cols = ['Avg Value', 'Value Std Dev', 'Total Value']
            display_df[currency_cols] = display_df[currency_cols].applymap(lambda x: f"${x:,.2f}")
            
            # Format score columns with crowns
            score_cols = ['Highest Potential Value', 'Safest Set to Rip', 'Best Balanced Set']
            for col in score_cols:
                display_df[col] = display_df[col].apply(lambda x: f"${x:,.2f}")
                
            # Add crowns after formatting
            for category, idx in crown_categories.items():
                if idx in display_df.index:
                    display_df.loc[idx, category] = "👑 " + display_df.loc[idx, category]

            # Display table with custom formatting
            st.dataframe(
                display_df.set_index('Set Name')[['Release Year', 'Total Cards'] + currency_cols + score_cols],
                use_container_width=True,
                column_config={
                    "Release Year": "Release Year",
                    "Total Cards": "Total Cards",
                    "Avg Value": "Average Value",
                    "Value Std Dev": "Value Std Dev",
                    "Total Value": "Total Set Value",
                    "Highest Potential Value": st.column_config.Column(
                        "Highest Potential Value",
                        help="Weighted score combining total value and variance"
                    ),
                    "Safest Set to Rip": st.column_config.Column(
                        "Safest Set to Rip",
                        help="Score emphasizing lower risk"
                    ),
                    "Best Balanced Set": st.column_config.Column(
                        "Best Balanced Set",
                        help="Balanced combination of factors"
                    )
                }
            )

            # Detailed view with clear crowns
            st.subheader("Set Details")
            cols = st.columns(len(selected_sets))
            
            for i, (index, row) in enumerate(display_df.iterrows()):
                with cols[i]:
                    # Header with potential crown
                    crown_str = ""
                    if index in crown_categories.values():
                        crown_str = " 👑"
                    st.markdown(f"### {row['Set Name']}{crown_str}")
                    
                    # Metrics with conditional styling
                    metric_kwargs = {
                        'Highest Potential Value': {'help': 'Includes total value and variance'},
                        'Safest Set to Rip': {'help': 'Lower risk indicator'},
                        'Best Balanced Set': {'help': 'Balanced performance'}
                    }
                    
                    st.metric("Release Year", row['Release Year'])
                    st.metric("Total Cards", row['Total Cards'])
                    st.metric("Average Value", row['Avg Value'])
                    st.metric("Value Std Dev", row['Value Std Dev'])
                    st.metric("Total Set Value", row['Total Value'])
                    
                    # Highlight crowned metrics
                    for score_col in score_cols:
                        value = row[score_col]
                        is_crowned = crown_categories.get(score_col, -1) == index
                        st.metric(
                            score_col,
                            value,
                            help="Top performer in this category" if is_crowned else "",
                            delta="★ Crowned Set" if is_crowned else None
                        )

        else:
            st.warning("Please select at least one set to compare")

    else:
        st.warning("No card data available. Please check your data source.")

if __name__ == "__main__":
    main()