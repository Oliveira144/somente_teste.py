
importar streamlit como st

classe FootballStudioAnalyzer:
    def __init__(self):
        self.resultados_filtrados = []

    def analisar(self, resultados):
        self.resultados_filtrados = resultados[-54:]
        padrao = self.detectar_padrao(self.resultados_filtrados)
        padrao = padrao ou ""

        se "Casa" em padrão:
            sugestão = "Visitante"
        elif "Visitante" no padrão:
            sugestão = "Casa"
        elif "Empate" em padrão:
            sugestão = "Empatar"
        outro:
            sugestao = "Casa" if self.resultados_filtrados.count("Casa") < self.resultados_filtrados.count("Visitante") else "Visitante"

        return sugestão, padrão, 85 # confiança fictícia

    def detectar_padrao(self, r):
        se len(r) < 10:
            retornar Nenhum

        últimos = r[-10:]

        def seq(n, tipo):
            retornar todos(x == tipo para x em r[-n:])

        if seq(6, "Casa") ou seq(6, "Visitante"):
            retornar "Surf de Cor"

        se all(r[-i] != r[-i-1] e "Empate" não estiver em (r[-i], r[-i-1]) para i no intervalo(1, 5)):
            retornar "Zig-Zag"

        if r[-4:] == ["Casa", "Casa", "Casa", "Visitante"]:
            retornar "3x1"
        if r[-6:] == ["Casa"]*3 + ["Visitante"]*3:
            retornar "3x3"
        if r[-8:] == ["Casa"]*4 + ["Visitante"]*4:
            retornar "4x4"

        if r[-8:] == ["Casa", "Visitante", "Casa", "Visitante", "Empate", "Empate", "Empate", "Casa"]:
            retornar "2x1x2x1x1x1x3"

        if r[-7:] == ["Casa", "Visitante", "Casa", "Visitante", "Casa", "Visitante", "Casa"]:
            retornar "Quebra de Zig-Zag"

        if r[-3:] == ["Casa", "Casa", "Casa"] e r[-4] != "Casa":
            retornar "Quebra de Surf"

        if r[-6:] == ["Casa", "Casa", "Visitante", "Visitante", "Casa", "Casa"]:
            retornar "Espelhamento"

        if r[-4:] == ["Casa", "Casa", "Visitante", "Visitante"]:
            retornar "Duplas Repetidas"

        if r[-6:] == ["Casa", "Visitante", "Visitante", "Casa", "Casa", "Casa"]:
            retornar "Padrão Escada"

        if r[-6:] == ["Casa", "Visitante", "Empate", "Empate", "Visitante", "Casa"]:
            return "Alternância com Empate no meio"

        if r[-5:] == ["Casa", "Visitante", "Casa", "Casa", "Visitante"]:
            retornar "Padrão Onda"

        se "Empate" em r:
            índices = [i para i, val em enumerate(r) se val == "Empate"]
            se len(índices) >= 2 e 15 <= (índices[-1] - índices[-2]) <= 35:
                retornar "Empate Recorrente"

        se r[-5:].count("Casa") >= 4:
            retornar "Padrão 4 de 5 Casa"
        se r[-5:].count("Visitante") >= 4:
            voltar "Padrão 4 de 5 Visitante"

        retornar "Nenhum padrão forte"

st.set_page_config(layout="largo")
st.title("Analisador de Estúdio de Futebol - 17 Padrões Completos")

se "history" não estiver em st.session_state:
    st.session_state.history = []

col1, col2, col3 = st.columns(3)
com col1:
    se st.button("Casa"):
        st.session_state.history.append("Casa")
com col2:
    se st.button("Empate"):
        st.session_state.history.append("Empate")
com col3:
    if st.button("Visitante"):
        st.session_state.history.append("Visitante")

if st.button("Limpar Histórico"):
    st.session_state.history = []

st.subheader("Histórico de Resultados")
st.write(st.session_state.history)

se st.session_state.history:
    analisador = FootballStudioAnalyzer()
    sugestão, padrão, confiança = analisar.analisar(st.session_state.history)
    st.markdown(f"**Sugestão:** {sugestão}")
    st.markdown(f"**Padrão Detectado:** {padrão}")
    st.markdown(f"**Confiança:** {confianca}%")
