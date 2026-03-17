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

    if extract is not None:
        df_new = read_extract_file(extract)

        if df_new is not None and st.sidebar.button("Revisar e Salvar"):
            popup_data_confirmation(df_new)


def filter_sidebar(month_list, df_raw):
    st.sidebar.header("Filtros")

    month_year_selected = st.sidebar.selectbox(
        "Selecione o mês/ano", month_list
    )   

    if month_year_selected != "Todos":
        # month_clean = str(month_year_selected).strip()

        df_filtered = df_raw[
            df_raw["month_year"] == month_year_selected
        ].copy()
    else:
        df_filtered = df_raw.copy()

    return df_filtered, month_year_selected
