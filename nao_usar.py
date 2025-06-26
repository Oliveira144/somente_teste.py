import streamlit as st
import streamlit.components.v1 as components
import random
from datetime import datetime
import collections

st.set_page_config(
    page_title="Football Studio Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
.roadmap-grid-container {
    display: grid;
    grid-template-columns: repeat(9, 28px);
    gap: 4px;
    padding: 5px;
    background-color: #1a1a1a;
    border: 1px solid #333;
    border-radius: 5px;
    width: fit-content;
}
.roadmap-item {
    width: 25px;
    height: 25px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.2);
}
</style>
""", unsafe_allow_html=True)
if 'historico' not in st.session_state:
    st.session_state.historico = []

if 'estatisticas' not in st.session_state:
    st.session_state.estatisticas = {
        'total_jogos': 0,
        'acertos': 0,
        'erros': 0,
        'historico_sugestoes': []
    }
class AnalisePadroes:
    def __init__(self, historico):
        self.historico = list(reversed(historico[:54]))
        self.padroes_ativos = self.analisar_todos()

    def analisar_todos(self):
        padroes = {
            "Sequência": self._sequencia,
            "Zig-Zag": self._zig_zag,
            "Quebra de Surf": self._quebra_de_surf,
            "Ondas Longas": self._ondas_longas,
            "Dominância": self._ciclo_dominancia
        }
        return {nome: True for nome, func in padroes.items() if func()}

    def _sequencia(self):
        return len(self.historico) >= 4 and all(r == self.historico[i] for i in range(4))

    def _zig_zag(self):
        if len(self.historico) < 6:
            return False
        return all(self.historico[i] != self.historico[i + 1] for i in range(5))

    def _quebra_de_surf(self):
        if len(self.historico) < 5:
            return False
        return self.historico[0] == self.historico[1] == self.historico[2] and self.historico[3] != self.historico[2]

    def _ondas_longas(self):
        count = 1
        for i in range(1, len(self.historico)):
            if self.historico[i] == self.historico[i - 1]:
                count += 1
                if count >= 5:
                    return True
            else:
                count = 1
        return False

    def _ciclo_dominancia(self):
        if len(self.historico) < 10:
            return False
        contagem = collections.Counter(self.historico[:10])
        return any(v >= 7 for v in contagem.values())

    def sugestao_inteligente(self):
        if len(self.historico) < 9:
            return {
                "sugerir": False,
                "entrada": None,
                "entrada_codigo": None,
                "motivo": "Histórico insuficiente",
                "padroes_ativos": [],
                "ultimos": self.historico[-5:]
            }

        ativos = self.padroes_ativos
        if not ativos:
            return {
                "sugerir": False,
                "entrada": None,
                "entrada_codigo": None,
                "motivo": "Nenhum padrão identificado",
                "padroes_ativos": [],
                "ultimos": self.historico[-5:]
            }

        ultima = self.historico[-1]
        opcoes = ["C", "V", "E"]

        if "Quebra de Surf" in ativos:
            entrada = random.choice([r for r in ["C", "V"] if r != ultima])
            motivo = "Quebra de sequência"
        elif "Sequência" in ativos or "Ondas Longas" in ativos:
            entrada = ultima
            motivo = "Sequência contínua"
        elif "Zig-Zag" in ativos:
            entrada = ultima  # Mantém alternância
            motivo = "Zig-Zag Detectado"
        elif "Dominância" in ativos:
            entrada = collections.Counter(self.historico[:10]).most_common(1)[0][0]
            motivo = "Forte tendência"
        else:
            entrada = random.choice(opcoes)
            motivo = "Fallback aleatório"

        nomes = {"C": "Casa", "V": "Visitante", "E": "Empate"}
        return {
            "sugerir": True,
            "entrada": nomes[entrada],
            "entrada_codigo": entrada,
            "motivo": motivo,
            "padroes_ativos": list(ativos.keys()),
            "ultimos": self.historico[-5:]
        }
def adicionar_resultado(resultado):
    if 'ultima_sugestao' in st.session_state and st.session_state.ultima_sugestao.get('sugerir'):
        sug = st.session_state.ultima_sugestao
        acertou = resultado == sug['entrada_codigo']
        if acertou:
            st.session_state.estatisticas['acertos'] += 1
        else:
            st.session_state.estatisticas['erros'] += 1
        st.session_state.estatisticas['historico_sugestoes'].append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'sugerido': sug['entrada'],
            'real': resultado,
            'acertou': acertou,
            'padrao': sug.get('motivo', '')
        })
        del st.session_state.ultima_sugestao
    st.session_state.historico.insert(0, resultado)
    st.session_state.estatisticas['total_jogos'] += 1

def desfazer_ultimo():
    if st.session_state.historico:
        st.session_state.historico.pop(0)
        st.session_state.estatisticas['total_jogos'] = max(0, st.session_state.estatisticas['total_jogos'] - 1)
        if 'ultima_sugestao' in st.session_state:
            del st.session_state.ultima_sugestao

def limpar_historico():
    st.session_state.historico.clear()
    st.session_state.estatisticas = {
        'total_jogos': 0,
        'acertos': 0,
        'erros': 0,
        'historico_sugestoes': []
    }
    if 'ultima_sugestao' in st.session_state:
        del st.session_state.ultima_sugestao

def get_resultado_html(resultado):
    color_map = {'C': '#FF4B4B', 'V': '#4B4BFF', 'E': '#FFD700'}
    return f"<div class='roadmap-item' style='background-color: {color_map.get(resultado, 'gray')};'></div>"
with st.sidebar:
    st.subheader("📊 Estatísticas")
    est = st.session_state.estatisticas
    if est['total_jogos'] > 0:
        acertos = est['acertos']
        erros = est['erros']
        taxa = (acertos / (acertos + erros)) * 100 if (acertos + erros) else 0
        st.metric("Total", est['total_jogos'])
        st.metric("Acertos", acertos)
        st.metric("Erros", erros)
        st.metric("Taxa de Acerto", f"{taxa:.1f}%")
    else:
        st.info("Nenhum jogo registrado.")
st.header("🎯 Inserir Resultado")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🔴 Casa"):
        adicionar_resultado('C')
        st.rerun()
with col2:
    if st.button("🟡 Empate"):
        adicionar_resultado('E')
        st.rerun()
with col3:
    if st.button("🔵 Visitante"):
        adicionar_resultado('V')
        st.rerun()
with col4:
    if st.button("↩️ Desfazer"):
        desfazer_ultimo()
        st.rerun()
with col5:
    if st.button("🗑️ Limpar"):
        limpar_historico()
        st.rerun()
st.subheader("📈 Histórico")
if not st.session_state.historico:
    st.info("Nenhum resultado registrado.")
else:
    html = ''.join(get_resultado_html(r) for r in st.session_state.historico)
    components.html(f"<div class='roadmap-grid-container'>{html}</div>", height=300, scrolling=False)
st.subheader("🧠 Sugestão Estratégica")

if len(st.session_state.historico) >= 9:
    analise = AnalisePadroes(st.session_state.historico)
    resultado = analise.sugestao_inteligente()
    st.session_state.ultima_sugestao = resultado

    if resultado["sugerir"]:
        st.success(f"🎯 Sugerido: **{resultado['entrada']}** via padrão: {resultado['motivo']}")
        st.markdown(f"**Últimos 5 resultados:** {' - '.join(resultado['ultimos'])}")
        st.markdown(f"**Padrões Ativos:** {', '.join(resultado['padroes_ativos'])}")
    else:
        st.info(f"🤖 Sem sugestão no momento ({resultado['motivo']}).")
else:
    st.warning("💡 Insira pelo menos 9 jogos para ativar a análise.")
class AnalisePadroes:
    def __init__(self, historico):
        self.historico = list(reversed(historico[:54]))
        self.padroes_ativos = self.analisar_todos()

    def analisar_todos(self):
        padroes = {
            "Sequência": self._sequencia,
            "Zig-Zag": self._zig_zag,
            "Quebra de Surf": self._quebra_de_surf,
            "Ondas Longas": self._ondas_longas,
            "Dominância": self._ciclo_dominancia
        }
        return {nome: True for nome, func in padroes.items() if func()}

    def _sequencia(self):
        return len(self.historico) >= 4 and all(r == self.historico[i] for i in range(4))

    def _zig_zag(self):
        if len(self.historico) < 6:
            return False
        return all(self.historico[i] != self.historico[i + 1] for i in range(5))

    def _quebra_de_surf(self):
        if len(self.historico) < 5:
            return False
        return self.historico[0] == self.historico[1] == self.historico[2] and self.historico[3] != self.historico[2]

    def _ondas_longas(self):
        count = 1
        for i in range(1, len(self.historico)):
            if self.historico[i] == self.historico[i - 1]:
                count += 1
                if count >= 5:
                    return True
            else:
                count = 1
        return False

    def _ciclo_dominancia(self):
        if len(self.historico) < 10:
            return False
        contagem = collections.Counter(self.historico[:10])
        return any(v >= 7 for v in contagem.values())

    def sugestao_inteligente(self):
        if len(self.historico) < 9:
            return {
                "sugerir": False,
                "entrada": None,
                "entrada_codigo": None,
                "motivo": "Histórico insuficiente",
                "padroes_ativos": [],
                "ultimos": self.historico[-5:]
            }

        ativos = self.padroes_ativos
        if not ativos:
            return {
                "sugerir": False,
                "entrada": None,
                "entrada_codigo": None,
                "motivo": "Nenhum padrão identificado",
                "padroes_ativos": [],
                "ultimos": self.historico[-5:]
            }

        ultima = self.historico[-1]
        opcoes = ["C", "V", "E"]

        if "Quebra de Surf" in ativos:
            entrada = random.choice([r for r in ["C", "V"] if r != ultima])
            motivo = "Quebra de sequência"
        elif "Sequência" in ativos or "Ondas Longas" in ativos:
            entrada = ultima
            motivo = "Sequência contínua"
        elif "Zig-Zag" in ativos:
            entrada = ultima  # Mantém alternância
            motivo = "Zig-Zag Detectado"
        elif "Dominância" in ativos:
            entrada = collections.Counter(self.historico[:10]).most_common(1)[0][0]
            motivo = "Forte tendência"
        else:
            entrada = random.choice(opcoes)
            motivo = "Fallback aleatório"

        nomes = {"C": "Casa", "V": "Visitante", "E": "Empate"}
        return {
            "sugerir": True,
            "entrada": nomes[entrada],
            "entrada_codigo": entrada,
            "motivo": motivo,
            "padroes_ativos": list(ativos.keys()),
            "ultimos": self.historico[-5:]
        }
