import streamlit as st
import collections

class AnalisePadroes:
    def __init__(self, historico):
        self.historico = historico[:27]
        self.padroes_ativos = {
            "Sequência (Surf de Cor)": self._sequencia_simples,
            "Zig-Zag": self._zig_zag,
            "Quebra de Surf": self._quebra_de_surf,
            "Quebra de Zig-Zag": self._quebra_de_zig_zag,
            "Duplas repetidas": self._duplas_repetidas,
            "Empate recorrente": self._empate_recorrente,
            "Padrão Escada": self._padrao_escada,
            "Espelho": self._espelho,
            "Alternância com empate no meio": self._alternancia_empate_meio,
            "Padrão 'onda'": self._padrao_onda,
            "Padrões últimos 5/7/10 jogos": self._padroes_ultimos_jogos,
            "Padrão 3x1": self._padrao_3x1,
            "Padrão 3x3": self._padrao_3x3,
            "Padrão 4x4": self._padrao_4x4,
            "Padrão 4x1": self._padrao_4x1,
            "Empate em Zona de Ocorrência": self._empate_zona_ocorrencia
        }

    def analisar_todos(self):
        resultados = {}
        for nome, func in self.padroes_ativos.items():
            try:
                resultados[nome] = func()
            except:
                resultados[nome] = False
        return resultados

    # (Coloque aqui todos os métodos de padrões: _sequencia_simples, _zig_zag, etc.)
    # Se quiser, posso colar todos eles novamente para garantir que estão certos.
    def sugestao_inteligente(self):
        analise = self.analisar_todos()
        pontuacoes = {"C": 0, "V": 0, "E": 0}
        motivos = {"C": [], "V": [], "E": []}
        historico = self.historico

        def pontuar(codigo, pontos, motivo):
            pontuacoes[codigo] += pontos
            motivos[codigo].append(motivo)

        # Quebra de sequência
        if len(historico) >= 5 and historico[0] != historico[1] and all(historico[1] == historico[i] for i in range(1, 5)):
            pontuar(historico[1], 40, "Quebra de 4x1")
        elif len(historico) >= 4 and historico[0] != historico[1] and all(historico[1] == historico[i] for i in range(1, 4)):
            pontuar(historico[1], 35, "Quebra de 3x1")

        if analise.get("Empate em Zona de Ocorrência"):
            pontuar("E", 45 if historico[0] == "E" else 35, "Zona de Empate ativa")

        if len(historico) >= 4 and all(historico[i] == historico[0] for i in range(4)):
            pontuar(historico[0], 30, "Sequência de 4+ detectada")

        # Padrões médios
        if analise.get("Zig-Zag"):
            proxima = "C" if historico[0] == "V" else "V"
            pontuar(proxima, 15, "Padrão Zig-Zag")
        if analise.get("Duplas repetidas"):
            pontuar(historico[0], 20, "Duplas Repetidas")
        if analise.get("Empate recorrente") and historico[0] != "E":
            pontuar("E", 20, "Empate recorrente identificado")
        if analise.get("Padrão 'onda'") and len(historico) >= 4:
            pontuar(historico[1], 15, "Padrão de Onda")
        if analise.get("Padrão Escada"):
            pontuar(historico[0], 20, "Padrão Escada")
        if analise.get("Alternância com empate no meio"):
            proxima = "C" if historico[0] == "V" else "V"
            pontuar(proxima, 15, "Alternância com empate")

        # Blocos e padrões longos
        if analise.get("Padrão 3x1") and historico[1] == historico[2] == historico[3]:
            pontuar(historico[1], 25, "Padrão 3x1")
        if analise.get("Padrão 3x3") and historico[0] == historico[1] == historico[2]:
            pontuar(historico[0], 25, "Padrão 3x3")
        if analise.get("Padrão 4x4") and historico[0] == historico[1] == historico[2] == historico[3]:
            pontuar(historico[0], 25, "Padrão 4x4")
        if analise.get("Padrão 4x1") and historico[0] == historico[1] == historico[2] == historico[3]:
            pontuar(historico[0], 30, "Padrão 4x1")

        if analise.get("Espelho"):
            pontuar(historico[0], 10, "Padrão Espelho")

        # Frequência geral
        freq = self.calcular_frequencias()
        menor_freq = min(freq.values())
        for cor, valor in freq.items():
            if valor == menor_freq:
                pontuar(cor, 10, "Menor frequência recente")

        # Bônus por múltiplos padrões
        for cor in pontuacoes:
            if len(motivos[cor]) >= 2:
                pontuar(cor, 10, "Convergência de padrões")

        # Resultado final
        melhor = max(pontuacoes, key=pontuacoes.get)
        entrada_legivel = {"C": "Casa", "V": "Visitante", "E": "Empate"}[melhor]

        return {
            "sugerir": True,
            "entrada": entrada_legivel,
            "entrada_codigo": melhor,
            "motivos": motivos[melhor],
            "confianca": min(90, pontuacoes[melhor]),
            "frequencias": freq,
            "ultimos_resultados": historico[:3]
        }
# --- CONFIGURAÇÃO DO STREAMLIT ---
st.set_page_config(layout="wide", page_title="Análise de Padrões de Jogos")

# --- INICIALIZAÇÃO DO ESTADO DA SESSÃO ---
if 'historico' not in st.session_state:
    st.session_state.historico = []
    st.session_state.hits = 0
    st.session_state.misses = 0
    st.session_state.last_suggestion_made_code = None
    st.session_state.g1_active = False
    st.session_state.g1_hits = 0
    st.session_state.g1_attempts = 0

# --- FUNÇÕES AUXILIARES ---
def adicionar_resultado(res):
    if st.session_state.last_suggestion_made_code is not None:
        if res == st.session_state.last_suggestion_made_code:
            st.session_state.hits += 1
            if st.session_state.g1_active:
                st.session_state.g1_hits += 1
            st.session_state.g1_active = False
        else:
            st.session_state.misses += 1
            st.session_state.g1_active = True
    st.session_state.historico.insert(0, res)
    st.session_state.historico = st.session_state.historico[:27]
    st.session_state.last_suggestion_made_code = None

def desfazer():
    if st.session_state.historico:
        st.session_state.historico.pop(0)
        st.session_state.last_suggestion_made_code = None

def limpar():
    st.session_state.historico = []
    st.session_state.hits = 0
    st.session_state.misses = 0
    st.session_state.last_suggestion_made_code = None
    st.session_state.g1_active = False
    st.session_state.g1_hits = 0
    st.session_state.g1_attempts = 0

def bolinha_html(codigo):
    cores = {'C': '#FF4B4B', 'V': '#4B4BFF', 'E': '#FFD700'}
    return f"<span style='display:inline-block; width:20px; height:20px; border-radius:50%; background-color:{cores.get(codigo, 'gray')}; margin:2px;'></span>"
# --- TÍTULO E INSERÇÃO DE RESULTADO ---
st.title("⚽ Análise de Padrões de Jogos")
st.subheader("Inserir novo resultado:")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🟥 Casa"):
        adicionar_resultado("C")
with col2:
    if st.button("🟦 Visitante"):
        adicionar_resultado("V")
with col3:
    if st.button("🟨 Empate"):
        adicionar_resultado("E")
with col4:
    if st.button("↩️ Desfazer"):
        desfazer()
with col5:
    if st.button("🧹 Limpar"):
        limpar()

st.markdown("---")

# --- SUGESTÃO E HISTÓRICO IMEDIATO ---
if len(st.session_state.historico) >= 9:
    app = AnalisePadroes(st.session_state.historico)
    sugestao = app.sugestao_inteligente()

    st.subheader("💡 Sugestão inteligente")
    st.success(f"**Sugestão:** {sugestao['entrada']}")
    st.metric("Confiança", f"{sugestao['confianca']}%")
    st.info("Motivos:\n- " + "\n- ".join(sugestao['motivos']))
    st.session_state.last_suggestion_made_code = sugestao['entrada_codigo']
    if st.session_state.g1_active:
        st.session_state.g1_attempts += 1

    # Histórico visual logo abaixo da sugestão
    st.subheader("📌 Últimos resultados (mais recente à esquerda)")
    html_hist = "".join([bolinha_html(x) for x in st.session_state.historico])
    st.markdown(html_hist, unsafe_allow_html=True)
    st.caption(f"Total: {len(st.session_state.historico)} jogos")

    # Padrões detectados
    st.markdown("---")
    st.subheader("🔍 Padrões encontrados")
    resultados = app.analisar_todos()
    colA, colB = st.columns(2)
    with colA:
        st.markdown("**Detectados:**")
        for nome, ativo in resultados.items():
            if ativo:
                st.success(f"✔️ {nome}")
    with colB:
        st.markdown("**Não encontrados:**")
        for nome, ativo in resultados.items():
            if not ativo:
                st.markdown(f"<span style='color: grey;'>✖️ {nome}</span>", unsafe_allow_html=True)

    # Frequência dos resultados
    st.markdown("---")
    st.subheader("📊 Frequência dos resultados")
    st.bar_chart({"Resultado": {
        "Casa": sugestao["frequencias"]['C'],
        "Visitante": sugestao["frequencias"]['V'],
        "Empate": sugestao["frequencias"]['E']
    }})

# --- ESTATÍSTICAS GERAIS ---
st.markdown("---")
st.subheader("📈 Estatísticas de desempenho")
total = st.session_state.hits + st.session_state.misses
taxa = (st.session_state.hits / total * 100) if total else 0
colX, colY, colZ = st.columns(3)
with colX:
    st.metric("✅ Acertos", st.session_state.hits)
    st.metric("Taxa de acerto", f"{taxa:.1f}%" if total else "0%")
with colY:
    st.metric("❌ Erros", st.session_state.misses)
    st.metric("G1", "Ativo" if st.session_state.g1_active else "Inativo")
with colZ:
    st.metric("🎯 G1 Acertos", st.session_state.g1_hits)
    st.metric("G1 Tentativas", st.session_state.g1_attempts)
