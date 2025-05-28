
import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# 🎨 Layout e título
# =========================
st.set_page_config(page_title="Dashboard de Marketing - Leila", layout="wide")
st.title("📊 Dashboard de Marketing - Leila")

# =========================
# 📥 Entrada do usuário: ID da Planilha e Nome da Aba
# =========================
st.sidebar.header("🔗 Conexão com Google Sheets")

sheet_id = st.sidebar.text_input(
    "🔑 ID da Planilha (Google Sheets)",
    placeholder="Cole aqui o ID da planilha...")

sheet_name = st.sidebar.text_input(
    "📄 Nome da aba",
    placeholder="Digite o nome exato da aba...")

if sheet_id and sheet_name:
    try:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        df = pd.read_csv(url)

        st.subheader("✅ Dados carregados da planilha")
        st.dataframe(df)

        # Conversão de coluna de data se existir
        if 'Mês/Ano' in df.columns:
            df['Mês/Ano'] = pd.to_datetime(df['Mês/Ano'], format='%m/%Y')

            # Filtros
            with st.sidebar:
                st.header("🎯 Filtros")
                plataformas = st.multiselect("Plataforma", df['Plataforma'].unique(), default=df['Plataforma'].unique())
                campanhas = st.multiselect("Campanha", df['Campanha'].unique(), default=df['Campanha'].unique())
                mes_inicial = st.date_input("Mês Inicial", df['Mês/Ano'].min())
                mes_final = st.date_input("Mês Final", df['Mês/Ano'].max())

            data = df.copy()
            data = data[(data['Plataforma'].isin(plataformas)) & (data['Campanha'].isin(campanhas))]
            data = data[(data['Mês/Ano'] >= pd.to_datetime(mes_inicial)) & (data['Mês/Ano'] <= pd.to_datetime(mes_final))]

            # KPIs
            investimento = data['Investimento'].sum()
            leads = data['Leads'].sum()
            vendas = data['Vendas'].sum()
            impressoes = data['Impressões'].sum()
            cliques = data['Cliques'].sum()
            cpc_medio = (investimento / cliques) if cliques != 0 else 0
            cpl = (investimento / leads) if leads != 0 else 0
            roas = (vendas * cpl) / investimento if investimento != 0 else 0

            st.subheader("🎯 Indicadores")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("💰 Investimento", f"R$ {investimento:,.2f}")
            col2.metric("🎯 Leads", f"{leads}")
            col3.metric("📈 CPL", f"R$ {cpl:,.2f}")
            col4.metric("🚀 ROAS", f"{roas:,.2f}")

            # Gráficos
            st.subheader("📊 Gráficos")
            fig1 = px.line(data, x='Mês/Ano', y=['Leads', 'Investimento'], markers=True, title="Evolução de Leads e Investimento")
            st.plotly_chart(fig1, use_container_width=True)

            df_group = data.groupby('Plataforma').agg({'Leads':'sum', 'Investimento':'sum'}).reset_index()
            fig2 = px.bar(df_group, x='Plataforma', y='Leads', color='Plataforma', title="Leads por Plataforma")
            st.plotly_chart(fig2, use_container_width=True)

            fig3 = px.pie(df_group, names='Plataforma', values='Investimento', title='Distribuição de Investimento')
            st.plotly_chart(fig3, use_container_width=True)

            # Dados detalhados
            st.subheader("📑 Dados Detalhados")
            st.dataframe(data)

        else:
            st.error("⚠️ A coluna 'Mês/Ano' não foi encontrada na planilha. Verifique o nome das colunas.")

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

else:
    st.info("🔗 Insira o ID da planilha e o nome da aba na barra lateral para começar.")
