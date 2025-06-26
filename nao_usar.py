import streamlit as st
import collections
import random
import numpy as np
from datetime import datetime
import pandas as pd
import os # Para lidar com arquivos

# --- CONFIGURAÇÕES DE ARQUIVO ---
DATA_FILE = 'football_studio_data.csv'

# --- CLASSE ANALISEPADROES REFINADA ---
class AnalisePadroes:
    def __init__(self, historico):
        # Aumentado para 50 jogos para melhor análise
        self.historico = historico[:50]  
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
        
        # Pesos dos padrões para calcular confiança (ajustados)
        # Ajuste esses pesos com base nos seus testes e experiência!
        self.pesos_padroes = {
            "Sequência (Surf de Cor)": 0.9,
            "Zig-Zag Perfeito": 0.8,
            "Quebra de Surf": 0.85,
            "Quebra de Zig-Zag": 0.8,
            "Padrão Fibonacci": 0.7, # Reduzido - padrão conceitual complexo
            "Sequência Dourada": 0.8,
            "Padrão Dragon Tiger": 0.9, # Alta relevância em jogos de cartas
            "Ciclo de Dominância": 0.95, # Padrão forte
            "Padrão de Momentum": 0.9,
            "Sequência de Breakout": 0.95, # Padrão forte
            "Empate Recorrente": 0.8,
            "Ciclo de Empates": 0.85,
            "Padrão Martingale": 0.75,
            "Padrão de Ondas Longas": 0.85,
            "Espelho": 0.7,
        }

    def analisar_todos(self):
        resultados = {}
        for nome, func in self.padroes_ativos.items():
            try:
                resultados[nome] = func()
            except Exception as e:
                # print(f"Erro ao analisar padrão {nome}: {e}") # Descomente para depurar
                resultados[nome] = False # Retorna False em caso de erro
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
            # Verifica se os intervalos seguem um padrão (ex: variação baixa)
            media_intervalo = sum(intervalos) / len(intervalos)
            if media_intervalo > 0: # Evita divisão por zero
                desvio_padrao = (sum((x - media_intervalo) ** 2 for x in intervalos) / len(intervalos)) ** 0.5
                # Um desvio padrão baixo indica regularidade
                return desvio_padrao < 2 and 2 <= media_intervalo <= 8
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
        # Limitado a 10 para não buscar espelhos muito grandes e raros
        for tamanho in range(4, min(len(self.historico) + 1, 11)): 
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
        """Detecta padrões baseados na sequência de Fibonacci em blocos de resultados"""
        # Ex: C, V, CC, VVV, CCCC, VVVVVV... (1, 1, 2, 3, 5, 8...)
        if len(self.historico) < 10: # Necessita de um histórico maior para detectar bem
            return False
        
        fib_sequence = [1, 1, 2, 3, 5, 8]
        
        for start_idx in range(len(self.historico) - sum(fib_sequence) + 1):
            current_idx = start_idx
            pattern_match = True
            last_result_type = None

            for fib_num in fib_sequence:
                if current_idx + fib_num > len(self.historico):
                    pattern_match = False
                    break
                
                segment = self.historico[current_idx : current_idx + fib_num]
                
                # Todos os elementos do segmento devem ser iguais
                if not all(res == segment[0] for res in segment):
                    pattern_match = False
                    break
                
                # Alternância entre os blocos (C/V) e não Empate
                if last_result_type is not None and segment[0] == last_result_type:
                    pattern_match = False # O bloco atual não é alternado
                    break
                
                if segment[0] == 'E': # Ignora empates para esta sequência (Fibonacci de cores)
                    pattern_match = False
                    break

                last_result_type = segment[0]
                current_idx += fib_num
            
            if pattern_match:
                return True
        return False


    def _sequencia_dourada(self):
        """Detecta sequências baseadas na proporção áurea (ex: 3 de um, 5 do outro, 8 do primeiro)"""
        if len(self.historico) < 16: # 3+5+8 = 16
            return False
        
        for i in range(len(self.historico) - 15):
            seg = self.historico[i:i+16]
            if (all(x == seg[0] for x in seg[0:3]) and  # 3 do primeiro
                all(x == seg[3] for x in seg[3:8]) and  # 5 do segundo
                all(x == seg[8] for x in seg[8:16]) and # 8 do terceiro
                seg[0] != seg[3] and seg[3] != seg[8] and seg[0] == seg[8]):
                return True
        return False

    def _padrao_triangular(self):
        """Detecta padrões triangulares: 1, 2, 3, 2, 1 (simétrico)"""
        if len(self.historico) < 9:
            return False
        
        for i in range(len(self.historico) - 8):
            segment = self.historico[i:i+9]
            # Ex: C, VV, CCC, VV, C
            if (segment[0] != segment[1] and segment[1] == segment[2] and
                segment[2] != segment[3] and segment[3] == segment[4] == segment[5] and
                segment[5] != segment[6] and segment[6] == segment[7] and
                segment[7] != segment[8] and segment[0] == segment[8]):
                return True
        return False


    def _ciclo_empates(self):
        """Detecta ciclos específicos de empates (ex: E a cada 5-8 jogos)"""
        empates_indices = [i for i, x in enumerate(self.historico) if x == 'E']
        if len(empates_indices) < 3: # Mínimo de 3 empates para detectar ciclo
            return False
        
        # Verifica se os intervalos entre os empates são consistentes
        intervalos = [empates_indices[i+1] - empates_indices[i] for i in range(len(empates_indices) - 1)]
        
        if len(intervalos) > 1:
            primeiro_intervalo = intervalos[0]
            # Se a maioria dos intervalos está dentro de uma pequena variação do primeiro
            if all(abs(inv - primeiro_intervalo) <= 2 for inv in intervalos):
                return True
        return False


    def _padrao_martingale(self):
        """Detecta padrões de duplicação de sequência (Martingale: 1, 2, 4 do mesmo resultado)"""
        if len(self.historico) < 7:
            return False
        
        for i in range(len(self.historico) - 6):
            # Padrão: 1 resultado (X), 2 iguais (Y,Y), 4 iguais (Z,Z,Z,Z) onde Y e Z são o mesmo e diferente de X
            if (self.historico[i] != self.historico[i+1] and # Quebra inicial
                self.historico[i+1] == self.historico[i+2] and # Dupla
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] == self.historico[i+6] and # Quádrupla
                self.historico[i+1] != 'E' and self.historico[i+1] == self.historico[i+3]): # Não é empate e continua a progressão
                return True
        return False

    def _fibonacci_invertida(self):
        """Detecta Fibonacci invertida (Ex: 8 do mesmo, 5 do outro, 3 do mesmo)"""
        if len(self.historico) < 17: # 8+5+3 = 16
            return False
        
        for i in range(len(self.historico) - 16):
            seg = self.historico[i:i+17]
            if (all(x == seg[0] for x in seg[0:8]) and # 8 do primeiro
                all(x == seg[8] for x in seg[8:13]) and # 5 do segundo
                all(x == seg[13] for x in seg[13:16]) and # 3 do terceiro
                seg[0] != seg[8] and seg[8] != seg[13] and seg[0] == seg[13]):
                return True
        return False

    def _padrao_dragon_tiger(self):
        """Padrão específico de Dragon Tiger adaptado: alternância longa seguida de um resultado forte"""
        if len(self.historico) < 7:
            return False
        
        for i in range(len(self.historico) - 6):
            # Ex: C,V,C,V,C,V, C (Alternância de 6, seguida de 1 forte)
            if (self.historico[i] != self.historico[i+1] and
                self.historico[i+1] != self.historico[i+2] and
                self.historico[i+2] != self.historico[i+3] and
                self.historico[i+3] != self.historico[i+4] and
                self.historico[i+4] != self.historico[i+5] and # 5 alternâncias
                self.historico[i+5] == self.historico[i+6] # Quebra com repetição
                and self.historico[i+5] != 'E' # Não é empate
                ):
                return True
        return False


    def _sequencia_paroli(self):
        """Detecta padrões de progressão positiva (1, 2, 4 de vitórias, depois volta)"""
        if len(self.historico) < 8:
            return False
        
        for i in range(len(self.historico) - 7):
            # Ex: C, CC, CCCC, V (1, 2, 4 do mesmo, depois quebra)
            if (self.historico[i] != 'E' and # Não é empate
                self.historico[i] == self.historico[i+1] and # 2 do mesmo
                self.historico[i+2] == self.historico[i+3] == self.historico[i+4] == self.historico[i+5] and # 4 do mesmo
                self.historico[i] == self.historico[i+2] and # Mesma cor
                self.historico[i+6] != self.historico[i]): # Quebra
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
        """Detecta ciclos de dominância de um resultado (ex: 70%+ de uma cor em 10 jogos)"""
        if len(self.historico) < 10:
            return False
        
        for i in range(len(self.historico) - 9):
            window = self.historico[i:i+10]
            counter = collections.Counter(window)
            
            # Verifica se um resultado domina (70%+)
            for resultado, count in counter.items():
                if resultado != 'E' and count >= 7: # Considera dominância de C ou V
                    return True
        return False

    def _padrao_tensao(self):
        """Detecta padrões de tensão (alternância seguida de explosão do mesmo resultado)"""
        if len(self.historico) < 8:
            return False
        
        for i in range(len(self.historico) - 7):
            # Padrão: C,V,C,V (4 alternâncias) seguido de C,C,C (3 do mesmo)
            if (self.historico[i] != self.historico[i+1] and
                self.historico[i+1] != self.historico[i+2] and
                self.historico[i+2] != self.historico[i+3] and # Quatro alternâncias
                self.historico[i+3] != self.historico[i+4] and # Mais uma alternância
                self.historico[i+4] == self.historico[i+5] == self.historico[i+6] == self.historico[i+7] and # Sequência forte
                self.historico[i+4] != 'E'): # Não é empate
                return True
        return False

    def _sequencia_labouchere(self):
        """Detecta padrões de 'cancelamento' (simetria complexa)"""
        if len(self.historico) < 6:
            return False
        
        for i in range(len(self.historico) - 5):
            # Padrão: X, Y, Z, Z, Y, X (simetria onde X e Y são diferentes)
            if (self.historico[i] == self.historico[i+5] and
                self.historico[i+1] == self.historico[i+4] and
                self.historico[i+2] == self.historico[i+3] and
                self.historico[i] != self.historico[i+1] and # X diferente de Y
                self.historico[i+1] != self.historico[i+2] and # Y diferente de Z
                self.historico[i] != 'E' and self.historico[i+1] != 'E' and self.historico[i+2] != 'E'): # Sem empates
                return True
        return False

    def _ritmo_cardiaco(self):
        """Detecta padrões de ritmo cardíaco (batimentos irregulares, 2, 1, 2, 3...)"""
        if len(self.historico) < 8:
            return False
        
        for i in range(len(self.historico) - 7):
            # Padrão: C C, V, C C, V V V, V
            if (self.historico[i] == self.historico[i+1] and # Dupla
                self.historico[i+2] != self.historico[i] and # Quebra
                self.historico[i+3] == self.historico[i+4] and # Dupla
                self.historico[i+5] == self.historico[i+6] == self.historico[i+7] and # Tripla
                self.historico[i] != 'E' and self.historico[i+2] != 'E' and self.historico[i+5] != 'E'): # Sem empates
                return True
        return False

    def _ciclo_pressao(self):
        """Detecta ciclos de pressão crescente (Ex: 1, 2, 3, 1, 2, 3)"""
        if len(self.historico) < 9:
            return False
        
        for i in range(len(self.historico) - 8):
            # C, VV, CCC, V, CC, VVV
            if (self.historico[i] != self.historico[i+1] and # Unidade
                self.historico[i+1] == self.historico[i+2] and # Dupla
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] and # Tripla
                self.historico[i+6] != self.historico[i+5] and # Quebra
                self.historico[i+7] == self.historico[i+8] and # Dupla
                self.historico[i] == self.historico[i+6] and # Retorno ao padrão
                self.historico[i] != 'E' and self.historico[i+1] != 'E' and self.historico[i+3] != 'E' and self.historico[i+6] != 'E'): # Sem empates
                return True
        return False

    def _padrao_clusters(self):
        """Detecta agrupamentos (clusters) de resultados em janelas"""
        if len(self.historico) < 12:
            return False
        
        # Analisa janelas de 12 para encontrar clusters
        for i in range(len(self.historico) - 11):
            window = self.historico[i:i+12]
            
            # Divide em 3 clusters de 4
            cluster1 = window[:4]
            cluster2 = window[4:8]
            cluster3 = window[8:12]
            
            # Verifica se cada cluster tem dominância (3+ iguais) e são diferentes entre si
            mc1 = collections.Counter(cluster1).most_common(1)
            mc2 = collections.Counter(cluster2).most_common(1)
            mc3 = collections.Counter(cluster3).most_common(1)

            if (mc1 and mc1[0][1] >= 3 and mc1[0][0] != 'E' and
                mc2 and mc2[0][1] >= 3 and mc2[0][0] != 'E' and
                mc3 and mc3[0][1] >= 3 and mc3[0][0] != 'E'):
                # Verifica se há uma mudança de maioria entre os clusters principais
                if mc1[0][0] != mc2[0][0] or mc2[0][0] != mc3[0][0]:
                    return True
        return False

    def _sequencia_polar(self):
        """Detecta sequências polares (alternância extrema sem empates)"""
        if len(self.historico) < 10:
            return False
        
        for i in range(len(self.historico) - 9):
            window = self.historico[i:i+10]
            
            # Verifica se há polarização (só 2 tipos de resultado, sem empates)
            unique_results = set(window)
            if len(unique_results) == 2 and 'E' not in unique_results:
                # Verifica alternância polar: pelo menos 7 mudanças em 9 pares
                changes = sum(1 for j in range(len(window)-1) if window[j] != window[j+1])
                if changes >= 7:  # Muitas mudanças
                    return True
        return False

    def _padrao_momentum(self):
        """Detecta padrões de momentum (aceleração no tamanho da sequência)"""
        if len(self.historico) < 10:
            return False
        
        for i in range(len(self.historico) - 9):
            # Padrão: 1, 2, 3, 4 do mesmo resultado (Ex: C, VV, CCC, VVVV)
            # Verifica se é o mesmo tipo de resultado crescente, mas não necessariamente quebrando
            seg = self.historico[i:i+10]
            if (seg[0] != 'E' and
                seg[0] == seg[1] and # 2
                seg[2] == seg[3] == seg[4] and # 3
                seg[5] == seg[6] == seg[7] == seg[8] and # 4
                seg[0] != seg[2] and seg[2] != seg[5] and seg[0] != seg[5]): # Tipos diferentes entre os blocos
                return True
        return False

    def _ciclo_respiracao(self):
        """Detecta padrões de respiração (expansão e contração de sequências)"""
        if len(self.historico) < 8:
            return False
        
        for i in range(len(self.historico) - 7):
            # Padrão: CCCC (expansão), V (contração), VVV (expansão novamente)
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] == self.historico[i+3] and # 4 do mesmo
                self.historico[i+4] != self.historico[i] and # Quebra
                self.historico[i+5] == self.historico[i+6] == self.historico[i+7] and # 3 do mesmo
                self.historico[i] != 'E' and self.historico[i+4] != 'E' and # Sem empates
                self.historico[i+4] == self.historico[i+5]): # O da quebra é o que se expande
                return True
        return False

    def _padrao_resistencia(self):
        """Detecta padrões de resistência (resultado dominante resiste a várias tentativas de quebra)"""
        if len(self.historico) < 7:
            return False
        
        for i in range(len(self.historico) - 6):
            # Padrão: C,V,C,V,C,V,C (Alternância seguida de retorno ao mesmo)
            # Objetivo é ver se um resultado (Ex: C) se mantém mesmo com alternâncias
            if (self.historico[i] != 'E' and
                self.historico[i] == self.historico[i+2] == self.historico[i+4] == self.historico[i+6] and
                self.historico[i+1] != self.historico[i] and
                self.historico[i+3] != self.historico[i] and
                self.historico[i+5] != self.historico[i]):
                return True
        return False

    def _sequencia_breakout(self):
        """Detecta sequências de breakout (longa estabilidade seguida de mudança abrupta e nova estabilidade)"""
        if len(self.historico) < 8:
            return False
        
        for i in range(len(self.historico) - 7):
            # Padrão: C,C,C,C (estabilidade), V (quebra), V,V,V (nova estabilidade)
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] == self.historico[i+3] and # 4 do mesmo
                self.historico[i+4] != self.historico[i] and # Quebra (breakout)
                self.historico[i+5] == self.historico[i+6] == self.historico[i+7] and # Nova sequência
                self.historico[i+4] == self.historico[i+5] and # A quebra inicia a nova sequência
                self.historico[i] != 'E' and self.historico[i+4] != 'E'): # Sem empates
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
        """Calcula tendência dos últimos 18 resultados"""
        if len(self.historico) < 18:
            return "Dados insuficientes"
        
        ultimos_18 = self.historico[:18]
        contador = collections.Counter(ultimos_18)
        
        # Ajustado para 18 resultados
        if contador.most_common(1)[0][1] >= 11: # Ex: 11 ou mais (aprox. 61%)
            return f"Forte tendência: {contador.most_common(1)[0][0]}"
        elif contador.most_common(1)[0][1] >= 7: # Ex: 7 ou mais (aprox. 39%)
            return f"Tendência moderada: {contador.most_common(1)[0][0]}"
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
                "ultimos_resultados": self.historico[:5] # Apenas os 5 para visualização rápida
            }
        
        # Calcula confiança baseada nos pesos dos padrões
        confianca_total = 0
        peso_total = 0
        
        for padrao in padroes_identificados:
            peso = self.pesos_padroes.get(padrao, 0.5) # Padrões sem peso definido recebem 0.5
            confianca_total += peso
            peso_total += peso
        
        confianca_media = (confianca_total / peso_total) * 100 if peso_total > 0 else 0
        
        # Ajusta confiança baseada na quantidade de padrões
        bonus_quantidade = min(20, len(padroes_identificados) * 3) # Bônus reduzido para não inflar demais
        confianca_final = min(98, int(confianca_media + bonus_quantidade)) # Limite superior de 98%
        
        # Análise de frequências e tendências
        frequencias = self.calcular_frequencias()
        tendencia = self.calcular_tendencia()
        
        opcoes = ["V", "C", "E"]
        
        entrada_sugerida = None
        motivos_sugestao = []

        # 1. Prioriza padrões de QUEBRA/OPORTUNIDADE
        padroes_oportunidade = [p for p in padroes_identificados if 
                                "quebra" in p.lower() or "breakout" in p.lower() or 
                                "tensão" in p.lower() or "martingale" in p.lower()]
        
        if padroes_oportunidade and self.historico:
            ultimo_resultado = self.historico[0]
            # Se a última sequência foi longa, sugere o oposto
            if ultimo_resultado != 'E' and collections.Counter(self.historico[:5]).get(ultimo_resultado, 0) >= 3:
                oposto = 'V' if ultimo_resultado == 'C' else 'C'
                if oposto in opcoes: # Garante que não tente sugerir algo inválido
                    entrada_sugerida = oposto
                    motivos_sugestao.append(f"Padrão de Oportunidade e quebra: sugerindo o oposto de {ultimo_resultado}")
            elif 'Empate Recorrente' in padroes_identificados or 'Ciclo de Empates' in padroes_identificados:
                entrada_sugerida = 'E'
                motivos_sugestao.append("Padrão de Empate Recorrente detectado")
            
        # 2. Se não houver padrões de quebra/oportunidade claros, ou empate não é prioridade, usa lógica de frequência/tendência
        if entrada_sugerida is None:
            # Prefere a que está menos frequente, buscando equilíbrio
            menor_freq_val = float('inf')
            temp_sug = None
            
            # Garante que 'C' e 'V' sejam priorizados sobre 'E' se houver muita diferença,
            # a menos que 'E' seja extremamente raro ou parte de um ciclo.
            
            # Se C e V tiverem frequências muito próximas, e E for bem baixo
            if abs(frequencias['C'] - frequencias['V']) < 10 and frequencias['E'] < 15:
                # Sugere o que está menos frequente entre C e V
                if frequencias['C'] < frequencias['V']:
                    temp_sug = 'C'
                else:
                    temp_sug = 'V'
                motivos_sugestao.append("Frequências de C/V próximas, buscando equilíbrio.")
            else:
                # Caso contrário, sugere o de menor frequência geral
                for opt in opcoes:
                    if frequencias.get(opt, 0) < menor_freq_val:
                        menor_freq_val = frequencias.get(opt, 0)
                        temp_sug = opt
                motivos_sugestao.append("Sugestão baseada na menor frequência geral.")

            entrada_sugerida = temp_sug

            # Ajuste final se a tendência for muito forte na direção oposta
            if "Forte tendência" in tendencia and entrada_sugerida not in tendencia:
                tendencia_resultado = tendencia.split(': ')[1]
                if frequencias[tendencia_resultado] > 60 and random.random() > 0.7: # 30% de chance de ir contra tendência muito forte
                    # Neste caso, mantém a sugestão de menor frequência, apostando na virada.
                    pass 
                else:
                    # Caso contrário, pode ser mais cauteloso e sugerir o da tendência forte.
                    # Mas para Football Studio, muitas vezes ir contra a onda em algum ponto é a estratégia.
                    # Mantenho a lógica de menor frequência, que é uma aposta na regressão à média.
                    pass

        # Lógica de desempate se ainda não houver sugestão forte ou clara
        if entrada_sugerida is None:
            if self.historico:
                # Prioriza o oposto do último se ele foi uma sequência
                last_result = self.historico[0]
                if collections.Counter(self.historico[:3]).get(last_result, 0) >= 2 and last_result != 'E':
                    entrada_sugerida = 'V' if last_result == 'C' else 'C'
                    motivos_sugestao.append(f"Últimos resultados em sequência, sugerindo o oposto de {last_result}.")
                else:
                    entrada_sugerida = random.choice(opcoes) # Último recurso
                    motivos_sugestao.append("Sugestão aleatória (lógica de desempate).")
            else:
                entrada_sugerida = random.choice(opcoes) # Se não há histórico
                motivos_sugestao.append("Sugestão aleatória (sem histórico).")


        mapeamento = {"C": "Casa", "V": "Visitante", "E": "Empate"}
        entrada_legivel = mapeamento[entrada_sugerida]
        
        return {
            "sugerir": True,
            "entrada": entrada_legivel,
            "entrada_codigo": entrada_sugerida,
            "motivos": padroes_identificados + motivos_sugestao, # Combina os padrões com os motivos da sugestão
            "confianca": confianca_final,
            "frequencias": frequencias,
            "tendencia": tendencia,
            "ultimos_resultados": self.historico[:5],
            "analise_detalhada": self._gerar_analise_detalhada(padroes_identificados)
        }

    def _gerar_analise_detalhada(self, padroes):
        """Gera análise detalhada dos padrões encontrados"""
        categorias = {
            "Padrões de Sequência": ["Sequência", "Surf", "Ondas", "Fibonacci", "Paroli", "Momentum"],
            "Padrões de Quebra/Oportunidade": ["Quebra", "Breakout", "Tensão", "Martingale", "Dragon Tiger"],
            "Padrões Cíclicos/Repetição": ["Ciclo", "Respiração", "Empate Recorrente", "Ritmo Cardíaco"],
            "Padrões Simétricos/Estruturais": ["Espelho", "Escada", "Triangular", "Labouchere", "Clusters", "Resistência", "Polar"],
        }
        
        analise = {}
        for categoria, keywords in categorias.items():
            padroes_categoria = [p for p in padroes if any(k.lower() in p.lower() for k in keywords)]
            if padroes_categoria:
                analise[categoria] = padroes_categoria
        
        return analise

# --- FUNÇÕES DE INTERFACE E LÓGICA DE HISTÓRICO ---

def load_data():
    """Carrega o histórico e estatísticas de um arquivo CSV."""
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            # Converte a coluna 'historico' de string para lista
            # Ex: "['C', 'V', 'E']" -> ['C', 'V', 'E']
            df['historico'] = df['historico'].apply(eval) 
            
            # Carrega o último estado salvo
            if not df.empty:
                last_row = df.iloc[-1]
                st.session_state.historico = last_row['historico']
                st.session_state.estatisticas = {
                    'total_jogos': last_row['total_jogos'],
                    'acertos': last_row['acertos'],
                    'erros': last_row['erros'],
                    'historico_sugestoes': eval(last_row['historico_sugestoes'])
                }
                return
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}. Iniciando com dados vazios.")
            # Limpa o arquivo se houver erro de carregamento para evitar loop
            os.remove(DATA_FILE) 
    
    # Se o arquivo não existe ou houve erro, inicializa vazio
    st.session_state.historico = []
    st.session_state.estatisticas = {
        'total_jogos': 0,
        'acertos': 0,
        'erros': 0,
        'historico_sugestoes': [] # Lista de dicionários para registrar sugestões
    }

def save_data():
    """Salva o histórico e estatísticas em um arquivo CSV."""
    data_to_save = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'historico': [st.session_state.historico], # Salva como lista no DF
        'total_jogos': st.session_state.estatisticas['total_jogos'],
        'acertos': st.session_state.estatisticas['acertos'],
        'erros': st.session_state.estatisticas['erros'],
        'historico_sugestoes': [st.session_state.estatisticas['historico_sugestoes']] # Salva como lista de dicts
    }
    df_to_save = pd.DataFrame(data_to_save)

    # Verifica se o arquivo existe para adicionar cabeçalho apenas na primeira vez
    header = not os.path.exists(DATA_FILE)
    df_to_save.to_csv(DATA_FILE, mode='a', index=False, header=header)


# Carrega os dados na inicialização
if 'historico' not in st.session_state:
    load_data()

# Variável para armazenar a última sugestão antes de um novo resultado
if 'ultima_sugestao' not in st.session_state:
    st.session_state.ultima_sugestao = None

def adicionar_resultado(resultado):
    """Adiciona novo resultado ao histórico e valida a sugestão anterior."""
    if st.session_state.ultima_sugestao:
        sugestao_para_validar = st.session_state.ultima_sugestao
        acertou = validar_sugestao(sugestao_para_validar, resultado)
        
        # Registra a validação no histórico de sugestões
        log_entry = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "sugestao_entrada": sugestao_para_validar['entrada_codigo'],
            "sugestao_confianca": sugestao_para_validar['confianca'],
            "sugestao_padroes": sugestao_para_validar['motivos'], # Padrões ativos no momento da sugestão
            "resultado_real": resultado,
            "acertou": acertou
        }
        st.session_state.estatisticas['historico_sugestoes'].append(log_entry)
        st.session_state.ultima_sugestao = None # Limpa após validação

    st.session_state.historico.insert(0, resultado) # Novo resultado na primeira posição
    if len(st.session_state.historico) > 50:
        st.session_state.historico = st.session_state.historico[:50]
    st.session_state.estatisticas['total_jogos'] += 1
    save_data() # Salva dados após cada adição

def limpar_historico():
    """Limpa todo o histórico e zera estatísticas."""
    st.session_state.historico = []
    st.session_state.estatisticas = {
        'total_jogos': 0,
        'acertos': 0,
        'erros': 0,
        'historico_sugestoes': []
    }
    save_data() # Salva dados vazios
    st.session_state.ultima_sugestao = None # Limpa sugestão pendente

def desfazer_ultimo():
    """Remove o último resultado e ajusta estatísticas."""
    if st.session_state.historico:
        # Se houve uma sugestão que não foi validada (porque o último resultado foi desfeito)
        # não deve impactar acertos/erros.
        st.session_state.historico.pop(0)
        if st.session_state.estatisticas['total_jogos'] > 0:
            st.session_state.estatisticas['total_jogos'] -= 1
        st.session_state.ultima_sugestao = None # Cancela qualquer sugestão pendente
        save_data() # Salva dados após desfazer

def validar_sugestao(sugestao_anterior, resultado_real):
    """Valida se a sugestão anterior estava correta."""
    if sugestao_anterior['entrada_codigo'] == resultado_real:
        st.session_state.estatisticas['acertos'] += 1
        return True
    else:
        st.session_state.estatisticas['erros'] += 1
        return False

def get_resultado_html(resultado):
    """Retorna HTML para visualização do resultado."""
    color_map = {'C': '#FF4B4B', 'V': '#4B4BFF', 'E': '#FFD700'}
    symbol_map = {'C': '🏠', 'V': '✈️', 'E': '⚖️'}
    
    return f"""
    <span style='
        display: inline-block; 
        width: 30px; 
        height: 30px; 
        border-radius: 50%; 
        background-color: {color_map.get(resultado, 'gray')}; 
        margin: 2px; 
        text-align: center; 
        line-height: 30px; 
        font-size: 14px;
        color: {"black" if resultado == "E" else "white"};
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    '>
        {symbol_map.get(resultado, '?')}
    </span>
    """

def get_confianca_color(confianca):
    """Retorna cor baseada no nível de confiança."""
    if confianca >= 80:
        return "#4CAF50"  # Verde
    elif confianca >= 60:
        return "#FF9800"  # Laranja
    elif confianca >= 40:
        return "#FFC107"  # Amarelo
    else:
        return "#F44336"  # Vermelho

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    layout="wide", 
    page_title="🎯 Football Studio Live Analyzer",
    page_icon="⚽",
    initial_sidebar_state="expanded"
)

# CSS Aprimorado
st.markdown("""
<style>
/* Estilo geral */
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    text-align: center;
}

.main-header h1 {
    color: white;
    font-size: 2.5rem;
    margin: 0;
}

.main-header p {
    color: white;
    font-size: 1.2rem;
    margin: 0.5rem 0 0 0;
    opacity: 0.9;
}

/* Botões */
div.stButton > button:first-child {
    font-size: 16px;
    padding: 12px 24px;
    border-radius: 8px;
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

/* Botões específicos */
div.stButton > button[data-testid="stButton-🏠 Casa (C)"] {
    background: linear-gradient(135deg, #FF6B6B, #FF4B4B);
}

div.stButton > button[data-testid="stButton-✈️ Visitante (V)"] {
    background: linear-gradient(135deg, #4ECDC4, #4B4BFF);
}

div.stButton > button[data-testid="stButton-⚖️ Empate (E)"] {
    background: linear-gradient(135deg, #FFE66D, #FFD700);
    color: black;
}

div.stButton > button[data-testid="stButton-↩️ Desfazer"] {
    background: linear-gradient(135deg, #95A5A6, #7F8C8D);
}

div.stButton > button[data-testid="stButton-🗑️ Limpar Tudo"] { # Ajustado o key para ser diferente do Desfazer
    background: linear-gradient(135deg, #E74C3C, #C0392B);
}

/* Cards de estatísticas */
.metric-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-left: 4px solid #667eea;
    margin: 1rem 0;
}

.metric-card h3 {
    margin: 0 0 0.5rem 0;
    color: #2C3E50;
}

.metric-card p {
    margin: 0;
    font-size: 1.1rem;
    font-weight: bold;
}

/* Seções */
.section-header {
    background: linear-gradient(135deg, #74b9ff, #0984e3);
    color: white;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
    text-align: center;
}

.pattern-found {
    background: linear-gradient(135deg, #00b894, #55a3ff);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    margin: 0.25rem 0;
    font-weight: bold;
}

.pattern-not-found {
    background: #f8f9fa;
    color: #6c757d;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    margin: 0.25rem 0;
    border: 1px solid #dee2e6;
}

.suggestion-box {
    background: linear-gradient(135deg, #a8edea, #fed6e3);
    padding: 2rem;
    border-radius: 12px;
    margin: 1rem 0;
    border: 2px solid #667eea;
}

.confidence-high { color: #27AE60; font-weight: bold; }
.confidence-medium { color: #F39C12; font-weight: bold; }
.confidence-low { color: #E74C3C; font-weight: bold; }

.historic-container {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    margin: 1rem 0;
    border: 1px solid #dee2e6;
    display: flex; /* Habilita flexbox para os itens */
    flex-wrap: wrap; /* Permite que os itens quebrem linha */
    justify-content: flex-start; /* Alinha itens ao início */
}

/* Garante que os spans de resultado fiquem em linha */
.historic-container span {
    display: inline-flex; 
    align-items: center;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

# --- CABEÇALHO PRINCIPAL ---
st.markdown("""
<div class="main-header">
    <h1>⚽ Football Studio Live Analyzer</h1>
    <p>Análise Inteligente de Padrões - Evolution Gaming</p>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR COM ESTATÍSTICAS ---
with st.sidebar:
    st.markdown("## 📊 Estatísticas da Sessão")
    
    total_jogos = st.session_state.estatisticas['total_jogos']
    acertos = st.session_state.estatisticas['acertos']
    erros = st.session_state.estatisticas['erros']
    
    if total_jogos > 0:
        taxa_acerto = (acertos / total_jogos) * 100
        st.metric("Total de Jogos", total_jogos)
        st.metric("Taxa de Acerto", f"{taxa_acerto:.1f}%")
        # delta = acertos - (total_jogos - acertos) # Outra forma de ver o delta
        st.metric("Acertos", acertos)
        st.metric("Erros", erros)
    else:
        st.info("Nenhum jogo analisado ainda")
    
    st.markdown("---")
    st.markdown("## ⚙️ Configurações")
    
    auto_suggest = st.checkbox("Sugestão Automática", value=True)
    show_advanced = st.checkbox("Análise Avançada", value=True)
    confidence_threshold = st.slider("Limite de Confiança para Sugestão", 0, 100, 60)

# --- SEÇÃO DE INSERÇÃO DE RESULTADOS ---
st.markdown('<div class="section-header"><h2>🎯 Inserir Resultado do Jogo</h2></div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🏠 Casa (C)", key="🏠 Casa (C)", use_container_width=True, help="Vitória da Casa"):
        adicionar_resultado('C')
        st.rerun()

with col2:
    if st.button("✈️ Visitante (V)", key="✈️ Visitante (V)", use_container_width=True, help="Vitória do Visitante"):
        adicionar_resultado('V')
        st.rerun()

with col3:
    if st.button("⚖️ Empate (E)", key="⚖️ Empate (E)", use_container_width=True, help="Empate"):
        adicionar_resultado('E')
        st.rerun()

with col4:
    if st.button("↩️ Desfazer", key="↩️ Desfazer", use_container_width=True, help="Desfazer último resultado"):
        desfazer_ultimo()
        st.rerun()

with col5:
    if st.button("🗑️ Limpar Tudo", key="🗑️ Limpar Tudo", use_container_width=True, help="Limpar todo o histórico e estatísticas"):
        limpar_historico()
        st.rerun()

# --- EXIBIÇÃO DO HISTÓRICO ---
st.markdown('<div class="section-header"><h2>📈 Histórico de Resultados</h2></div>', unsafe_allow_html=True)

if not st.session_state.historico:
    st.info("🎮 Nenhum resultado registrado. Comece inserindo os resultados dos jogos!")
else:
    st.markdown('<div class="historic-container">', unsafe_allow_html=True)
    
    historico_html = ""
    # Itera sobre o histórico para exibir em blocos de 9
    for i, resultado in enumerate(st.session_state.historico):
        historico_html += get_resultado_html(resultado)
        # Quebra a linha a cada 9 resultados
        if (i + 1) % 9 == 0 and (i + 1) < len(st.session_state.historico):
            historico_html += "<br>" # Adiciona uma quebra de linha HTML
    
    st.markdown(historico_html, unsafe_allow_html=True)
    st.markdown(f"**Total:** {len(st.session_state.historico)} jogos (máx. 50)", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ANÁLISE PRINCIPAL ---
if len(st.session_state.historico) >= 5: # Mínimo de 5 para iniciar qualquer análise
    analyzer = AnalisePadroes(st.session_state.historico)
    
    # --- SUGESTÃO INTELIGENTE ---
    st.markdown('<div class="section-header"><h2>🎯 Sugestão Inteligente</h2></div>', unsafe_allow_html=True)
    
    sugestao = analyzer.sugestao_inteligente()
    
    # Armazena a sugestão atual para validação posterior
    st.session_state.ultima_sugestao = sugestao

    if sugestao['sugerir'] and sugestao['confianca'] >= confidence_threshold:
        confianca_color = get_confianca_color(sugestao['confianca'])
        
        st.markdown(f"""
        <div class="suggestion-box">
            <h3>🎯 Próxima Sugestão</h3>
            <h2 style="color: {confianca_color}; margin: 1rem 0;">
                {sugestao['entrada']} ({sugestao['entrada_codigo']})
            </h2>
            <p><strong>Confiança:</strong> 
                <span style="color: {confianca_color}; font-weight: bold;">
                    {sugestao['confianca']}%
                </span>
            </p>
            <p><strong>Tendência dos Últimos 18 Jogos:</strong> {sugestao['tendencia']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detalhes da análise
        if show_advanced:
            with st.expander("📋 Detalhes da Análise"):
                st.write("**Motivos da Sugestão:**")
                for motivo in sugestao['motivos']:
                    st.write(f"• {motivo}")
                
                if 'analise_detalhada' in sugestao and sugestao['analise_detalhada']:
                    st.write("**Análise por Categoria de Padrões Encontrados:**")
                    for categoria, padroes in sugestao['analise_detalhada'].items():
                        st.write(f"**{categoria}:** {', '.join(padroes)}")
                else:
                    st.write("Nenhum padrão específico encontrado para categorização detalhada.")
    else:
        st.warning(f"🤔 Confiança insuficiente ({sugestao['confianca']}%) ou nenhum padrão detectado acima do limite. Não há sugestão forte no momento.")
    
    # --- ANÁLISE DE PADRÕES ---
    st.markdown('<div class="section-header"><h2>🔍 Padrões Detectados</h2></div>', unsafe_allow_html=True)
    
    padroes_encontrados = analyzer.analisar_todos()
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### ✅ Padrões Encontrados")
        encontrados = [nome for nome, status in padroes_encontrados.items() if status]
        
        if encontrados:
            for padrao in encontrados:
                peso = analyzer.pesos_padroes.get(padrao, 0.5)
                st.markdown(f'<div class="pattern-found">✅ {padrao} (Peso: {peso})</div>', unsafe_allow_html=True)
        else:
            st.info("Nenhum padrão específico detectado.")
    
    with col_right:
        st.markdown("### ❌ Padrões Não Encontrados (Amostra)")
        nao_encontrados = [nome for nome, status in padroes_encontrados.items() if not status]
        
        # Exibe apenas os primeiros 10 não encontrados para não sobrecarregar
        for padrao in nao_encontrados[:10]:  
            st.markdown(f'<div class="pattern-not-found">❌ {padrao}</div>', unsafe_allow_html=True)
        if len(nao_encontrados) > 10:
            st.markdown(f'<div class="pattern-not-found">... e mais {len(nao_encontrados) - 10} padrões não encontrados.</div>', unsafe_allow_html=True)

    # --- ANÁLISE ESTATÍSTICA ---
    st.markdown('<div class="section-header"><h2>📊 Análise Estatística</h2></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    frequencias = analyzer.calcular_frequencias()
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏠 Casa</h3>
            <p style="color: #FF4B4B;">{frequencias['C']}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>✈️ Visitante</h3>
            <p style="color: #4B4BFF;">{frequencias['V']}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚖️ Empate</h3>
            <p style="color: #FFD700;">{frequencias['E']}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráfico de frequências
    if show_advanced:
        st.markdown("### 📈 Distribuição das Frequências de Resultados")
        chart_data = pd.DataFrame({
            'Resultado': ['Casa', 'Visitante', 'Empate'],
            'Frequência': [frequencias['C'], frequencias['V'], frequencias['E']],
            'Cor': ['#FF4B4B', '#4B4BFF', '#FFD700']
        })
        
        # Cria um gráfico de barras com cores personalizadas
        st.bar_chart(chart_data.set_index('Resultado')['Frequência'], color=chart_data['Cor'])

        # Detalhes do histórico de sugestões
        st.markdown("### 📜 Histórico de Sugestões e Validações")
        if st.session_state.estatisticas['historico_sugestoes']:
            df_sugestoes = pd.DataFrame(st.session_state.estatisticas['historico_sugestoes'])
            st.dataframe(df_sugestoes)
        else:
            st.info("Nenhuma sugestão foi registrada ainda.")

else:
    st.info("🎮 Insira pelo menos 5 resultados para começar a análise inteligente e 18 para a tendência completa!")

# --- RODAPÉ ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; margin-top: 2rem;">
    <p>⚽ Football Studio Live Analyzer v2.0 | Análise Inteligente de Padrões</p>
    <p><small>Desenvolvido para Evolution Gaming Football Studio</small></p>
</div>
""", unsafe_allow_html=True)
