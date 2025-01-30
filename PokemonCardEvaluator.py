import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pokémon Set Analyzer", layout="wide")

def load_card_data():
    try:
        # Try to load the CSV file
        df = pd.read_csv("pricecharting_data_20250129.csv")
    except FileNotFoundError:
        st.error("The file 'pricecharting_data_20250129.csv' was not found. Please ensure the file is in the correct directory.")
        raise
    except UnicodeDecodeError:
        try:
            df = pd.read_csv("pricecharting_data_20250129.csv", encoding='latin1')
        except Exception as e:
            st.error(f"An error occurred while reading the file: {e}")
            raise
    
    required_columns = ['console-name', 'new-price', 'product-name', 'release-date', 'language']
    if not all(col in df.columns for col in required_columns):
        st.error("CSV is missing required columns. Using sample data.")
        raise ValueError("Missing required columns in CSV file.")
    
    df['release-date'] = pd.to_datetime(df['release-date'], errors='coerce')
    df = df[df['release-date'].notna()]
    df['Release Year'] = df['release-date'].dt.year
    
    df['Category'] = df['Release Year'].apply(lambda x: 'Vintage' if x < 2010 else 'Modern')
    df['Language'] = df['language'].apply(lambda x: 'English' if 'English' in x else 'Japanese')
    
    price_columns = [col for col in df.columns if '-price' in col]
    for col in price_columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace(r'[^\d.]', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    grouped = df.groupby(['console-name']).agg(
        Total_Cards=('product-name', 'count'),
        Avg_Value=('new-price', lambda x: round(x.mean(), 2)),
        Value_Std_Dev=('new-price', lambda x: round(x.std(), 2)),
        Total_Value=('new-price', 'sum'),
        Release_Year=('Release Year', 'first'),
        Category=('Category', 'first'),
        Language=('Language', 'first')
    ).reset_index()
    
    grouped['Set Type'] = grouped['Total_Cards'].apply(lambda x: 'Niche' if x < 10 else 'Mainstream')
    
    return grouped.rename(columns={'console-name': 'Set Name'})