import streamlit as st
import random
import json

st.set_page_config(page_title="Football Studio Pro Analyzer", layout="wide")

def gerar_carta():
    naipes = ['♠', '♥', '♦', '♣']
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

    # Zig-Zag simples
    if len(resultados) >= 4 and all(resultados[i] != resultados[i+1] for i in range(-4, -1)):
        padroes.append("🔁 Zig-Zag detectado")

    # 2x1x2x1x1x3 (exato)
    seq = resultados[-7:]
    if seq == ['HOME', 'HOME', 'AWAY', 'HOME', 'HOME', 'HOME', 'AWAY']:
        padroes.append("🔀 Padrão 2x1x2x1x1x3")

    # Sequência longa (streak)
    if len(set(resultados[-5:])) == 1:
        padroes.append(f"🔥 Streak de {resultados[-1]}")

    return padroes

def ia_analise(historico):
    if len(historico) < 5:
        return {"sugestao": None, "confiança": 0, "motivo": "Poucos dados"}

    ultimos = historico[-5:]
    home_score = sum([x["home"]["valor"] for x in ultimos])
    away_score = sum([x["away"]["valor"] for x in ultimos])
    tendencia = "HOME" if home_score > away_score else "AWAY"
    confianca = abs(home_score - away_score) / (5 * 14)

    return {
        "sugestao": tendencia,
        "confiança": round(confianca * 100, 1),
        "motivo": f"Tendência de cartas altas favorecendo {tendencia}"
    }

# Estado
if "historico" not in st.session_state:
    st.session_state.historico = []
if "acertos" not in st.session_state:
    st.session_state.acertos = 0
    st.session_state.erros = 0

st.title("🧠 Football Studio Pro Analyzer")

col1, col2 = st.columns([1, 2])

# Painel de Controle
with col1:
    st.header("🎮 Controle")

    if st.button("🎲 Nova Rodada Aleatória"):
        c1 = gerar_carta()
        c2 = gerar_carta()
        res = resultado(c1, c2)
        st.session_state.historico.append({"home": c1, "away": c2, "resultado": res})

    if st.button("🔁 Resetar Histórico"):
        st.session_state.historico = []
        st.session_state.acertos = 0
        st.session_state.erros = 0

    uploaded = st.file_uploader("📥 Importar Histórico", type=["json"])
    if uploaded:
        st.session_state.historico = json.load(uploaded)

    st.download_button(
        "📤 Exportar Histórico",
        data=json.dumps(st.session_state.historico),
        file_name="historico_fsp.json"
    )

    if st.session_state.historico:
        analise = ia_analise(st.session_state.historico)
        st.subheader("🤖 IA Preditiva")
        st.markdown(f"**Sugestão:** `{analise['sugestao']}`")
        st.markdown(f"**Confiança:** `{analise['confiança']}%`")
        st.caption(f"Motivo: {analise['motivo']}")

        st.subheader("🧩 Padrões Detectados")
        for padrao in detectar_padroes(st.session_state.historico):
            st.success(padrao)

        st.subheader("📊 Assertividade")
        st.metric("✅ Acertos", st.session_state.acertos)
        st.metric("❌ Erros", st.session_state.erros)

# Histórico Visual
with col2:
    st.header("📋 Histórico Visual")

    if st.session_state.historico:
        # Exibe últimas 30 rodadas
        for h in reversed(st.session_state.historico[-30:]):
            colh1, colh2, colh3 = st.columns([1, 1, 2])
            v_home = valor_para_nome(h["home"]["valor"])
            v_away = valor_para_nome(h["away"]["valor"])
            colh1.markdown(f"**{v_home}{h['home']['naipe']}**")
            colh2.markdown(f"**{v_away}{h['away']['naipe']}**")
            cor = {"HOME": "blue", "AWAY": "red", "DRAW": "gray"}[h["resultado"]]
            colh3.markdown(
                f"<span style='color:{cor}'>**{h['resultado']}**</span>",
                unsafe_allow_html=True
            )

        # Contagem de resultados
        resultados = [x["resultado"] for x in st.session_state.historico]
        home_count = resultados.count("HOME")
        away_count = resultados.count("AWAY")
        draw_count = resultados.count("DRAW")

        st.subheader("📈 Contagem de Resultados")
        st.write(f"- HOME: {home_count}")
        st.write(f"- AWAY: {away_count}")
        st.write(f"- DRAW: {draw_count}")
    else:
        st.info("Nenhum resultado ainda. Gere rodadas para começar.")
