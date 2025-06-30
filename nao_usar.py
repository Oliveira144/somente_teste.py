football_studio_analyzer.py

import streamlit as st import datetime import random import pandas as pd

st.set_page_config(page_title="Football Studio Pro Analyzer", layout="wide") st.title("⚽ Football Studio Pro Analyzer")

if "game_history" not in st.session_state: st.session_state.game_history = [] st.session_state.round = 1 st.session_state.ia_stats = {"total": 0, "hits": 0, "misses": 0, "accuracy": 0, "last_prediction": None} st.session_state.manual_mode = True

Função para adicionar resultado manual ou simulado

def add_result(home_card, away_card): result = "DRAW" if home_card > away_card: result = "HOME" elif away_card > home_card: result = "AWAY"

new_game = {
    "round": st.session_state.round,
    "result": result,
    "home_card": home_card,
    "away_card": away_card,
    "timestamp": datetime.datetime.now()
}

# Verifica previsão anterior
ia = st.session_state.ia_stats
if ia["last_prediction"]:
    hit = ia["last_prediction"] == result
    ia["total"] += 1
    if hit:
        ia["hits"] += 1
    else:
        ia["misses"] += 1
    ia["accuracy"] = round((ia["hits"] / ia["total"]) * 100, 1)

st.session_state.ia_stats["last_prediction"] = generate_recommendation()["recommendation"]

st.session_state.game_history.append(new_game)
st.session_state.round += 1

Estatísticas básicas

def get_statistics(): h = st.session_state.game_history total = len(h) home = len([g for g in h if g["result"] == "HOME"]) away = len([g for g in h if g["result"] == "AWAY"]) draw = len([g for g in h if g["result"] == "DRAW"]) return { "HOME": (home, round(home / total * 100, 1) if total else 0), "AWAY": (away, round(away / total * 100, 1) if total else 0), "DRAW": (draw, round(draw / total * 100, 1) if total else 0) }

Detectar padrões

def detect_patterns(): h = st.session_state.game_history[-20:] results = [g["result"] for g in h] patterns = []

if len(results) >= 3 and results[-1] == results[-2] == results[-3]:
    patterns.append(("Sequência de 3+ resultados", "high"))

if len(results) >= 6:
    alt = all(results[i] != results[i+1] for i in range(5))
    if alt:
        patterns.append(("Alternância detectada", "medium"))

if len(h) >= 7:
    high_cards = [max(g["home_card"], g["away_card"]) for g in h]
    if len([c for c in high_cards if c >= 10]) >= 5:
        patterns.append(("Tendência de cartas altas", "low"))

expected = ["HOME","HOME","AWAY","HOME","HOME","AWAY","HOME","HOME","HOME","AWAY","AWAY","AWAY"]
if results[-12:] == expected:
    patterns.append(("Padrão 2x1x2x1x1x1x3 detectado", "high"))

# Padrão Fibonacci básico (ex: H,A,H,A,H -> 1,1,2,3,5 ou variações)
if len(results) >= 5:
    fib = [1,1,2,3,5,8]
    streaks = []
    count = 1
    for i in range(1, len(results)):
        if results[i] == results[i-1]:
            count += 1
        else:
            streaks.append(count)
            count = 1
    streaks.append(count)
    if streaks[:len(fib)] == fib[:len(streaks)]:
        patterns.append(("Padrão Fibonacci detectado", "medium"))

# Zig-Zag (H,A,H,A,...)
if len(results) >= 6:
    zigzag = True
    for i in range(1, 6):
        if results[-i] == results[-(i+1)]:
            zigzag = False
            break
    if zigzag:
        patterns.append(("Padrão Zig-Zag detectado", "medium"))

return patterns

Recomendação

def generate_recommendation(): h = st.session_state.game_history[-10:] counts = {"HOME": 0, "AWAY": 0, "DRAW": 0} for g in h: counts[g["result"]] += 1

recommendation = "DRAW"
confidence = 50

if counts["HOME"] <= 2:
    recommendation = "HOME"
    confidence = 75
elif counts["AWAY"] <= 2:
    recommendation = "AWAY"
    confidence = 75
elif counts["DRAW"] <= 1:
    recommendation = "DRAW"
    confidence = 80

streak = 1
for i in range(len(h)-2, -1, -1):
    if h[i]["result"] == h[-1]["result"]:
        streak += 1
    else:
        break

if streak >= 4:
    if h[-1]["result"] == "HOME":
        recommendation = random.choice(["AWAY", "DRAW"])
    elif h[-1]["result"] == "AWAY":
        recommendation = random.choice(["HOME", "DRAW"])
    else:
        recommendation = random.choice(["HOME", "AWAY"])
    confidence += 10

return {"recommendation": recommendation, "confidence": min(100, confidence)}

Interface

st.sidebar.title("⚙️ Controles") if st.sidebar.button("🔁 Resetar Histórico"): st.session_state.game_history = [] st.session_state.round = 1 st.session_state.ia_stats = {"total": 0, "hits": 0, "misses": 0, "accuracy": 0, "last_prediction": None}

st.sidebar.toggle("Modo Manual", value=st.session_state.manual_mode, key="manual_mode")

if st.sidebar.button("📤 Exportar Histórico"): df = pd.DataFrame(st.session_state.game_history) csv = df.to_csv(index=False).encode('utf-8') st.download_button("📥 Baixar CSV", csv, "historico.csv", "text/csv")

col1, col2 = st.columns([2, 1]) with col1: st.subheader("🔎 Recomendação da IA") rec = generate_recommendation() st.metric("Sugestão", rec["recommendation"]) st.metric("Confiança", f"{rec['confidence']}%")

st.subheader("📈 Estatísticas")
stats = get_statistics()
for side, (wins, perc) in stats.items():
    st.write(f"{side}: {wins} vitórias ({perc}%)")

st.subheader("📌 Padrões Detectados")
for desc, impact in detect_patterns():
    st.write(f"- {desc} ({impact.upper()})")

with col2: st.subheader("🎯 IA - Precisão") ia = st.session_state.ia_stats st.metric("Total", ia["total"]) st.metric("Acertos", ia["hits"]) st.metric("Erros", ia["misses"]) st.metric("Precisão", f"{ia['accuracy']}%")

st.divider()

if st.session_state.manual_mode: st.subheader("✍️ Inserir Resultado Manual") c1, c2, c3 = st.columns(3) with c1: home_card = st.number_input("Carta HOME (2-14)", min_value=2, max_value=14, step=1) with c2: away_card = st.number_input("Carta AWAY (2-14)", min_value=2, max_value=14, step=1) with c3: if st.button("✅ Adicionar Resultado"): add_result(home_card, away_card) else: st.subheader("🧪 Modo Simulação") c1, c2, c3 = st.columns(3) if c1.button("Simular HOME"): add_result(random.randint(5,14), random.randint(2,10)) if c2.button("Simular AWAY"): add_result(random.randint(2,10), random.randint(5,14)) if c3.button("Simular DRAW"): val = random.randint(2,14) add_result(val, val)

st.divider() st.subheader("📜 Histórico de Resultados") hist = st.session_state.game_history[-54:] rows = [hist[i:i+9] for i in range(0, len(hist), 9)] for row in rows: cols = st.columns(9) for i, g in enumerate(row): with cols[i]: color = {"HOME": "#3b82f6", "AWAY": "#ef4444", "DRAW": "#facc15"}[g["result"]] st.markdown(f"<div style='background:{color};color:black;text-align:center;padding:4px;border-radius:8px;font-weight:bold'>{g['result'][0]}</div>", unsafe_allow_html=True) st.caption(f"{g['home_card']}-{g['away_card']}")

