
# coding: utf-8
import streamlit as st

# InicializaÃ§Ã£o de variÃ¡veis de estado
if "historico" not in st.session_state:
    st.session_state.historico = []
if "acertos" not in st.session_state:
    st.session_state.acertos = 0
if "erros" not in st.session_state:
    st.session_state.erros = 0
if "ultima_sugestao" not in st.session_state:
    st.session_state.ultima_sugestao = None

st.title("ðŸŽ¯ Football Studio Analyzer - Todos os PadrÃµes")

# FunÃ§Ã£o para detectar padrÃµes e sugerir entrada
def analisar_padroes(historico):
    if len(historico) < 5:
        return None, "", 0

    recentes = historico[-10:]
    ultima = recentes[-1]

    # PadrÃ£o: Surf (mesma cor 3x ou mais)
    surf_cor = 1
    for i in range(len(recentes)-2, -1, -1):
        if recentes[i] == ultima and ultima != "Empate":
            surf_cor += 1
        else:
            break
    tem_surf = surf_cor >= 3

    # PadrÃ£o: Zig-Zag
    zigzag = True
    for i in range(2, len(recentes)):
        if recentes[i] == recentes[i-2] or "Empate" in (recentes[i], recentes[i-1], recentes[i-2]):
            zigzag = False
            break

    # PadrÃ£o: Empate recorrente (15 a 35 rodadas)
    empates = [i for i, r in enumerate(historico) if r == "Empate"]
    empate_recorrente = False
    if len(empates) >= 2:
        intervalo = empates[-1] - empates[-2]
        if 15 <= intervalo <= 35:
            empate_recorrente = True

    # PadrÃ£o: 3x1, 4x4
    def match_padroes_blocos(seq, blocos):
        idx = 0
        for bloco in blocos:
            if idx + bloco > len(seq):
                return False
            if len(set(seq[idx:idx+bloco])) != 1:
                return False
            idx += bloco
        return True

    ultimos8 = historico[-8:]
    padrao_4x4 = match_padroes_blocos(ultimos8, [4, 4])
    padrao_3x1 = match_padroes_blocos(historico[-4:], [3, 1])
    padrao_2x1x2x1x1x1x3 = match_padroes_blocos(historico[-11:], [2,1,2,1,1,1,3])

    # Gerar sugestÃ£o
    sugestao = None
    padrao_detectado = ""
    confianca = 50

    if padrao_2x1x2x1x1x1x3:
        padrao_detectado = "2x1x2x1x1x1x3"
        sugestao = "Empate"
        confianca = 95
    elif padrao_4x4:
        padrao_detectado = "4x4"
        sugestao = "Casa" if ultimos8[-1] == "Visitante" else "Visitante"
        confianca = 90
    elif padrao_3x1:
        padrao_detectado = "3x1"
        sugestao = historico[-1]
        confianca = 85
    elif tem_surf:
        padrao_detectado = "Surf de Cor"
        sugestao = ultima
        confianca = 75 + (surf_cor - 3) * 5
    elif zigzag:
        padrao_detectado = "Zig-Zag"
        sugestao = "Visitante" if ultima == "Casa" else "Casa"
        confianca = 70
    elif empate_recorrente:
        padrao_detectado = "Empate Recorrente"
        sugestao = "Empate"
        confianca = 65
    else:
        padrao_detectado = "Sem padrÃ£o forte"
        sugestao = "Casa" if historico.count("Casa") < historico.count("Visitante") else "Visitante"
        confianca = 55

    return sugestao, padrao_detectado, min(confianca, 98)

# BotÃµes
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Casa"):
        st.session_state.historico.append("Casa")
with col2:
    if st.button("Empate"):
        st.session_state.historico.append("Empate")
with col3:
    if st.button("Visitante"):
        st.session_state.historico.append("Visitante")

if st.button("Limpar HistÃ³rico"):
    st.session_state.historico = []
    st.session_state.acertos = 0
    st.session_state.erros = 0
    st.session_state.ultima_sugestao = None

st.subheader("ðŸ“œ HistÃ³rico de Resultados")
st.write(st.session_state.historico)

# AnÃ¡lise e sugestÃ£o
if st.session_state.historico:
    sugestao, padrao, confianca = analisar_padroes(st.session_state.historico)

    st.markdown(f"**SugestÃ£o:** {sugestao}")
    st.markdown(f"**PadrÃ£o Detectado:** {padrao}")
    st.markdown(f"**ConfianÃ§a:** {confianca}%")

    # Conferidor de acerto/erro
    if st.session_state.ultima_sugestao:
        resultado_real = st.session_state.historico[-1]
        if resultado_real == st.session_state.ultima_sugestao:
            st.session_state.acertos += 1
        else:
            st.session_state.erros += 1

    st.session_state.ultima_sugestao = sugestao

    total = st.session_state.acertos + st.session_state.erros
    if total > 0:
        taxa = (st.session_state.acertos / total) * 100
        st.success(f"ðŸŽ¯ Acertos: {st.session_state.acertos} | âŒ Erros: {st.session_state.erros} | âœ… PrecisÃ£o: {taxa:.1f}%")
