import streamlit as st
from sqlalchemy.exc import SQLAlchemyError

from fluxosolo.services.save_df_to_sql import persist_on_db
from fluxosolo.services.verify_database import verify_database

# ---------------------- Popup de confirmação de dados ------------------------


@st.dialog("Revisão do Extrato Bancário")
def popup_data_confirmation(df_new):
    st.success("Extrato processado com sucesso!")
    st.write("Pré-vizualização do upload:", df_new.head())

    qtd_exists = verify_database(df_new)

    if qtd_exists > 0:
        st.warning(
            f"Atenção, já extiste {qtd_exists} transações para este periodo \
                de datas com este banco no seu banco de dados"
        )
        st.write(
            "Se você continuar podera duplicar dados. Deseja prosseguir \
                mesmo assim?"
        )

        if st.button("Sim, salvar duplicado/complementar"):
            persist_on_db(df_new)

            st.session_state["id_uploader"] += 1
            # limpa o cache para atualizar a tabela referente ao banco
            # de dados e em seguida da o rerun na aplicação.
            st.cache_data.clear()
            st.rerun()

    else:
        if st.button("Salvar no banco de dados"):
            try:
                persist_on_db(df_new)

                st.session_state["id_uploader"] += 1
                # limpa o cache para atualizar a tabela referente ao banco
                # de dados e em seguida da o rerun na aplicação.
                st.cache_data.clear()
                st.rerun()

            except ValueError as e:
                st.error(f"Erro ao salvar no banco {e}")
                st.info(
                    "Verifique se o arquivo está no formato correto e tente \
                        novamente."
                )
            except SQLAlchemyError as e:
                st.error(f"Erro no banco de dados: {e}")
