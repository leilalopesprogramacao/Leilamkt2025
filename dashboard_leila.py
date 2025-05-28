import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Marketing - Leila", layout="wide")
st.title("📊 Dashboard de Marketing - Leila")

# 📥 Sidebar para entrada do ID da planilha e nome da aba
st.sidebar.header("🔗 Conectar Planilha Google Sheets")
sheet_id = st.sidebar.text_input("ID da Planilha", placeholder="Cole o ID aqui...")
sheet_name = st.sidebar.text_input("Nome da Aba", placeholder="Digite o nome da aba...")

if sheet_id and sheet_name:
    try:
        # 🔗 Montar URL da planilha
        sheet_name_encoded = sheet_name.replace(' ', '%20')
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/_
