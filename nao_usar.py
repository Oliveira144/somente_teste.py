import streamlit as st
import collections
import random

# --- CLASSE ANALISEPADROES (COM NOVO PADRÃO DE EMPATE) ---
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
            "Empate em Zona de Ocorrência": self._empate_zona_ocorrencia # NOVO PADRÃO
        }

    def analisar_todos(self):
        resultados = {}
        for nome, func in self.padroes_ativos.items():
            try:
                resultados[nome] = func()
            except Exception as e:
                resultados[nome] = False
        return resultados

    # --- MÉTODOS DE VERIFICAÇÃO DE PADRÕES (EXISTENTES) ---
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
        ultimos5 = self.historico[:5]
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

    # --- NOVO MÉTODO DE PADRÃO: Empate em Zona de Ocorrência ---
    def _empate_zona_ocorrencia(self):
        # Baseado na descrição: "não aparece por muitas rodadas, tende a reaparecer em intervalos médios entre 15 e 35 rodadas – e às vezes vem em duplas."
        
        # 1. Verifica se houve um longo período sem empates
        #    Vamos procurar por um trecho de histórico recente (ex: últimos 15 a 35 jogos)
        #    onde não houve empates, seguido por um ou dois empates.
        
        # Consideramos o histórico em ordem do mais novo para o mais antigo (esquerda para direita)
        # Portanto, o histórico[0] é o mais recente.
        
        # Encontra os índices de todos os empates no histórico atual
        empate_indices = [i for i, x in enumerate(self.historico) if x == 'E']

        # Se não houver empates suficientes para analisar a zona ou intervalo
        if len(empate_indices) < 2:
            # Se houver apenas 1 empate, verificamos se ele é o resultado mais recente e se os anteriores não são empates.
            # Isso pode indicar o início de uma "zona" após um período sem.
            if len(empate_indices) == 1 and empate_indices[0] == 0: # O empate mais recente é o atual (índice 0)
                # Verifica se nos últimos 15 a 35 resultados anteriores não houve empates
                # Isso significa que todos os resultados de 1 até 15 (ou até onde o histórico permitir) não são 'E'.
                # A lógica será: se o último foi 'E' e antes dele não houve 'E' por um longo tempo.
                for i in range(1, min(len(self.historico), 35)): # Olha até 35 resultados atrás
                    if self.historico[i] == 'E':
                        return False # Achou um empate recente, então não houve "longo período sem"
                
                # Se chegou aqui, o último é 'E' e não houve outros 'E' no intervalo considerado (15 a 35 posições anteriores)
                return True # Encontrou um empate que pode indicar o início de uma zona após um longo período
        
        # Se há múltiplos empates, verifica os intervalos entre eles
        # A distância entre dois empates (índices na lista, do mais novo ao mais antigo)
        # representa o número de jogos ENTRE eles.
        for i in range(len(empate_indices) - 1):
            # A diferença entre os índices é a quantidade de resultados entre eles
            distancia = empate_indices[i+1] - empate_indices[i] - 1 # subtrai 1 porque a distância é entre os resultados, não entre os índices

            # "reaparecer em intervalos médios entre 15 e 35 rodadas"
            # O índice 'i' é do empate mais recente, 'i+1' é do anterior a ele.
            # Se o empate atual (índice 0) é um dos dois (i ou i+1)
            # E a distância do próximo empate se encaixa no padrão
            
            # Se a distância entre o empate mais recente e o anterior está na faixa
            if empate_indices[i] == 0: # O empate mais recente está no índice 0
                if 15 <= distancia + 1 <= 35: # Ajuste para a contagem de "rodadas"
                    return True

        # Se o histórico atual tem empates em sequência no início (duplas) e não houve empates recentes antes
        if len(self.historico) >= 2 and self.historico[0] == 'E' and self.historico[1] == 'E':
            # Verifica se nos resultados anteriores (a partir do terceiro) não houve empates por um tempo
            # Por exemplo, se tivemos EE e os últimos 15 a 35 resultados antes disso não tiveram E.
            for i in range(2, min(len(self.historico), 35)):
                if self.historico[i] == 'E':
                    return False # Achou um empate recente antes da dupla
            if len(self.historico) >= 15: # Precisa de histórico suficiente para verificar o "longo período"
                return True # Encontrou uma dupla de empates após um possível longo período sem.
        
        return False # Padrão não encontrado
        
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

            for op in opcoes:
                if frequencias.get(op, 0) < min_freq:
                    min_freq = frequencias.get(op, 0)
                    entrada_sugerida = op

            if not entrada_sugerida or len(set(frequencias.values())) == 1:
                 entrada_sugerida = random.choice(opcoes)

            mapeamento = {"C": "Casa", "V": "Visitante", "E": "Empate"}
            entrada_legivel = mapeamento[entrada_sugerida]

            confianca = min(90, int((len(padroes_identificados) / len(self.padroes_ativos)) * 100) + 20)

            return {
                "sugerir": True,
                "entrada": entrada_legivel,
                "entrada_codigo": entrada_sugerida,
                "motivos": padroes_identificados,
                "confianca": confianca,
                "frequencias": frequencias,
                "ultimos_resultados": self.historico[:3]
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

# --- FUNÇÕES DE INTERFACE E LÓGICA DE HISTÓRICO (SEM MUDANÇAS) ---

# Inicializa o estado da sessão para armazenar o histórico
if 'historico' not in st.session_state:
    st.session_state.historico = []

def adicionar_resultado(resultado):
    st.session_state.historico.insert(0, resultado)
    if len(st.session_state.historico) > 27:
        st.session_state.historico = st.session_state.historico[:27]

def limpar_historico():
    st.session_state.historico = []

def desfazer_ultimo():
    if st.session_state.historico:
        st.session_state.historico.pop(0)

def get_resultado_html(resultado):
    color_map = {'C': 'red', 'V': 'blue', 'E': 'gold'}
    return f"<span style='display:inline-block; width:20px; height:20px; border-radius:50%; background-color:{color_map.get(resultado, 'gray')}; margin:2px; vertical-align:middle;'></span>"

# --- CONFIGURAÇÃO DA PÁGINA STREAMLIT (SEM MUDANÇAS) ---
st.set_page_config(layout="wide", page_title="Análise de Padrões de Jogos")

st.title("⚽ Análise de Padrões de Resultados")
st.markdown("---")

# --- CSS PARA BOTÕES COLORIDOS (SEM MUDANÇAS) ---
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


# --- SEÇÃO DE INSERÇÃO DE RESULTADOS COM BOTÕES COLORIDOS (SEM MUDANÇAS) ---
st.subheader("Inserir Novo Resultado")

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

# --- LÓGICA DE ANÁLISE E SUGESTÃO (REORDENADA) ---
if len(st.session_state.historico) >= 9:
    app_analise = AnalisePadroes(st.session_state.historico)
    sugestao = app_analise.sugestao_inteligente()

    st.header("💡 Sugestão Inteligente para o Próximo Jogo")

    if sugestao['sugerir']:
        st.write(f"Considerando os padrões e frequências do histórico atual:")
        st.success(f"**Sugestão:** Próximo resultado provável: **{sugestao['entrada']}**")
        st.metric(label="Confiança da Sugestão", value=f"{sugestao['confianca']}%")
        st.info(f"**Motivos:** {', '.join(sugestao['motivos'])}")
        st.markdown(f"Últimos 3 resultados analisados (mais novo à esquerda): `{', '.join(sugestao['ultimos_resultados'])}`")
    else:
        st.warning(f"**Sem sugestão:** {sugestao['motivos'][0]}")

    st.markdown("---")

# --- EXIBIÇÃO DO HISTÓRICO (SEM MUDANÇAS) ---
st.subheader("Histórico de Resultados (Mais novo à esquerda)")

if not st.session_state.historico:
    st.info("O histórico está vazio. Comece inserindo resultados acima.")
else:
    historico_display = ""
    for i, resultado in enumerate(st.session_state.historico):
        historico_display += get_resultado_html(resultado)
        if (i + 1) % 9 == 0 and (i + 1) < len(st.session_state.historico):
            historico_display += "<br>" 

    st.markdown(historico_display, unsafe_allow_html=True)
    st.write(f"Total de resultados no histórico: **{len(st.session_state.historico)}** (máx. 27)")

st.markdown("---")

# --- PADRÕES DETECTADOS E FREQUÊNCIA (SEM MUDANÇAS) ---
if len(st.session_state.historico) >= 9:
    # Reusa o objeto app_analise já criado acima
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
    st.warning(f"A análise completa (sugestão, padrões e frequência) será exibida quando houver pelo menos 9 resultados no histórico. Resultados atuais: **{len(st.session_state.historico)}**")

