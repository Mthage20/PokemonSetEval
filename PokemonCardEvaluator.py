import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pokémon Set Analyzer", layout="wide")

# Function to load and process data
def load_card_data():
    try:
        # Load the CSV file
        df = pd.read_csv("pricecharting_data_20250129.csv")
    except UnicodeDecodeError:
        # Alternative encoding if needed
        df = pd.read_csv("pricecharting_data_20250129.csv", encoding='latin1')
    
    # Check for required columns
    required_columns = ['console-name', 'new-price', 'product-name', 'release-date']
    if not all(col in df.columns for col in required_columns):
        st.error("CSV is missing required columns. Please ensure the file contains: 'console-name', 'new-price', 'product-name', 'release-date'.")
        raise FileNotFoundError
    
    # Infer language from set names (console-name)
    df['Language'] = df['console-name'].apply(
        lambda x: 'Japanese' if 'Japanese' in str(x) else 'English'
    )
    
    # Convert release-date to datetime
    df['release-date'] = pd.to_datetime(df['release-date'], errors='coerce')
    df = df[df['release-date'].notna()]
    df['Release Year'] = df['release-date'].dt.year
    
    # Categorize sets as Vintage or Modern
    df['Category'] = df['Release Year'].apply(lambda x: 'Vintage' if x < 2010 else 'Modern')
    
    # Clean and convert price columns
    price_columns = [col for col in df.columns if '-price' in col]
    for col in price_columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace(r'[^\d.]', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Group data by set
    grouped = df.groupby(['console-name']).agg(
        Total_Cards=('product-name', 'count'),
        Avg_Value=('new-price', lambda x: round(x.mean(), 2)),
        Value_Std_Dev=('new-price', lambda x: round(x.std(), 2)),
        Total_Value=('new-price', 'sum'),
        Release_Year=('Release Year', 'first'),
        Category=('Category', 'first'),
        Language=('Language', 'first')  # Include inferred language
    ).reset_index()
    
    # Categorize sets as Niche or Mainstream
    grouped['Set Type'] = grouped['Total_Cards'].apply(lambda x: 'Niche' if x < 10 else 'Mainstream')
    
    # Rename columns for display
    return grouped.rename(columns={'console-name': 'Set Name'})

# Function to calculate final scores
def calculate_final_scores(card_data):
    card_data['Highest Potential Value'] = (
        (card_data['Total_Value'] * 0.40) + 
        (card_data['Avg_Value'] * 0.30) + 
        (card_data['Value_Std_Dev'] * 0.30)
    ).round(2)
    
    card_data['Safest Set to Rip'] = (
        (card_data['Value_Std_Dev'] * 0.50) + 
        (card_data['Avg_Value'] * 0.30) + 
        (card_data['Total_Value'] * 0.20)
    ).round(2)
    
    card_data['Best Balanced Set'] = (
        (card_data['Total_Value'] * 0.30) + 
        (card_data['Avg_Value'] * 0.30) + 
        (card_data['Value_Std_Dev'] * 0.40)
    ).round(2)
    
    return card_data

# Main function to run the app
def main():
    if 'card_data' not in st.session_state:
        st.session_state.card_data = load_card_data()
        st.session_state.card_data = calculate_final_scores(st.session_state.card_data)
    
    card_data = st.session_state.card_data
    
    # App title and description
    st.title("💰 Pokémon Set Value Analyzer")
    st.markdown("Compare Pokémon card set investment potential based on market data")
    
    # Filters
    set_category = st.selectbox("Filter by Set Type", ['All', 'Vintage', 'Modern'])
    set_type = st.selectbox("Filter by Set Size", ['All', 'Mainstream', 'Niche'])
    set_language = st.selectbox("Filter by Language", ['All', 'English', 'Japanese'])
    
    # Apply filters
    filtered_data = card_data.copy()
    if set_category != 'All':
        filtered_data = filtered_data[filtered_data['Category'] == set_category]
    if set_type != 'All':
        filtered_data = filtered_data[filtered_data['Set Type'] == set_type]
    if set_language != 'All':
        filtered_data = filtered_data[filtered_data['Language'] == set_language]
    
    # Display leaderboards
    st.header("📈 Investment Leaderboards")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🔥 Highest Potential Value")
        st.dataframe(
            filtered_data[['Set Name', 'Highest Potential Value']]
            .sort_values('Highest Potential Value', ascending=False)
            .reset_index(drop=True)
        )
    
    with col2:
        st.subheader("🛡️ Safest Set to Rip")
        st.dataframe(
            filtered_data[['Set Name', 'Safest Set to Rip']]
            .sort_values('Safest Set to Rip', ascending=False)
            .reset_index(drop=True)
        )
    
    with col3:
        st.subheader("⚖️ Best Balanced Set")
        st.dataframe(
            filtered_data[['Set Name', 'Best Balanced Set']]
            .sort_values('Best Balanced Set', ascending=False)
            .reset_index(drop=True)
        )
    
    # Set comparison tool
    st.divider()
    st.header("🔍 Set Comparison Tool")
    
    selected_sets = st.multiselect(
        "Select sets to compare:", 
        filtered_data['Set Name'].unique(), 
        placeholder="Choose 2-5 sets"
    )
    
    # Ensure the `if selected_sets:` block is inside the `main()` function
    if selected_sets:
        # Calculate ranks relative to all filtered sets
        filtered_data['Highest Potential Value Rank'] = (
            filtered_data['Highest Potential Value']
            .rank(ascending=False, method='min', na_option='keep')
            .fillna(9999)  # Replace NaN with a placeholder
            .astype(int)   # Cast to integer
            .replace(9999, pd.NA)  # Replace placeholder back with NaN
        )
        
        filtered_data['Safest Set to Rip Rank'] = (
            filtered_data['Safest Set to Rip']
            .rank(ascending=False, method='min', na_option='keep')
            .fillna(9999)  # Replace NaN with a placeholder
            .astype(int)   # Cast to integer
            .replace(9999, pd.NA)  # Replace placeholder back with NaN
        )
        
        filtered_data['Best Balanced Set Rank'] = (
            filtered_data['Best Balanced Set']
            .rank(ascending=False, method='min', na_option='keep')
            .fillna(9999)  # Replace NaN with a placeholder
            .astype(int)   # Cast to integer
            .replace(9999, pd.NA)  # Replace placeholder back with NaN
        )
        
        # Filter the selected sets
        compare_data = filtered_data[filtered_data['Set Name'].isin(selected_sets)].copy()
        
        # Display comparison table with ranks and key metrics
        st.dataframe(
            compare_data[['Set Name', 'Total_Cards', 'Avg_Value', 'Value_Std_Dev', 'Total_Value', 
                        'Highest Potential Value Rank',
                        'Safest Set to Rip Rank',
                        'Best Balanced Set Rank']],
            use_container_width=True,
            column_config={
                "Total_Cards": "Cards in Set",
                "Avg_Value": st.column_config.NumberColumn("Avg Card Value", format="$%.2f"),
                "Value_Std_Dev": st.column_config.NumberColumn("Std Dev", format="$%.2f"),
                "Total_Value": st.column_config.NumberColumn("Total Set Value", format="$%.2f"),
                "Highest Potential Value Rank": "Rank (HPV)",
                "Safest Set to Rip Rank": "Rank (SSR)",
                "Best Balanced Set Rank": "Rank (BBS)",
            }
        )

        # --- WINNER SECTION ---
        st.divider()
        st.header("🏆 Category Winners (Selected Sets)")

        # custom CSS for winner cards
        st.markdown("""
        <style>
            .winner-card {
                padding: 20px;
                border-radius: 10px;
                background: #f8f9fa;
                border-left: 5px solid #4CAF50;
                margin: 10px 0;
                position: relative;
                color: #2c3e50;
            }
            .winner-card h3 {
                margin-top: 0;
            }
            .winner-card::after {
                content: '🏆';
                position: absolute;
                right: 15px;
                top: 15px;
                font-size: 24px;
                opacity: 0.3;
            }
        </style>
        """, unsafe_allow_html=True)

        # Create columns for winners
        col1, col2, col3 = st.columns(3)

        # Function to display a winner card
        def display_winner(column, title, score_column):
            with column:
                # Find the top-performing set in the filtered data
                winner = filtered_data.nlargest(1, score_column)
                st.write(f"Debug - {title} Winner:", winner)  # Debugging print
                st.write(f"Debug - Selected Sets:", selected_sets)  # Debugging print
                # Check if the winner is among the selected sets
                if not winner.empty and winner.iloc[0]['Set Name'] in selected_sets:
                    st.markdown(f"""
                    <div class="winner-card">
                        <h3>{title}</h3>
                        <p><strong>{winner.iloc[0]['Set Name']}</strong></p>
                        <p>Score: {winner.iloc[0][score_column]}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="winner-card">
                        <h3>{title}</h3>
                        <p><em>No winner found</em></p>
                    </div>
                    """, unsafe_allow_html=True)

        # Display winners
        display_winner(col1, "🔥 Highest Potential Value", "Highest Potential Value")
        display_winner(col2, "🛡️ Safest Set to Rip", "Safest Set to Rip")
        display_winner(col3, "⚖️ Best Balanced Set", "Best Balanced Set")

# Run the app
if __name__ == "__main__":
    main()
