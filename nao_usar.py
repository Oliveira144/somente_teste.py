
import streamlit as st
import random
import json
import matplotlib.pyplot as plt

st.set_page_config(page_title="Football Studio Pro Analyzer", layout="wide")

def gerar_carta():
    naipes = ['â™ ', 'â™¥', 'â™¦', 'â™£']
    valores = list(range(2, 15))
    return {"valor": random.choice(valores), "naipe": random.choice(naipes)}

def valor_para_nome(valor):
    nomes = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    return str(valor) if valor < 11 else nomes[valor]

def resultado(c1, c2):
    if c1["valor"] > c2["valor"]:
        return "HOME"
    elif c1["valor"] < c2["valor"]:
        return "AWAY"
    else:
        return "DRAW"

def detectar_padroes(historico):
    padroes = []
    resultados = [x["resultado"] for x in historico]

    if len(resultados) >= 4 and all(resultados[i] != resultados[i+1] for i in range(-4, -1)):
        padroes.append("ðŸ” Zig-Zag detectado")

    seq = resultados[-7:]
    if seq == ['HOME', 'HOME', 'AWAY', 'HOME', 'HOME', 'HOME', 'AWAY']:
        padroes.append("ðŸ”€ PadrÃ£o 2x1x2x1x1x3")

    if len(set(resultados[-5:])) == 1:
        padroes.append(f"ðŸ”¥ Streak de {resultados[-1]}")

    return padroes

def ia_analise(historico):
    if len(historico) < 5:
        return {"sugestao": None, "confianÃ§a": 0, "motivo": "Poucos dados"}

    ultimos = historico[-5:]
    home_score = sum([x["home"]["valor"] for x in ultimos])
    away_score = sum([x["away"]["valor"] for x in ultimos])
    tendencia = "HOME" if home_score > away_score else "AWAY"
    confianca = abs(home_score - away_score) / (5 * 14)

    return {
        "sugestao": tendencia,
        "confianÃ§a": round(confianca * 100, 1),
        "motivo": f"TendÃªncia de cartas altas favorecendo {tendencia}"
    }

if "historico" not in st.session_state:
    st.session_state.historico = []

if "acertos" not in st.session_state:
    st.session_state.acertos = 0
    st.session_state.erros = 0

st.title("ðŸ§  Football Studio Pro Analyzer")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("ðŸŽ® Controle")

    if st.button("ðŸŽ² Nova Rodada AleatÃ³ria"):
        c1 = gerar_carta()
        c2 = gerar_carta()
        res = resultado(c1, c2)
        st.session_state.historico.append({"home": c1, "away": c2, "resultado": res})

    if st.button("ðŸ” Resetar HistÃ³rico"):
        st.session_state.historico = []
        st.session_state.acertos = 0
        st.session_state.erros = 0

    uploaded = st.file_uploader("ðŸ“¥ Importar HistÃ³rico", type=["json"])
    if uploaded:
        data = json.load(uploaded)
        st.session_state.historico = data

    st.download_button("ðŸ“¤ Exportar HistÃ³rico",
                       data=json.dumps(st.session_state.historico),
                       file_name="historico_fsp.json")

    if st.session_state.historico:
        analise = ia_analise(st.session_state.historico)
        st.subheader("ðŸ¤– IA Preditiva")
        st.markdown(f"**SugestÃ£o:** `{analise['sugestao']}`")
        st.markdown(f"**ConfianÃ§a:** `{analise['confianÃ§a']}%`")
        st.caption(f"Motivo: {analise['motivo']}")

        st.subheader("ðŸ§© PadrÃµes Detectados")
        for padrao in detectar_padroes(st.session_state.historico):
            st.success(padrao)

        st.subheader("ðŸ“Š Assertividade")
        st.metric("âœ… Acertos", st.session_state.acertos)
        st.metric("âŒ Erros", st.session_state.erros)

with col2:
    st.header("ðŸ“‹ HistÃ³rico Visual")

    if st.session_state.historico:
        for i, h in enumerate(reversed(st.session_state.historico[-30:])):
            colh1, colh2, colh3 = st.columns([1, 1, 2])
            v_home = valor_para_nome(h["home"]["valor"])
            v_away = valor_para_nome(h["away"]["valor"])
            colh1.markdown(f"**{v_home}{h['home']['naipe']}**")
            colh2.markdown(f"**{v_away}{h['away']['naipe']}**")
            cor = {"HOME": "blue", "AWAY": "red", "DRAW": "gray"}[h["resultado"]]
            colh3.markdown(f"<span style='color:{cor}'>**{h['resultado']}**</span>", unsafe_allow_html=True)

        resultados = [x["resultado"] for x in st.session_state.historico]
        labels = ["HOME", "AWAY", "DRAW"]
        counts = [resultados.count(r) for r in labels]

        fig, ax = plt.subplots()
        ax.bar(labels, counts, color=["blue", "red", "gray"])
        ax.set_title("DistribuiÃ§Ã£o de Resultados")
        st.pyplot(fig)
    else:
        st.info("Nenhum resultado ainda. Gere rodadas para comeÃ§ar.")
