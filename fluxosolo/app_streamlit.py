import streamlit as st
import time

from fluxosolo.utils.api import login_user, create_user

st.set_page_config(page_title='FluxoSolo - Login')

tab_login, tab_create = st.tabs(["Entrar", "Criar Conta"])

with tab_login:
    with st.form(key='login_form'):
        email = st.text_input('E-mail')
        password = st.text_input('Senha', type='password')
        submit_button = st.form_submit_button(label='Entrar')

    if submit_button:
        if not email or not password:
            st.warning('Preencha todos os campos')
        
        else:
            with st.spinner('Autenticando...'):
                time.sleep(1)

                form_login = login_user(email, password)


                if form_login:
                    st.session_state['logado'] = True
                    st.session_state['token'] = form_login['access_token']
                    st.session_state['user_id'] = form_login['user_id']

                    st.success('Login realizado com sucesso!')
                    time.sleep(0.5)
                
                    st.switch_page('pages/dashboard.py')
                else:
                    st.error('email ou senha incorretos')


with tab_create:
    with st.form(key='register_form'):
        first_name = st.text_input('Nome', key='reg_first_name')
        last_name = st.text_input('Sobrenome', key='reg_last_name')
        new_username = st.text_input('Username', key='reg_username')
        new_email = st.text_input('E-mail', key="reg_email")
        new_password = st.text_input('Senha', type='password', key="reg_senha")
        confirm_password = st.text_input(
            'Confirmar Senha', type='password', key="reg_conf_senha"
        )
        
        submit_cadastro = st.form_submit_button(label='Cadastrar')

    if submit_cadastro:
        if not new_email or not new_password or not confirm_password or not first_name or not last_name or not new_username:
            st.warning("Preencha todos os campos.")
        elif new_password != confirm_password:
            st.error("As senhas não coincidem!")
        else:
            with st.spinner("Criando usuário..."):
                resposta_api = create_user(
                    first_name,
                    last_name,
                    new_username,
                    new_email,
                    new_password
                )
                
                if resposta_api and resposta_api.status_code in [200, 201]:
                    st.success("Conta criada com sucesso! Vá para a aba 'Entrar' para fazer o login.")
                    # st.balloons() # Opcional: efeito visual de sucesso
                
                elif resposta_api and resposta_api.status_code == 400:
                    erro = resposta_api.json().get("detail", "Erro ao criar conta.")
                    st.error(erro)

                elif resposta_api and resposta_api.status_code == 409:
                    erro = resposta_api.json().get("detail", "E-mail ou username já existem.")
                    st.error(erro)
                
                else:
                    # st.error("Ocorreu um erro no servidor. Tente novamente mais tarde.")  
                    st.error(f"Código: {resposta_api.status_code}")
                    st.json(resposta_api.json())
