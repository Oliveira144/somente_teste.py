
importar streamlit como st
importar aleatório

st.set_page_config(page_title="Analisador de Estúdio de Futebol", layout="centralizado")

# ---------- Função para análise dos 13 padrões ----------
def analisar_padroes(resultados):
    se len(resultados) < 3:
        retornar Nenhum

    recentes = resultados[-10:]
    ultimos3 = resultados[-3:]
    ultimos5 = resultados[-5:]
    ultimos7 = resultados[-7:]

    surf_detectado = Falso
    sequência_atual = 1
    para i no intervalo(len(recentes) - 2, -1, -1):
        if recentes[i] == recentes[-1] e recentes[i] != "Empate":
            sequência_atual += 1
        outro:
            quebrar
    se current_streak >= 3:
        surf_detectado = Verdadeiro

    contagem_em_ziguezague = 0
    para i no intervalo(1, len(ultimos5)):
        if ultimos5[i] != ultimos5[i-1] e ultimos5[i] != "Empate" e ultimos5[i-1] != "Empate":
            contagem_em_ziguezague += 1
    zigzag_detectado = contagem_zigzag >= 3

    duplas_repetidas = False
    se len(recentes) >= 6:
        dupla_count = 0
        para i no intervalo(0, len(recentes) - 1, 2):
            if recentes[i] == recentes[i + 1] e recentes[i] != "Empate":
                contagem_dupla += 1
        duplas_repetidas = dupla_count >= 2

    pos_empates = [i para i, r em enumerate(resultados) se r == "Empate"]
    empate_recorrente = False
    se len(pos_empates) >= 2:
        intervalo = len(resultados) - 1 - pos_empates[-1]
        se 15 <= intervalo <= 35:
            empate_recorrente = True

    padrao_escada = False
    se len(recentes) >= 6:
        grupos = []
        contagem = 1
        atual = recentes[0]
        para i em intervalo(1, len(recentes)):
            if recentes[i] == atual e recentes[i] != "Empate":
                contagem += 1
            outro:
                se atual != "Empate":
                    grupos.append(contagem)
                atual = recentes[i]
                contagem = 1
        se atual != "Empate":
            grupos.append(contagem)
        para i no intervalo(len(grupos) - 2):
            se grupos[i+1] == grupos[i] + 1 e grupos[i+2] == grupos[i] + 2:
                padrao_escada = True
                quebrar

    espelhamento = Falso
    se len(ultimos5) >= 4:
        para i no intervalo(len(ultimos5) - 3):
            seg = ultimos5[i:i+4]
            if seg[0] == seg[3] e seg[1] == seg[2] e seg[0] != seg[1] e seg[0] != "Empate" e seg[1] != "Empate":
                espelhamento = Verdadeiro
                quebrar

    alternancia_empate = False
    se len(ultimos5) >= 3:
        para i no intervalo(len(ultimos5) - 2):
            if ultimos5[i] != "Empate" e ultimos5[i+1] == "Empate" e ultimos5[i+2] != "Empate" e ultimos5[i] != ultimos5[i+2]:
                alternancia_empate = Verdadeiro
                quebrar

    padrao_onda = Falso
    se len(recentes) >= 6:
        grupos = []
        contagem = 1
        atual = recentes[0]
        para i em intervalo(1, len(recentes)):
            if recentes[i] == atual e recentes[i] != "Empate":
                contagem += 1
            outro:
                se atual != "Empate":
                    grupos.append(contagem)
                atual = recentes[i]
                contagem = 1
        se atual != "Empate":
            grupos.append(contagem)
        para i no intervalo(len(grupos) - 3):
            se grupos[i:i+4] == [1,2,1,2]:
                padrao_onda = Verdadeiro
                quebrar

    padrao_3x1 = Falso
    se len(recentes) >= 4:
        para i no intervalo(len(recentes) - 3):
            seg = recentes[i:i+4]
            if seg[0] == seg[1] == seg[2] e seg[2] != seg[3] e seg[0] != "Empate" e seg[3] != "Empate":
                padrao_3x1 = Verdadeiro
                quebrar

    padrao_3x3 = Falso
    se len(recentes) >= 6:
        para i no intervalo(len(recentes) - 5):
            seg = recentes[i:i+6]
            if seg[0] == seg[1] == seg[2] e seg[3] == seg[4] == seg[5] e seg[0] != seg[3] e seg[0] != "Empate" e seg[3] != "Empate":
                padrao_3x3 = Verdadeiro
                quebrar

    empates_fixos = False
    se len(pos_empates) >= 2:
        lacunas = [pos_empates[i] - pos_empates[i - 1] para i no intervalo(1, len(pos_empates))]
        mídia = soma(lacunas) / len(lacunas)
        se 9 <= media <= 10:
            empates_fixos = True

    quebrar_surf = surf_detectado e current_streak >= 4
    quebrar_zigzag = zigzag_detectado and all(r != "Empate" for r in ultimos3)
    quebrar_duplas = duplas_repetidas

    casa = recentes.count("Casa")
    visitante = recentes.count("Visitante")
    empate = recentes.count("Empate")

    entrada = Nenhuma
    confiança = 0
    padrão = ""

    se quebrar_surf:
        entrada = "Visitante" if recentes[-1] == "Casa" else "Casa"
        confiança = 88 + min(sequência_atual * 2, 10)
        padrão = "Quebra de Surf"
    elif empate_recorrente:
        entrada = "Empate"
        confiança = 82
        padrao = "Empate Recorrente"
    elif padrao_3x1:
        entrada = "Visitante" if recentes[-1] == "Casa" else "Casa"
        confiança = 80
        padrão = "Padrão 3x1"
    elif espelhamento:
        entrada = recentes[-2] if recentes[-2] != "Empate" else "Casa"
        confiança = 78
        padrão = "Espectro"
    elif zigzag_detectado:
        entrada = "Visitante" if recentes[-1] == "Casa" else "Casa"
        confiança = 75
        padrao = "Zig-Zag"
    elif alternancia_empate:
        entrada = "Empate"
        confiança = 72
        padrao = "Alternância c/ Empate"
    elif surf_detectado:
        entrada = recentes[-1]
        confianca = 65 + current_streak * 3
        padrao = "Surf Continuado"
    elif duplas_repetidas:
        entrada = recentes[-1]
        confiança = 68
        padrao = "Duplas Repetidas"
    elif padrao_escada:
        entrada = "Visitante" if recentes[-1] == "Casa" else "Casa"
        confiança = 70
        padrão = "Padrão Escada"
    outro:
        se casa > visitante + 2:
            entrada = "Visitante"
            confiança = 60
        elif visitante > casa + 2:
            entrada = "Casa"
            confiança = 60
        elif empate == 0 e len(recentes) >= 8:
            entrada = "Empate"
            confiança = 65
        outro:
            entrada = random.choice(["Casa", "Visitante"])
            confiança = 50
        padrao = "Análise Estatística"

    retornar {
        "entrada": entrada,
        "confianca": min(confianca, 95),
        "padrão": padrão
    }

# ---------- Interface ----------
st.title("₂ Analisador de Estúdio de Futebol")
st.markdown("Análise de padrões com base no histórico de resultados.")

se "historico" não estiver em st.session_state:
    st.session_state.historico = []

col1, col2, col3 = st.columns(3)
com col1:
    se st.button("ðŸ Casa", use_container_width=True):
        st.session_state.historico.append("Casa")
com col2:
    se st.button("ðŸ¤ Empate", use_container_width=True):
        st.session_state.historico.append("Empate")
com col3:
    se st.button("âœˆï¸ Visitante", use_container_width=True):
        st.session_state.historico.append("Visitante")

if st.button("ðŸ” Limpar histórico", use_container_width=True):
    st.session_state.historico.clear()

st.markdown("### Últimos Resultados:")
st.write(" ".join(st.session_state.historico[-20:]))

se st.session_state.historico:
    resultado = analisar_padroes(st.session_state.historico)
    se resultado:
        st.markdown(f"### Sugestão: **{resultado['entrada']}**")
        st.markdown(f"Confiança: **{resultado['confianca']}%**")
        st.markdown(f"Padrão Detectado: _{resultado['padrão']}_")
