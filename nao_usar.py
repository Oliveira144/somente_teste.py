import streamlit as st import random from statistics import mean

Classe analisadora

class FootballStudioAnalyzer: def init(self): self.history = [] self.suggestion = None self.confidence = 0 self.streak = {'type': None, 'count': 0}

def add_result(self, result):
    self.history.append(result)
    self.update_streak()
    analysis = self.analyze_patterns(self.history)
    if analysis:
        self.suggestion = analysis
        self.confidence = analysis['confidence']

def clear_history(self):
    self.history = []
    self.suggestion = None
    self.confidence = 0
    self.streak = {'type': None, 'count': 0}

def update_streak(self):
    if self.history:
        last_result = self.history[-1]
        if self.streak['type'] == last_result:
            self.streak['count'] += 1
        else:
            self.streak = {'type': last_result, 'count': 1}

def analyze_patterns(self, results):
    # (Função anterior completa - mantida para análise dos 13 padrões)
    # ... código omitido para brevidade, já está incluído na célula anterior ...
    pass

--- Início da Interface Streamlit ---

analyzer = FootballStudioAnalyzer()

st.set_page_config(page_title="Football Studio Pro", layout="wide") st.markdown(""" <style> .main { background: linear-gradient(to bottom right, #1a202c, #4c1d95); color: white; } </style> """, unsafe_allow_html=True)

st.title("⚽ Football Studio Pro") st.markdown("Análise Inteligente de Padrões - Evolution Gaming")

col1, col2, col3 = st.columns(3) if col1.button("🏠 CASA"): analyzer.add_result('Casa') if col2.button("🤝 EMPATE"): analyzer.add_result('Empate') if col3.button("✈️ VISITANTE"): analyzer.add_result('Visitante')

st.divider()

Sugestão principal

if analyzer.suggestion: entry = analyzer.suggestion['entry'] conf = analyzer.suggestion['confidence'] pattern = analyzer.suggestion['mainPattern']

st.subheader("🎯 Próxima Entrada")
color = 'red' if entry == 'Casa' else 'blue' if entry == 'Visitante' else 'gray'
emoji = '🏠' if entry == 'Casa' else '✈️' if entry == 'Visitante' else '🤝'
st.markdown(f"### <div style='background-color:{color};padding:20px;border-radius:10px;color:white;text-align:center'>{emoji} Apostar em {entry.upper()}</div>", unsafe_allow_html=True)
st.markdown(f"**Confiança:** `{conf}%` | **Padrão:** `{pattern}`")

with st.expander("📊 Padrões Detected"):
    for key, value in analyzer.suggestion['patterns'].items():
        if value and key != 'surfStreak':
            st.markdown(f"✔️ **{key.replace('_', ' ').capitalize()}**")
    if analyzer.suggestion['patterns'].get('surfStreak', 0) >= 3:
        st.markdown(f"🌊 **Surf de cor ({analyzer.suggestion['patterns']['surfStreak']}x)**")

st.divider()

Histórico visual

st.subheader(f"🕓 Últimos Resultados ({len(analyzer.history)})") colh1, colh2 = st.columns([5, 1]) with colh1: st.markdown("""<div style='display:flex;flex-wrap:wrap;gap:5px'>""", unsafe_allow_html=True) for result in reversed(analyzer.history): bg = '#dc2626' if result == 'Casa' else '#2563eb' if result == 'Visitante' else '#4b5563' txt = 'C' if result == 'Casa' else 'V' if result == 'Visitante' else 'E' st.markdown(f""" <div style='width:32px;height:32px;border-radius:50%;background-color:{bg};color:white;display:flex;align-items:center;justify-content:center;font-weight:bold'> {txt} </div> """, unsafe_allow_html=True) st.markdown("</div>", unsafe_allow_html=True) with colh2: if st.button("🗑️ Limpar Histórico"): analyzer.clear_history() st.experimental_rerun()

Estatísticas

if analyzer.history: st.subheader("📈 Estatísticas") casa = analyzer.history.count('Casa') visitante = analyzer.history.count('Visitante') empate = analyzer.history.count('Empate') total = len(analyzer.history) colc1, colc2, colc3 = st.columns(3) colc1.metric("🏠 Casa", f"{casa} ({(casa/total100):.1f}%)") colc2.metric("🤝 Empate", f"{empate} ({(empate/total100):.1f}%)") colc3.metric("✈️ Visitante", f"{visitante} ({(visitante/total*100):.1f}%)")

Streak

if analyzer.streak['count'] >= 2: streak = analyzer.streak warn = "⚠️ Possível Quebra" if streak['count'] >= 3 and streak['type'] != 'Empate' else "" st.markdown(f"### 🔁 Streak Atual: {streak['count']}x {streak['type']} {warn}")

Disclaimer

st.markdown("""

<div style='background-color:#2d2d2d;padding:10px;border-radius:10px;color:gray;text-align:center;margin-top:40px'>
⚠️ Este aplicativo é apenas para fins educacionais e de entretenimento.<br>
Apostas envolvem riscos. Jogue com responsabilidade.
</div>
""", unsafe_allow_html=True)
