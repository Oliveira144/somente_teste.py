import streamlit as st
import collections
import random

# --- CLASSE ANALISEPADROES ---
class AnalisePadroes:
    def __init__(self, historico):
        # Limita o histórico a 27 resultados para a análise, mantendo o mais novo à esquerda
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
            except Exception as e:
                #st.error(f"Erro ao analisar padrão {nome}: {e}") # Para depuração
                resultados[nome] = False
        return resultados

    # --- MÉTODOS DE VERIFICAÇÃO DE PADRÕES (EXISTENTES, SEM ALTERAÇÃO) ---
    def _sequencia_simples(self):
        # Verifica se há 3 ou mais resultados iguais consecutivos em qualquer parte do histórico
        for i in range(len(self.historico) - 2):
            if self.historico[i] == self.historico[i+1] and self.historico[i+1] == self.historico[i+2]: return True
        return False

    def _zig_zag(self):
        # Verifica se há um padrão de alternância (ex: C-V-C-V)
        if len(self.historico) < 4: return False
        for i in range(len(self.historico) - 1):
            if self.historico[i] == self.historico[i+1]: return False
        return True

    def _quebra_de_surf(self):
        # Verifica se houve uma sequência de 3 seguida de uma quebra (ex: C-C-C-V)
        for i in range(len(self.historico) - 3):
            if (self.historico[i] == self.historico[i+1] and self.historico[i+1] == self.historico[i+2] and self.historico[i+2] != self.historico[i+3]): return True
        return False

    def _quebra_de_zig_zag(self):
        # Verifica se um padrão zig-zag foi quebrado (ex: C-V-C-C)
        if len(self.historico) < 5: return False
        for i in range(len(self.historico) - 4):
            if (self.historico[i] != self.historico[i+1] and self.historico[i+1] != self.historico[i+2] and self.historico[i+2] == self.historico[i+3]): return True
        return False

    def _duplas_repetidas(self):
        # Verifica se há duplas de resultados repetidas (ex: C-C-V-V)
        if len(self.historico) < 4: return False
        for i in range(len(self.historico) - 3):
            if (self.historico[i] == self.historico[i+1] and self.historico[i+2] == self.historico[i+3] and self.historico[i] != self.historico[i+2]): return True
        return False

    def _empate_recorrente(self):
        # Verifica se empates estão ocorrendo em intervalos curtos/médios
        empates_indices = [i for i, r in enumerate(self.historico) if r == 'E']
        if len(empates_indices) < 2: return False
        for i in range(len(empates_indices) - 1):
            # Intervalo entre 2 e 4 rodadas entre empates (índices são 0-based, distancia real +1)
            if 2 <= (empates_indices[i+1] - empates_indices[i]) <= 4: return True
        return False

    def _padrao_escada(self):
        # Ex: V-C-C-V-V-V
        if len(self.historico) < 6: return False
        for i in range(len(self.historico) - 5):
            if (self.historico[i] != self.historico[i+1] and self.historico[i+1] == self.historico[i+2] and self.historico[i+3] == self.historico[i+4] and self.historico[i+4] == self.historico[i+5] and self.historico[i+1] != self.historico[i+3]): return True
        return False

    def _espelho(self):
        # Verifica se a primeira metade do histórico é o espelho da segunda metade (reversa)
        if len(self.historico) < 2: return False
        metade = len(self.historico) // 2
        primeira_metade = self.historico[:metade]
        segunda_metade_reversa = self.historico[len(self.historico) - metade:][::-1]
        return primeira_metade == segunda_metade_reversa

    def _alternancia_empate_meio(self):
        # Ex: C-E-V
        if len(self.historico) < 3: return False
        for i in range(len(self.historico) - 2):
            if (self.historico[i] != 'E' and self.historico[i+1] == 'E' and self.historico[i+2] != 'E' and self.historico[i] != self.historico[i+2]): return True
        return False

    def _padrao_onda(self):
        # Ex: C-V-C-V ou V-C-V-C
        if len(self.historico) < 4: return False
        for i in range(len(self.historico) - 3):
            if (self.historico[i] == self.historico[i+2] and self.historico[i+1] == self.historico[i+3] and self.historico[i] != self.historico[i+1]): return True
        return False

    def _padroes_ultimos_jogos(self):
        # Verifica se um resultado está dominando os últimos 5 jogos
        if len(self.historico) < 5: return False
        ultimos5 = self.historico[:5] # Pega os 5 mais NOVOS
        contador = collections.Counter(ultimos5)
        for resultado, count in contador.items():
            if count / len(ultimos5) >= 0.6: return True # Ex: 3 de 5 são iguais (60%)
        return False

    def _padrao_3x1(self):
        # Ex: C-C-C-V
        for i in range(len(self.historico) - 3):
            bloco = self.historico[i:i+4]
            if bloco[0] == bloco[1] == bloco[2] and bloco[3] != bloco[0]: return True
        return False

    def _padrao_3x3(self):
        # Ex: C-C-C-V-V-V
        for i in range(len(self.historico) - 5):
            bloco = self.historico[i:i+6]
            if (bloco[0] == bloco[1] == bloco[2] and bloco[3] == bloco[4] == bloco[5] and bloco[0] != bloco[3]): return True
        return False

    def _padrao_4x4(self):
        # Ex: C-C-C-C-V-V-V-V
        for i in range(len(self.historico) - 7):
            bloco = self.historico[i:i+8]
            if (bloco[0] == bloco[1] == bloco[2] == bloco[3] and bloco[4] == bloco[5] == bloco[6] == bloco[7] and bloco[0] != bloco[4]): return True
        return False

    def _padrao_4x1(self):
        # Ex: C-C-C-C-V
        for i in range(len(self.historico) - 4):
            bloco = self.historico[i:i+5]
            if (bloco[0] == bloco[1] == bloco[2] == bloco[3] and bloco[4] != bloco[0]): return True
        return False

    def _empate_zona_ocorrencia(self):
        empate_indices = [i for i, x in enumerate(self.historico) if x == 'E']

        # Condição 1: Um empate recente (último resultado) após um longo período sem empates
        if len(empate_indices) > 0 and empate_indices[0] == 0: # O mais recente é um empate
            if len(empate_indices) > 1: # Tem pelo menos um empate anterior
                distancia_ao_empate_anterior = empate_indices[1] - empate_indices[0] # Distância em posições
                if 15 <= distancia_ao_empate_anterior <= 35: # Ex: se o último E foi na pos 0 e o anterior na pos 15, distancia é 15
                    return True
            else: # Só tem um empate no histórico e é o mais recente
                # Verifica se nos resultados anteriores (até o limite de histórico ou 35) não houve empates
                ha_empates_anteriores_no_intervalo = False
                for i in range(1, min(len(self.historico), 35)):
                    if self.historico[i] == 'E':
                        ha_empates_anteriores_no_intervalo = True
                        break
                if not ha_empates_anteriores_no_intervalo and len(self.historico) >= 15:
                    return True

        # Condição 2: Empates em duplas ou trios após um período sem (indicando início de zona)
        if len(self.historico) >= 2 and self.historico[0] == 'E' and self.historico[1] == 'E': # Dupla recente de empates
            ha_empates_antes_da_dupla = False
            for i in range(2, min(len(self.historico), 35)): # Procura antes da dupla
                if self.historico[i] == 'E':
                    ha_empates_antes_da_dupla = True
                    break
            if not ha_empates_antes_da_dupla and len(self.historico) >= 15:
                return True
        
        # Condição 3: Três ou mais empates nos últimos 5 resultados (sugere que a "zona" está ativa com maior frequência)
        if len(self.historico) >= 5:
            num_empates_ultimos_5 = sum(1 for r in self.historico[:5] if r == 'E')
            if num_empates_ultimos_5 >= 3:
                return True

        return False


    def calcular_frequencias(self):
        contador = collections.Counter(self.historico)
        total = len(self.historico)
        if total == 0: return {'C': 0, 'V': 0, 'E': 0}
        result = {k: round(v / total * 100) for k, v in contador.items()}
        for tipo in ['C', 'V', 'E']:
            if tipo not in result: result[tipo] = 0
        return result

    # --- MÉTODO sugestao_inteligente REFINADO ---
    def sugestao_inteligente(self):
        analise = self.analisar_todos()
        
        sugestao_final_codigo = None
        motivo_principal = [] # Agora será uma lista para o motivo MAIS relevante
        confianca_base = 0 

        # --- Etapa 1: Prioridade Alta (Padrões de Quebra e Continuidade Fortes e Recentes) ---

        # 1.1 Quebra de Padrão (4x1 ou 3x1): Se o último resultado quebrou uma sequência forte
        if len(self.historico) >= 5:
            # 4x1 (último quebrou uma sequência de 4)
            if self.historico[0] != self.historico[1] and \
               self.historico[1] == self.historico[2] == self.historico[3] == self.historico[4]:
                sugestao_final_codigo = self.historico[1] # Sugere a cor que dominava antes da quebra
                motivo_principal.append(f"Quebra de padrão 4x1: A cor forte ({sugestao_final_codigo}) quebrou. Sugere o retorno da cor forte anterior.")
                confianca_base = 80 # Alta confiança para este tipo de quebra
        
        if sugestao_final_codigo is None and len(self.historico) >= 4:
            # 3x1 (último quebrou uma sequência de 3)
            if self.historico[0] != self.historico[1] and \
               self.historico[1] == self.historico[2] == self.historico[3]:
                sugestao_final_codigo = self.historico[1] # Sugere a cor que dominava antes da quebra
                motivo_principal.append(f"Quebra de padrão 3x1: A cor forte ({sugestao_final_codigo}) quebrou. Sugere o retorno da cor forte anterior.")
                confianca_base = 75 # Boa confiança para este tipo de quebra

        # 1.2 Empate em Zona de Ocorrência: Se o padrão específico do empate está ativo e forte
        if sugestao_final_codigo is None and "Empate em Zona de Ocorrência" in analise and analise["Empate em Zona de Ocorrência"]:
            if self.historico[0] == 'E': # Se o último resultado foi Empate e está na zona, sugere continuação
                sugestao_final_codigo = 'E'
                motivo_principal.append("Empate em Zona de Ocorrência: O último resultado foi Empate, indicando a força da zona. Sugere continuação.")
                confianca_base = 85 # Confiança muito alta para continuar o empate em zona
            else: # Se a zona está ativa, mas o último não foi E, sugere E como o próximo
                sugestao_final_codigo = 'E'
                motivo_principal.append("Empate em Zona de Ocorrência: Padrão ativo, o Empate pode surgir em breve.")
                confianca_base = 70 # Confiança um pouco menor se não for continuação direta


        # 1.3 Surf de Cor (Sequências longas e recentes): Se há uma sequência de 4+ e sugere continuação
        if sugestao_final_codigo is None and len(self.historico) >= 4 and \
           self.historico[0] == self.historico[1] == self.historico[2] == self.historico[3]:
            sugestao_final_codigo = self.historico[0] # Sugere a continuação da sequência
            motivo_principal.append(f"Continuação de Sequência (Surf de Cor) de 4+ resultados de {sugestao_final_codigo}.")
            confianca_base = 65 # Boa confiança para sequências fortes

        # --- Etapa 2: Prioridade Média (Somente se NENHUMA sugestão foi feita na Etapa 1) ---
        if sugestao_final_codigo is None:
            # Padrão Zig-Zag (ex: C-V-C - sugere V)
            if len(self.historico) >= 3 and \
               self.historico[0] != self.historico[1] and self.historico[1] != self.historico[2] and \
               self.historico[0] == self.historico[2]: 
                sugestao_final_codigo = self.historico[1] # Sugere o oposto do atual
                motivo_principal.append(f"Padrão Zig-Zag: sugere alternância.")
                confianca_base = 50

            # Duplas repetidas (Ex: CCVV - se o mais recente é V, sugere V para continuar a dupla)
            elif len(self.historico) >= 4 and \
                   self.historico[0] == self.historico[1] and \
                   self.historico[2] == self.historico[3] and \
                   self.historico[0] != self.historico[2]:
                sugestao_final_codigo = self.historico[0] # Sugere a continuação da dupla atual
                motivo_principal.append(f"Padrão Duplas Repetidas: sugere a continuação da dupla atual.")
                confianca_base = 45
            
            # Empate Recorrente (se empates estão vindo em intervalos curtos - menos forte que Zona de Ocorrência)
            elif "Empate recorrente" in analise and analise["Empate recorrente"] and self.historico[0] != 'E':
                sugestao_final_codigo = 'E'
                motivo_principal.append("Padrão Empate Recorrente: sugere que um Empate pode surgir em breve.")
                confianca_base = 40

        # --- Etapa 3: Prioridade Baixa (Menor Frequência - Somente se NENHUMA sugestão foi feita antes) ---
        if sugestao_final_codigo is None:
            frequencias = self.calcular_frequencias()
            opcoes = ["V", "C", "E"]
            
            # Encontra a opção com a menor frequência
            menor_freq_val = float('inf')
            candidatos_menor_freq = []

            for op in opcoes:
                freq_atual = frequencias.get(op, 0)
                if freq_atual < menor_freq_val:
                    menor_freq_val = freq_atual
                    candidatos_menor_freq = [op] 
                elif freq_atual == menor_freq_val:
                    candidatos_menor_freq.append(op) 

            sugestao_final_codigo = random.choice(candidatos_menor_freq) 
            motivo_principal.append(f"Sugestão baseada na menor frequência de ocorrência no histórico geral.")
            confianca_base = 30 # Confiança mais baixa para esta estratégia

        # --- Finalização da Sugestão ---
        if sugestao_final_codigo:
            mapeamento = {"C": "Casa", "V": "Visitante", "E": "Empate"}
            entrada_legivel = mapeamento[sugestao_final_codigo]

            # A confiança final é a confiança base do padrão que gerou a sugestão
            # Não adicionamos mais bônus de outros padrões para evitar a "mistura"
            confianca_final = min(90, max(0, confianca_base))

            return {
                "sugerir": True,
                "entrada": entrada_legivel,
                "entrada_codigo": sugestao_final_codigo,
                "motivos": motivo_principal, # Apenas o motivo principal
                "confianca": confianca_final,
                "frequencias": self.calcular_frequencias(),
                "ultimos_resultados": self.historico[:3]
            }
        else:
            return {
                "sugerir": False,
                "entrada": None,
                "entrada_codigo": None,
                "motivos": ["Não foi possível gerar uma sugestão clara com os padrões atuais."],
                "confianca": 0,
                "frequencias": self.calcular_frequencias(),
                "ultimos_resultados": self.historico[:3]
            }

# --- FUNÇÕES DE INTERFACE E LÓGICA DE HISTÓRICO (COM MODIFICAÇÕES PARA ESTATÍSTICAS) ---

# Inicializa o estado da sessão para armazenar o histórico e as estatísticas
if 'historico' not in st.session_state:
    st.session_state.historico = []
    st.session_state.hits = 0
    st.session_state.misses = 0
    st.session_state.last_suggestion_made_code = None # Armazena a sugestão da rodada *anterior* para comparação
    st.session_state.g1_active = False # True se a sugestão anterior foi um erro (miss)
    st.session_state.g1_hits = 0
    st.session_state.g1_attempts = 0 # Contabiliza quando uma aposta G1 foi feita

def adicionar_resultado(resultado):
    # 1. Avalia a sugestão da *rodada anterior* com o *resultado atual* que está sendo inserido
    # Esta lógica só é executada se havia uma sugestão pendente para avaliação
    if st.session_state.last_suggestion_made_code is not None:
        previous_suggestion = st.session_state.last_suggestion_made_code
        
        if resultado == previous_suggestion:
            st.session_state.hits += 1
            if st.session_state.g1_active: # Se o G1 estava ativo, significa que a aposta anterior foi errada e esta acertou
                st.session_state.g1_hits += 1
            st.session_state.g1_active = False # Reset G1 active status se a aposta foi um acerto
        else: # A sugestão anterior foi um erro
            st.session_state.misses += 1
            st.session_state.g1_active = True # Ativa o G1 para a *próxima* sugestão (que será a G1 attempt)

    # 2. Adiciona o novo resultado ao histórico principal
    st.session_state.historico.insert(0, resultado)
    if len(st.session_state.historico) > 27:
        st.session_state.historico = st.session_state.historico[:27]

    # 3. Limpa a última sugestão avaliada. Uma nova sugestão será gerada *após* a atualização do histórico.
    st.session_state.last_suggestion_made_code = None

def limpar_historico():
    st.session_state.historico = []
    # Reseta todas as estatísticas ao limpar o histórico
    st.session_state.hits = 0
    st.session_state.misses = 0
    st.session_state.last_suggestion_made_code = None
    st.session_state.g1_active = False
    st.session_state.g1_hits = 0
    st.session_state.g1_attempts = 0

def desfazer_ultimo():
    if st.session_state.historico:
        # Simplificando: desfazer não ajusta as estatísticas de acerto/erro, apenas o histórico.
        # Para uma lógica completa, teríamos que armazenar o estado das estatísticas a cada rodada.
        # Por simplicidade, Limpar Histórico deve ser usado para resetar as estatísticas.
        st.session_state.historico.pop(0)
        # Se desfizer o último resultado, a sugestão pendente para ele também é invalidada
        st.session_state.last_suggestion_made_code = None 

def get_resultado_html(resultado):
    color_map = {'C': 'red', 'V': 'blue', 'E': 'gold'}
    return f"<span style='display:inline-block; width:20px; height:20px; border-radius:50%; background-color:{color_map.get(resultado, 'gray')}; margin:2px; vertical-align:middle;'></span>"

# --- CONFIGURAÇÃO DA PÁGINA STREAMLIT ---
st.set_page_config(layout="wide", page_title="Análise de Padrões de Jogos")

st.title("⚽ Análise de Padrões de Resultados")
st.markdown("---")

# --- CSS PARA BOTÕES COLORIDOS ---
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
    if st.button("Limpar Histórico", help="Apaga todos os resultados do histórico e as estatísticas", key="Limpar Histórico", use_container_width=True):
        limpar_historico()

st.markdown("---")

# --- LÓGICA DE ANÁLISE E SUGESTÃO ---
if len(st.session_state.historico) >= 9:
    app_analise = AnalisePadroes(st.session_state.historico)
    sugestao = app_analise.sugestao_inteligente()

    st.header("💡 Sugestão Inteligente para o Próximo Jogo")

    if sugestao['sugerir']:
        st.write(f"Considerando os padrões e frequências do histórico atual:")
        st.success(f"**Sugestão:** Próximo resultado provável: **{sugestao['entrada']}**")
        st.metric(label="Confiança da Sugestão", value=f"{sugestao['confianca']}%")
        # A lista de motivos agora é 'motivo_principal' e mais concisa
        st.info(f"**Motivos:** {', '.join(sugestao['motivos'])}")
        st.markdown(f"Últimos 3 resultados analisados (mais novo à esquerda): `{', '.join(sugestao['ultimos_resultados'])}`")
        
        # Salva a sugestão feita para ser avaliada na próxima inserção de resultado
        st.session_state.last_suggestion_made_code = sugestao['entrada_codigo']
        
        # Se o G1 está ativo (sugestão anterior foi um erro), contabiliza como tentativa de G1
        if st.session_state.g1_active:
            st.session_state.g1_attempts += 1 # Conta a tentativa G1 aqui, pois a sugestão foi gerada
    else:
        st.warning(f"**Sem sugestão:** {sugestao['motivos'][0]}")
        # Se não há sugestão, limpa a última sugestão para evitar avaliação incorreta
        st.session_state.last_suggestion_made_code = None 

    st.markdown("---")

# --- EXIBIÇÃO DO HISTÓRICO ---
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

# --- PADRÕES DETECTADOS E FREQUÊNCIA ---
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

# --- SEÇÃO DE RESUMO DE ACERTOS E ERROS ---
st.markdown("---")
st.subheader("📊 Resumo de Acertos e Erros")

total_suggestions_evaluated = st.session_state.hits + st.session_state.misses
taxa_acerto = (st.session_state.hits / total_suggestions_evaluated * 100) if total_suggestions_evaluated > 0 else 0

col_stats1, col_stats2, col_stats3 = st.columns(3)

with col_stats1:
    st.metric(label="Acertos (Total)", value=st.session_state.hits)
    st.metric(label="Taxa de Acerto Geral", value=f"{taxa_acerto:.2f}%")
with col_stats2:
    st.metric(label="Erros (Total)", value=st.session_state.misses)
    # Exibe o status do G1
    st.markdown(f"Status G1: {'**Ativo**' if st.session_state.g1_active else 'Inativo'}") 
with col_stats3:
    st.metric(label="G1 Acertos", value=st.session_state.g1_hits)
    st.metric(label="G1 Tentativas", value=st.session_state.g1_attempts)

if total_suggestions_evaluated == 0:
    st.info("Insira resultados e aguarde as sugestões para ver o resumo de acertos/erros.")
