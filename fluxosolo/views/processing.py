import pandas as pd
import streamlit as st


# ------------------------------ Side Bar ---------------------------------


@st.cache_data
def prepare_data_sidebar(df_transactions):
    
    df_raw = df_transactions.copy()
    
    df_raw["date"] = pd.to_datetime(df_raw["date"], errors="coerce")
    df_raw = df_raw.dropna(subset=["date"])
    df_raw = df_raw.sort_values("date")

    df_raw["month_year"] = (
        df_raw["date"].dt.strftime("%m/%Y").astype(str).str.strip()
    )

    df_raw["type"] = df_raw["value"].apply(
        lambda x: "Ganhos" if x > 0 else "Gastos"
    )
    df_raw["absolut_value"] = df_raw["value"].abs()

    month_list = df_raw["month_year"].unique().tolist()
    month_list.reverse()
    month_list.insert(0, "Todos")

    return df_raw, month_list

# --------------------------- Gráfico de linha ----------------------------------

@st.cache_data
def prepare_data_chart_line_evolution_transactions(df_raw):
    df_chart = (
        df_raw
        .groupby(["month_year", "type"], sort=False)["absolut_value"]
        .sum()
        .reset_index()
    )
    return df_chart

# ------------------------ Gráficos de donut --------------------------------

@st.cache_data
def prepare_data_chart_donut_category_income(df_filtered):
    df_income = df_filtered[df_filtered["type"] == "Ganhos"]
    df_donut_income = (
        df_income.groupby(["category"])["absolut_value"].sum().reset_index()
    )
    return df_donut_income

@st.cache_data
def prepare_data_chart_donut_category_outgoing(df_filtered):
    df_outgoing = df_filtered[df_filtered["type"] == "Gastos"]
    df_donut_outgoing = (
        df_outgoing.groupby(["category"])["absolut_value"].sum().reset_index()
    )
    return df_donut_outgoing

# -------------------------- Cálculo de métricas --------------------------------

@st.cache_data
def prepare_data_metrics_outgoing(df_filtered):
    outgoing = df_filtered[df_filtered["type"] == "Gastos"]["absolut_value"].sum()
    return outgoing

@st.cache_data
def prepare_data_metrics_income(df_filtered):
    income = df_filtered[df_filtered["type"] == "Ganhos"]["absolut_value"].sum()
    return income