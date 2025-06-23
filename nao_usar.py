import streamlit as st
import collections
import random

# --- CLASSE DE ANÁLISE DE PADRÕES ---
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
            except Exception:
                resultados[nome] = False
        return resultados

    def _sequencia_simples(self):
        for i in range(len(self.historico) - 2):
            if self.historico[i] == self.historico[i+1] == self.historico[i+2]:
                return True
        return False

    def _zig_zag(self):
        if len(self.historico) < 4:
            return False
        for i in range(len(self.historico) - 1):
            if self.historico[i] == self.historico[i+1]:
                return False
        return True

    def _quebra_de_surf(self):
        for i in range(len(self.historico) - 3):
            if self.historico[i] == self.historico[i+1] == self.historico[i+2] and self.historico[i+2] != self.historico[i+3]:
                return True
        return False

    def _quebra_de_zig_zag(self):
        if len(self.historico) < 5:
            return False
        for i in range(len(self.historico) - 4):
            if self.historico[i] != self.historico[i+1] and self.historico[i+1] != self.historico[i+2] and self.historico[i+2] == self.historico[i+3]:
                return True
        return False

    def _duplas_repetidas(self):
        if len(self.historico) < 4:
            return False
        for i in range(len(self.historico) - 3):
            if self.historico[i] == self.historico[i+1] and self.historico[i+2] == self.historico[i+3] and self.historico[i] != self.historico[i+2]:
                return True
        return False

    def _empate_recorrente(self):
        empates = [i for i, r in enumerate(self.historico) if r == 'E']
        if len(empates) < 2:
            return False
        for i in range(len(empates) - 1):
            if 2 <= (empates[i+1] - empates[i]) <= 4:
                return True
        return False

    def _padrao_escada(self):
        if len(self.historico) < 6:
            return False
        for i in range(len(self.historico) - 5):
            if self.historico[i] != self.historico[i+1] and \
               self.historico[i+1] == self.historico[i+2] and \
               self.historico[i+3] == self.historico[i+4] == self.historico[i+5] and \
               self.historico[i+1] != self.historico[i+3]:
                return True
        return False

    def _espelho(self):
        if len(self.historico) < 2:
            return False
        metade = len(self.historico) // 2
        return self.historico[:metade] == self.historico[-metade:][::-1]

    def _alternancia_empate_meio(self):
        for i in range(len(self.historico) - 2):
            if self.historico[i] != 'E' and self.historico[i+1] == 'E' and self.historico[i+2] != 'E' and self.historico[i] != self.historico[i+2]:
                return True
        return False

    def _padrao_onda(self):
        if len(self.historico) < 4:
            return False
        for i in range(len(self.historico) - 3):
            if self.historico[i] == self.historico[i+2] and self.historico[i+1] == self.historico[i+3] and self.historico[i] != self.historico[i+1]:
                return True
        return False

    def _padroes_ultimos_jogos(self):
        if len(self.historico) < 5:
            return False
        ultimos = self.historico[:5]
        cont = collections.Counter(ultimos)
        return any(v / 5 >= 0.6 for v in cont.values())

    def _padrao_3x1(self):
        for i in range(len(self.historico) - 3):
            bloco = self.historico[i:i+4]
            if bloco[0] == bloco[1] == bloco[2] and bloco[3] != bloco[0]:
                return True
        return False

    def _padrao_3x3(self):
        for i in range(len(self.historico) - 5):
            bloco = self.historico[i:i+6]
            if bloco[0] == bloco[1] == bloco[2] and bloco[3] == bloco[4] == bloco[5] and bloco[0] != bloco[3]:
                return True
        return False

    def _padrao_4x4(self):
        for i in range(len(self.historico) - 7):
            bloco = self.historico[i:i+8]
            if bloco[0] == bloco[1] == bloco[2] == bloco[3] and bloco[4] == bloco[5] == bloco[6] == bloco[7] and bloco[0] != bloco[4]:
                return True
        return False

    def _padrao_4x1(self):
        for i in range(len(self.historico) - 4):
            bloco = self.historico[i:i+5]
            if bloco[0] == bloco[1] == bloco[2] == bloco[3] and bloco[4] != bloco[0]:
                return True
        return False

    def _empate_zona_ocorrencia(self):
        e_idx = [i for i, x in enumerate(self.historico) if x == 'E']
        if len(e_idx) >= 2 and e_idx[0] == 0:
            if 15 <= (e_idx[1] - e_idx[0]) <= 35:
                return True
        elif len(e_idx) == 1 and e_idx[0] == 0 and len(self.historico) >= 15:
            if all(self.historico[i] != 'E' for i in range(1, min(35, len(self.historico)))):
                return True
        elif len(self.historico) >= 5 and sum(1 for r in self.historico[:5] if r == 'E') >= 3:
            return True
        return False

    def calcular_frequencias(self):
        cont = collections.Counter(self.historico)
        total = len(self.historico)
        if total == 0:
            return {'C': 0, 'V': 0, 'E': 0}
        result = {k: round(v / total * 100) for k, v in cont.items()}
        for k in ['C', 'V', 'E']:
            if k not in result:
                result[k] = 0
        return result
    def sugestao_inteligente(self):
        analise = self.analisar_todos()
        pontuacoes = {"C": 0, "V": 0, "E": 0}
        motivos = {"C": [], "V": [], "E": []}
        historico = self.historico

        def pontuar(codigo, pontos, motivo):
            pontuacoes[codigo] += pontos
            motivos[codigo].append(motivo)

        # Quebra de padrões fortes
        if len(historico) >= 5 and historico[0] != historico[1] and all(historico[1] == historico[i] for i in range(1, 5)):
            pontuar(historico[1], 40, "Quebra de 4x1: tendência pode retornar")
        elif len(historico) >= 4 and historico[0] != historico[1] and all(historico[1] == historico[i] for i in range(1, 4)):
            pontuar(historico[1], 35, "Quebra de 3x1: cor anterior pode voltar")

        # Zona de empate
        if analise.get("Empate em Zona de Ocorrência"):
            if historico[0] == "E":
                pontuar("E", 45, "Zona de empate ativa com sequência")
            else:
                pontuar("E", 35, "Zona de empate ativa: possível empate próximo")

        # Sequência simples
        if len(historico) >= 4 and all(historico[i] == historico[0] for i in range(4)):
            pontuar(historico[0], 30, f"Sequência de 4+: favorece continuidade de {historico[0]}")

        # Outros padrões ativos
        if analise.get("Zig-Zag"):
            proxima = "C" if historico[0] == "V" else "V"
            pontuar(proxima, 15, "Zig-Zag identificado")

        if analise.get("Duplas repetidas"):
            pontuar(historico[0], 20, "Dupla repetida atual pode continuar")

        if analise.get("Empate recorrente") and historico[0] != "E":
            pontuar("E", 20, "Empates recorrentes próximos")

        if analise.get("Padrão 'onda'") and len(historico) >= 4:
            pontuar(historico[1], 15, "Padrão Onda detectado")

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

        # Frequência geral
        freq = self.calcular_frequencias()
        menor_freq_valor = min(freq.values())
        for cor, valor in freq.items():
            if valor == menor_freq_valor:
                pontuar(cor, 10, "Menor frequência recente")

        # Bônus por múltiplos padrões apontando para a mesma cor
        for cor in pontuacoes:
            if len(motivos[cor]) >= 2:
                pontuar(cor, 10, "Convergência de múltiplos padrões")

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
# --- CONFIGURAÇÃO STREAMLIT ---
st.set_page_config(layout="wide", page_title="Análise de Padrões de Jogos")

# --- INICIALIZA ESTADOS DA SESSÃO ---
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
# --- ESTILO PERSONALIZADO PARA BOTÕES ---
st.markdown("""
<style>
div.stButton > button:first-child {
    font-size: 17px; padding: 10px 20px; border-radius: 5px; margin: 5px;
    border: none; color: white;
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

# --- INTERFACE DE INSERÇÃO ---
st.title("⚽ Análise de Padrões de Jogos")
st.subheader("Inserir novo resultado:")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🏠 Casa", key="Casa"):
        adicionar_resultado("C")
with col2:
    if st.button("🚌 Visitante", key="Visitante"):
        adicionar_resultado("V")
with col3:
    if st.button("⚖️ Empate", key="Empate"):
        adicionar_resultado("E")
with col4:
    if st.button("↩️ Desfazer", key="Desfazer"):
        desfazer()
with col5:
    if st.button("🧹 Limpar", key="Limpar"):
        limpar()

st.markdown("---")

# --- SUGESTÃO E ANÁLISE ---
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

    # PADRÕES DETECTADOS
    st.markdown("---")
    st.subheader("🔍 Padrões encontrados")
    resultados = app.analisar_todos()
    colA, colB = st.columns(2)
    with colA:
        st.markdown("**Detectados:**")
        for nome, achou in resultados.items():
            if achou:
                st.success(f"✔️ {nome}")
    with colB:
        st.markdown("**Não encontrados:**")
        for nome, achou in resultados.items():
            if not achou:
                st.markdown(f"<span style='color: grey;'>✖️ {nome}</span>", unsafe_allow_html=True)

    # GRÁFICO DE FREQUÊNCIA
    st.markdown("---")
    st.subheader("📊 Frequência dos resultados")
    freq = sugestao["frequencias"]
    st.bar_chart({"Resultado": {"Casa": freq['C'], "Visitante": freq['V'], "Empate": freq['E']}})

# --- HISTÓRICO VISUAL ---
st.markdown("---")
st.subheader("📌 Histórico de resultados (mais recente à esquerda)")
if not st.session_state.historico:
    st.info("Nenhum resultado inserido ainda.")
else:
    html = "".join([bolinha_html(x) for x in st.session_state.historico])
    st.markdown(html, unsafe_allow_html=True)
    st.caption(f"Total: {len(st.session_state.historico)} jogos")

# --- ESTATÍSTICAS DE ACERTOS ---
st.markdown("---")
st.subheader("📈 Estatísticas de acertos")
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
