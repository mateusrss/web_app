import streamlit as st
import pandas as pd

# Definindo usuários e senhas
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

    # Nome do arquivo Excel onde as vendas serão salvas
    nome_arquivo = 'vendas.xlsx'

    # Criar um DataFrame vazio se o arquivo não existir
    try:
        df = pd.read_excel(nome_arquivo)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Data', 'Funcionário', 'Mercadoria', 'Quantidade'])

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
                # Adicionar nova venda ao DataFrame
                nova_venda = pd.DataFrame({
                    'Data': [data.strftime("%d/%m/%Y")],
                    'Funcionário': [funcionario],
                    'Mercadoria': [venda],
                    'Quantidade': [quantidade_int]
                })
                
                df = pd.concat([df, nova_venda], ignore_index=True)
                
                # Salvar o DataFrame atualizado em Excel
                df.to_excel(nome_arquivo, index=False)
                
                st.success(f"Mercadoria vendida registrada: {venda} (Quantidade: {quantidade_int})")
            except ValueError:
                st.error("Por favor, insira uma quantidade válida.")
        else:
            st.error("Por favor, insira a mercadoria vendida, o nome do funcionário, a data e a quantidade.")

    # Exibir vendas registradas
    st.write("Vendas registradas:")
    st.dataframe(df)

    st.write("Você pode usar esse aplicativo para registrar e visualizar as vendas.")

    # Botão de logout
    if st.button("Logout"):
        st.session_state['authenticated'] = False
        st.success("Você foi desconectado.")
        st.balloons()
