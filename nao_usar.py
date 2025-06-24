import streamlit as st
import collections
import random
import numpy as np
from datetime import datetime
import pandas as pd

# --- CLASSE ANALISEPADROES REFINADA ---
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
        
        # Pesos dos padrões para calcular confiança (você pode ajustar estes pesos)
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
            # Adicione pesos para todos os novos padrões se quiser que influenciem a confiança
            "Duplas Repetidas": 0.7,
            "Empate Recorrente": 0.75,
            "Padrão Escada": 0.6,
            "Espelho": 0.7,
            "Alternância com Empate": 0.65,
            "Padrão Onda": 0.7,
            "Padrão Triangular": 0.75,
            "Ciclo de Empates": 0.8,
            "Padrão Martingale": 0.8,
            "Sequência de Fibonacci Invertida": 0.85,
            "Sequência de Paroli": 0.7,
            "Padrão de Ondas Longas": 0.75,
            "Padrão de Tensão": 0.8,
            "Sequência de Labouchere": 0.6,
            "Padrão Ritmo Cardíaco": 0.7,
            "Ciclo de Pressão": 0.75,
            "Padrão de Clusters": 0.8,
            "Sequência Polar": 0.7,
            "Ciclo de Respiração": 0.65,
            "Padrão de Resistência": 0.7,
        }

    def analisar_todos(self):
        resultados = {}
        for nome, func in self.padroes_ativos.items():
            try:
                resultados[nome] = func()
            except Exception as e:
                #st.warning(f"Erro ao analisar padrão '{nome}': {e}") # Descomente para depurar
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
                if count >= 5: # Pelo menos 5 alternâncias para ser zig-zag
                    return True
                count = 0 # Resetar se houver repetição
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
        # Alternância seguida de repetição
        for i in range(len(self.historico) - 4):
            if (self.historico[i] != self.historico[i+1] and # A != B
                self.historico[i+1] != self.historico[i+2] and # B != C
                self.historico[i+2] == self.historico[i+3]): # C == D (quebra o zig-zag)
                return True
        return False

    def _duplas_repetidas(self):
        if len(self.historico) < 4:
            return False
        for i in range(len(self.historico) - 3):
            if (self.historico[i] == self.historico[i+1] and 
                self.historico[i+2] == self.historico[i+3] and 
                self.historico[i] != self.historico[i+2]): # ex: CCVV
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
            # Verifica se os intervalos seguem um padrão (ex: 3, 3, 3 ou 4, 4, 4)
            primeiro_intervalo = intervalos[0]
            if all(abs(intervalo - primeiro_intervalo) <= 1 for intervalo in intervalos): # Permite pequena variação
                return True
        return False

    def _padrao_escada(self):
        if len(self.historico) < 6:
            return False
        for i in range(len(self.historico) - 5):
            # Ex: C V V C C C (1, 2, 3) - C é diferente de V
            if (self.historico[i] != self.historico[i+1] and # C (1)
                self.historico[i+1] == self.historico[i+2] and # VV (2)
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] and # CCC (3)
                self.historico[i+1] != self.historico[i+3]): # V != C
                return True
        return False

    def _espelho(self):
        if len(self.historico) < 4:
            return False
        # Procura por sequências que são um espelho de si mesmas (ex: CVVC, CEEC, etc.)
        for tamanho in range(4, min(len(self.historico) + 1, 13)): # Espelhos de 4 a 12 resultados
            if tamanho % 2 == 0:
                metade = tamanho // 2
                for start in range(len(self.historico) - tamanho + 1):
                    primeira_metade = self.historico[start:start + metade]
                    segunda_metade = self.historico[start + metade:start + tamanho]
                    if primeira_metade == segunda_metade[::-1]: # Compara a primeira metade com a segunda invertida
                        return True
        return False

    def _alternancia_empate_meio(self):
        if len(self.historico) < 3:
            return False
        for i in range(len(self.historico) - 2):
            if (self.historico[i] != 'E' and self.historico[i+1] == 'E' and 
                self.historico[i+2] != 'E' and self.historico[i] != self.historico[i+2]): # Ex: C E V
                return True
        return False

    def _padrao_onda(self):
        if len(self.historico) < 6:
            return False
        for i in range(len(self.historico) - 5):
            # Ex: C V C V C V
            if (self.historico[i] == self.historico[i+2] == self.historico[i+4] and
                self.historico[i+1] == self.historico[i+3] == self.historico[i+5] and
                self.historico[i] != self.historico[i+1]):
                return True
        return False

    # --- NOVOS PADRÕES ESPECÍFICOS DO FOOTBALL STUDIO ---
    
    def _padrao_fibonacci(self):
        """Detecta padrões de contagem de sequências baseados na sequência de Fibonacci"""
        if len(self.historico) < 8: # Mínimo para ver 1,1,2,3
            return False
        
        fib_sequence = [1, 1, 2, 3, 5] # Usar até 5 para ser detectável em historico de 50
        
        # Procura por sequências de resultados que seguem o comprimento de Fibonacci
        for i in range(len(self.historico) - sum(fib_sequence) + 1): # Garante que há espaço para a sequência
            current_pos = i
            pattern_match = True
            
            for length in fib_sequence:
                if current_pos + length > len(self.historico):
                    pattern_match = False
                    break
                
                segment = self.historico[current_pos : current_pos + length]
                if not all(x == segment[0] for x in segment): # Verifica se o segmento tem resultados iguais
                    pattern_match = False
                    break
                current_pos += length
            
            if pattern_match:
                return True
        return False

    def _sequencia_dourada(self):
        """Detecta sequências de 3 e 5 do mesmo tipo (aproximação da proporção áurea)"""
        if len(self.historico) < 8:
            return False
        
        for i in range(len(self.historico) - 7):
            # Ex: CCC VVVVV (3 de um, 5 de outro, ou vice-versa, sem ser E)
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] and
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] == self.historico[i+6] == self.historico[i+7] and
                self.historico[i] != self.historico[i+3] and 'E' not in [self.historico[i], self.historico[i+3]]):
                return True
        return False

    def _padrao_triangular(self):
        """Detecta padrões triangulares: 1, 2, 3, 2, 1 (simétrico)"""
        if len(self.historico) < 9:
            return False
        
        for i in range(len(self.historico) - 8):
            s = self.historico[i:i+9]
            if (s[0] == s[8] and s[1] == s[7] and s[2] == s[6] and s[3] == s[5] and
                s[0] != s[1] and s[1] != s[2] and s[2] != s[3] and # garantir que os 'níveis' são diferentes
                len(set(s[2:7])) == 1 and # Centro homogêneo (o 3)
                s[3] != s[4]): # O pico '4' diferente dos lados '3'
                return True
        return False

    def _ciclo_empates(self):
        """Detecta ciclos específicos de empates (E no mesmo intervalo)"""
        empates_indices = [i for i, x in enumerate(self.historico) if x == 'E']
        if len(empates_indices) < 3:
            return False
        
        # Verifica se empates aparecem em intervalos cíclicos, e.g., a cada 5, 7 ou 9 jogos
        for cycle_length in range(5, 10): # Ciclos de 5 a 9 jogos
            found_cycle = True
            if len(empates_indices) > 1:
                # Considera o último intervalo como base
                base_interval = empates_indices[-1] - empates_indices[-2]
                if not (cycle_length - 2 <= base_interval <= cycle_length + 2): # Permite variação de +-2
                    found_cycle = False
            
            # Verifica se os últimos N empates mantêm um intervalo aproximado
            if found_cycle and len(empates_indices) >= 3:
                for j in range(len(empates_indices) - 2):
                    interval1 = empates_indices[j+1] - empates_indices[j]
                    interval2 = empates_indices[j+2] - empates_indices[j+1]
                    if not (abs(interval1 - cycle_length) <= 2 and abs(interval2 - cycle_length) <= 2):
                        found_cycle = False
                        break
            if found_cycle:
                return True
        return False

    def _padrao_martingale(self):
        """Detecta padrões de duplicação: 1, 2, 4 (Ex: C, VV, CCCC)"""
        if len(self.historico) < 7:
            return False
        
        for i in range(len(self.historico) - 6):
            if (self.historico[i] != self.historico[i+1] and # C (1)
                self.historico[i+1] == self.historico[i+2] and # VV (2)
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] == self.historico[i+6] and # CCCC (4)
                self.historico[i+1] != self.historico[i+3] and 'E' not in [self.historico[i], self.historico[i+1], self.historico[i+3]]): # C!=V e V!=C e sem Empate
                return True
        return False

    def _fibonacci_invertida(self):
        """Detecta Fibonacci invertida: 5, 3, 2, 1, 1"""
        if len(self.historico) < 12: # Pelo menos 5+3+2+1+1=12
            return False
        
        fib_sequence_rev = [5, 3, 2, 1, 1]
        
        for i in range(len(self.historico) - sum(fib_sequence_rev) + 1):
            current_pos = i
            pattern_match = True
            
            for length in fib_sequence_rev:
                if current_pos + length > len(self.historico):
                    pattern_match = False
                    break
                
                segment = self.historico[current_pos : current_pos + length]
                if not all(x == segment[0] for x in segment):
                    pattern_match = False
                    break
                current_pos += length
            
            if pattern_match:
                return True
        return False

    def _padrao_dragon_tiger(self):
        """Padrão de alternância forte com empate no meio ou no fim."""
        if len(self.historico) < 6:
            return False
        
        for i in range(len(self.historico) - 5):
            # Ex: C V C V E V (Alternância, empate, alternância)
            if (self.historico[i] != self.historico[i+1] and
                self.historico[i+1] != self.historico[i+2] and
                self.historico[i+2] != self.historico[i+3] and # Três alternâncias
                self.historico[i+3] == 'E' and # Seguido por empate
                self.historico[i+4] != 'E' and self.historico[i+5] != 'E' and
                self.historico[i+4] != self.historico[i+5]): # E depois alternância novamente
                return True
        return False

    def _sequencia_paroli(self):
        """Detecta padrões de progressão positiva: 1, 2, 4 (mas com repetição)"""
        if len(self.historico) < 7:
            return False
        
        for i in range(len(self.historico) - 6):
            # Ex: C V V C C C C (1, 2, 4 - mas volta ao tipo inicial)
            if (self.historico[i] == self.historico[i+3] and # Tipo inicial e tipo 4 iguais
                self.historico[i] != self.historico[i+1] and # Tipo 1 diferente do 2
                self.historico[i+1] == self.historico[i+2] and # Tipo 2 e 3 são iguais
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] == self.historico[i+6]): # Tipos 4,5,6,7 são iguais
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
                if count >= 5: # 5 ou mais resultados iguais
                    return True
            else:
                count = 1
        return False

    def _ciclo_dominancia(self):
        """Detecta ciclos de dominância de um resultado (80% da janela)"""
        if len(self.historico) < 10:
            return False
        
        for i in range(len(self.historico) - 9):
            window = self.historico[i:i+10]
            counter = collections.Counter(window)
            
            # Verifica se um resultado domina (80% ou mais)
            for resultado, count in counter.items():
                if count >= 8 and resultado != 'E': # 8 de 10 não pode ser empate
                    return True
        return False

    def _padrao_tensao(self):
        """Detecta padrões de tensão (alternância seguida de explosão)"""
        if len(self.historico) < 8:
            return False
        
        for i in range(len(self.historico) - 7):
            # Padrão: 3 alternâncias (abaixo) seguidas de 3 sequenciais (explosão)
            # Ex: C V C V | C C C
            if (self.historico[i] != self.historico[i+1] and 
                self.historico[i+1] != self.historico[i+2] and 
                self.historico[i+2] != self.historico[i+3] and # Alternância de 4
                self.historico[i+4] == self.historico[i+5] == self.historico[i+6]): # Sequência de 3
                return True
        return False

    def _sequencia_labouchere(self):
        """Detecta padrões de cancelamento (simetria com o centro diferente)"""
        if len(self.historico) < 6:
            return False
        
        for i in range(len(self.historico) - 5):
            # Ex: C V E E V C (primeiro e último iguais, segundo e penúltimo iguais, centro diferente)
            if (self.historico[i] == self.historico[i+5] and
                self.historico[i+1] == self.historico[i+4] and
                self.historico[i+2] != self.historico[i+3] and # Centro diferente
                self.historico[i] != self.historico[i+1]): # Pontas diferentes do meio
                return True
        return False

    def _ritmo_cardiaco(self):
        """Detecta padrões de ritmo cardíaco (batimentos irregulares, 2-1-2-3)"""
        if len(self.historico) < 8:
            return False
        
        for i in range(len(self.historico) - 7):
            # Ex: C C V V V C C C (2 de um, 1 de outro, 2 de outro, 3 de outro)
            if (self.historico[i] == self.historico[i+1] and # 2
                self.historico[i+2] != self.historico[i] and # 1
                self.historico[i+3] == self.historico[i+4] and # 2
                self.historico[i+5] == self.historico[i+6] == self.historico[i+7] and # 3
                self.historico[i+2] != self.historico[i+3] and
                self.historico[i+3] != self.historico[i+5]): # Garantir que são blocos diferentes
                return True
        return False

    def _ciclo_pressao(self):
        """Detecta ciclos de pressão crescente (sequências que aumentam de tamanho)"""
        if len(self.historico) < 9:
            return False
        
        for i in range(len(self.historico) - 8):
            # Ex: C V V C C C V V V V (1, 2, 3, 4) ou (1, 2, 3, 1, 2, 3)
            # Aqui adaptando para um ciclo de 1,2,3 repetido
            if (self.historico[i] != self.historico[i+1] and
                self.historico[i+1] == self.historico[i+2] and
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] and
                self.historico[i+6] != self.historico[i+7] and # Recomeça o ciclo
                self.historico[i+7] == self.historico[i+8] and
                self.historico[i] == self.historico[i+6] and # Primeiro elemento do ciclo 1
                self.historico[i+1] == self.historico[i+7]): # Primeiro elemento do ciclo 2
                return True
        return False

    def _padrao_clusters(self):
        """Detecta agrupamentos (clusters) de resultados onde um tipo domina pequenas janelas"""
        if len(self.historico) < 12:
            return False
        
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
        """Detecta sequências polares (extremos, apenas C e V, com muitas mudanças)"""
        if len(self.historico) < 10:
            return False
        
        for i in range(len(self.historico) - 9):
            window = self.historico[i:i+10]
            
            # Verifica se há polarização (só 2 tipos de resultado, sem empates)
            unique_results = set(window)
            if len(unique_results) == 2 and 'E' not in unique_results:
                # Verifica alternância polar: muitas mudanças entre os dois tipos
                changes = sum(1 for j in range(len(window)-1) if window[j] != window[j+1])
                if changes >= 6:  # Mais da metade da janela é de mudanças (ex: CVCVCVCVCV)
                    return True
        return False

    def _padrao_momentum(self):
        """Detecta padrões de momentum (aceleração, sequências crescentes de repetições)"""
        if len(self.historico) < 10:
            return False
        
        for i in range(len(self.historico) - 9):
            # Ex: C V V C C C V V V V (1, 2, 3, 4 - crescimento do mesmo tipo)
            if (self.historico[i] != self.historico[i+1] and # C (1)
                self.historico[i+1] == self.historico[i+2] and # VV (2)
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] and # CCC (3)
                self.historico[i+6] == self.historico[i+7] == self.historico[i+8] == self.historico[i+9] and # VVVV (4)
                self.historico[i+1] != self.historico[i+3] and # Garantir que são diferentes
                self.historico[i+3] != self.historico[i+6]):
                return True
        return False

    def _ciclo_respiracao(self):
        """Detecta padrões de respiração (expansão/contração de resultados)"""
        if len(self.historico) < 8:
            return False
        
        for i in range(len(self.historico) - 7):
            # Ex: C C C C V V V C (4 de um, 3 de outro, 1 de outro)
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] == self.historico[i+3] and # 4
                self.historico[i+4] != self.historico[i] and # Mudança
                self.historico[i+4] == self.historico[i+5] == self.historico[i+6] and # 3
                self.historico[i+7] != self.historico[i+4]): # 1
                return True
        return False

    def _padrao_resistencia(self):
        """Detecta padrões de resistência (tentativas de quebra de uma sequência dominante)"""
        if len(self.historico) < 6:
            return False
        
        for i in range(len(self.historico) - 5):
            # Ex: C V C V C C (C tenta quebrar o padrão de alternância)
            if (self.historico[i] != self.historico[i+1] and
                self.historico[i+1] != self.historico[i+2] and
                self.historico[i+2] != self.historico[i+3] and # Zig-zag de 4 elementos
                self.historico[i+4] == self.historico[i+5] and # Quebra com 2 iguais
                self.historico[i+4] == self.historico[i+2]): # E o que quebra é igual a um anterior
                return True
        return False

    def _sequencia_breakout(self):
        """Detecta sequências de breakout (estabilidade seguida de mudança abrupta e sustentada)"""
        if len(self.historico) < 8:
            return False
        
        for i in range(len(self.historico) - 7):
            # Ex: C C C C V V V V (4 iguais, depois 4 do outro)
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] == self.historico[i+3] and
                self.historico[i+4] != self.historico[i] and # Quebra (breakout)
                self.historico[i+4] == self.historico[i+5] == self.historico[i+6] == self.historico[i+7]): # Novo padrão se estabelece
                return True
        return False

    def calcular_frequencias(self):
        """Calcula frequências dos resultados"""
        contador = collections.Counter(self.historico)
        total = len(self.historico)
        if total == 0:
            return {'C': 0, 'V': 0, 'E': 0}
        
        result = {k: round(v / total * 100, 1) for k, v in contador.items()}
        for tipo in ['C', 'V', 'E']:
            if tipo not in result:
                result[tipo] = 0
        return result

    def calcular_tendencia(self):
        """Calcula tendência dos últimos resultados"""
        if len(self.historico) < 5:
            return "Dados insuficientes"
        
        ultimos_5 = self.historico[:5]
        contador = collections.Counter(ultimos_5)
        
        most_common_result, most_common_count = contador.most_common(1)[0]

        if most_common_count >= 4:
            return f"Forte tendência: {most_common_result}"
        elif most_common_count >= 3:
            return f"Tendência moderada: {most_common_result}"
        else:
            return "Sem tendência clara"

    def sugestao_inteligente(self):
        """Gera sugestão inteligente baseada em múltiplos fatores"""
        analise = self.analisar_todos()
        padroes_identificados = [nome for nome, ok in analise.items() if ok]
        
        if not padroes_identificados:
            return {
                "sugerir": False,
                "entrada": None,
                "entrada_codigo": None,
                "motivos": ["Nenhum padrão confiável identificado"],
                "confianca": 0,
                "frequencias": self.calcular_frequencias(),
                "tendencia": self.calcular_tendencia(),
                "ultimos_resultados": self.historico[:5]
            }
        
        # Calcula confiança baseada nos pesos dos padrões
        confianca_total = 0
        peso_total = 0
        
        for padrao in padroes_identificados:
            peso = self.pesos_padroes.get(padrao, 0.5) # Peso padrão de 0.5 se não definido
            confianca_total += peso
            peso_total += peso
        
        confianca_media = (confianca_total / peso_total) * 100 if peso_total > 0 else 0
        
        # Ajusta confiança baseada na quantidade de padrões
        bonus_quantidade = min(20, len(padroes_identificados) * 3) # Bônus reduzido para evitar superestimar
        confianca_final = min(95, int(confianca_media + bonus_quantidade))
        
        # Análise de frequências e tendências
        frequencias = self.calcular_frequencias()
        tendencia_str = self.calcular_tendencia()
        
        opcoes = ["V", "C", "E"]
        
        # Lógica de sugestão aprimorada
        entrada_sugerida = None
        
        # 1. Tentar reverter padrões de sequência muito longos
        if self._ondas_longas():
            # Se uma onda longa está acontecendo, sugerir o oposto
            ultimo_resultado = self.historico[0]
            if ultimo_resultado == 'C':
                entrada_sugerida = 'V'
            elif ultimo_resultado == 'V':
                entrada_sugerida = 'C'
            else: # Empate (E) não tem "oposto" claro para sequência
                entrada_sugerida = random.choice(['C', 'V']) # Aleatório entre C e V
        
        # 2. Considerar padrões de quebra/breakout
        elif any(p for p in padroes_identificados if "quebra" in p.lower() or "breakout" in p.lower() or "tensão" in p.lower()):
            # Se há padrões de quebra, sugere o oposto da tendência ou do último resultado
            ultimo_resultado = self.historico[0] if self.historico else None
            if ultimo_resultado and ultimo_resultado != 'E':
                entrada_sugerida = 'V' if ultimo_resultado == 'C' else 'C'
            else: # Se o último foi Empate ou não há histórico, sugere o menos frequente
                entrada_sugerida = min(opcoes, key=lambda x: frequencias.get(x, 0))
        
        # 3. Lógica normal: sugere o menos frequente ou baseado na tendência
        else:
            # Pegar o que tem menor frequência (menos apareceu)
            # Excluir empate se tiver pouca frequência, mas não for o menos frequente
            opcoes_nao_empate = [o for o in opcoes if o != 'E']
            if len(opcoes_nao_empate) > 0:
                entrada_sugerida = min(opcoes, key=lambda x: frequencias.get(x, 0))
            else: # Caso só tenha empate ou não haja dados
                entrada_sugerida = random.choice(opcoes)

            # Se a tendência é forte, sugerir o contrário para quebrar ou seguir a minoria
            if "Forte tendência" in tendencia_str:
                resultado_tendencia = tendencia_str.split(': ')[1]
                if resultado_tendencia != 'E': # Não tentar "quebrar" empate forte, mas focar em C/V
                    opcoes_contrarias = [op for op in ['C', 'V'] if op != resultado_tendencia]
                    if opcoes_contrarias:
                        entrada_sugerida = random.choice(opcoes_contrarias)
                else: # Se a tendência forte é Empate, sugere um C ou V aleatoriamente
                    entrada_sugerida = random.choice(['C', 'V'])
            
            # Ajuste final se a sugestão for Empate e a confiança não for super alta (apenas um exemplo)
            if entrada_sugerida == 'E' and confianca_final < 70:
                # Se não tem muita confiança em empate, sugere C ou V com menor frequência
                entrada_sugerida = min(opcoes_nao_empate, key=lambda x: frequencias.get(x, 0))


        # Se todas as frequências são iguais ou muito próximas, usa análise de momentum dos últimos
        if len(set(frequencias.values())) <= 1 or confianca_final < 60: # Se a confiança for baixa, tenta uma lógica alternativa
            ultimos_3 = self.historico[:3]
            if len(ultimos_3) >= 3:
                contador_recente = collections.Counter(ultimos_3)
                if contador_recente.most_common(1)[0][1] >= 2: # Se tem repetição recente
                    resultado_frequente = contador_recente.most_common(1)[0][0]
                    # Sugere o oposto do que mais apareceu recentemente
                    opcoes_mudanca = [op for op in opcoes if op != resultado_frequente]
                    if opcoes_mudanca:
                        entrada_sugerida = random.choice(opcoes_mudanca)
                    else: # Se só tem um tipo nos ultimos 3 (ex: CCC), sugere o menos frequente geral
                        entrada_sugerida = min(opcoes, key=lambda x: frequencias.get(x, 0))
                else: # Nenhuma repetição forte nos últimos 3
                    entrada_sugerida = random.choice(opcoes)
            elif self.historico: # Se tem histórico mas menos de 3, pega o oposto do último
                ultimo_resultado = self.historico[0]
                entrada_sugerida = [o for o in opcoes if o != ultimo_resultado][0] if ultimo_resultado != 'E' else random.choice(['C', 'V'])
            else: # Sem histórico
                entrada_sugerida = random.choice(opcoes)

        mapeamento = {"C": "Casa", "V": "Visitante", "E": "Empate"}
        entrada_legivel = mapeamento.get(entrada_sugerida, "Indefinido") # Usar .get para evitar KeyError

        return {
            "sugerir": True,
            "entrada": entrada_legivel,
            "entrada_codigo": entrada_sugerida,
            "motivos": padroes_identificados,
            "confianca": confianca_final,
            "frequencias": frequencias,
            "tendencia": tendencia_str, # Usar a string formatada
            "ultimos_resultados": self.historico[:5],
            "analise_detalhada": self._gerar_analise_detalhada(padroes_identificados)
        }

    def _gerar_analise_detalhada(self, padroes):
        """Gera análise detalhada dos padrões encontrados"""
        categorias = {
            "Padrões de Sequência": ["Sequência", "Surf", "Ondas", "Fibonacci", "Dourada", "Paroli", "Momentum", "Respiração"],
            "Padrões de Quebra/Inversão": ["Quebra", "Breakout", "Tensão", "Martingale", "Resistência", "Fibonacci Invertida"],
            "Padrões Cíclicos/Simétricos": ["Ciclo", "Espelho", "Triangular", "Labouchere", "Ritmo Cardíaco", "Pressão"],
            "Padrões de Ocorrência": ["Duplas Repetidas", "Empate Recorrente", "Alternância com Empate", "Clusters", "Polar", "Dragon Tiger"]
        }
        
        analise = {}
        for categoria, keywords in categorias.items():
            padroes_categoria = [p for p in padroes if any(k.lower() in p.lower() for k in keywords)]
            if padroes_categoria:
                analise[categoria] = padroes_categoria
        
        return analise

# --- FUNÇÕES DE INTERFACE E LÓGICA DE HISTÓRICO ---

# Inicializa o estado da sessão
if 'historico' not in st.session_state:
    st.session_state.historico = []

if 'estatisticas' not in st.session_state:
    st.session_state.estatisticas = {
        'total_jogos': 0,
        'acertos': 0,
        'erros': 0,
    }
# Adiciona um novo estado para a última sugestão dada e se ela foi avaliada
if 'ultima_sugestao' not in st.session_state:
    st.session_state.ultima_sugestao = None # Armazena a última sugestão válida
if 'sugestao_avaliada' not in st.session_state:
    st.session_state.sugestao_avaliada = False # Flag para saber se a sugestão já foi avaliada

def adicionar_resultado(resultado):
    """Adiciona resultado ao histórico"""
    st.session_state.historico.insert(0, resultado)
    if len(st.session_state.historico) > 50:
        st.session_state.historico = st.session_state.historico[:50]
    st.session_state.estatisticas['total_jogos'] += 1
    # Resetar a flag de sugestão avaliada quando um novo resultado é adicionado
    st.session_state.sugestao_avaliada = False

def limpar_historico():
    """Limpa todo o histórico"""
    st.session_state.historico = []
    st.session_state.estatisticas = {
        'total_jogos': 0,
        'acertos': 0,
        'erros': 0,
    }
    st.session_state.ultima_sugestao = None
    st.session_state.sugestao_avaliada = False

def desfazer_ultimo():
    """Remove o último resultado"""
    if st.session_state.historico:
        st.session_state.historico.pop(0)
        if st.session_state.estatisticas['total_jogos'] > 0:
            st.session_state.estatisticas['total_jogos'] -= 1
        # Se desfizer o último, pode precisar reavaliar a sugestão anterior ou limpar
        st.session_state.ultima_sugestao = None
        st.session_state.sugestao_avaliada = False


def registrar_avaliacao(resultado_real):
    """Verifica e registra se a última sugestão estava correta"""
    if st.session_state.ultima_sugestao and not st.session_state.sugestao_avaliada:
        sugestao_codigo = st.session_state.ultima_sugestao['entrada_codigo']
        if sugestao_codigo == resultado_real:
            st.session_state.estatisticas['acertos'] += 1
            st.success(f"🎉 Acerto! A sugestão era **{st.session_state.ultima_sugestao['entrada']}** e o resultado real foi **{st.session_state.ultima_sugestao['entrada']}**.")
        else:
            st.session_state.estatisticas['erros'] += 1
            st.error(f"😔 Erro. A sugestão era **{st.session_state.ultima_sugestao['entrada']}**, mas o resultado real foi **{resultado_real}**.")
        st.session_state.sugestao_avaliada = True # Marca como avaliada
        st.session_state.ultima_sugestao = None # Limpa a sugestão para a próxima rodada
    elif st.session_state.sugestao_avaliada:
        st.warning("Esta sugestão já foi avaliada ou não há sugestão ativa para avaliar.")


def get_resultado_html(resultado):
    """Retorna HTML para bolinha colorida"""
    color_map = {'C': '#FF4B4B', 'V': '#4B4BFF', 'E': '#FFD700'}
    label_map = {'C': 'C', 'V': 'V', 'E': 'E'}
    
    return f"""
    <span style='
        display: inline-block; 
        width: 25px; 
        height: 25px; 
        border-radius: 50%; 
        background-color: {color_map.get(resultado, 'gray')}; 
        color: {'black' if resultado == 'E' else 'white'};
        text-align: center;
        line-height: 25px;
        font-weight: bold;
        font-size: 12px;
        margin: 2px;
        border: 2px solid #333;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    '>{label_map.get(resultado, '?')}</span>
    """

def get_trend_arrow(frequencias):
    """Retorna seta de tendência baseada nas frequências"""
    if not frequencias or sum(frequencias.values()) == 0:
        return '⚪' # Sem tendência

    valores = list(frequencias.values())
    max_val = max(valores)
    
    # Se houver múltiplos resultados com a mesma frequência máxima, é sem tendência clara
    resultados_dominantes = [k for k, v in frequencias.items() if v == max_val]
    
    if len(resultados_dominantes) > 1:
        return '⚪' # Mais de um com a mesma frequência máxima
    
    resultado_dominante = resultados_dominantes[0]
    
    arrows = {'C': '🔴', 'V': '🔵', 'E': '🟡'}
    return arrows.get(resultado_dominante, '⚪')

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    layout="wide", 
    page_title="Football Studio Live Analyzer Pro",
    page_icon="⚽"
)

# CSS melhorado (já estava bom, mantido)
st.markdown("""
<style>
/* Estilo geral */
.main-header {
    background: linear-gradient(90deg, #FF4B4B, #4B4BFF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-size: 3em;
    font-weight: bold;
    margin-bottom: 20px;
}

.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin: 10px 0;
    box-shadow: 0 8px 16px rgba(0,0,0,0.3);
}

/* Botões coloridos */
div.stButton > button:first-child {
    font-size: 16px;
    padding: 12px 24px;
    border-radius: 10px;
    cursor: pointer;
    margin: 5px;
    color: white;
    border: none;
    font-weight: bold;
    transition: all 0.3s ease;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

div.stButton > button:first-child:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
}

/* Casa (Vermelho) */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #FF4B4B, #FF6B6B);
}

/* Visitante (Azul) */
div.stButton > button[kind="secondary"] {
    background: linear-gradient(135deg, #4B4BFF, #6B6BFF);
}

/* Empate (Dourado) */
div.stButton > button[kind="tertiary"] {
    background: linear-gradient(135deg, #FFD700, #FFA500);
    color: black;
}

/* Botões de ação */
/* Ajuste para botões de "Verificar Sugestão" - manter verde*/
div.stButton button[data-testid="stFormSubmitButton"] {
    background: linear-gradient(135deg, #28a745, #20c997) !important;
}
div.stButton button[data-testid="stFormSubmitButton"]:hover {
    background: linear-gradient(135deg, #20c997, #28a745) !important;
}


.pattern-found {
    background: linear-gradient(135deg, #28a745, #20c997);
    color: white;
    padding: 8px 12px;
    border-radius: 8px;
    margin: 2px;
    display: inline-block;
    font-size: 12px;
    font-weight: bold;
}

.pattern-not-found {
    background: linear-gradient(135deg, #6c757d, #495057);
    color: white;
    padding: 8px 12px;
    border-radius: 8px;
    margin: 2px;
    display: inline-block;
    font-size: 12px;
    opacity: 0.6;
}

.suggestion-box {
    background: linear-gradient(135deg, #17a2b8, #138496);
    color: white;
    padding: 20px;
    border-radius: 15px;
    margin: 10px 0;
    border-left: 5px solid #FFD700;
}

.confidence-high { color: #28a745; font-weight: bold; }
.confidence-medium { color: #ffc107; font-weight: bold; }
.confidence-low { color: #dc3545; font-weight: bold; }

.history-container {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    border: 1px solid rgba(255,255,255,0.1);
    /* Para quebras de linha automáticas e responsivas */
    display: flex;
    flex-wrap: wrap;
    gap: 5px; /* Espaço entre as bolinhas */
}

</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<h1 class="main-header">⚽ Football Studio Live Analyzer Pro</h1>', unsafe_allow_html=True)
st.markdown("---")

# --- ESTATÍSTICAS RÁPIDAS ---
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>🎯 Total de Jogos</h3>
        <h2>{st.session_state.estatisticas['total_jogos']}</h2>
    </div>
    """, unsafe_allow_html=True)

with col_stat2:
    acertos = st.session_state.estatisticas['acertos']
    st.markdown(f"""
    <div class="metric-card">
        <h3>✅ Acertos</h3>
        <h2>{acertos}</h2>
    </div>
    """, unsafe_allow_html=True)

with col_stat3:
    erros = st.session_state.estatisticas['erros']
    st.markdown(f"""
    <div class="metric-card">
        <h3>❌ Erros</h3>
        <h2>{erros}</h2>
    </div>
    """, unsafe_allow_html=True)

with col_stat4:
    total_sugestoes = acertos + erros
    precisao = round((acertos / total_sugestoes * 100), 1) if total_sugestoes > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <h3>📊 Precisão</h3>
        <h2>{precisao}%</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- INSERÇÃO DE RESULTADOS ---
st.subheader("🎮 Inserir Novo Resultado")

col_btn1, col_btn2, col_btn3, col_btn4, col_btn5 = st.columns(5)

with col_btn1:
    if st.button("🔴 Casa (C)", help="Vitória da Casa", key="casa", use_container_width=True):
        adicionar_resultado('C')
        st.rerun()

with col_btn2:
    if st.button("🔵 Visitante (V)", help="Vitória do Visitante", key="visitante", use_container_width=True):
        adicionar_resultado('V')
        st.rerun()

with col_btn3:
    if st.button("🟡 Empate (E)", help="Resultado Empate", key="empate", use_container_width=True):
        adicionar_resultado('E')
        st.rerun()

with col_btn4:
    if st.button("↩️ Desfazer", help="Remove último resultado", key="desfazer", use_container_width=True):
        desfazer_ultimo()
        st.rerun()

with col_btn5:
    if st.button("🗑️ Limpar Tudo", help="Limpa histórico completo", key="limpar", use_container_width=True):
        limpar_historico()
        st.rerun()

st.markdown("---")

# --- HISTÓRICO ---
st.subheader("📈 Histórico de Resultados")

if not st.session_state.historico:
    st.info("🎯 Histórico vazio. Comece inserindo alguns resultados para ver a mágica acontecer!")
else:
    # Exibe histórico com styling
    historico_html = "<div class='history-container'>"
    historico_html += "<h4>Últimos Resultados (mais recente à esquerda):</h4>"
    
    for resultado in st.session_state.historico:
        historico_html += get_resultado_html(resultado)
    
    historico_html += "</div>" # Fecha o container flex
    historico_html += f"<small>Total: {len(st.session_state.historico)} resultados</small>"
    
    st.markdown(historico_html, unsafe_allow_html=True)

st.markdown("---")

# --- ANÁLISE PRINCIPAL ---
if len(st.session_state.historico) >= 9:
    analyzer = AnalisePadroes(st.session_state.historico)
    
    # --- SUGESTÃO PRINCIPAL ---
    st.header("🔮 Sugestão Inteligente")
    
    sugestao = analyzer.sugestao_inteligente()
    
    if sugestao['sugerir']:
        # Armazena a sugestão para futura avaliação
        st.session_state.ultima_sugestao = sugestao

        # Determina cor da confiança
        if sugestao['confianca'] >= 75:
            conf_class = "confidence-high"
            conf_emoji = "🟢"
        elif sugestao['confianca'] >= 50:
            conf_class = "confidence-medium"
            conf_emoji = "🟡"
        else:
            conf_class = "confidence-low"
            conf_emoji = "🔴"
        
        # Box de sugestão
        st.markdown(f"""
        <div class="suggestion-box">
            <h2>🎯 Próxima Jogada Sugerida: <strong>{sugestao['entrada']}</strong></h2>
            <h3>{conf_emoji} Confiança: <span class="{conf_class}">{sugestao['confianca']}%</span></h3>
            <p><strong>Tendência:</strong> {sugestao['tendencia']}</p>
            <p><strong>Últimos 5:</strong> {' → '.join(sugestao['ultimos_resultados'])}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Análise detalhada
        if 'analise_detalhada' in sugestao and sugestao['analise_detalhada']:
            st.subheader("🔍 Análise Detalhada por Categoria")
            for categoria, padroes in sugestao['analise_detalhada'].items():
                st.write(f"**{categoria}:**")
                for padrao in padroes:
                    st.markdown(f"<span class='pattern-found'>✓ {padrao}</span>", unsafe_allow_html=True)
                st.write("")
        
        st.markdown("---")

        # --- AVALIAÇÃO DA SUGESTÃO ---
        if not st.session_state.sugestao_avaliada:
            st.subheader("🤔 O resultado real correspondeu à sugestão?")
            col_eval1, col_eval2, col_eval3 = st.columns(3)
            with col_eval1:
                if st.button("🔴 Casa (Real)", key="real_casa", use_container_width=True):
                    registrar_avaliacao('C')
                    st.rerun()
            with col_eval2:
                if st.button("🔵 Visitante (Real)", key="real_visitante", use_container_width=True):
                    registrar_avaliacao('V')
                    st.rerun()
            with col_eval3:
                if st.button("🟡 Empate (Real)", key="real_empate", use_container_width=True):
                    registrar_avaliacao('E')
                    st.rerun()
        else:
            st.info("✅ Esta sugestão já foi avaliada.")

    else:
        st.warning("⚠️ Dados insuficientes para sugestão confiável. Continue inserindo resultados!")
    
    st.markdown("---")
    
    # --- PADRÕES DETECTADOS ---
    st.header("🎨 Padrões Detectados")
    
    padroes_encontrados = analyzer.analisar_todos()
    
    col_found, col_not_found = st.columns(2)
    
    with col_found:
        st.subheader("✅ Padrões Ativos")
        encontrados = [nome for nome, found in padroes_encontrados.items() if found]
        
        if encontrados:
            for padrao in encontrados:
                st.markdown(f"<span class='pattern-found'>✓ {padrao}</span>", unsafe_allow_html=True)
        else:
            st.info("Nenhum padrão específico ativo no momento.")
    
    with col_not_found:
        st.subheader("⏳ Padrões Inativos")
        nao_encontrados = [nome for nome, found in padroes_encontrados.items() if not found]
        
        if nao_encontrados:
            # Mostra apenas os primeiros 10 para não sobrecarregar
            for padrao in nao_encontrados[:10]:
                st.markdown(f"<span class='pattern-not-found'>○ {padrao}</span>", unsafe_allow_html=True)
            
            if len(nao_encontrados) > 10:
                st.write(f"... e mais {len(nao_encontrados) - 10} padrões")
    
    st.markdown("---")
    
    # --- ANÁLISE FREQUENCIAL ---
    st.header("📊 Análise de Frequências")
    
    frequencias = analyzer.calcular_frequencias()
    
    col_freq1, col_freq2 = st.columns(2)
    
    with col_freq1:
        # Gráfico de barras
        df_freq = pd.DataFrame([
            {'Resultado': 'Casa', 'Frequência': frequencias['C'], 'Cor': '#FF4B4B'},
            {'Resultado': 'Visitante', 'Frequência': frequencias['V'], 'Cor': '#4B4BFF'},
            {'Resultado': 'Empate', 'Frequência': frequencias['E'], 'Cor': '#FFD700'}
        ])
        
        st.bar_chart(df_freq.set_index('Resultado')['Frequência'])
    
    with col_freq2:
        # Métricas detalhadas
        st.metric("🔴 Casa", f"{frequencias['C']}%")
        st.metric("🔵 Visitante", f"{frequencias['V']}%")
        st.metric("🟡 Empate", f"{frequencias['E']}%")
        
        # Indicador de tendência
        trend_arrow = get_trend_arrow(frequencias)
        st.markdown(f"**Tendência Atual:** {trend_arrow}")

else:
    st.warning(f"📊 Análise será exibida com pelo menos 9 resultados. Atual: **{len(st.session_state.historico)}**")
    
    progress = len(st.session_state.historico) / 9
    st.progress(progress)
    st.write(f"Progresso: {len(st.session_state.historico)}/9 resultados")

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; margin-top: 50px;'>
    <h4>⚽ Football Studio Live Analyzer Pro</h4>
    <p>Análise inteligente de padrões para Football Studio da Evolution Gaming</p>
    <p><small>Desenvolvido com algoritmos avançados de detecção de padrões</small></p>
</div>
""", unsafe_allow_html=True)
