import streamlit as st

from fluxosolo.components.charts import (
    plot_chart_donut_category_income,
    plot_chart_donut_category_outgoing,
    plot_chart_line_evolution_transactions,
    print_metrics_income,
    print_metrics_outgoing,
    table_transaction_history,
    plot_chart_horizontal_bar
)
from fluxosolo.utils.processing import (
    prepare_data_chart_donut_category_income,
    prepare_data_chart_donut_category_outgoing,
    prepare_data_chart_line_evolution_transactions,
    prepare_data_metrics_income,
    prepare_data_metrics_outgoing,
    prepare_data_sidebar,
    prepare_data_horizontal_bar_outgoing
)
from fluxosolo.components.sidebar import filter_sidebar, side_bar

st.set_page_config(layout="wide", page_title="Gestão Financeira")


# Injeta CSS para diminuir a margem superior da página
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 3rem;
        }
    </style>
""",
    unsafe_allow_html=True,
)

if "logado" not in st.session_state or not st.session_state["logado"]:
    st.markdown("   ")
    st.markdown("   ")
    st.warning("Você precisa fazer login para acessar esta página.")
    st.switch_page("fluxosolo/app_streamlit.py") # Manda de volta pro login
    st.stop() # Para a execução do código aqui


conn = st.connection("sql")
current_user_id = st.session_state.get('user_id')

df_transactions = conn.query(
    "SELECT t.date, t.value, t.details, b.name AS 'bank', "
    "c.name AS 'category', tt.name AS 'transaction' "
    "FROM transactions t "
    "JOIN banks b ON b.id = t.bank_id "
    "JOIN categories c ON c.id = t.category_id "
    "JOIN transactions_type tt ON tt.id = t.transaction_type_id "
    "WHERE t.user_id = :userid",
    params={'userid': current_user_id},
    ttl=600,
)

side_bar()

if not df_transactions.empty:
    # ------------------------------ Filtro de mês ----------------------------------

    df_raw, month_list, year_list = prepare_data_sidebar(df_transactions)
    df_filtered, df_year, month_selected, year_selected = filter_sidebar(
        df_raw, month_list, year_list
    )

    # -------------------------- Divisão em Colunas ---------------------------------

    left_column, right_column = st.columns([3, 1])

    with left_column:
        st.title("Gestão Financeira")

        left_left_column, right_left_column = st.columns(2)

        with left_left_column:
            income, difference = prepare_data_metrics_income(
                df_filtered, df_raw, month_selected, year_selected
            )
            print_metrics_income(
                income, month_selected, year_selected, difference
            )

        with right_left_column:
            outgoing, difference = prepare_data_metrics_outgoing(
                df_filtered, df_raw, month_selected, year_selected
            )
            print_metrics_outgoing(
                outgoing, month_selected, year_selected, difference
            )

        df_chart = prepare_data_chart_line_evolution_transactions(df_year)
        plot_chart_line_evolution_transactions(df_chart, year_selected)

        df_top5 = prepare_data_horizontal_bar_outgoing(df_filtered)
        plot_chart_horizontal_bar(df_top5)

    with right_column:
        df_donut_income = prepare_data_chart_donut_category_income(df_filtered)
        plot_chart_donut_category_income(
            df_donut_income, month_selected, year_selected
        )

        df_donut_outgoing = prepare_data_chart_donut_category_outgoing(
            df_filtered
        )
        plot_chart_donut_category_outgoing(
            df_donut_outgoing, month_selected, year_selected
        )

else:
    st.markdown("   ")
    st.markdown("   ")
    st.info("Aguardando dados para gerar gráficos")

# ------------------------ Histórico de transações ------------------------------

if not df_transactions.empty:
    table_transaction_history(df_transactions)
else:
    st.info("O banco de dados está vazio. Faça um upload de um extrato.")
