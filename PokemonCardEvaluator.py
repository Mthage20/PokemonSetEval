import streamlit as st
import plotly.express as px

st.header("🏆 Set Leaderboards")

# Column layout for leaderboards
col1, col2, col3 = st.columns(3)

# Leaderboard 1: Highest Potential Value
with col1:
    st.subheader("💰 Highest Potential Value")
    top_highest = card_data.sort_values('Highest Potential Value', ascending=False).head(10)
    st.dataframe(top_highest[['Set Name', 'Highest Potential Value', 'Avg Value', 'Total Value']])
    
    # Add a bar chart for better visualization
    fig1 = px.bar(top_highest, x='Set Name', y='Highest Potential Value', title="Highest Potential Value Ranking",
                  text='Highest Potential Value', color='Highest Potential Value', color_continuous_scale="Blues")
    fig1.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig1, use_container_width=True)

# Leaderboard 2: Safest Set to Rip
with col2:
    st.subheader("🛡️ Safest Set to Rip")
    top_safest = card_data.sort_values('Safest Set to Rip', ascending=False).head(10)
    st.dataframe(top_safest[['Set Name', 'Safest Set to Rip', 'Value Std Dev', 'Avg Value']])

    fig2 = px.bar(top_safest, x='Set Name', y='Safest Set to Rip', title="Safest Set to Rip Ranking",
                  text='Safest Set to Rip', color='Safest Set to Rip', color_continuous_scale="Greens")
    fig2.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig2, use_container_width=True)

# Leaderboard 3: Best Balanced Set
with col3:
    st.subheader("⚖️ Best Balanced Set")
    top_balanced = card_data.sort_values('Best Balanced Set', ascending=False).head(10)
    st.dataframe(top_balanced[['Set Name', 'Best Balanced Set', 'Total Value', 'Avg Value']])

    fig3 = px.bar(top_balanced, x='Set Name', y='Best Balanced Set', title="Best Balanced Set Ranking",
                  text='Best Balanced Set', color='Best Balanced Set', color_continuous_scale="Reds")
    fig3.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig3, use_container_width=True)
