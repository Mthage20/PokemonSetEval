import streamlit as st
import pandas as pd
import os

# Set page configuration for the app
st.set_page_config(page_title="Pokémon Card Calculator", layout="wide")

# Load and process the Pokémon card data
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
    
    # Group by set and calculate metrics with additional stats
    grouped = df.groupby('console-name').agg({
        'product-name': 'count',
        'new-price': ['mean', 'std', 'sum'],
        'Release Year': 'first'
    }).reset_index()
    
    # Flatten multi-index columns
    grouped.columns = ['Set Name', 'Total Cards', 
                      'Avg Rare Value', 'Value Std Dev', 'Total Set Value',
                      'Release Year']
    
    return grouped

# Main application
def main():
    # Load the card data
    card_data = load_card_data()
    
    st.title("Pokémon Card Set Calculator")
    st.write("Evaluate Pokémon card sets based on actual market data")

    if not card_data.empty:
        # Create selection options
        set_options = card_data.to_dict('records')
        selected_set = st.selectbox(
            "Select a Pokémon Set",
            options=set_options,
            format_func=lambda x: f"{x['Set Name']} ({x['Release Year']})"
        )

        st.divider()
        
        # Display set info with new metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Cards", selected_set['Total Cards'])
        with col2:
            st.metric("Avg Value", f"${selected_set['Avg Rare Value']:,.2f}")
        with col3:
            st.metric("Value Std Dev", f"${selected_set['Value Std Dev']:,.2f}")
        with col4:
            st.metric("Total Set Value", f"${selected_set['Total Set Value']:,.2f}")
        with col5:
            st.metric("Release Year", selected_set['Release Year'])

        # Calculation inputs
        st.subheader("Investment Calculator")
        cost = st.number_input("Cost of the Set ($)", 
                              min_value=10, max_value=10000, 
                              value=500, step=50)
        pack_quantity = st.number_input("Number of Items (Packs/Boxes)", 
                                       min_value=1, max_value=1000, 
                                       value=36, step=1)

        # Updated calculation logic using Total Set Value
        if st.button("Calculate Potential Value"):
            total_value = selected_set['Total Set Value']
            potential_return = (total_value * pack_quantity) - cost
            
            st.subheader("Results")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Potential Value", 
                         f"${total_value * pack_quantity:,.2f}", 
                         delta=f"{potential_return:,.2f} Potential Return")
            with col2:
                roi = (potential_return / cost) * 100
                st.metric("ROI Potential", 
                         f"{roi:.1f}%", 
                         delta_color="inverse" if roi < 0 else "normal")

    else:
        st.warning("No card data available. Please check your data source.")

if __name__ == "__main__":
    main()