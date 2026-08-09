# Datathon Passos Mágicos — FIAP Pós-Tech Data Analytics

Análise de dados e modelo preditivo de risco de defasagem escolar para a
[Associação Passos Mágicos](https://passosmagicos.org.br/), com base nos
dados da Pesquisa Extensiva do Desenvolvimento Educacional (PEDE) de 2022,
2023 e 2024.

## 🎯 Objetivo

A Passos Mágicos atua há 35 anos transformando a vida de crianças e jovens
em vulnerabilidade social através da educação. Este projeto tem dois
objetivos principais:

1. **Storytelling analítico**: responder 11 perguntas de negócio sobre os
   indicadores educacionais dos alunos (IAN, IDA, IEG, IAA, IPS, IPP, IPV,
   INDE) e a efetividade do programa ao longo do tempo.
2. **Modelo preditivo**: estimar a probabilidade de um aluno entrar em
   risco de defasagem escolar no ano seguinte, disponibilizado como
   ferramenta interativa via Streamlit.

## 📁 Estrutura do repositório

```
notebooks/
└── DATATHON-PASSOS-MAGICOS.ipynb   # Limpeza, consolidação dos 3 anos, as 11 perguntas
                                     # e o modelo preditivo (feature engineering,
                                     # treino/teste, modelagem, avaliação)

streamlit_app/
├── app.py                        # Aplicação Streamlit
├── requirements.txt
└── modelo/                       # Artefatos do modelo treinado (.pkl)

apresentacao/
└── storytelling_passos_magicos.pdf  # Apresentação gerencial (PPT/PDF)
```

## 📊 Principais achados

- A proporção de alunos com nível **adequado** (IAN) subiu de **28,7% (2022)
  para 42,0% (2024)**, com queda consistente de defasagem moderada/severa.
- **Engajamento (IEG)** correlaciona fortemente com aprendizagem (IDA,
  r=0,54) e ponto de virada (IPV, r=0,56) — é um dos alavancadores mais
  acionáveis do programa.
- A **autoavaliação dos alunos (IAA)** tem baixa correlação com o
  desempenho real (r≈0,12) — quase metade dos alunos se autoavalia acima
  do desempenho medido.
- Aspectos **psicossociais (IPS)** fracos antecedem quedas de desempenho
  no ano seguinte, embora com efeito modesto.
- A mobilidade de saída do tier mais vulnerável (**Quartzo**) **piorou**
  entre 2022-2023 e 2023-2024, enquanto a retenção no tier mais alto
  (**Topázio**) aumentou.

*(lista completa de achados com gráficos nos notebooks)*

## 🤖 Modelo preditivo

- **Alvo**: probabilidade de o aluno apresentar defasagem moderada/severa
  (2+ fases abaixo do nível ideal) no ano seguinte.
- **Algoritmo**: Random Forest (comparado com Regressão Logística).
- **Performance no conjunto de teste**: AUC-ROC = 0,90, recall = 0,82 para
  a classe de risco.
- **Features**: indicadores PEDE do ano corrente (IAN, IDA, IEG, IAA, IPS,
  IPV, INDE, defasagem atual), dados cadastrais (idade, gênero, fase,
  tempo na instituição) e notas por disciplina.

## 🚀 Aplicação Streamlit

A aplicação permite inserir os indicadores de um aluno e obter a
probabilidade de risco de defasagem em tempo real.

**Link do app**: _(adicionar após o deploy no Streamlit Community Cloud)_

### Rodando localmente

```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

## 🎥 Vídeo de apresentação

_(adicionar link do vídeo, até 5 minutos)_

## 👥 Autores

- _(adicionar nomes do grupo)_

## 📚 Fonte dos dados

Dataset fornecido pela Associação Passos Mágicos para o Datathon FIAP
Pós-Tech (Fase 5), com base nas pesquisas PEDE 2022, 2023 e 2024.
Consulte os [relatórios de atividades](https://passosmagicos.org.br/impacto-e-transparencia/)
da associação para mais contexto sobre a metodologia dos indicadores.
