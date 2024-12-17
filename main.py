import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import pandas as pd
from datetime import date

# Definir a base e o engine do SQLAlchemy
engine = create_engine('sqlite:///database.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Definir a classe que representa a tabela de vendas no banco de dados
class Venda(Base):
    __tablename__ = 'venda'
    id = Column(Integer, primary_key=True)
    data = Column(String)
    funcionario = Column(String)
    mercadoria = Column(String)
    quantidade = Column(Integer)

# Criar a tabela no banco de dados, se não existir
Base.metadata.create_all(engine)

# Definindo usuário e senha para autenticação
USER = "Logistica"  # Altere para o seu nome de usuário
PASSWORD = "12345"  # Altere para a sua senha

# Função de autenticação
def check_credentials(username, password):
    return username == USER and password == PASSWORD

# Título do aplicativo
st.title("Meu App Silvério")
st.write("Compras de funcionários!")

# Seção de login
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    username = st.text_input("Usuário:")
    password = st.text_input("Senha:", type='password')

    if st.button("Entrar"):
        if check_credentials(username, password):
            st.session_state['authenticated'] = True
            st.success("Login bem-sucedido!")
            st.balloons()
        else:
            st.error("Nome de usuário ou senha incorretos.")
else:
    # Entradas do usuário
    venda = st.text_input("Mercadoria vendida")
    funcionario = st.text_input("Cliente Funcionario")
    quantidade = st.text_input("Quantidade")

    # Seletor de data
    st.title("Selecione a data:")
    data = st.date_input("Selecione a data:")

    # Mostrar a data selecionada em formato PT-BR
    st.write("Data selecionada:", data.strftime("%d/%m/%Y"))

    # Registrar Funcionário
    if st.button("Registrar Funcionario"):  
        if funcionario:
            st.success(f"Venda registrada para o funcionário: {funcionario}")
        else:
            st.error("Por favor, insira o nome do funcionário.")

    # Registrar Venda
    if st.button("Registrar Venda"):  
        if venda and funcionario and data and quantidade:
            try:
                quantidade_int = int(quantidade)  # Converte a quantidade para inteiro

                # Criar uma nova venda e adicioná-la ao banco de dados
                nova_venda = Venda(
                    data=data.strftime("%d/%m/%Y"),
                    funcionario=funcionario,
                    mercadoria=venda,
                    quantidade=quantidade_int
                )

                # Adicionar a venda à sessão e commitar para o banco de dados
                session.add(nova_venda)
                session.commit()

                st.success(f"Mercadoria vendida registrada: {venda} (Quantidade: {quantidade_int})")
            except ValueError:
                st.error("Por favor, insira uma quantidade válida.")
        else:
            st.error("Por favor, insira a mercadoria vendida, o nome do funcionário, a data e a quantidade.")

    # Exibir vendas registradas
    st.write("Vendas registradas:")
    vendas = session.query(Venda).all()

    # Se houver vendas, processa para exibir no formato de tabela
    if vendas:
        # Criação da lista 'venda_data' com as informações das vendas
        venda_data = [(venda.data, venda.funcionario, venda.mercadoria, venda.quantidade) for venda in vendas]

        # Criar o DataFrame com as vendas
        df_vendas = pd.DataFrame(venda_data, columns=["Data", "Funcionário", "Mercadoria", "Quantidade"])

        # Exibir o DataFrame no Streamlit
        st.dataframe(df_vendas)
    else:
        st.write("Nenhuma venda registrada até o momento.")

    # Botão de logout
    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.success("Você foi desconectado.")
        st.balloons()
        st.write("Para se conectar novamente, clique no botão 'Login' no canto superior")
if __name__ == '__main__':
    os.system("cls") 
    Base.metadata.create_all(engine)
