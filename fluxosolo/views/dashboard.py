import streamlit as st
import pandas as pd
import plotly.express as px

from fluxosolo.services.verify_database import verify_database
from fluxosolo.services.save_extract import save_extract
from fluxosolo.services.parsers.main import read_extract_file

st.set_page_config(layout='wide', page_title='Gestão Financeira')

conn = st.connection('sql')

st.title('Gestão Financeira')

# id unico da session para controloar o widget de upload
if 'id_uploader' not in st.session_state:
    st.session_state['id_uploader'] = 0

left_column, right_column = st.columns([2, 1])

# Widget de upload com key dinamica
st.sidebar.header('Adicionar novos dados.')
extract = st.sidebar.file_uploader(
    'Faça o upload do seu extrato, NuBank e Banco do Brasil (.csv) e Sicoob (.pdf)',
    type=['csv', 'pdf'],
    key=f'uploader_{st.session_state['id_uploader']}'
)

df_transactions = conn.query('SELECT * FROM transactions', ttl=600)

if not df_transactions.empty:

#------------------------------ Filtro de mês ----------------------------------

    df_raw = df_transactions.copy()
    df_raw['date'] = pd.to_datetime(df_raw['date'], errors='coerce')
    df_raw = df_raw.dropna(subset=['date'])
    df_raw = df_raw.sort_values('date')

    df_raw['month_year'] = df_raw['date'].dt.strftime('%m/%Y').astype(str).str.strip()

    df_raw['type'] = df_raw['value'].apply(
        lambda x: 'Ganhos' if x > 0 else 'Gastos'
    )
    df_raw['absolut_value'] = df_raw['value'].abs()

    st.sidebar.header('Filtros')

    month_list = df_raw['month_year'].unique().tolist()
    month_list.reverse()
    month_list.insert(0, 'Todos')

    month_year_selected = st.sidebar.selectbox('Selecione o mês/ano', month_list)

    if month_year_selected != 'Todos':
        # month_clean = str(month_year_selected).strip()

        df_filtered = df_raw[df_raw['month_year'] == month_year_selected].copy()
    else:
        df_filtered = df_raw.copy()

#--------------------------- Gráfico de linha ----------------------------------

    # cria coluna type para saber a qual linha cada dado pertence e transforma 
    # value em absoluto
    df_transactions['type'] = df_transactions['value'].apply(
        lambda x: 'Ganhos' if x > 0 else 'Gastos'
    )
    df_transactions['absolut_value'] = df_transactions['value'].abs()

    # Converte para datatime
    df_transactions['date'] = pd.to_datetime(df_transactions['date'])

    # Separa mes_ano de date para poder agrupar em seguida
    df_transactions['month_year'] = df_transactions['date'].dt.to_period('M').astype(str)

    # Agrupa por mes_ano e tipo os valores absolutos para plotar cada linha separadamente
    df_chart = df_transactions.groupby(['month_year', 'type'])['absolut_value'].sum().reset_index()

    fig_chart_line = px.line(
        df_chart,
        x='month_year',
        y='absolut_value',
        color='type',
        markers=True,
        title='Comparativo Mensal',
        color_discrete_map={
            'Ganhos': 'green',
            'Gastos': 'red'
        },
        labels={'absolut_value': 'Valor (R$)', 'month_year': 'Mês'},
    )

    fig_chart_line.update_layout(yaxis_tickprefix='R$ ')

    #------------------------ Gráficos de donut --------------------------------

    # Filtro para criar novos df dividos por ganhos e gastos
    df_outgoing = df_filtered[df_filtered['type'] == 'Gastos']
    df_income = df_filtered[df_filtered['type'] == 'Ganhos']

    # criando novos df para agrupar por categoria os ganhos e gastos para gerar o gráfico pie
    df_donut_outgoing = df_outgoing.groupby(['category'])['absolut_value'].sum().reset_index()
    df_donut_income = df_income.groupby(['category'])['absolut_value'].sum().reset_index()

    fig_chart_donut_outgoing = px.pie(
        df_donut_outgoing,
        values='absolut_value',
        names='category',
        title=f'Gastos por categoria - {month_year_selected}',
        hole=0.7,
        color_discrete_sequence=px.colors.qualitative.G10,
    )

    fig_chart_donut_income = px.pie(
        df_donut_income,
        values='absolut_value',
        names='category',
        title=f'Ganhos por categoria - {month_year_selected}',
        hole=0.7,
        color_discrete_sequence=px.colors.qualitative.G10,
    )

#-------------------------- Cálculo de métricas --------------------------------

    income = df_filtered[df_filtered['type'] == 'Ganhos']['absolut_value'].sum()
    outgoing = df_filtered[df_filtered['type'] == 'Gastos']['absolut_value'].sum()

#-------------------------- Divisão em Colunas ---------------------------------

    with left_column:

        left_left_column, right_left_column = st.columns(2)

        with left_left_column:
            st.metric(f'Receitas do Mẽs - {month_year_selected}', f'R$ {income:,.2f}')

        with right_left_column:
            st.metric(f'Despesas do Mês - {month_year_selected}', f'R$ {outgoing:,.2f}')

        st.subheader('Evolução Financeira: Ganhos VS Gastos')
        st.plotly_chart(fig_chart_line, width='stretch')

    with right_column:
        st.plotly_chart(fig_chart_donut_outgoing, width='stretch')
        st.plotly_chart(fig_chart_donut_income, width='stretch')

else:
    st.info('Aguardando dados para gerar gráficos')

#------------------------ Histórico de transações ------------------------------

st.subheader('Histórico das transações')

df_banco = conn.query('SELECT * FROM transactions;', ttl=600)

if not df_banco.empty:
    st.dataframe(df_banco)
else:
    st.info('O banco de dados está vazio. Faça um upload de um extrato.')

#---------------------- Popup de confirmação de dados --------------------------

@st.dialog('Revisão do Extrato Bancário')
def popup_data_confirmation(df):
    st.success('Extrato processado com sucesso!')
    st.write('Pré-vizualização do upload:', df_new.head())

    qtd_exists = verify_database(df_new)
    
    if qtd_exists > 0:

        st.warning(f"Atenção, já extiste {qtd_exists} transações para este periodo de datas com este banco no seu banco de dados")
        st.write('Se você continuar podera duplicar dados. Deseja prosseguir mesmo assim?')
        
        if st.button('Sim, salvar duplicado/complementar'):
            save_extract(df_new)

            st.session_state['id_uploader'] += 1
            # limpa o cache para atualizar a tabela referente ao banco 
            # de dados e em seguida da o rerun na aplicação.
            st.cache_data.clear()
            st.rerun()
    
    else:
        if st.button('Salvar no banco de dados'):
            try:
                save_extract(df_new)
                
                st.session_state['id_uploader'] += 1
                # limpa o cache para atualizar a tabela referente ao banco 
                # de dados e em seguida da o rerun na aplicação.
                st.cache_data.clear()
                st.rerun()

            except Exception as e:
                st.error(f'Erro ao salvar no banco {e}')

#------------------------ Adicionar novos extratos -----------------------------

if extract is not None:
    df_new = read_extract_file(extract)

    if df_new is not None and st.sidebar.button('Revisar e Salvar'):
        popup_data_confirmation(df_new)

        
