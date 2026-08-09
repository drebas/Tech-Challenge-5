import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(
    page_title="Passos Mágicos - Risco de Defasagem",
    page_icon="🎓",
    layout="centered"
)

# --------------------------------------------------------------------------
# Carregamento do modelo e artefatos
# --------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_MODELO = os.path.join(BASE_DIR, "modelo", "modelo_risco_defasagem.pkl")
CAMINHO_MEDIANAS = os.path.join(BASE_DIR, "modelo", "medianas_features.pkl")
CAMINHO_FEATURES = os.path.join(BASE_DIR, "modelo", "lista_features.pkl")

@st.cache_resource
def carregar_artefatos():
    modelo = joblib.load(CAMINHO_MODELO)
    medianas = joblib.load(CAMINHO_MEDIANAS)
    features = joblib.load(CAMINHO_FEATURES)
    return modelo, medianas, features

modelo, medianas, features_esperadas = carregar_artefatos()

# --------------------------------------------------------------------------
# Cabeçalho
# --------------------------------------------------------------------------
st.title("🎓 Passos Mágicos")
st.subheader("Preditor de Risco de Defasagem")
st.markdown(
    """
    Esta ferramenta estima a **probabilidade de um aluno ficar moderada ou
    severamente defasado (2 ou mais fases abaixo do nível ideal) no próximo
    ano**, com base nos indicadores atuais do PEDE.

    Preencha os campos abaixo com os dados mais recentes do aluno.
    """
)
st.divider()

# --------------------------------------------------------------------------
# Formulário de entrada
# --------------------------------------------------------------------------
with st.form("form_predicao"):
    st.markdown("### Indicadores PEDE (escala 0 a 10)")
    col1, col2 = st.columns(2)

    with col1:
        ian = st.slider("IAN — Adequação de Nível", 0.0, 10.0, 7.5, 0.1)
        ida = st.slider("IDA — Aprendizagem", 0.0, 10.0, 6.5, 0.1)
        ieg = st.slider("IEG — Engajamento", 0.0, 10.0, 7.5, 0.1)
        iaa = st.slider("IAA — Autoavaliação", 0.0, 10.0, 8.0, 0.1)

    with col2:
        ips = st.slider("IPS — Psicossocial", 0.0, 10.0, 6.5, 0.1)
        ipv = st.slider("IPV — Ponto de Virada", 0.0, 10.0, 7.0, 0.1)
        inde = st.slider("INDE — Índice Geral", 0.0, 10.0, 6.8, 0.1)
        defasagem = st.slider("Defasagem atual (Fase - Fase Ideal)", -6, 3, 0, 1)

    st.markdown("### Dados cadastrais e notas")
    col3, col4 = st.columns(2)

    with col3:
        idade = st.number_input("Idade", min_value=6, max_value=30, value=12)
        genero = st.selectbox("Gênero", ["Feminino", "Masculino"])
        fase = st.number_input("Fase atual", min_value=0, max_value=9, value=3)
        tempo_pm = st.number_input("Anos na Passos Mágicos", min_value=0, max_value=15, value=2)

    with col4:
        n_avaliacoes = st.number_input("Número de avaliações no ano", min_value=1, max_value=10, value=4)
        nota_mat = st.slider("Nota Matemática", 0.0, 10.0, 6.0, 0.1)
        nota_por = st.slider("Nota Português", 0.0, 10.0, 6.0, 0.1)

    enviado = st.form_submit_button("Calcular risco", use_container_width=True)

# --------------------------------------------------------------------------
# Predição
# --------------------------------------------------------------------------
if enviado:
    dados_aluno = {
        "IAN": ian,
        "IDA": ida,
        "IEG": ieg,
        "IAA": iaa,
        "IPS": ips,
        "IPV": ipv,
        "INDE": inde,
        "DEFASAGEM": defasagem,
        "IDADE": idade,
        "GENERO_COD": 0 if genero == "Feminino" else 1,
        "FASE": fase,
        "N_AVALIACOES": n_avaliacoes,
        "NOTA_MAT": nota_mat,
        "NOTA_POR": nota_por,
        "TEMPO_NA_PM": tempo_pm,
    }

    linha = pd.Series({f: dados_aluno.get(f, np.nan) for f in features_esperadas})
    linha = linha.fillna(medianas)
    X = pd.DataFrame([linha[features_esperadas].values], columns=features_esperadas)

    probabilidade = modelo.predict_proba(X)[0, 1]
    classe = modelo.predict(X)[0]

    st.divider()
    st.markdown("### Resultado")

    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.metric("Probabilidade de risco", f"{probabilidade:.1%}")

    with col_b:
        if classe == 1:
            st.error(
                f"⚠️ **Risco elevado de defasagem** — recomenda-se acompanhamento "
                f"pedagógico/psicopedagógico prioritário para este aluno."
            )
        elif probabilidade >= 0.3:
            st.warning(
                "🟡 **Risco moderado** — vale monitorar a evolução do aluno nos "
                "próximos indicadores."
            )
        else:
            st.success(
                "✅ **Baixo risco de defasagem** — aluno dentro do esperado "
                "para o perfil atual."
            )

    st.progress(min(float(probabilidade), 1.0))

    with st.expander("Ver dados usados na predição"):
        st.dataframe(pd.DataFrame([dados_aluno]).T.rename(columns={0: "Valor"}))

st.divider()
st.caption(
    "Modelo: Random Forest treinado com dados PEDE 2022-2024 da Associação "
    "Passos Mágicos · Projeto acadêmico FIAP Pós-Tech Data Analytics."
)
