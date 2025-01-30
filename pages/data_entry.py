{\rtf1\ansi\ansicpg1252\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww9800\viewh11980\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
\
st.set_page_config(page_title="Enter Pok\'e9mon Set Data", layout="wide")\
\
st.title("Enter Pok\'e9mon Set Data")\
st.write("Manually input Pok\'e9mon card set details.")\
\
# Form for Data Entry\
with st.form("set_data"):\
    set_name = st.text_input("Set Name", "")\
    release_year = st.number_input("Release Year", min_value=1996, max_value=2025, value=2024, step=1)\
    total_cards = st.number_input("Total Cards in Set", min_value=1, max_value=1000, value=200, step=1)\
    rare_card_value = st.number_input("Avg Value of Rare Cards ($)", min_value=0.0, value=10.0, step=0.01)\
    \
    submit_button = st.form_submit_button("Save Data")\
\
if submit_button:\
    st.success(f"Saved Data for \{set_name\} (Released: \{release_year\})")\
}