import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(page_title="Pokémon Card Calculator", layout="wide")

def load_card_data():
    # Load data with proper encoding
    df = pd.read_csv("pricecharting_data_20250129.csv")
    
    # Clean price columns more robustly
    price_columns = [
        "loose-price", "cib-price", "new-price", "graded-price",
        "box-only-price", "manual-only-price", "bgs-10-price",
        "condition-17-price", "condition-18-price"
    ]
    
    for col in price_columns:
        # Remove $ and commas, handle empty values
        df[col] = df[col].replace('[\$,]', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Handle dates
    df['release-date'] = pd.to_datetime(df['release-date'], errors='coerce')
    df = df.dropna(subset=['release-date'])
    df['Release Year'] = df['release-date'].dt.year
    
    # Group by set with proper aggregation
    grouped = df.groupby('console-name').agg(
        Total_Cards=('product-name', 'count'),
        Avg_Value=('new-price', 'mean'),
        Value_Std_Dev=('new-price', 'std'),
        Total_Value=('new-price', 'sum'),
        Release_Year=('Release Year', 'first')
    ).reset_index()
    
    return grouped.rename(columns={
        'console-name': 'Set Name',
        'Total_Cards': 'Total Cards',
        'Avg_Value': 'Avg Value',
        'Value_Std_Dev': 'Value Std Dev',
        'Total_Value': 'Total Value',
        'Release_Year': 'Release Year'
    })

def calculate_final_scores(card_data):
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
        # Leaderboards Section
        st.subheader("Set Leaderboards")
        
        # Create three columns for the leaderboards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Highest Potential Value**")
            high_potential = card_data.sort_values('Highest Potential Value', ascending=False).head(10)
            st.dataframe(
                high_potential[['Set Name', 'Highest Potential Value', 'Avg Value', 'Total Value']],
                column_config={
                    "Set Name": "Set Name",
                    "Highest Potential Value": st.column_config.NumberColumn(
                        "Potential Value",
                        format="$%.2f"
                    ),
                    "Avg Value": st.column_config.NumberColumn(
                        "Avg Value",
                        format="$%.2f"
                    ),
                    "Total Value": st.column_config.NumberColumn(
                        "Total Value",
                        format="$%.2f"
                    )
                },
                height=400,
                hide_index=True,
                use_container_width=True
            )
        
        with col2:
            st.markdown("**Safest Set to Rip**")
            safest = card_data.sort_values('Safest Set to Rip', ascending=False).head(10)
            st.dataframe(
                safest[['Set Name', 'Safest Set to Rip', 'Value Std Dev', 'Avg Value']],
                column_config={
                    "Set Name": "Set Name",
                    "Safest Set to Rip": st.column_config.NumberColumn(
                        "Safety Score",
                        format="$%.2f"
                    ),
                    "Value Std Dev": st.column_config.NumberColumn(
                        "Value Std Dev",
                        format="$%.2f"
                    ),
                    "Avg Value": st.column_config.NumberColumn(
                        "Avg Value",
                        format="$%.2f"
                    )
                },
                height=400,
                hide_index=True,
                use_container_width=True
            )
        
        with col3:
            st.markdown("**Best Balanced Set**")
            balanced = card_data.sort_values('Best Balanced Set', ascending=False).head(10)
            st.dataframe(
                balanced[['Set Name', 'Best Balanced Set', 'Total Value', 'Avg Value']],
                column_config={
                    "Set Name": "Set Name",
                    "Best Balanced Set": st.column_config.NumberColumn(
                        "Balance Score",
                        format="$%.2f"
                    ),
                    "Total Value": st.column_config.NumberColumn(
                        "Total Value",
                        format="$%.2f"
                    ),
                    "Avg Value": st.column_config.NumberColumn(
                        "Avg Value",
                        format="$%.2f"
                    )
                },
                height=400,
                hide_index=True,
                use_container_width=True
            )

        # Comparison Section
        st.divider()
        st.subheader("Set Comparison")
        
        selected_sets = st.multiselect(
            "Select sets to compare",
            options=card_data['Set Name'].unique(),
            default=card_data['Set Name'].head(3).tolist()
        )
        
        if selected_sets:
            comparison_data = card_data[card_data['Set Name'].isin(selected_sets)]
            
            st.dataframe(
                comparison_data.set_index('Set Name'),
                column_config={
                    "Release Year": st.column_config.NumberColumn(format="%d"),
                    "Total Cards": st.column_config.NumberColumn(format="%d"),
                    "Avg Value": st.column_config.NumberColumn(format="$%.2f"),
                    "Value Std Dev": st.column_config.NumberColumn(format="$%.2f"),
                    "Total Value": st.column_config.NumberColumn(format="$%.2f"),
                    "Highest Potential Value": st.column_config.NumberColumn(format="$%.2f"),
                    "Safest Set to Rip": st.column_config.NumberColumn(format="$%.2f"),
                    "Best Balanced Set": st.column_config.NumberColumn(format="$%.2f")
                },
                use_container_width=True
            )

    else:
        st.error("No data loaded. Check CSV file format and path.")

if __name__ == "__main__":
    main()