import streamlit as st
import collections
import random
import numpy as np
from datetime import datetime
import pandas as pd

# --- CLASSE ANALISEPADROES REFINADA (SEU CÓDIGO INTACTO) ---
class AnalisePadroes:
    def __init__(self, historico):
        self.historico = historico[:50]  # Aumentado para 50 jogos para melhor análise
        self.padroes_ativos = {
            # Padrões básicos existentes
            "Sequência (Surf de Cor)": self._sequencia_simples,
            "Zig-Zag Perfeito": self._zig_zag,
            "Quebra de Surf": self._quebra_de_surf,
            "Quebra de Zig-Zag": self._quebra_de_zig_zag,
            "Duplas Repetidas": self._duplas_repetidas,
            "Empate Recorrente": self._empate_recorrente,
            "Padrão Escada": self._padrao_escada,
            "Espelho": self._espelho,
            "Alternância com Empate": self._alternancia_empate_meio,
            "Padrão Onda": self._padrao_onda,
            
            # Novos padrões específicos do Football Studio
            "Padrão Fibonacci": self._padrao_fibonacci,
            "Sequência Dourada": self._sequencia_dourada,
            "Padrão Triangular": self._padrao_triangular,
            "Ciclo de Empates": self._ciclo_empates,
            "Padrão Martingale": self._padrao_martingale,
            "Sequência de Fibonacci Invertida": self._fibonacci_invertida,
            "Padrão Dragon Tiger": self._padrao_dragon_tiger,
            "Sequência de Paroli": self._sequencia_paroli,
            "Padrão de Ondas Longas": self._ondas_longas,
            "Ciclo de Dominância": self._ciclo_dominancia,
            "Padrão de Tensão": self._padrao_tensao,
            "Sequência de Labouchere": self._sequencia_labouchere,
            "Padrão Ritmo Cardíaco": self._ritmo_cardiaco,
            "Ciclo de Pressão": self._ciclo_pressao,
            "Padrão de Clusters": self._padrao_clusters,
            "Sequência Polar": self._sequencia_polar,
            "Padrão de Momentum": self._padrao_momentum,
            "Ciclo de Respiração": self._ciclo_respiracao,
            "Padrão de Resistência": self._padrao_resistencia,
            "Sequência de Breakout": self._sequencia_breakout,
        }
        
        # Pesos dos padrões para calcular confiança
        self.pesos_padroes = {
            "Sequência (Surf de Cor)": 0.9,
            "Zig-Zag Perfeito": 0.8,
            "Quebra de Surf": 0.85,
            "Quebra de Zig-Zag": 0.8,
            "Padrão Fibonacci": 0.95,
            "Sequência Dourada": 0.9,
            "Padrão Dragon Tiger": 0.85,
            "Ciclo de Dominância": 0.8,
            "Padrão de Momentum": 0.9,
            "Sequência de Breakout": 0.95,
        }

    def analisar_todos(self):
        resultados = {}
        for nome, func in self.padroes_ativos.items():
            try:
                resultados[nome] = func()
            except Exception as e:
                # Opcional: st.warning(f"Erro ao analisar padrão '{nome}': {e}")
                resultados[nome] = False
        return resultados

    # --- PADRÕES BÁSICOS EXISTENTES ---
    def _sequencia_simples(self):
        for i in range(len(self.historico) - 2):
            if self.historico[i] == self.historico[i+1] == self.historico[i+2]:
                return True
        return False

    def _zig_zag(self):
        if len(self.historico) < 6:
            return False
        count = 0
        for i in range(len(self.historico) - 1):
            if self.historico[i] != self.historico[i+1]:
                count += 1
            else:
                if count >= 5:
                    return True
                count = 0
        return count >= 5

    def _quebra_de_surf(self):
        for i in range(len(self.historico) - 3):
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] and 
                self.historico[i+2] != self.historico[i+3]):
                return True
        return False

    def _quebra_de_zig_zag(self):
        if len(self.historico) < 5:
            return False
        for i in range(len(self.historico) - 4):
            if (self.historico[i] != self.historico[i+1] != self.historico[i+2] and 
                self.historico[i+2] == self.historico[i+3]):
                return True
        return False

    def _duplas_repetidas(self):
        if len(self.historico) < 4:
            return False
        for i in range(len(self.historico) - 3):
            if (self.historico[i] == self.historico[i+1] and 
                self.historico[i+2] == self.historico[i+3] and 
                self.historico[i] != self.historico[i+2]):
                return True
        return False

    def _empate_recorrente(self):
        empates_indices = [i for i, r in enumerate(self.historico) if r == 'E']
        if len(empates_indices) < 3:
            return False
        
        # Verifica se há um padrão de intervalos regulares entre empates
        intervalos = []
        for i in range(len(empates_indices) - 1):
            intervalos.append(empates_indices[i+1] - empates_indices[i])
        
        if len(intervalos) >= 2:
            # Verifica se os intervalos seguem um padrão
            media_intervalo = sum(intervalos) / len(intervalos)
            return 2 <= media_intervalo <= 8
        return False

    def _padrao_escada(self):
        if len(self.historico) < 6:
            return False
        for i in range(len(self.historico) - 5):
            if (self.historico[i] != self.historico[i+1] == self.historico[i+2] and
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] and
                self.historico[i+1] != self.historico[i+3]):
                return True
        return False

    def _espelho(self):
        if len(self.historico) < 4:
            return False
        for tamanho in range(4, min(len(self.historico) + 1, 13)):
            if tamanho % 2 == 0:
                metade = tamanho // 2
                for start in range(len(self.historico) - tamanho + 1):
                    primeira_metade = self.historico[start:start + metade]
                    segunda_metade = self.historico[start + metade:start + tamanho]
                    if primeira_metade == segunda_metade[::-1]:
                        return True
        return False

    def _alternancia_empate_meio(self):
        if len(self.historico) < 3:
            return False
        for i in range(len(self.historico) - 2):
            if (self.historico[i] != 'E' and self.historico[i+1] == 'E' and 
                self.historico[i+2] != 'E' and self.historico[i] != self.historico[i+2]):
                return True
        return False

    def _padrao_onda(self):
        if len(self.historico) < 6:
            return False
        for i in range(len(self.historico) - 5):
            if (self.historico[i] == self.historico[i+2] == self.historico[i+4] and
                self.historico[i+1] == self.historico[i+3] == self.historico[i+5] and
                self.historico[i] != self.historico[i+1]):
                return True
        return False

    # --- NOVOS PADRÕES ESPECÍFICOS DO FOOTBALL STUDIO ---
    
    def _padrao_fibonacci(self):
        """Detecta padrões baseados na sequência de Fibonacci"""
        if len(self.historico) < 8:
            return False
        
        fib_sequence = [1, 1, 2, 3, 5, 8]
        
        for i in range(len(self.historico) - 7):
            # Verifica se há uma sequência que segue o padrão Fibonacci
            segment = self.historico[i:i+6]
            pattern_found = True
            
            for j in range(len(fib_sequence)):
                expected_count = fib_sequence[j]
                actual_segment = segment[sum(fib_sequence[:j]):sum(fib_sequence[:j+1])] if j < len(fib_sequence)-1 else segment[sum(fib_sequence[:j]):]
                
                if len(actual_segment) != expected_count:
                    pattern_found = False
                    break
                    
                if not all(x == actual_segment[0] for x in actual_segment):
                    pattern_found = False
                    break
            
            if pattern_found:
                return True
        return False

    def _sequencia_dourada(self):
        """Detecta sequências baseadas na proporção áurea"""
        if len(self.historico) < 8:
            return False
        
        # Padrão dourado: 3, 5, 8, 13...
        for i in range(len(self.historico) - 7):
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] and
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] == self.historico[i+6] == self.historico[i+7] and
                self.historico[i] != self.historico[i+3]):
                return True
        return False

    def _padrao_triangular(self):
        """Detecta padrões triangulares: 1, 2, 3, 2, 1"""
        if len(self.historico) < 9:
            return False
        
        for i in range(len(self.historico) - 8):
            segment = self.historico[i:i+9]
            if (segment[0] == segment[8] and 
                segment[1] == segment[7] and 
                segment[2] == segment[6] and 
                segment[3] == segment[5] and
                len(set(segment[2:7])) == 1 and
                segment[0] != segment[4]):
                return True
        return False

    def _ciclo_empates(self):
        """Detecta ciclos específicos de empates"""
        empates = [i for i, x in enumerate(self.historico) if x == 'E']
        if len(empates) < 3:
            return False
        
        # Verifica se empates aparecem em intervalos cíclicos
        for cycle_length in range(3, 10):
            cycle_found = True
            for i in range(len(empates) - 1):
                if i + cycle_length < len(empates):
                    expected_pos = empates[i] + cycle_length
                    actual_pos = empates[i + 1] if i + 1 < len(empates) else None
                    if actual_pos and abs(expected_pos - actual_pos) > 2:
                        cycle_found = False
                        break
            if cycle_found and len(empates) >= 3:
                return True
        return False

    def _padrao_martingale(self):
        """Detecta padrões de duplicação (Martingale)"""
        if len(self.historico) < 7:
            return False
        
        for i in range(len(self.historico) - 6):
            # Padrão: 1, 2, 4 (1 resultado, 2 iguais, 4 iguais)
            if (self.historico[i] != self.historico[i+1] and
                self.historico[i+1] == self.historico[i+2] and
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] == self.historico[i+6] and
                self.historico[i+1] != self.historico[i+3]):
                return True
        return False

    def _fibonacci_invertida(self):
        """Detecta Fibonacci invertida"""
        if len(self.historico) < 8:
            return False
        
        # Padrão: 8, 5, 3, 2, 1, 1
        for i in range(len(self.historico) - 7):
            segment = self.historico[i:i+8]
            if (len(set(segment[:2])) == 1 and  # 8 primeiros iguais (simulando)
                segment[2] != segment[0] and
                segment[3] == segment[4] and
                segment[5] != segment[6] and
                segment[6] == segment[7]):
                return True
        return False

    def _padrao_dragon_tiger(self):
        """Padrão específico de Dragon Tiger adaptado"""
        if len(self.historico) < 6:
            return False
        
        for i in range(len(self.historico) - 5):
            # Padrão: Alternância forte seguida de empate
            if (self.historico[i] != self.historico[i+1] != self.historico[i+2] and
                self.historico[i+3] == 'E' and
                self.historico[i+4] == self.historico[i+5] and
                self.historico[i+4] != 'E'):
                return True
        return False

    def _sequencia_paroli(self):
        """Detecta padrões de progressão positiva"""
        if len(self.historico) < 7:
            return False
        
        for i in range(len(self.historico) - 6):
            # Padrão: 1, 2, 4, volta ao 1
            if (self.historico[i] != self.historico[i+1] and
                self.historico[i+1] == self.historico[i+2] and
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] == self.historico[i+6] and
                self.historico[i] == self.historico[i+3]):
                return True
        return False

    def _ondas_longas(self):
        """Detecta ondas longas (sequências de 5+ do mesmo resultado)"""
        if len(self.historico) < 5:
            return False
        
        count = 1
        for i in range(1, len(self.historico)):
            if self.historico[i] == self.historico[i-1]:
                count += 1
                if count >= 5:
                    return True
            else:
                count = 1
        return False

    def _ciclo_dominancia(self):
        """Detecta ciclos de dominância de um resultado"""
        if len(self.historico) < 10:
            return False
        
        # Analisa janelas de 10 resultados
        for i in range(len(self.historico) - 9):
            window = self.historico[i:i+10]
            counter = collections.Counter(window)
            
            # Verifica se um resultado domina (70%+)
            for resultado, count in counter.items():
                if count >= 7:
                    return True
        return False

    def _padrao_tensao(self):
        """Detecta padrões de tensão (alternância seguida de explosão)"""
        if len(self.historico) < 8:
            return False
        
        for i in range(len(self.historico) - 7):
            # Padrão: 4+ alternâncias seguidas de sequência
            alternations = 0
            for j in range(i, i+4):
                if j+1 < len(self.historico) and self.historico[j] != self.historico[j+1]:
                    alternations += 1
            
            if alternations >= 3:
                # Verifica se há sequência após as alternâncias
                if (i+5 < len(self.historico) and 
                    self.historico[i+4] == self.historico[i+5] == self.historico[i+6]):
                    return True
        return False

    def _sequencia_labouchere(self):
        """Detecta padrões de cancelamento"""
        if len(self.historico) < 6:
            return False
        
        for i in range(len(self.historico) - 5):
            # Padrão: início e fim iguais, meio diferente
            if (self.historico[i] == self.historico[i+5] and
                self.historico[i+1] == self.historico[i+4] and
                self.historico[i+2] != self.historico[i] and
                self.historico[i+3] != self.historico[i]):
                return True
        return False

    def _ritmo_cardiaco(self):
        """Detecta padrões de ritmo cardíaco (batimentos irregulares)"""
        if len(self.historico) < 8:
            return False
        
        for i in range(len(self.historico) - 7):
            # Padrão: 2, 1, 2, 3, 2, 1, 2
            segment = self.historico[i:i+8]
            if (segment[0] == segment[1] and
                segment[2] != segment[0] and
                segment[3] == segment[4] and
                segment[5] == segment[6] == segment[7] and
                segment[3] != segment[5]):
                return True
        return False

    def _ciclo_pressao(self):
        """Detecta ciclos de pressão crescente"""
        if len(self.historico) < 9:
            return False
        
        for i in range(len(self.historico) - 8):
            # Padrão: 1, 2, 3, 1, 2, 3
            if (self.historico[i] != self.historico[i+1] and
                self.historico[i+1] == self.historico[i+2] and
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] and
                self.historico[i+6] == self.historico[i] and
                self.historico[i+7] == self.historico[i+8]):
                return True
        return False

    def _padrao_clusters(self):
        """Detecta agrupamentos (clusters) de resultados"""
        if len(self.historico) < 12:
            return False
        
        # Analisa janelas de 12 para encontrar clusters
        for i in range(len(self.historico) - 11):
            window = self.historico[i:i+12]
            
            # Divide em 3 clusters de 4
            cluster1 = window[:4]
            cluster2 = window[4:8]
            cluster3 = window[8:12]
            
            # Verifica se cada cluster tem dominância (3+ iguais)
            if (collections.Counter(cluster1).most_common(1)[0][1] >= 3 and
                collections.Counter(cluster2).most_common(1)[0][1] >= 3 and
                collections.Counter(cluster3).most_common(1)[0][1] >= 3):
                return True
        return False

    def _sequencia_polar(self):
        """Detecta sequências polares (extremos)"""
        if len(self.historico) < 10:
            return False
        
        for i in range(len(self.historico) - 9):
            window = self.historico[i:i+10]
            
            # Verifica se há polarização (só 2 tipos de resultado, sem empates)
            unique_results = set(window)
            if len(unique_results) == 2 and 'E' not in unique_results:
                # Verifica alternância polar
                changes = sum(1 for j in range(len(window)-1) if window[j] != window[j+1])
                if changes >= 6:  # Muitas mudanças
                    return True
        return False

    def _padrao_momentum(self):
        """Detecta padrões de momentum (aceleração)"""
        if len(self.historico) < 10:
            return False
        
        for i in range(len(self.historico) - 9):
            # Padrão: 1, 2, 3, 4 (crescimento)
            if (self.historico[i] != self.historico[i+1] and
                self.historico[i+1] == self.historico[i+2] and
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] and
                self.historico[i+6] == self.historico[i+7] == self.historico[i+8] == self.historico[i+9]):
                return True
        return False

    def _ciclo_respiracao(self):
        """Detecta padrões de respiração (inspiração/expiração)"""
        if len(self.historico) < 8:
            return False
        
        for i in range(len(self.historico) - 7):
            # Padrão: expansão e contração
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] == self.historico[i+3] and
                self.historico[i+4] != self.historico[i] and
                self.historico[i+5] == self.historico[i+6] == self.historico[i+7] and
                self.historico[i+5] != self.historico[i+4]):
                return True
        return False

    def _padrao_resistencia(self):
        """Detecta padrões de resistência (tentativas de quebra)"""
        if len(self.historico) < 6:
            return False
        
        for i in range(len(self.historico) - 5):
            # Padrão: resultado dominante resiste a mudanças
            if (self.historico[i] == self.historico[i+2] == self.historico[i+4] == self.historico[i+5] and
                self.historico[i+1] != self.historico[i] and
                self.historico[i+3] != self.historico[i]):
                return True
        return False

    def _sequencia_breakout(self):
        """Detecta sequências de breakout (quebra de padrão)"""
        if len(self.historico) < 8:
            return False
        
        for i in range(len(self.historico) - 7):
            # Padrão: estabilidade seguida de mudança abrupta
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] == self.historico[i+3] and
                self.historico[i+4] != self.historico[i] and
                self.historico[i+5] == self.historico[i+6] == self.historico[i+7] and
                self.historico[i+5] == self.historico[i+4]):
                return True
        return False

# --- CÓDIGO STREAMLIT PARA EXIBIÇÃO ---

st.set_page_config(layout="wide") # Opcional: para usar mais largura da tela

st.title("Análise de Padrões Football Studio")

# Simulação de histórico de resultados (substitua isso pelos seus dados reais)
# Para fins de teste, estou gerando um histórico aleatório.
if 'historico' not in st.session_state:
    st.session_state.historico = collections.deque(maxlen=50) # Usar deque para performance

# Adiciona alguns resultados de exemplo ao histórico
# No seu caso real, isso viria de uma API ou outra fonte de dados
if st.button("Adicionar Novo Resultado (Aleatório para Teste)"):
    possiveis_resultados = ['V', 'C', 'E'] # V = Vitória (Home), C = Convidado (Away), E = Empate (Tie)
    novo_resultado = random.choice(possiveis_resultados)
    st.session_state.historico.appendleft(novo_resultado) # Adiciona no início para o mais recente à esquerda

# Converte o deque para uma lista para a análise da classe
historico_lista = list(st.session_state.historico)

# Instancia a classe de análise
analisador = AnalisePadroes(historico_lista)

# Analisa os padrões
padroes_encontrados = analisador.analisar_todos()

# --- EXIBIÇÃO DO HISTÓRICO CORRIGIDA ---
st.subheader("Últimos Resultados (mais recente à esquerda):")

# Dicionário para mapear resultados a cores
cores = {
    'V': '#FF4B4B',  # Vermelho (similar ao 'C' na sua imagem, mas estou usando para 'V' = Home)
    'C': '#007bff',  # Azul (similar ao 'V' na sua imagem, mas estou usando para 'C' = Away)
    'E': '#6c757d'   # Cinza para Empate
}

# Inverte o histórico para que o mais recente (que foi adicionado com appendleft)
# seja o primeiro a ser processado para exibição da esquerda para a direita.
# No entanto, se você adiciona com append(), não precisaria inverter aqui.
# A imagem que você mostrou tem 'V' na esquerda (mais recente) e depois 'E', 'C', etc.
# Se `st.session_state.historico` já está do mais recente para o mais antigo,
# não precisamos do `reversed()`. Mas para garantir, vou usar a lista bruta
# e fazer a inversão necessária para a ordem de exibição.
historico_para_exibir = list(st.session_state.historico) # já está na ordem 'mais recente à esquerda' se appendleft foi usado

# Gera a string HTML para os círculos do histórico
html_historico = "<div style='display: flex; flex-wrap: wrap; gap: 5px;'>" # Flexbox para alinhar na linha e quebrar se necessário
for resultado in historico_para_exibir:
    cor_fundo = cores.get(resultado, '#cccccc') # Cor padrão se o resultado não for reconhecido
    html_historico += f"""
    <span style='
        display: inline-block;
        width: 25px;
        height: 25px;
        border-radius: 50%;
        background-color: {cor_fundo};
        color: white;
        text-align: center;
        line-height: 25px;
        font-weight: bold;
        font-size: 12px;
        border: 2px solid #333;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    '>{resultado}</span>
    """
html_historico += "</div>"

# Renderiza o HTML no Streamlit. O parâmetro unsafe_allow_html=True é CRUCIAL!
st.markdown(html_historico, unsafe_allow_html=True)

st.markdown("---") # Linha divisória

# --- EXIBIÇÃO DOS PADRÕES ENCONTRADOS ---
st.subheader("Padrões Encontrados:")
encontrou_algum_padrao = False
for padrao, encontrado in padroes_encontrados.items():
    if encontrado:
        st.success(f"✅ Padrão **'{padrao}'** encontrado!")
        encontrou_algum_padrao = True
if not encontrou_algum_padrao:
    st.info("Nenhum padrão detectado no histórico atual.")

st.markdown("---")

# Opcional: Mostrar o histórico em formato de tabela para depuração
# st.subheader("Histórico Completo (para depuração):")
# st.write(historico_lista)
