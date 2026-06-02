import requests
import streamlit as st


def login_user(email, password):
    try:
        response = requests.post(
            'http://localhost:8000/auth/token', 
            data={"username": email, "password": password}
        )

        if response.status_code == 200:
            return response.json()
    
        return None

    except requests.exceptions.ConnectionError:
        # Se o FastAPI estiver desligado, avisa o usuário em vez de quebrar a tela
        st.error("Não foi possível conectar ao servidor. Verifique se a API está rodando.")
        return None


def create_user(first_name, last_name, username, email, password):
    try:
        response = requests.post(
            'http://localhost:8000/users/', 
            json={
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "email": email,
                "password": password,
            }
        )
    
        return response

    except requests.exceptions.ConnectionError:
        # Se o FastAPI estiver desligado, avisa o usuário em vez de quebrar a tela
        st.error("Não foi possível conectar ao servidor. Verifique se a API está rodando.")
        return None
