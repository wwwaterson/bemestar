# Este código requer o módulo Streamlit instalado.
# Para rodar, certifique-se de executar:
# pip install streamlit pandas

import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Nome do arquivo CSV para salvar os dados
CSV_FILE = "registro_bem_estar.csv"

# Função para carregar dados existentes
def carregar_dados():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=[
            "Data", "Nome", "Sono", "Dor Muscular", "Energia", "Humor",
            "Hidratacao", "Alimentacao", "Treinou", "Observacoes"])

# Função para salvar novo registro
def salvar_dados(novo_registro):
    df = carregar_dados()
    df = pd.concat([df, pd.DataFrame([novo_registro])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

# Interface Streamlit
st.set_page_config(page_title="Bem-Estar", layout="centered")
st.markdown("""
    <style>
        .main {
            background-color: #e6f0ff;
        }
        h1, .stButton>button {
            color: #003366;
        }
        .stSlider>div>div>div>div {
            background: #3399ff !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("\U0001F535 Controle Diário de Bem-Estar")

# Formulário de entrada
enviar = False
with st.form("formulario_bem_estar"):
    nome = st.text_input("Nome do atleta")
    sono = st.slider("Qualidade do sono (1 = ruim / 5 = ótimo)", 1, 5, 3)
    dor = st.slider("Nível de dor muscular (0 = nenhuma / 5 = intensa)", 0, 5, 0)
    energia = st.slider("Nível de energia (1 = sem energia / 5 = cheio de energia)", 1, 5, 3)
    humor = st.slider("Humor/ânimo (1 = ruim / 5 = ótimo)", 1, 5, 3)
    hidratacao = st.slider("Hidratação (1 = ruim / 5 = excelente)", 1, 5, 3)
    alimentacao = st.slider("Alimentação (1 = ruim / 5 = excelente)", 1, 5, 3)
    treinou = st.radio("Treinou/jogou hoje?", ["Sim", "Não"])
    observacoes = st.text_area("Observações")
    enviar = st.form_submit_button("Salvar Registro")

# Salvando os dados se enviado
if enviar and nome.strip() != "":
    registro = {
        "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Nome": nome.strip(),
        "Sono": sono,
        "Dor Muscular": dor,
        "Energia": energia,
        "Humor": humor,
        "Hidratacao": hidratacao,
        "Alimentacao": alimentacao,
        "Treinou": treinou,
        "Observacoes": observacoes.strip()
    }
    salvar_dados(registro)
    st.success("Registro salvo com sucesso!")

# Carregar e exibir dados anteriores
df = carregar_dados()
if not df.empty:
    st.subheader("\U0001F4CA Histórico de Registros")
    st.dataframe(df.sort_values("Data", ascending=False))

    # Gráfico de médias dos últimos 7 dias
    st.subheader("\U0001F4C8 Média de Indicadores (últimos 7 dias)")
    df['Data'] = pd.to_datetime(df['Data'])
    ultimos_dias = df[df['Data'] >= pd.Timestamp.now() - pd.Timedelta(days=7)]
    if not ultimos_dias.empty:
        medias = ultimos_dias[[
            "Sono", "Dor Muscular", "Energia", "Humor", "Hidratacao", "Alimentacao"]].mean()
        st.bar_chart(medias)
    else:
        st.info("Ainda não há dados suficientes dos últimos 7 dias.")
else:
    st.info("Nenhum dado registrado ainda. Preencha o formulário acima para começar.")
