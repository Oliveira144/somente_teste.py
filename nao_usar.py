import streamlit as st
class AnalisePadroes:
    def __init__(self, resultados):
        self.resultados = resultados[-54:]
        self.resultados_filtrados = [r for r in self.resultados if r in ["Casa", "Empate", "Visitante"]]

    def detectar_padrao(self):
        r = self.resultados_filtrados
        if len(r) < 5:
            return None, 0

        if len(r) >= 4 and all(x == r[-1] for x in r[-4:]):
            return f"Surf de Cor ({r[-1]})", 90

        if len(r) >= 6 and r[-6:] == ["Casa", "Visitante", "Casa", "Visitante", "Casa", "Visitante"]:
            return "Zig-Zag", 85

        if len(r) >= 3 and r[-3] == r[-2] and r[-1] != r[-2]:
            return "Quebra de Surf", 70

        if len(r) >= 6 and all(r[i] == r[i+1] for i in range(-6, -1, 2)):
            return "Duplas repetidas", 68

        empates = [i for i, x in enumerate(r) if x == "Empate"]
        if len(empates) >= 2 and 15 <= (len(r) - empates[-1]) <= 35:
            return "Empate recorrente", 65

        if len(r) >= 6 and r[-6:] == ["Casa", "Visitante", "Visitante", "Casa", "Visitante", "Visitante"]:
            return "Espelho", 65

        if len(r) >= 6 and r[-6:] == ["Casa", "Visitante", "Empate", "Empate", "Casa", "Visitante"]:
            return "AlternÃ¢ncia com empate", 60

        if len(r) >= 7 and r[-7:] == ["Casa", "Visitante", "Casa", "Visitante", "Empate", "Casa", "Visitante"]:
            return "AlternÃ¢ncia com empate no meio", 60

        if len(r) >= 7 and r[-7:] == ["Casa", "Visitante", "Casa", "Visitante", "Casa", "Visitante", "Casa"]:
            return "PadrÃ£o Escada", 67

        if len(r) >= 7 and r[-7:] == ["Casa", "Visitante", "Casa", "Visitante", "Casa", "Visitante", "Visitante"]:
            return "PadrÃ£o Onda", 62

        if len(r) >= 4 and r[-4:] == ["Casa"] * 3 + ["Visitante"]:
            return "PadrÃ£o 3x1", 70
        if len(r) >= 6 and r[-6:] == ["Casa"] * 3 + ["Visitante"] * 3:
            return "PadrÃ£o 3x3", 75
        if len(r) >= 8 and r[-8:] == ["Casa"] * 4 + ["Visitante"] * 4:
            return "PadrÃ£o 4x4", 78
        if len(r) >= 10 and r[-10:] == ["Casa", "Visitante", "Casa", "Visitante", "Empate", "Empate", "Empate", "Empate", "Casa", "Visitante"]:
            return "2x1x2x1x1x1x3", 80

        return "Nenhum padrÃ£o identificado", 50

    def gerar_sugestao(self):
        padrao, confianca = self.detectar_padrao()
        if "Casa" in padrao:
            sugestao = "Visitante"
        elif "Visitante" in padrao:
            sugestao = "Casa"
        elif "Empate" in padrao:
            sugestao = "Empate"
        else:
            sugestao = "Casa" if self.resultados_filtrados.count("Casa") < self.resultados_filtrados.count("Visitante") else "Visitante"
        return sugestao, padrao, confianca

if 'history' not in st.session_state:
    st.session_state.history = []
if 'log_entradas' not in st.session_state:
    st.session_state.log_entradas = []
if 'streak' not in st.session_state:
    st.session_state.streak = {"type": None, "count": 0}
if 'sugestao' not in st.session_state:
    st.session_state.sugestao = None

st.title("âš½ Football Studio Analyzer - Todos os PadrÃµes")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("ðŸ  Casa"):
        resultado = "Casa"
        st.session_state.history.append(resultado)
with col2:
    if st.button("ðŸ¤ Empate"):
        resultado = "Empate"
        st.session_state.history.append(resultado)
with col3:
    if st.button("âœˆï¸ Visitante"):
        resultado = "Visitante"
        st.session_state.history.append(resultado)

if len(st.session_state.history) > 0:
    analise = AnalisePadroes(st.session_state.history)
    sugestao, padrao, confianca = analise.gerar_sugestao()

    if st.session_state.sugestao:
        entrada_anterior = st.session_state.sugestao['sugestao']
        resultado_real = st.session_state.history[-1]
        acertou = entrada_anterior == resultado_real
        st.session_state.log_entradas.append({
            "entrada": entrada_anterior,
            "real": resultado_real,
            "acertou": acertou,
            "padrao": st.session_state.sugestao['padrao']
        })

    st.session_state.sugestao = {
        "sugestao": sugestao,
        "padrao": padrao,
        "confianca": confianca
    }

    if st.session_state.streak['type'] == resultado:
        st.session_state.streak['count'] += 1
    else:
        st.session_state.streak = {'type': resultado, 'count': 1}

if st.session_state.sugestao:
    st.subheader("ðŸŽ¯ SugestÃ£o de Entrada")
    st.markdown(f"**Entrada:** `{st.session_state.sugestao['sugestao']}`")
    st.markdown(f"**PadrÃ£o Detectado:** `{st.session_state.sugestao['padrao']}`")
    st.markdown(f"**ConfianÃ§a:** `{st.session_state.sugestao['confianca']}%`")

st.subheader("ðŸ“Š HistÃ³rico de Resultados")
for r in reversed(st.session_state.history):
    color = "#dc2626" if r == "Casa" else "#3b82f6" if r == "Visitante" else "#6b7280"
    st.markdown(f"<div style='display:inline-block;width:20px;height:20px;border-radius:50%;margin:2px;background:{color}'></div>", unsafe_allow_html=True)

st.subheader("ðŸ“ˆ EstatÃ­sticas")
total = len(st.session_state.history)
if total:
    casa = st.session_state.history.count("Casa")
    empate = st.session_state.history.count("Empate")
    visitante = st.session_state.history.count("Visitante")
    st.write(f"Casa: {casa} ({(casa/total)*100:.1f}%) | Empate: {empate} ({(empate/total)*100:.1f}%) | Visitante: {visitante} ({(visitante/total)*100:.1f}%)")

st.subheader("âœ… ConferÃªncia de Entradas")
acertos = sum(1 for l in st.session_state.log_entradas if l["acertou"])
total_logs = len(st.session_state.log_entradas)
if total_logs:
    st.write(f"Acertos: {acertos} / {total_logs} ({(acertos/total_logs)*100:.1f}%)")
    with st.expander("ðŸ“‹ Ver HistÃ³rico de Entradas"):
        for i, log in enumerate(reversed(st.session_state.log_entradas[-15:])):
            st.write(f"{i+1}. Entrada: `{log['entrada']}` | Resultado: `{log['real']}` â†’ {'âœ…' if log['acertou'] else 'âŒ'} via `{log['padrao']}`")
