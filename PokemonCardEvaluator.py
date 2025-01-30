import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Pokémon Set Analyzer", layout="wide")

def load_card_data():
    # (Keep the same load_card_data function from previous implementation)
    # ... [previous load_card_data code here] ...

def calculate_final_scores(card_data):
    # (Keep the same score calculation from previous implementation)
    # ... [previous calculate_final_scores code here] ...

def main():
    # Load and process data
    if 'card_data' not in st.session_state:
        st.session_state.card_data = load_card_data()
        st.session_state.card_data = calculate_final_scores(st.session_state.card_data)
    
    card_data = st.session_state.card_data

    st.title("💰 Pokémon Set Value Analyzer")
    st.markdown("Compare Pokémon card set investment potential based on market data")
    
    # Remove the debug section entirely
    
    # Improved Leaderboards with key metrics
    st.header("📈 Investment Leaderboards")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        top_hpv = card_data.sort_values('Highest Potential Value', ascending=False).iloc[0]
        st.metric(label="🔥 Highest Potential Value", 
                value=f"{top_hpv['Set Name']}",
                help="Best set for high-risk/high-reward investors")
        st.bar_chart(card_data.set_index('Set Name')['Highest Potential Value'].head(5))
    
    with col2:
        top_safe = card_data.sort_values('Safest Set to Rip', ascending=False).iloc[0]
        st.metric(label="🛡️ Safest Investment", 
                value=f"{top_safe['Set Name']}",
                help="Most stable set with consistent value")
        st.bar_chart(card_data.set_index('Set Name')['Safest Set to Rip'].head(5))
    
    with col3:
        top_balanced = card_data.sort_values('Best Balanced Set', ascending=False).iloc[0]
        st.metric(label="⚖️ Best Balanced", 
                value=f"{top_balanced['Set Name']}",
                help="Best combination of stability and growth potential")
        st.bar_chart(card_data.set_index('Set Name')['Best Balanced Set'].head(5))

    # Improved comparison section
    st.divider()
    st.header("🔍 Set Comparison Tool")
    
    selected_sets = st.multiselect("Select sets to compare:", 
                                 card_data['Set Name'].unique(),
                                 placeholder="Choose 2-5 sets")
    
    if selected_sets:
        compare_data = card_data[card_data['Set Name'].isin(selected_sets)].set_index('Set Name')
        st.dataframe(
            compare_data[['Total_Cards', 'Avg_Value', 'Total_Value', 
                        'Highest Potential Value', 'Safest Set to Rip', 
                        'Best Balanced Set']],
            use_container_width=True,
            column_config={
                "Total_Cards": "Cards in Set",
                "Avg_Value": st.column_config.NumberColumn("Avg Card Value", format="$%.2f"),
                "Total_Value": st.column_config.NumberColumn("Total Set Value", format="$%.2f"),
            }
        )

if __name__ == "__main__":
    main()