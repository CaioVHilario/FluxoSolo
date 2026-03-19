import pandas as pd
import plotly.express as px
import streamlit as st

# ------------------------------ Métricas --------------------------------------


def print_metrics_outgoing(outgoing, month_selected, year_selected, difference):

    month_year = f'{month_selected}/{year_selected}'
    month_or_year = 'mês'
    if month_selected == 'Todos':
        month_or_year = 'ano'
        month_year = year_selected

    if outgoing == difference:
        difference = 0

    value=f'R$ {difference:,.2f} que o {month_or_year} anterior'
    if difference > 0:
        color = 'red'
    elif difference == 0:
        value=''
        color='grey'
    else:
        color = 'green'

    st.metric(
        f"Despesas do {month_or_year} - {month_year}",
        f"R$ {outgoing:,.2f}",
        value,
        delta_color=color
    )


def print_metrics_income(income, month_selected, year_selected, difference):

    month_year = f'{month_selected}/{year_selected}'
    month_or_year = 'mês'
    if month_selected == 'Todos':
        month_or_year = 'ano'
        month_year = year_selected


    value=f'R$ {difference:,.2f} que o {month_or_year} anterior'
    if income == difference:
        difference = 0
        value=''

    st.metric(
        f"Receitas do {month_or_year} - {month_year}",
        f"R$ {income:,.2f}",
        value,
    )

# --------------------------- Gráficos de donut --------------------------------


def plot_chart_donut_category_outgoing(df_donut_outgoing, month_selected, year_selected):

    month_year = f'{month_selected}/{year_selected}'
    if month_selected == 'Todos':
        month_year = year_selected

    fig_chart_donut_outgoing = px.pie(
        df_donut_outgoing,
        values="absolut_value",
        names="category",
        title=f"Gastos por categoria - {month_year}",
        hole=0.7,
        color_discrete_sequence=px.colors.sequential.Reds_r,
    )

    fig_chart_donut_outgoing.update_layout(
        legend=dict(
            orientation='h',
            yanchor='top',
            y=-0.1,
            xanchor='center',
            x=0.5
        )
    )

    st.plotly_chart(fig_chart_donut_outgoing, width="stretch")


def plot_chart_donut_category_income(df_donut_income, month_selected, year_selected):

    month_year = f'{month_selected}/{year_selected}'
    if month_selected == 'Todos':
        month_year = year_selected

    fig_chart_donut_income = px.pie(
        df_donut_income,
        values="absolut_value",
        names="category",
        title=f"Ganhos por categoria - {month_year}",
        hole=0.7,
        color_discrete_sequence=px.colors.sequential.Greens_r,
    )

    fig_chart_donut_income.update_layout(
        legend=dict(
            orientation='h',
            yanchor='top',
            y=-0.1,
            xanchor='center',
            x=0.5
        )
    )

    st.plotly_chart(fig_chart_donut_income, width="stretch")

# --------------------------- Gráfico de linha ---------------------------------


def plot_chart_line_evolution_transactions(df_chart, year_selected):

    fig_chart_line = px.line(
        df_chart,
        x="month_abrev",
        y="absolut_value",
        color="type",
        markers=True,
        color_discrete_map={"Ganhos": "green", "Gastos": "red"},
        labels={"absolut_value": "Valor (R$)", "month_abrev": "Mês"},
    )

    fig_chart_line.update_layout(yaxis_tickprefix="R$ ")

    fig_chart_line.update_xaxes(
        dtick=1,           # Pula a legenda de 2 em 2 (mostra mês sim, mês não)
    )

    st.subheader(f"Evolução Financeira de {year_selected}: Ganhos VS Gastos")
    st.plotly_chart(fig_chart_line, width="stretch")

# ------------------------ Histórico de transações ------------------------------


def table_transaction_history(df_banco):
    st.subheader("Histórico das transações")
    st.dataframe(df_banco)