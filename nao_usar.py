import streamlit as st
import collections
import random

# --- CLASSE ANALISEPADROES (Pequena alteração na inicialização para lidar com a ordem) ---
class AnalisePadroes:
    def __init__(self, historico):
        # NOTA IMPORTANTE: O histórico AGORA virá com o resultado mais NOVO na posição 0.
        # A lógica dos padrões já está adaptada para ler do início ao fim (que agora é do mais novo para o mais antigo).
        self.historico = historico[:27] # Pega os 27 primeiros (mais novos)
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
            "Padrão 4x1": self._padrao_4x1
        }

    def analisar_todos(self):
        resultados = {}
        for nome, func in self.padroes_ativos.items():
            try:
                resultados[nome] = func()
            except Exception as e:
                resultados[nome] = False
        return resultados

    # --- MÉTODOS DE VERIFICAÇÃO DE PADRÕES (COPIE E COLE TODOS AQUI) ---
    # Eles já leem da esquerda para a direita (índice 0 em diante),
    # então funcionarão corretamente com o novo histórico ordenado.
    def _sequencia_simples(self):
        for i in range(len(self.historico) - 2):
            if self.historico[i] == self.historico[i+1] and self.historico[i+1] == self.historico[i+2]: return True
        return False
    def _zig_zag(self):
        if len(self.historico) < 4: return False
        for i in range(len(self.historico) - 1):
            if self.historico[i] == self.historico[i+1]: return False
        return True
    def _quebra_de_surf(self):
        for i in range(len(self.historico) - 3):
            if (self.historico[i] == self.historico[i+1] and self.historico[i+1] == self.historico[i+2] and self.historico[i+2] != self.historico[i+3]): return True
        return False
    def _quebra_de_zig_zag(self):
        if len(self.historico) < 5: return False
        for i in range(len(self.historico) - 4):
            if (self.historico[i] != self.historico[i+1] and self.historico[i+1] != self.historico[i+2] and self.historico[i+2] == self.historico[i+3]): return True
        return False
    def _duplas_repetidas(self):
        if len(self.historico) < 4: return False
        for i in range(len(self.historico) - 3):
            if (self.historico[i] == self.historico[i+1] and self.historico[i+2] == self.historico[i+3] and self.historico[i] != self.historico[i+2]): return True
        return False
    def _empate_recorrente(self):
        empates_indices = [i for i, r in enumerate(self.historico) if r == 'E']
        if len(empates_indices) < 2: return False
        for i in range(len(empates_indices) - 1):
            if 2 <= (empates_indices[i+1] - empates_indices[i]) <= 4: return True
        return False
    def _padrao_escada(self):
        if len(self.historico) < 6: return False
        for i in range(len(self.historico) - 5):
            if (self.historico[i] != self.historico[i+1] and self.historico[i+1] == self.historico[i+2] and self.historico[i+3] == self.historico[i+4] and self.historico[i+4] == self.historico[i+5] and self.historico[i+1] != self.historico[i+3]): return True
        return False
    def _espelho(self):
        if len(self.historico) < 2: return False
        metade = len(self.historico) // 2
        primeira_metade = self.historico[:metade]
        segunda_metade_reversa = self.historico[len(self.historico) - metade:][::-1]
        return primeira_metade == segunda_metade_reversa
    def _alternancia_empate_meio(self):
        if len(self.historico) < 3: return False
        for i in range(len(self.historico) - 2):
            if (self.historico[i] != 'E' and self.historico[i+1] == 'E' and self.historico[i+2] != 'E' and self.historico[i] != self.historico[i+2]): return True
        return False
    def _padrao_onda(self):
        if len(self.historico) < 4: return False
        for i in range(len(self.historico) - 3):
            if (self.historico[i] == self.historico[i+2] and self.historico[i+1] == self.historico[i+3] and self.historico[i] != self.historico[i+1]): return True
        return False
    def _padroes_ultimos_jogos(self):
        if len(self.historico) < 5: return False
        ultimos5 = self.historico[-5:] # Aqui ele pega os 5 mais antigos dos 27, se quiser os 5 mais novos, seria historico[:5]
        contador = collections.Counter(ultimos5)
        for resultado, count in contador.items():
            if count / len(ultimos5) >= 0.6: return True
        return False
    def _padrao_3x1(self):
        for i in range(len(self.historico) - 3):
            bloco = self.historico[i:i+4]
            if bloco[0] == bloco[1] == bloco[2] and bloco[3] != bloco[0]: return True
        return False
    def _padrao_3x3(self):
        for i in range(len(self.historico) - 5):
            bloco = self.historico[i:i+6]
            if (bloco[0] == bloco[1] == bloco[2] and bloco[3] == bloco[4] == bloco[5] and bloco[0] != bloco[3]): return True
        return False
    def _padrao_4x4(self):
        for i in range(len(self.historico) - 7):
            bloco = self.historico[i:i+8]
            if (bloco[0] == bloco[1] == bloco[2] == bloco[3] and bloco[4] == bloco[5] == bloco[6] == bloco[7] and bloco[0] != bloco[4]): return True
        return False
    def _padrao_4x1(self):
        for i in range(len(self.historico) - 4):
            bloco = self.historico[i:i+5]
            if (bloco[0] == bloco[1] == bloco[2] == bloco[3] and bloco[4] != bloco[0]): return True
        return False

    def calcular_frequencias(self):
        contador = collections.Counter(self.historico)
        total = len(self.historico)
        if total == 0: return {'C': 0, 'V': 0, 'E': 0}
        result = {k: round(v / total * 100) for k, v in contador.items()}
        for tipo in ['C', 'V', 'E']:
            if tipo not in result: result[tipo] = 0
        return result

    def sugestao_inteligente(self):
        analise = self.analisar_todos()
        padroes_identificados = [nome for nome, ok in analise.items() if ok]

        if padroes_identificados:
            frequencias = self.calcular_frequencias()
            opcoes = ["V", "C", "E"]
            entrada_sugerida = None
            min_freq = float('inf')

            # Sugere a opção com menor frequência para "quebrar" o padrão,
            # ou uma aleatória se as frequências forem iguais.
            for op in opcoes:
                if frequencias.get(op, 0) < min_freq:
                    min_freq = frequencias.get(op, 0)
                    entrada_sugerida = op

            if not entrada_sugerida or len(set(frequencias.values())) == 1:
                 entrada_sugerida = random.choice(opcoes)

            mapeamento = {"C": "Casa", "V": "Visitante", "E": "Empate"}
            entrada_legivel = mapeamento[entrada_sugerida]

            # Aumenta a confiança se mais padrões forem identificados
            confianca = min(90, int((len(padroes_identificados) / len(self.padroes_ativos)) * 100) + 20)

            return {
                "sugerir": True,
                "entrada": entrada_legivel,
                "entrada_codigo": entrada_sugerida,
                "motivos": padroes_identificados,
                "confianca": confianca,
                "frequencias": frequencias,
                "ultimos_resultados": self.historico[:3] # Pega os 3 mais recentes (início da lista)
            }
        else:
            return {
                "sugerir": False,
                "entrada": None,
                "entrada_codigo": None,
                "motivos": ["Nenhum padrão confiável identificado"],
                "confianca": 0,
                "frequencias": self.calcular_frequencias(),
                "ultimos_resultados": self.historico[:3]
            }

# --- FUNÇÕES DE INTERFACE E LÓGICA DE HISTÓRICO ---

# Inicializa o estado da sessão para armazenar o histórico
if 'historico' not in st.session_state:
    st.session_state.historico = []

def adicionar_resultado(resultado):
    # Insere o novo resultado no INÍCIO da lista
    st.session_state.historico.insert(0, resultado)
    # Limita o histórico a 27 resultados, removendo os mais antigos (do final)
    if len(st.session_state.historico) > 27:
        st.session_state.historico = st.session_state.historico[:27] # Mantém os 27 mais recentes

def limpar_historico():
    st.session_state.historico = []

def desfazer_ultimo():
    # Remove o primeiro item (o mais recente)
    if st.session_state.historico:
        st.session_state.historico.pop(0)

def get_resultado_html(resultado):
    """Retorna o HTML para uma bolinha colorida com base no resultado."""
    color_map = {'C': 'red', 'V': 'blue', 'E': 'gold'} # Amarelo para Empate
    return f"<span style='display:inline-block; width:20px; height:20px; border-radius:50%; background-color:{color_map.get(resultado, 'gray')}; margin:2px; vertical-align:middle;'></span>"

# --- CONFIGURAÇÃO DA PÁGINA STREAMLIT ---
st.set_page_config(layout="wide", page_title="Análise de Padrões de Jogos")

st.title("⚽ Análise de Padrões de Resultados")
st.markdown("---")

# --- CSS PARA BOTÕES COLORIDOS ---
# Importante: Este CSS é injetado no HTML da página.
# Ele usa IDs para direcionar botões específicos.
# st.markdown com unsafe_allow_html=True
st.markdown("""
<style>
/* Estilo geral para todos os botões do tipo stButton */
div.stButton > button:first-child {
    font-size: 16px;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    margin: 5px;
    color: white; /* Cor do texto padrão para botões coloridos */
    border: none;
}

/* Casa (Vermelho) */
div.stButton > button[data-testid="stButton-Casa (C)"] {
    background-color: #FF4B4B; 
}
div.stButton > button[data-testid="stButton-Casa (C)"]:hover {
    background-color: #FF6666;
}

/* Visitante (Azul) */
div.stButton > button[data-testid="stButton-Visitante (V)"] {
    background-color: #4B4BFF;
}
div.stButton > button[data-testid="stButton-Visitante (V)"]:hover {
    background-color: #6666FF;
}

/* Empate (Amarelo/Dourado) */
div.stButton > button[data-testid="stButton-Empate (E)"] {
    background-color: #FFD700;
    color: black; /* Texto preto para contraste no amarelo */
}
div.stButton > button[data-testid="stButton-Empate (E)"]:hover {
    background-color: #FFE666;
}

/* Desfazer Último e Limpar Histórico (Cinza padrão, texto preto) */
div.stButton > button[data-testid="stButton-Desfazer Último"],
div.stButton > button[data-testid="stButton-Limpar Histórico"] {
    background-color: #E0E0E0;
    color: black;
}
div.stButton > button[data-testid="stButton-Desfazer Último"]:hover,
div.stButton > button[data-testid="stButton-Limpar Histórico"]:hover {
    background-color: #F0F0F0;
}
</style>
""", unsafe_allow_html=True)


# --- SEÇÃO DE INSERÇÃO DE RESULTADOS COM BOTÕES COLORIDOS ---
st.subheader("Inserir Novo Resultado")

# Os 'key's dos botões agora correspondem aos 'data-testid' no CSS
col_btn1, col_btn2, col_btn3, col_btn4, col_btn5 = st.columns(5)

with col_btn1:
    if st.button("Casa (C)", help="Adiciona um resultado de Casa", key="Casa (C)", use_container_width=True):
        adicionar_resultado('C')
with col_btn2:
    if st.button("Visitante (V)", help="Adiciona um resultado de Visitante", key="Visitante (V)", use_container_width=True):
        adicionar_resultado('V')
with col_btn3:
    if st.button("Empate (E)", help="Adiciona um resultado de Empate", key="Empate (E)", use_container_width=True):
        adicionar_resultado('E')
with col_btn4:
    if st.button("Desfazer Último", help="Remove o último resultado inserido", key="Desfazer Último", use_container_width=True):
        desfazer_ultimo()
with col_btn5:
    if st.button("Limpar Histórico", help="Apaga todos os resultados do histórico", key="Limpar Histórico", use_container_width=True):
        limpar_historico()

st.markdown("---")

# --- EXIBIÇÃO DO HISTÓRICO ---
st.subheader("Histórico de Resultados (Mais novo à esquerda)")

if not st.session_state.historico:
    st.info("O histórico está vazio. Comece inserindo resultados acima.")
else:
    historico_display = ""
    # O loop já processa do mais novo para o mais antigo (posição 0 em diante)
    for i, resultado in enumerate(st.session_state.historico):
        historico_display += get_resultado_html(resultado)
        if (i + 1) % 9 == 0 and (i + 1) < len(st.session_state.historico): # Quebra a linha a cada 9 resultados
            historico_display += "<br>" # Quebra de linha HTML

    st.markdown(historico_display, unsafe_allow_html=True)
    st.write(f"Total de resultados no histórico: **{len(st.session_state.historico)}** (máx. 27)")

st.markdown("---")

# --- ANÁLISE E SUGESTÃO AUTOMÁTICA ---
if len(st.session_state.historico) >= 9:
    # A classe AnalisePadroes agora recebe o histórico já ordenado do mais novo para o mais antigo
    app_analise = AnalisePadroes(st.session_state.historico)

    st.header("🔍 Padrões Detectados")
    padroes_encontrados = app_analise.analisar_todos()
    
    col_pat1, col_pat2 = st.columns(2)

    with col_pat1:
        st.subheader("Padrões Encontrados:")
        encontrados_lista = [nome for nome, encontrado in padroes_encontrados.items() if encontrado]
        if encontrados_lista:
            for padrao in encontrados_lista:
                st.success(f"✔️ {padrao}")
        else:
            st.info("Nenhum padrão específico detectado no momento.")
    
    with col_pat2:
        st.subheader("Padrões Não Encontrados:")
        nao_encontrados_lista = [nome for nome, encontrado in padroes_encontrados.items() if not encontrado]
        if nao_encontrados_lista:
            for padrao in nao_encontrados_lista:
                st.markdown(f"<span style='color: grey;'>✖️ {padrao}</span>", unsafe_allow_html=True)
        else:
            st.info("Todos os padrões foram encontrados!")

    st.markdown("---")
    st.header("💡 Sugestão Inteligente para o Próximo Jogo")
    sugestao = app_analise.sugestao_inteligente()

    if sugestao['sugerir']:
        st.write(f"Considerando os padrões e frequências do histórico atual:")
        st.success(f"**Sugestão:** Próximo resultado provável: **{sugestao['entrada']}**")
        st.metric(label="Confiança da Sugestão", value=f"{sugestao['confianca']}%")
        st.info(f"**Motivos:** {', '.join(sugestao['motivos'])}")
        st.markdown(f"Últimos 3 resultados analisados: `{', '.join(sugestao['ultimos_resultados'])}`")
    else:
        st.warning(f"**Sem sugestão:** {sugestao['motivos'][0]}")
    
    st.markdown("---")
    st.header("📊 Frequência dos Resultados no Histórico")
    frequencias = app_analise.calcular_frequencias()
    
    mapeamento_freq_legivel = {"C": "Casa", "V": "Visitante", "E": "Empate"}
    freq_data = {
        "Resultado": [mapeamento_freq_legivel[t] for t in ['C', 'V', 'E']],
        "Porcentagem": [frequencias.get(t, 0) for t in ['C', 'V', 'E']]
    }
    
    st.bar_chart(freq_data, x="Resultado", y="Porcentagem")
    st.write(f"Total de jogos no histórico analisado: **{len(app_analise.historico)}**")

else:
    st.warning(f"A análise e sugestão serão exibidas quando houver pelo menos 9 resultados no histórico. Resultados atuais: **{len(st.session_state.historico)}**")

