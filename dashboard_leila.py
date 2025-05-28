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
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name_encoded}"

        # 📊 Ler dados
        df = pd.read_csv(url)

        st.success("✅ Dados carregados com sucesso!")

        # 🔥 Conversão de colunas numéricas
        colunas_numericas = ['Investimento', 'Leads', 'Vendas', 'Impressões', 'Cliques']
        for coluna in colunas_numericas:
            if coluna in df.columns:
                df[coluna] = pd.to_numeric(df[coluna], errors='coerce').fillna(0)

        # 🔥 Conversão da coluna de data
        if 'Mês/Ano' in df.columns:
            df['Mês/Ano'] = pd.to_datetime(df['Mês/Ano'], format='%m/%Y', errors='coerce')
        else:
            st.error("❌ A coluna 'Mês/Ano' não foi encontrada. Verifique se está escrita exatamente assim.")
            st.stop()

        # ✅ Filtros na sidebar
        with st.sidebar:
            st.header("🎯 Filtros")
            plataformas = st.multiselect("Plataforma", df['Plataforma'].unique(), default=df['Plataforma'].unique())
            campanhas = st.multiselect("Campanha", df['Campanha'].unique(), default=df['Campanha'].unique())
            data_inicial = st.date_input("Mês Inicial", df['Mês/Ano'].min())
            data_final = st.date_input("Mês Final", df['Mês/Ano'].max())

        # 🧠 Aplicar filtros
        data = df.copy()
        data = data[(data['Plataforma'].isin(plataformas)) & (data['Campanha'].isin(campanhas))]
        data = data[(data['Mês/Ano'] >= pd.to_datetime(data_inicial)) & (data['Mês/Ano'] <= pd.to_datetime(data_final))]

        # 🔢 Cálculo dos KPIs
        investimento = data['Investimento'].sum()
        leads = data['Leads'].sum()
        vendas = data['Vendas'].sum()
        impressoes = data['Impressões'].sum()
        cliques = data['Cliques'].sum()

        cpc_medio = (investimento / cliques) if cliques != 0 else 0
        cpl = (investimento / leads) if leads != 0 else 0
        roas = (vendas * cpl) / investimento if investimento != 0 else 0

        # 🎯 Mostrar KPIs
        st.subheader("🎯 Indicadores")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 Investimento", f"R$ {investimento:,.2f}")
        col2.metric("🎯 Leads", f"{leads}")
        col3.metric("📈 CPL", f"R$ {cpl:,.2f}")
        col4.metric("🚀 ROAS", f"{roas:,.2f}")

        col5, col6, col7 = st.columns(3)
        col5.metric("👀 Impressões", f"{impressoes:,}")
        col6.metric("🖱️ Cliques", f"{cliques}")
        col7.metric("💵 CPC Médio", f"R$ {cpc_medio:,.2f}")

        # 📈 Gráfico de evolução
        st.subheader("📊 Evolução Mensal")
        fig1 = px.line(data, x='Mês/Ano', y=['Leads', 'Investimento'],
                       markers=True, title="Leads e Investimento por Mês")
        st.plotly_chart(fig1, use_container_width=True)

        # 📊 Gráficos por plataforma
        st.subheader("🔍 Desempenho por Plataforma")
        df_group = data.groupby('Plataforma').agg({'Leads':'sum', 'Investimento':'sum'}).reset_index()

        fig2 = px.bar(df_group, x='Plataforma', y='Leads', color='Plataforma', title="Leads por Plataforma")
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.pie(df_group, names='Plataforma', values='Investimento', title='Distribuição de Investimento')
        st.plotly_chart(fig3, use_container_width=True)

        # 📑 Dados detalhados
        st.subheader("📑 Dados Detalhados")
        st.dataframe(data)

    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")

else:
    st.info("🔗 Insira o ID da planilha e o nome da aba na barra lateral para começar.")
