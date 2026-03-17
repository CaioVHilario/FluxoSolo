import streamlit as st

from fluxosolo.views.charts import (
    print_metrics_outgoing,
    print_metrics_income,
    plot_chart_donut_category_income,
    plot_chart_donut_category_outgoing,
    plot_chart_line_evolution_transactions,
    table_transaction_history
)
from fluxosolo.views.processing import (
    prepare_data_chart_donut_category_income,
    prepare_data_chart_donut_category_outgoing,
    prepare_data_chart_line_evolution_transactions, 
    prepare_data_metrics_outgoing,
    prepare_data_metrics_income,
    prepare_data_sidebar
)
from fluxosolo.views.sidebar import side_bar, filter_sidebar

st.set_page_config(layout="wide", page_title="Gestão Financeira")

conn = st.connection("sql")

st.title("Gestão Financeira")

df_transactions = conn.query("SELECT * FROM transactions", ttl=600)

side_bar()

if not df_transactions.empty:
    # ------------------------------ Filtro de mês ----------------------------------

    df_raw, month_list = prepare_data_sidebar(df_transactions)
    df_filtered, month_year_selected = filter_sidebar(month_list, df_raw)

    # -------------------------- Divisão em Colunas ---------------------------------

    left_column, right_column = st.columns([3,1])

    with left_column:
        left_left_column, right_left_column = st.columns(2)

        with left_left_column:
            income = prepare_data_metrics_income(df_filtered)
            print_metrics_income(income, month_year_selected)

        with right_left_column:
            outgoing = prepare_data_metrics_outgoing(df_filtered)
            print_metrics_outgoing(outgoing, month_year_selected)

        df_chart = prepare_data_chart_line_evolution_transactions(df_raw)
        plot_chart_line_evolution_transactions(df_chart)

    with right_column:
        df_donut_income = prepare_data_chart_donut_category_income(df_filtered)
        plot_chart_donut_category_income(df_donut_income, month_year_selected)

        df_donut_outgoing = prepare_data_chart_donut_category_outgoing(df_filtered)
        plot_chart_donut_category_outgoing(df_donut_outgoing, month_year_selected)

else:
    st.info("Aguardando dados para gerar gráficos")

# ------------------------ Histórico de transações ------------------------------

if not df_transactions.empty:
    table_transaction_history(df_transactions)
else:
    st.info("O banco de dados está vazio. Faça um upload de um extrato.")

