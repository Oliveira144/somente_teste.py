import streamlit as st
import collections
import random

# --- CLASSE ANALISEPADROES COM PONTUAÇÃO HÍBRIDA ---
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

    # (aqui entram todos os métodos de padrões: _sequencia_simples até _empate_zona_ocorrencia, sem alterações)
    def sugestao_inteligente(self):
        analise = self.analisar_todos()
        pontuacoes = {"C": 0, "V": 0, "E": 0}
        motivos = {"C": [], "V": [], "E": []}
        historico = self.historico

        def pontuar(codigo, pontos, motivo):
            pontuacoes[codigo] += pontos
            motivos[codigo].append(motivo)

        # --- PADRÕES DE ALTA PRIORIDADE ---
        if len(historico) >= 5 and historico[0] != historico[1] and all(historico[1] == historico[i] for i in range(1, 5)):
            pontuar(historico[1], 40, "Quebra de 4x1: tendência pode retornar")

        elif len(historico) >= 4 and historico[0] != historico[1] and all(historico[1] == historico[i] for i in range(1, 4)):
            pontuar(historico[1], 35, "Quebra de 3x1: cor anterior pode voltar")

        if analise.get("Empate em Zona de Ocorrência"):
            if historico[0] == "E":
                pontuar("E", 45, "Zona de empate ativa com sequência")
            else:
                pontuar("E", 35, "Zona de empate ativa: possível empate próximo")

        # --- CONTINUIDADE ---
        if len(historico) >= 4 and all(historico[i] == historico[0] for i in range(4)):
            pontuar(historico[0], 30, f"Sequência de 4+: favorece continuidade de {historico[0]}")

        # --- PADRÕES MEDIANOS ---
        if analise.get("Zig-Zag"):
            proxima = "C" if historico[0] == "V" else "V"
            pontuar(proxima, 15, "Zig-Zag identificado")

        if analise.get("Duplas repetidas"):
            pontuar(historico[0], 20, "Dupla repetida atual pode continuar")

        if analise.get("Empate recorrente") and historico[0] != "E":
            pontuar("E", 20, "Empates recorrentes próximos")

        if analise.get("Padrão 'onda'") and len(historico) >= 4:
            proxima = historico[1]
            pontuar(proxima, 15, "Padrão Onda detectado")

        if analise.get("Padrão Escada"):
            pontuar(historico[0], 20, "Padrão Escada pode continuar")

        if analise.get("Alternância com empate no meio"):
            proxima = "C" if historico[0] == "V" else "V"
            pontuar(proxima, 15, "Alternância com empate no meio")

        if analise.get("Padrão 3x1"):
            bloco = historico[:4]
            if bloco[0] == bloco[1] == bloco[2] and bloco[3] != bloco[0]:
                pontuar(bloco[0], 25, "Padrão 3x1 detectado")

        if analise.get("Padrão 3x3"):
            bloco = historico[:6]
            if bloco[0] == bloco[1] == bloco[2]:
                pontuar(bloco[0], 25, "Padrão 3x3 identificado")

        if analise.get("Padrão 4x4"):
            bloco = historico[:8]
            if bloco[0] == bloco[1] == bloco[2] == bloco[3]:
                pontuar(bloco[0], 25, "Padrão 4x4 detectado")

        if analise.get("Padrão 4x1"):
            bloco = historico[:5]
            if bloco[0] == bloco[1] == bloco[2] == bloco[3]:
                pontuar(bloco[0], 30, "Padrão 4x1 ativo")

        if analise.get("Espelho"):
            pontuar(historico[0], 10, "Padrão Espelho identificado")

        # --- PADRÃO DE MENOR FREQUÊNCIA ---
        freq = self.calcular_frequencias()
        menor_freq_valor = min(freq.values())
        for cor, valor in freq.items():
            if valor == menor_freq_valor:
                pontuar(cor, 10, "Menor frequência recente")

        # --- BÔNUS POR PADRÕES COINCIDENTES ---
        for cor in pontuacoes:
            if len(motivos[cor]) >= 2:
                pontuar(cor, 10, "Bônus por múltiplos padrões")

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
# --- CONFIGURAÇÃO STREAMLIT E ESTADO ---
st.set_page_config(layout="wide", page_title="⚽ Análise de Padrões")

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

def limpar():
    st.session_state.historico.clear()
    st.session_state.hits = 0
    st.session_state.misses = 0
    st.session_state.last_suggestion_made_code = None
    st.session_state.g1_active = False
    st.session_state.g1_hits = 0
    st.session_state.g1_attempts = 0

def desfazer():
    if st.session_state.historico:
        st.session_state.historico.pop(0)
        st.session_state.last_suggestion_made_code = None

def bolinha(cor):
    cores = {'C': '#FF4B4B', 'V': '#4B4BFF', 'E': '#FFD700'}
    return f"<span style='display:inline-block; width:20px; height:20px; border-radius:50%; background-color:{cores.get(cor, 'gray')}; margin:2px;'></span>"
# --- CSS PARA BOTÕES ---
st.markdown("""
<style>
div.stButton > button:first-child {
    font-size: 17px; padding: 10px 20px;
    border-radius: 5px; margin: 5px; border: none; color: white;
}
div.stButton > button[data-testid="stButton-Casa"] {
    background-color: #FF4B4B;
}
div.stButton > button[data-testid="stButton-Visitante"] {
    background-color: #4B4BFF;
}
div.stButton > button[data-testid="stButton-Empate"] {
    background-color: #FFD700; color: black;
}
div.stButton > button[data-testid*="Desfazer"],
div.stButton > button[data-testid*="Limpar"] {
    background-color: #E0E0E0; color: black;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("⚽ Análise de Padrões de Jogos")
st.subheader("Insira o resultado mais recente:")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🏠 Casa", key="Casa"):
        adicionar_resultado('C')
with col2:
    if st.button("🚌 Visitante", key="Visitante"):
        adicionar_resultado('V')
with col3:
    if st.button("⚖️ Empate", key="Empate"):
        adicionar_resultado('E')
with col4:
    if st.button("↩️ Desfazer", key="Desfazer"):
        desfazer()
with col5:
    if st.button("🧹 Limpar Histórico", key="Limpar"):
        limpar()

st.markdown("---")

# --- ANÁLISE ---
if len(st.session_state.historico) >= 9:
    app = AnalisePadroes(st.session_state.historico)
    sugestao = app.sugestao_inteligente()

    st.subheader("💡 Sugestão para o próximo jogo")
    if sugestao['sugerir']:
        st.success(f"Sugestão: **{sugestao['entrada']}**")
        st.metric("Confiança", f"{sugestao['confianca']}%")
        st.info("Motivos:\n- " + "\n- ".join(sugestao['motivos']))
        st.session_state.last_suggestion_made_code = sugestao['entrada_codigo']
        if st.session_state.g1_active:
            st.session_state.g1_attempts += 1
    else:
        st.warning("Sem sugestão clara no momento.")

    # Padrões detectados
    st.markdown("---")
    st.subheader("🔍 Padrões identificados")
    resultados = app.analisar_todos()
    colA, colB = st.columns(2)
    with colA:
        st.markdown("**Detectados:**")
        for k, v in resultados.items():
            if v: st.success(f"✔️ {k}")
    with colB:
        st.markdown("**Não encontrados:**")
        for k, v in resultados.items():
            if not v: st.markdown(f"<span style='color:grey;'>✖️ {k}</span>", unsafe_allow_html=True)

    # Frequência
    st.markdown("---")
    st.subheader("📊 Frequência no histórico")
    freq = sugestao['frequencias']
    st.bar_chart({"Resultado": {"Casa": freq['C'], "Visitante": freq['V'], "Empate": freq['E']}})

# Histórico visual
st.markdown("---")
st.subheader("📌 Histórico (mais recente à esquerda)")
if not st.session_state.historico:
    st.info("Histórico vazio. Comece registrando resultados.")
else:
    html_hist = "".join([bolinha(x) for x in st.session_state.historico])
    st.markdown(html_hist, unsafe_allow_html=True)
    st.caption(f"Total: {len(st.session_state.historico)} jogos")

# Estatísticas
st.markdown("---")
st.subheader("📈 Estatísticas de acertos")
totais = st.session_state.hits + st.session_state.misses
taxa = (st.session_state.hits / totais * 100) if totais else 0
colA, colB, colC = st.columns(3)
with colA:
    st.metric("✅ Acertos", st.session_state.hits)
    st.metric("Taxa de acerto", f"{taxa:.1f}%" if totais else "0%")
with colB:
    st.metric("❌ Erros", st.session_state.misses)
    st.metric("Status G1", "Ativo" if st.session_state.g1_active else "Inativo")
with colC:
    st.metric("🎯 G1 Acertos", st.session_state.g1_hits)
    st.metric("Tentativas G1", st.session_state.g1_attempts)
