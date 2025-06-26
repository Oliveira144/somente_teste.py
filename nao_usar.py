import streamlit as st
class FootballStudioAnalyzer:
    def __init__(self):
        self.filtered_results = []

    def analyze(self, results):
        self.filtered_results = results[-54:]
        pattern = self.detect_pattern(self.filtered_results) or ""

        if "Casa" in pattern:
            suggestion = "Visitante"
        elif "Visitante" in pattern:
            suggestion = "Casa"
        elif "Empate" in pattern:
            suggestion = "Empate"
        else:
            suggestion = "Casa" if self.filtered_results.count("Casa") < self.filtered_results.count("Visitante") else "Visitante"

        return suggestion, pattern, 85

    def detect_pattern(self, r):
        if len(r) < 10:
            return None

        def seq(n, tipo):
            return all(x == tipo for x in r[-n:])

        if seq(6, "Casa") or seq(6, "Visitante"):
            return "Surf de Cor"

        if all(r[-i] != r[-i-1] and "Empate" not in (r[-i], r[-i-1]) for i in range(1, 5)):
            return "Zig-Zag"

        if r[-4:] == ["Casa", "Casa", "Casa", "Visitante"]:
            return "3x1"
        if r[-6:] == ["Casa"]*3 + ["Visitante"]*3:
            return "3x3"
        if r[-8:] == ["Casa"]*4 + ["Visitante"]*4:
            return "4x4"

        if r[-8:] == ["Casa", "Visitante", "Casa", "Visitante", "Empate", "Empate", "Empate", "Casa"]:
            return "2x1x2x1x1x1x3"

        if r[-7:] == ["Casa", "Visitante", "Casa", "Visitante", "Casa", "Visitante", "Casa"]:
            return "Quebra de Zig-Zag"

        if r[-3:] == ["Casa", "Casa", "Casa"] and r[-4] != "Casa":
            return "Quebra de Surf"

        if r[-6:] == ["Casa", "Casa", "Visitante", "Visitante", "Casa", "Casa"]:
            return "Espelhamento"

        if r[-4:] == ["Casa", "Casa", "Visitante", "Visitante"]:
            return "Duplas Repetidas"

        if r[-6:] == ["Casa", "Visitante", "Visitante", "Casa", "Casa", "Casa"]:
            return "PadrÃ£o Escada"

        if r[-6:] == ["Casa", "Visitante", "Empate", "Empate", "Visitante", "Casa"]:
            return "AlternÃ¢ncia com Empate no meio"

        if r[-5:] == ["Casa", "Visitante", "Casa", "Casa", "Visitante"]:
            return "PadrÃ£o Onda"

        if "Empate" in r:
            indices = [i for i, val in enumerate(r) if val == "Empate"]
            if len(indices) >= 2 and 15 <= (indices[-1] - indices[-2]) <= 35:
                return "Empate Recorrente"

        if r[-5:].count("Casa") >= 4:
            return "PadrÃ£o 4 de 5 Casa"
        if r[-5:].count("Visitante") >= 4:
            return "PadrÃ£o 4 de 5 Visitante"

        return "Nenhum padrÃ£o forte"

st.set_page_config(layout="wide")
st.title("Football Studio Analyzer - Corrigido e Revisado")

if "history" not in st.session_state:
    st.session_state.history = []

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Casa"):
        st.session_state.history.append("Casa")
with col2:
    if st.button("Empate"):
        st.session_state.history.append("Empate")
with col3:
    if st.button("Visitante"):
        st.session_state.history.append("Visitante")

if st.button("Limpar HistÃ³rico"):
    st.session_state.history = []

st.subheader("HistÃ³rico de Resultados")
st.write(st.session_state.history)

if st.session_state.history:
    analyzer = FootballStudioAnalyzer()
    suggestion, pattern, confidence = analyzer.analyze(st.session_state.history)
    st.markdown(f"**SugestÃ£o:** {suggestion}")
    st.markdown(f"**PadrÃ£o Detectado:** {pattern}")
    st.markdown(f"**ConfianÃ§a:** {confidence}%")
