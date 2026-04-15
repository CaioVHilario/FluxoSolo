import streamlit as st

from fluxosolo.services.parsers.main import read_extract_file
from fluxosolo.views.popups import popup_data_confirmation


def side_bar():

    # id unico da session para controloar o widget de upload de arquivos, para
    # forçar o reset do widget a cada upload e evitar bugs de arquivos e evitar que
    # o arquivo fique preso na tela.
    if "id_uploader" not in st.session_state:
        st.session_state["id_uploader"] = 0

    # Widget de upload com key dinamica
    st.sidebar.header("Adicionar novos dados.")
    extract = st.sidebar.file_uploader(
        "Faça o upload do seu extrato, NuBank e Banco do Brasil (.csv) e Sicoob (.pdf)",
        type=["csv", "pdf"],
        key=f"uploader_{st.session_state['id_uploader']}",
    )

    # ------------------------ Adicionar novos extratos ------------------------

    try:
        if extract is not None:
            df_new = read_extract_file(extract)

            if df_new is not None and st.sidebar.button("Revisar e Salvar"):
                popup_data_confirmation(df_new)

    except AttributeError:
        st.sidebar.error(
            "Aqruivo incompativel! Por favor, envie apenas extratos válidos do NuBank, BB ou Sicoob."
        )


def filter_sidebar(df_raw, month_list, year_list):
    st.sidebar.header("Filtros")

    year_selected = st.sidebar.selectbox("Selecione o ano", year_list)

    month_dict = {
        "Todos": "Todos",
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro",
    }

    month_selected = st.sidebar.selectbox(
        "Selecione o mês", month_dict.values()
    )
    month_selected = list(month_dict.keys())[
        list(month_dict.values()).index(month_selected)
    ]

    # year_clean = str(year_selected).strip()
    # month_clean = str(month_selected).strip()

    df_year = df_raw[df_raw["year"] == year_selected].copy()

    if month_selected != "Todos":
        df_filtered = df_year[df_year["month"] == month_selected].copy()
    else:
        df_filtered = df_year.copy()

    return df_filtered, df_year, month_selected, year_selected
