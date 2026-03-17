import plotly.express as px
import streamlit as st

# ------------------------------ Métricas --------------------------------------


def print_metrics_outgoing(outgoing, month_year_selected):
    st.metric(
        f"Despesas do Mês - {month_year_selected}",
        f"R$ {outgoing:,.2f}",
    )


def print_metrics_income(income, month_year_selected):
    st.metric(
        f"Receitas do Mês - {month_year_selected}",
        f"R$ {income:,.2f}",
    )

# --------------------------- Gráficos de donut --------------------------------


def plot_chart_donut_category_outgoing(df_donut_outgoing, month_year_selected):
    fig_chart_donut_outgoing = px.pie(
        df_donut_outgoing,
        values="absolut_value",
        names="category",
        title=f"Gastos por categoria - {month_year_selected}",
        hole=0.7,
        color_discrete_sequence=px.colors.qualitative.G10,
    )
    st.plotly_chart(fig_chart_donut_outgoing, width="stretch")


def plot_chart_donut_category_income(df_donut_income, month_year_selected):
    fig_chart_donut_income = px.pie(
        df_donut_income,
        values="absolut_value",
        names="category",
        title=f"Ganhos por categoria - {month_year_selected}",
        hole=0.7,
        color_discrete_sequence=px.colors.qualitative.G10,
    )
    st.plotly_chart(fig_chart_donut_income, width="stretch")

# --------------------------- Gráfico de linha ---------------------------------


def plot_chart_line_evolution_transactions(df_chart):

    fig_chart_line = px.line(
        df_chart,
        x="month_year",
        y="absolut_value",
        color="type",
        markers=True,
        title="Comparativo Mensal",
        color_discrete_map={"Ganhos": "green", "Gastos": "red"},
        labels={"absolut_value": "Valor (R$)", "month_year": "Mês"},
    )

    fig_chart_line.update_layout(yaxis_tickprefix="R$ ")

    fig_chart_line.update_xaxes(
        dtick=2,           # Pula a legenda de 2 em 2 (mostra mês sim, mês não)
    )

    st.subheader("Evolução Financeira: Ganhos VS Gastos")
    st.plotly_chart(fig_chart_line, width="stretch")

# ------------------------ Histórico de transações ------------------------------


def table_transaction_history(df_banco):
    st.subheader("Histórico das transações")
    st.dataframe(df_banco)