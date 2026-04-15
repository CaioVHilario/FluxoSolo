import pandas as pd
import streamlit as st

# ------------------------------ Side Bar ---------------------------------


@st.cache_data
def prepare_data_sidebar(df_transactions):

    df_raw = df_transactions.copy()

    df_raw["date"] = pd.to_datetime(df_raw["date"], errors="coerce")
    df_raw = df_raw.dropna(subset=["date"])
    df_raw = df_raw.sort_values("date")
    df_raw["month"] = df_raw["date"].dt.month
    df_raw["year"] = df_raw["date"].dt.year

    df_raw["month_year"] = (
        df_raw["date"].dt.strftime("%m/%Y").astype(str).str.strip()
    )

    df_raw["type"] = df_raw["value"].apply(
        lambda x: "Ganhos" if x > 0 else "Gastos"
    )
    df_raw["absolut_value"] = df_raw["value"].abs()

    month_list = df_raw["month"].unique().tolist()
    month_list.reverse()
    month_list.insert(0, "Todos")

    # Pegando todos os anos unicos
    year_list = df_raw["year"].unique().tolist()
    year_list.reverse()

    return df_raw, month_list, year_list


# --------------------------- Gráfico de linha ----------------------------------


@st.cache_data
def prepare_data_chart_line_evolution_transactions(df_year):

    month_dict = {
        1: "JAN",
        2: "FEV",
        3: "MAR",
        4: "ABR",
        5: "MAI",
        6: "JUN",
        7: "JUL",
        8: "AGO",
        9: "SET",
        10: "OUT",
        11: "NOV",
        12: "DEZ",
    }

    df_year["month_abrev"] = df_year["month"].map(month_dict)

    return (
        df_year
        .groupby(["month_year", "type", "month_abrev"], sort=False)[
            "absolut_value"
        ]
        .sum()
        .reset_index()
    )


# ------------------------ Gráficos de donut --------------------------------


@st.cache_data
def prepare_data_chart_donut_category_income(df_filtered):
    df_income = df_filtered[df_filtered["type"] == "Ganhos"]
    return df_income.groupby(["category"])["absolut_value"].sum().reset_index()


@st.cache_data
def prepare_data_chart_donut_category_outgoing(df_filtered):
    df_outgoing = df_filtered[df_filtered["type"] == "Gastos"]
    return (
        df_outgoing.groupby(["category"])["absolut_value"].sum().reset_index()
    )


# -------------------------- Cálculo de métricas --------------------------------


@st.cache_data
def prepare_data_metrics_outgoing(
    df_filtered, df_raw, month_selected, year_selected
):
    outgoing = df_filtered[df_filtered["type"] == "Gastos"][
        "absolut_value"
    ].sum()

    if month_selected == "Todos":
        df_year = df_raw[df_raw["year"] == int(year_selected) - 1]
        before_year = df_year[df_year["type"] == "Gastos"]
        outgoing_before = before_year["absolut_value"].sum()
        difference = outgoing - outgoing_before

    elif month_selected != 1:
        df_year = df_raw[df_raw["year"] == year_selected]
        before_month = df_year[df_raw["month"] == int(month_selected) - 1]
        before_month = before_month[before_month["type"] == "Gastos"]
        outgoing_before = before_month["absolut_value"].sum()
        difference = outgoing - outgoing_before

    else:
        df_year = df_raw[df_raw["year"] == int(year_selected) - 1]
        before_month = df_year[df_year["month"] == 12]
        before_month = before_month[before_month["type"] == "Gastos"]
        outgoing_before = before_month["absolut_value"].sum()
        difference = outgoing - outgoing_before

    return outgoing, difference


@st.cache_data
def prepare_data_metrics_income(
    df_filtered, df_raw, month_selected, year_selected
):

    income = df_filtered[df_filtered["type"] == "Ganhos"][
        "absolut_value"
    ].sum()

    if month_selected == "Todos":
        df_year = df_raw[df_raw["year"] == int(year_selected) - 1]
        before_year = df_year[df_year["type"] == "Ganhos"]
        income_before = before_year["absolut_value"].sum()
        difference = income - income_before

    elif month_selected != 1:
        df_year = df_raw[df_raw["year"] == year_selected]
        before_month = df_year[df_raw["month"] == int(month_selected) - 1]
        before_month = before_month[before_month["type"] == "Ganhos"]
        income_before = before_month["absolut_value"].sum()
        difference = income - income_before

    else:
        df_year = df_raw[df_raw["year"] == int(year_selected) - 1]
        before_month = df_year[df_year["month"] == 12]
        before_month = before_month[before_month["type"] == "Ganhos"]
        income_before = before_month["absolut_value"].sum()
        difference = income - income_before

    return income, difference
