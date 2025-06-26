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
        
        # Pesos dos padrões para calcular confiança (ajustados para maior relevância de padrões chave)
        # Ajuste esses pesos com base nos seus testes e experiência!
        self.pesos_padroes = {
            "Sequência (Surf de Cor)": 0.95, # Muito forte se ativo
            "Zig-Zag Perfeito": 0.9,
            "Quebra de Surf": 1.0, # Quebra é crucial
            "Quebra de Zig-Zag": 0.95, # Quebra é crucial
            "Padrão Fibonacci": 0.6, 
            "Sequência Dourada": 0.7,
            "Padrão Dragon Tiger": 0.85, 
            "Ciclo de Dominância": 0.9, 
            "Padrão de Momentum": 0.85,
            "Sequência de Breakout": 1.0, # Breakout é um sinal muito forte de mudança
            "Empate Recorrente": 0.85,
            "Ciclo de Empates": 0.9,
            "Padrão Martingale": 0.8,
            "Padrão de Ondas Longas": 0.8,
            "Espelho": 0.7,
            "Padrão de Tensão": 0.95, # Indica forte pressão para uma quebra
            "Padrão Ritmo Cardíaco": 0.75,
            "Ciclo de Pressão": 0.8,
            "Padrão de Clusters": 0.7,
            "Sequência Polar": 0.75,
            "Ciclo de Respiração": 0.7,
            "Padrão de Resistência": 0.85,
        }

    def analisar_todos(self):
        resultados = {}
        for nome, func in self.padroes_ativos.items():
            try:
                resultados[nome] = func()
            except Exception as e:
                # print(f"Erro ao analisar padrão {nome}: {e}") # Descomente para depurar
                resultados[nome] = False 
        return resultados

    # --- PADRÕES BÁSICOS EXISTENTES (Revisados) ---
    def _sequencia_simples(self):
        # Detecta 3 ou mais seguidos
        if len(self.historico) < 3: return False
        for i in range(len(self.historico) - 2):
            if self.historico[i] == self.historico[i+1] == self.historico[i+2]:
                return True
        return False

    def _zig_zag(self):
        # Detecta alternância por 5 ou mais
        if len(self.historico) < 5: return False
        count = 0
        for i in range(len(self.historico) - 1):
            if self.historico[i] != self.historico[i+1] and self.historico[i] != 'E' and self.historico[i+1] != 'E':
                count += 1
            else:
                if count >= 4: # 4 mudanças significam 5 resultados alternados (X,Y,X,Y,X)
                    return True
                count = 0
        return count >= 4

    def _quebra_de_surf(self):
        # Detecta sequência de 3+ e quebra
        if len(self.historico) < 4: return False
        if (self.historico[0] == self.historico[1] == self.historico[2] and 
            self.historico[2] != self.historico[3]):
            return True
        return False

    def _quebra_de_zig_zag(self):
        # Detecta zig-zag por 3+ e quebra (repete)
        if len(self.historico) < 4: return False
        if (self.historico[0] != self.historico[1] and 
            self.historico[1] != self.historico[2] and 
            self.historico[2] == self.historico[3] and
            self.historico[0] != 'E' and self.historico[1] != 'E' and self.historico[2] != 'E' and self.historico[3] != 'E'):
            return True
        return False

    def _duplas_repetidas(self):
        # Detecta CCVV ou VVCC etc.
        if len(self.historico) < 4: return False
        if (self.historico[0] == self.historico[1] and 
            self.historico[2] == self.historico[3] and 
            self.historico[0] != self.historico[2]):
            return True
        return False

    def _empate_recorrente(self):
        # Empates em intervalos regulares
        empates_indices = [i for i, r in enumerate(self.historico) if r == 'E']
        if len(empates_indices) < 3: return False
        
        intervalos = []
        for i in range(len(empates_indices) - 1):
            intervalos.append(empates_indices[i+1] - empates_indices[i])
        
        if len(intervalos) >= 2:
            media_intervalo = sum(intervalos) / len(intervalos)
            if media_intervalo > 0:
                desvio_padrao = np.std(intervalos) # Usando numpy para desvio padrão
                return desvio_padrao < 1.5 and 2 <= media_intervalo <= 8
        return False

    def _padrao_escada(self):
        # C VV CCC (crescente) ou CCC VV C (decrescente)
        if len(self.historico) < 6: return False
        if (self.historico[0] == self.historico[1] == self.historico[2] and # CCC
            self.historico[3] == self.historico[4] and # VV
            self.historico[5] != self.historico[3] and self.historico[5] != self.historico[0] and # C
            self.historico[0] != self.historico[3] and self.historico[0] != 'E'): # C != V
            return True
        return False

    def _espelho(self):
        # ABCBA
        if len(self.historico) < 5: return False
        for start in range(len(self.historico) - 4):
            if (self.historico[start] == self.historico[start+4] and
                self.historico[start+1] == self.historico[start+3] and
                self.historico[start] != self.historico[start+1]):
                return True
        return False

    def _alternancia_empate_meio(self):
        # C E V ou V E C
        if len(self.historico) < 3: return False
        if (self.historico[0] == 'E' and self.historico[1] != 'E' and 
            self.historico[2] != 'E' and self.historico[1] != self.historico[2]):
            return True
        return False

    def _padrao_onda(self):
        # C V C V C V
        if len(self.historico) < 6: return False
        if (self.historico[0] != self.historico[1] and self.historico[1] != self.historico[2] and
            self.historico[2] != self.historico[3] and self.historico[3] != self.historico[4] and
            self.historico[4] != self.historico[5] and
            self.historico[0] != 'E' and self.historico[1] != 'E'): # Excluir empates para alternância de cores
            return True
        return False

    # --- NOVOS PADRÕES ESPECÍFICOS DO FOOTBALL STUDIO (Revisados) ---
    
    def _padrao_fibonacci(self):
        # Baseado em blocos: 1, 1, 2, 3, 5... (ex: C,V,CC,VVV,CCCCC)
        if len(self.historico) < 10: return False
        fib_sequence = [1, 1, 2, 3, 5] # Simplificado para os últimos 5 blocos
        
        current_idx = 0
        last_block_val = None
        for fib_num in fib_sequence:
            if current_idx + fib_num > len(self.historico): return False
            
            block = self.historico[current_idx : current_idx + fib_num]
            
            if not all(x == block[0] for x in block): return False # Bloco não homogêneo
            if block[0] == 'E': return False # Bloco não pode ser empate
            
            if last_block_val is not None and block[0] == last_block_val: return False # Não alternou
            
            last_block_val = block[0]
            current_idx += fib_num
        return True

    def _sequencia_dourada(self):
        # 3 do primeiro, 5 do segundo, 8 do primeiro
        if len(self.historico) < 16: return False
        seg = self.historico[:16] # Últimos 16
        if (all(x == seg[0] for x in seg[0:3]) and  
            all(x == seg[3] for x in seg[3:8]) and  
            all(x == seg[8] for x in seg[8:16]) and 
            seg[0] != seg[3] and seg[3] != seg[8] and seg[0] == seg[8] and
            seg[0] != 'E'): # Sem empates
            return True
        return False

    def _padrao_triangular(self):
        # 1, 2, 3, 2, 1 simétrico
        if len(self.historico) < 9: return False
        seg = self.historico[:9]
        if (seg[0] == seg[8] and seg[1] == seg[7] and seg[2] == seg[6] and seg[3] == seg[5] and # Simetria
            seg[0] != seg[1] and seg[1] != seg[2] and seg[2] != seg[3] and # Mudança entre blocos
            seg[0] != 'E' and seg[1] != 'E' and seg[2] != 'E'): # Sem empates
            return True
        return False

    def _ciclo_empates(self):
        # Ciclo E a cada X jogos
        empates_indices = [i for i, x in enumerate(self.historico) if x == 'E']
        if len(empates_indices) < 3: return False
        
        intervalos = [empates_indices[i+1] - empates_indices[i] for i in range(len(empates_indices) - 1)]
        
        if len(intervalos) > 1:
            primeiro_intervalo = intervalos[0]
            if all(abs(inv - primeiro_intervalo) <= 1 for inv in intervalos): # Variação menor para ser um ciclo
                return True
        return False

    def _padrao_martingale(self):
        # 1 de A, 2 de B, 4 de B (Ex: C, VV, VVVV)
        if len(self.historico) < 7: return False
        if (self.historico[0] != self.historico[1] and # Quebra
            self.historico[1] == self.historico[2] and # Dupla
            self.historico[3] == self.historico[4] == self.historico[5] == self.historico[6] and # Quádrupla
            self.historico[1] == self.historico[3] and # Cor se mantém
            self.historico[1] != 'E'): # Não é empate
            return True
        return False

    def _fibonacci_invertida(self):
        # 8 de A, 5 de B, 3 de A
        if len(self.historico) < 16: return False # 8+5+3
        seg = self.historico[:16]
        if (all(x == seg[0] for x in seg[0:8]) and 
            all(x == seg[8] for x in seg[8:13]) and 
            all(x == seg[13] for x in seg[13:16]) and 
            seg[0] != seg[8] and seg[8] != seg[13] and seg[0] == seg[13] and
            seg[0] != 'E'): # Sem empates
            return True
        return False

    def _padrao_dragon_tiger(self):
        # Alternância longa seguida de um resultado forte (ex: CVCVCVC C)
        if len(self.historico) < 7: return False
        # Alternância de 5 seguidos de uma repetição (C,V,C,V,C,V, C)
        if (self.historico[0] != self.historico[1] and self.historico[1] != self.historico[2] and
            self.historico[2] != self.historico[3] and self.historico[3] != self.historico[4] and
            self.historico[4] != self.historico[5] and # 5 alternâncias
            self.historico[5] == self.historico[6] and # Seguido do mesmo
            self.historico[0] != 'E' and self.historico[1] != 'E'): # Sem empates
            return True
        return False

    def _sequencia_paroli(self):
        # 1 de A, 2 de A, 4 de A (progressão positiva)
        if len(self.historico) < 7: return False # 1+2+4
        seg = self.historico[:7]
        if (seg[0] == seg[1] and # 2
            seg[2] == seg[3] == seg[4] == seg[5] and # 4
            seg[0] == seg[2] and # Mesma cor
            seg[6] != seg[0] and # Quebra
            seg[0] != 'E'): # Sem empates
            return True
        return False

    def _ondas_longas(self):
        # 5+ do mesmo resultado
        if len(self.historico) < 5: return False
        for i in range(len(self.historico) - 4):
            if self.historico[i] == self.historico[i+1] == self.historico[i+2] == self.historico[i+3] == self.historico[i+4]:
                return True
        return False

    def _ciclo_dominancia(self):
        # 70%+ de uma cor em 10 jogos
        if len(self.historico) < 10: return False
        
        window = self.historico[:10] # Últimos 10 jogos
        counter = collections.Counter(window)
        
        for resultado, count in counter.items():
            if resultado != 'E' and count >= 7: # 7 de 10 (70%)
                return True
        return False

    def _padrao_tensao(self):
        # Alternância seguida de explosão do mesmo resultado (CV C V C V C C C)
        if len(self.historico) < 8: return False
        if (self.historico[0] != self.historico[1] and self.historico[1] != self.historico[2] and 
            self.historico[2] != self.historico[3] and # 3 alternâncias
            self.historico[4] == self.historico[5] == self.historico[6] == self.historico[7] and # Sequência de 4
            self.historico[3] != self.historico[4] and # Quebra
            self.historico[3] != 'E' and self.historico[4] != 'E'): # Sem empates
            return True
        return False

    def _sequencia_labouchere(self):
        # Simetria: X, Y, Z, Y, X
        if len(self.historico) < 5: return False
        if (self.historico[0] == self.historico[4] and
            self.historico[1] == self.historico[3] and
            self.historico[0] != self.historico[1] and
            self.historico[1] != self.historico[2] and
            self.historico[0] != 'E' and self.historico[1] != 'E' and self.historico[2] != 'E'): # Sem empates
            return True
        return False

    def _ritmo_cardiaco(self):
        # Irregular, mas com repetições (Ex: CC V CC VVV V)
        if len(self.historico) < 8: return False
        if (self.historico[0] == self.historico[1] and # 2
            self.historico[2] != self.historico[0] and # Quebra
            self.historico[3] == self.historico[4] and # 2
            self.historico[5] == self.historico[6] == self.historico[7] and # 3
            self.historico[0] != 'E' and self.historico[2] != 'E' and self.historico[5] != 'E'): # Sem empates
            return True
        return False

    def _ciclo_pressao(self):
        # 1, 2, 3, 1, 2, 3 (crescimento e reinício)
        if len(self.historico) < 9: return False
        seg = self.historico[:9]
        if (seg[0] != seg[1] and # 1
            seg[1] == seg[2] and # 2
            seg[3] == seg[4] == seg[5] and # 3
            seg[6] != seg[5] and # Quebra para recomeço
            seg[6] == seg[7] and # 1 (reinicia como 1)
            seg[7] == seg[8] and # 2 (reinicia como 2)
            seg[0] != 'E' and seg[1] != 'E' and seg[3] != 'E' and seg[6] != 'E'): # Sem empates
            return True
        return False

    def _padrao_clusters(self):
        # Agrupamentos fortes de resultados em janelas
        if len(self.historico) < 6: return False # Mínimo para 2 clusters de 3
        
        # Últimos 6 resultados para 2 clusters de 3
        window = self.historico[:6]
        c1 = collections.Counter(window[:3])
        c2 = collections.Counter(window[3:])
        
        if (c1.most_common(1)[0][1] >= 2 and c2.most_common(1)[0][1] >= 2 and # Ambos clusters têm maioria
            c1.most_common(1)[0][0] != c2.most_common(1)[0][0] and # São de cores diferentes
            c1.most_common(1)[0][0] != 'E' and c2.most_common(1)[0][0] != 'E'): # Sem empates
            return True
        return False

    def _sequencia_polar(self):
        # Alternância extrema sem empates (ex: CVCVCVCVCV)
        if len(self.historico) < 10: return False
        
        window = self.historico[:10]
        unique_results = set(window)
        if len(unique_results) == 2 and 'E' not in unique_results:
            # Verifica se há alta alternância
            changes = sum(1 for j in range(len(window)-1) if window[j] != window[j+1])
            if changes >= 8: # Pelo menos 8 mudanças em 9 pares (muita alternância)
                return True
        return False

    def _padrao_momentum(self):
        # Aceleração no tamanho da sequência (Ex: C, VV, CCC, VVVV)
        if len(self.historico) < 10: return False
        seg = self.historico[:10]
        if (seg[0] == seg[1] and # 2
            seg[2] == seg[3] == seg[4] and # 3
            seg[5] == seg[6] == seg[7] == seg[8] and # 4
            seg[0] != seg[2] and seg[2] != seg[5] and # Cores diferentes
            seg[0] != 'E' and seg[2] != 'E' and seg[5] != 'E'): # Sem empates
            return True
        return False

    def _ciclo_respiracao(self):
        # Expansão e contração (Ex: C C C C, V, V V V)
        if len(self.historico) < 8: return False
        if (self.historico[0] == self.historico[1] == self.historico[2] == self.historico[3] and # 4 do mesmo
            self.historico[4] != self.historico[0] and # Quebra
            self.historico[5] == self.historico[6] == self.historico[7] and # 3 do novo
            self.historico[4] == self.historico[5] and # A quebra inicia a nova sequência
            self.historico[0] != 'E' and self.historico[4] != 'E'): # Sem empates
            return True
        return False

    def _padrao_resistencia(self):
        # Resultado dominante resiste a várias tentativas de quebra (Ex: C,V,C,V,C,V,C)
        if len(self.historico) < 7: return False
        if (self.historico[0] == self.historico[2] == self.historico[4] == self.historico[6] and # C,C,C,C nas posições pares
            self.historico[1] != self.historico[0] and # V
            self.historico[3] != self.historico[0] and # V
            self.historico[5] != self.historico[0] and # V
            self.historico[0] != 'E' and self.historico[1] != 'E'): # Sem empates
            return True
        return False

    def _sequencia_breakout(self):
        # Longa estabilidade seguida de mudança abrupta e nova estabilidade (Ex: CCCC, V, VVV)
        if len(self.historico) < 8: return False
        if (self.historico[0] == self.historico[1] == self.historico[2] == self.historico[3] and # 4 do mesmo
            self.historico[4] != self.historico[0] and # Quebra
            self.historico[5] == self.historico[6] == self.historico[7] and # Nova sequência de 3
            self.historico[4] == self.historico[5] and # A quebra inicia a nova sequência
            self.historico[0] != 'E' and self.historico[4] != 'E'): # Sem empates
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
        
        if not contador: # Se contador estiver vazio (pode acontecer com dados insuficientes)
            return "Sem tendência clara"

        most_common_result, most_common_count = contador.most_common(1)[0]

        if most_common_count >= 11: # Ex: 11 ou mais (aprox. 61%)
            return f"Forte tendência: {most_common_result}"
        elif most_common_count >= 7: # Ex: 7 ou mais (aprox. 39%)
            return f"Tendência moderada: {most_common_result}"
        else:
            return "Sem tendência clara"

    def sugestao_inteligente(self):
        """Gera sugestão inteligente baseada em múltiplos fatores e hierarquia de decisão."""
        analise = self.analisar_todos()
        padroes_identificados = [nome for nome, ok in analise.items() if ok]
        
        motivos_sugestao = []
        entrada_sugerida = None
        
        # --- CALCULA CONFIANÇA BASEADA NOS PESOS DOS PADRÕES ---
        confianca_total = 0
        peso_total = 0
        for padrao in padroes_identificados:
            peso = self.pesos_padroes.get(padrao, 0.5)
            confianca_total += peso
            peso_total += peso
        
        confianca_media = (confianca_total / peso_total) * 100 if peso_total > 0 else 0
        bonus_quantidade = min(20, len(padroes_identificados) * 3) # Bônus por múltiplos padrões
        confianca_final = min(99, int(confianca_media + bonus_quantidade)) # Limite superior de 99%

        # --- HIERARQUIA DE DECISÃO ---
        frequencias = self.calcular_frequencias()
        tendencia_str = self.calcular_tendencia()
        
        # Extrai o tipo de resultado da tendência
        tendencia_resultado = None
        if "tendência" in tendencia_str:
            tendencia_resultado = tendencia_str.split(': ')[1]


        # 1. Prioridade Máxima: Padrões de QUEBRA / REVERSÃO
        # Se o histórico for longo o suficiente para identificar quebras
        if len(self.historico) >= 4:
            ultimo_resultado = self.historico[0]
            penultimo_resultado = self.historico[1] if len(self.historico) > 1 else None
            antepenultimo_resultado = self.historico[2] if len(self.historico) > 2 else None

            # Padrões que indicam forte quebra ou mudança
            quebra_padroes = [p for p in padroes_identificados if 
                              "quebra" in p.lower() or "breakout" in p.lower() or 
                              "tensao" in p.lower() or "martingale" in p.lower()]

            if quebra_padroes:
                # Se o último resultado é uma sequência clara e uma quebra é detectada
                # Ex: C C C C e detecta "Quebra de Surf" -> Sugere V
                if ultimo_resultado != 'E' and collections.Counter(self.historico[:4]).get(ultimo_resultado, 0) >= 3: # 3 ou 4 do mesmo
                    entrada_sugerida = 'V' if ultimo_resultado == 'C' else 'C'
                    motivos_sugestao.append(f"Forte padrão de QUEBRA/OPORTUNIDADE detectado. Sugerindo o oposto de {ultimo_resultado}.")
                    motivos_sugestao.extend(quebra_padroes)
                    
            # Outros padrões de quebra/inversão
            if entrada_sugerida is None and 'Padrão Dragon Tiger' in padroes_identificados:
                # Dragon Tiger geralmente quebra a alternância e continua o último elemento
                # Ex: CVCVCV C. Sugere C.
                if self.historico[0] != 'E':
                    entrada_sugerida = self.historico[0]
                    motivos_sugestao.append(f"Padrão Dragon Tiger detectado. Sugerindo continuação após alternância.")
            
            if entrada_sugerida is None and 'Sequência de Labouchere' in padroes_identificados:
                 # Simetria de 5 (X Y Z Y X). Sugere continuar a "dobra" do meio ou quebrar
                 # Nesse caso, a próxima seria o quebra o padrão se for um novo X
                 if self.historico[0] != self.historico[1] and self.historico[0] != 'E' and self.historico[1] != 'E':
                     entrada_sugerida = self.historico[1] # Sugere o que quebraria a simetria se ela estivesse se formando
                     motivos_sugestao.append(f"Padrão Labouchere detectado. Sugerindo quebra da simetria.")

            if entrada_sugerida is None and 'Sequência de Fibonacci Invertida' in padroes_identificados:
                 # 8A 5B 3A. A próxima seria B, quebrando a sequência de 3A
                 if self.historico[0] == self.historico[1] == self.historico[2] and self.historico[0] != 'E':
                     entrada_sugerida = 'V' if self.historico[0] == 'C' else 'C'
                     motivos_sugestao.append(f"Padrão Fibonacci Invertida detectado. Sugerindo quebra da sequência final.")

        # 2. Prioridade Média: Padrões de Continuação (se não houver quebra iminente)
        if entrada_sugerida is None:
            continuation_padroes = [p for p in padroes_identificados if 
                                    "sequencia" in p.lower() or "surf" in p.lower() or 
                                    "ondas" in p.lower() or "dominancia" in p.lower() or 
                                    "momentum" in p.lower() or "paroli" in p.lower()]
            
            if continuation_padroes and self.historico:
                entrada_sugerida = self.historico[0] # Sugere continuar o último resultado
                motivos_sugestao.append(f"Padrão(ões) de CONTINUAÇÃO detectado(s). Sugerindo seguir a tendência atual ({self.historico[0]}).")
                motivos_sugestao.extend(continuation_padroes)
        
        # 3. Prioridade para Empates Cíclicos/Recorrentes (se não houver padrões de cor mais fortes)
        if entrada_sugerida is None:
            if 'Empate Recorrente' in padroes_identificados or 'Ciclo de Empates' in padroes_identificados:
                entrada_sugerida = 'E'
                motivos_sugestao.append("Padrão(ões) de Empate cíclico/recorrente detectado(s). Sugerindo Empate.")
                motivos_sugestao.extend([p for p in padroes_identificados if 'Empate' in p])

        # 4. Último Recurso: Frequência e Tendência (se nenhum padrão forte for encontrado)
        if entrada_sugerida is None:
            # Prefere a cor com menor frequência (regressão à média)
            opcoes_c_v = ['C', 'V']
            if len(self.historico) >= 10: # Só considera frequências se houver histórico suficiente
                freq_c_v = {k: frequencias[k] for k in opcoes_c_v}
                sorted_freq = sorted(freq_c_v.items(), key=lambda item: item[1])
                
                # Se uma cor é significativamente menos frequente, sugere ela.
                if sorted_freq[0][1] < sorted_freq[1][1] - 5: # Diferença de 5% ou mais
                    entrada_sugerida = sorted_freq[0][0]
                    motivos_sugestao.append(f"Sugestão baseada na menor frequência geral ({entrada_sugerida}).")
                else: # Frequências muito próximas, considera tendência ou aleatório
                    if tendencia_resultado and tendencia_resultado != 'E':
                        entrada_sugerida = tendencia_resultado
                        motivos_sugestao.append(f"Frequências de C/V próximas. Sugerindo baseado na tendência ({tendencia_resultado}).")
                    elif self.historico: # Se tudo mais falhar, inverte o último ou aleatório
                        last_res = self.historico[0]
                        if last_res != 'E':
                            entrada_sugerida = 'V' if last_res == 'C' else 'C'
                            motivos_sugestao.append(f"Frequências e tendências indefinidas. Sugerindo o oposto do último resultado ({last_res}).")
                        else:
                            entrada_sugerida = random.choice(['C', 'V'])
                            motivos_sugestao.append("Dados insuficientes/ambíguos para padrão forte. Sugestão aleatória de cor.")
                    else:
                        entrada_sugerida = random.choice(['C', 'V', 'E'])
                        motivos_sugestao.append("Sem histórico. Sugestão aleatória.")
            else: # Histórico muito curto para análise de frequência robusta
                if self.historico:
                    # Tenta alternar se o último não foi E
                    if self.historico[0] != 'E':
                        entrada_sugerida = 'V' if self.historico[0] == 'C' else 'C'
                        motivos_sugestao.append(f"Histórico curto. Sugerindo o oposto de {self.historico[0]} para alternância.")
                    else: # Se o último foi empate, sugere uma cor aleatória
                        entrada_sugerida = random.choice(['C', 'V'])
                        motivos_sugestao.append("Histórico curto com Empate. Sugerindo cor aleatória.")
                else: # Sem histórico algum
                    entrada_sugerida = random.choice(['C', 'V', 'E'])
                    motivos_sugestao.append("Sem histórico. Sugestão aleatória.")


        mapeamento = {"C": "Casa", "V": "Visitante", "E": "Empate"}
        entrada_legivel = mapeamento.get(entrada_sugerida, "Indefinido")
        
        return {
            "sugerir": True,
            "entrada": entrada_legivel,
            "entrada_codigo": entrada_sugerida,
            "motivos": list(set(motivos_sugestao)), # Remove duplicatas
            "confianca": confianca_final,
            "frequencias": frequencias,
            "tendencia": tendencia_str,
            "ultimos_resultados": self.historico[:5],
            "analise_detalhada": self._gerar_analise_detalhada(padroes_identificados)
        }

    def _gerar_analise_detalhada(self, padroes):
        """Gera análise detalhada dos padrões encontrados"""
        categorias = {
            "Padrões de Sequência (Continuação)": ["Sequência", "Surf", "Ondas", "Paroli", "Momentum", "Ciclo de Dominância"],
            "Padrões de Quebra/Reversão": ["Quebra", "Breakout", "Tensão", "Martingale", "Dragon Tiger", "Fibonacci Invertida", "Labouchere"],
            "Padrões Cíclicos/Repetição": ["Ciclo", "Respiração", "Empate Recorrente", "Ritmo Cardíaco"],
            "Padrões Simétricos/Estruturais": ["Espelho", "Escada", "Triangular", "Clusters", "Resistência", "Polar"],
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
            if not df.empty:
                last_row = df.iloc[-1]
                # Usa ast.literal_eval para converter string de lista/dict de forma segura
                import ast
                st.session_state.historico = ast.literal_eval(last_row['historico'])
                st.session_state.estatisticas = {
                    'total_jogos': last_row['total_jogos'],
                    'acertos': last_row['acertos'],
                    'erros': last_row['erros'],
                    'historico_sugestoes': ast.literal_eval(last_row['historico_sugestoes'])
                }
                return
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}. Iniciando com dados vazios.")
            # Opcional: remover o arquivo corrompido para evitar loop
            # os.remove(DATA_FILE) 
    
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
        'historico': [str(st.session_state.historico)], # Converte para string para salvar no CSV
        'total_jogos': st.session_state.estatisticas['total_jogos'],
        'acertos': st.session_state.estatisticas['acertos'],
        'erros': st.session_state.estatisticas['erros'],
        'historico_sugestoes': [str(st.session_state.estatisticas['historico_sugestoes'])] # Converte para string
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
            "sugestao_padroes_motivos": sugestao_para_validar['motivos'], # Padrões ativos no momento da sugestão
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
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE) # Remove o arquivo CSV para um início limpo
    st.session_state.ultima_sugestao = None # Limpa sugestão pendente
    st.rerun() # Recarrega para mostrar o estado limpo

def desfazer_ultimo():
    """Remove o último resultado e ajusta estatísticas."""
    if st.session_state.historico:
        # Não ajusta acertos/erros aqui, pois a sugestão anterior simplesmente não foi validada
        st.session_state.historico.pop(0)
        if st.session_state.estatisticas['total_jogos'] > 0:
            st.session_state.estatisticas['total_jogos'] -= 1
        st.session_state.ultima_sugestao = None # Cancela qualquer sugestão pendente
        save_data() # Salva dados após desfazer
        st.rerun() # Recarrega para mostrar o estado atualizado

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
    <div style='
        display: inline-flex; 
        align-items: center; 
        justify-content: center;
        width: 38px; 
        height: 38px; 
        border-radius: 50%; 
        background-color: {color_map.get(resultado, 'gray')}; 
        margin: 3px; 
        text-align: center; 
        line-height: 38px; 
        font-size: 16px;
        color: {"black" if resultado == "E" else "white"};
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        flex-shrink: 0; /* Impede que o item encolha */
    '>
        {symbol_map.get(resultado, '?')}
    </div>
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
div.stButton > button[data-testid*="Casa (C)"] {
    background: linear-gradient(135deg, #FF6B6B, #FF4B4B);
}

div.stButton > button[data-testid*="Visitante (V)"] {
    background: linear-gradient(135deg, #4ECDC4, #4B4BFF);
}

div.stButton > button[data-testid*="Empate (E)"] {
    background: linear-gradient(135deg, #FFE66D, #FFD700);
    color: black;
}

div.stButton > button[data-testid*="Desfazer"] {
    background: linear-gradient(135deg, #95A5A6, #7F8C8D);
}

div.stButton > button[data-testid*="Limpar Tudo"] {
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
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    border: 1px solid #dee2e6;
    overflow-x: auto; /* Permite rolagem horizontal se necessário */
    white-space: nowrap; /* Mantém os itens na mesma linha */
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
        st.metric("Acertos", acertos)
        st.metric("Erros", erros)
    else:
        st.info("Nenhum jogo analisado ainda")
    
    st.markdown("---")
    st.markdown("## ⚙️ Configurações")
    
    # auto_suggest = st.checkbox("Sugestão Automática", value=True) # Removido para simplificar
    show_advanced = st.checkbox("Análise Avançada", value=True)
    confidence_threshold = st.slider("Limite de Confiança para Sugestão", 0, 100, 60)

# --- SEÇÃO DE INSERÇÃO DE RESULTADOS ---
st.markdown('<div class="section-header"><h2>🎯 Inserir Resultado do Jogo</h2></div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🏠 Casa (C)", key="Casa (C)", use_container_width=True, help="Vitória da Casa"):
        adicionar_resultado('C')
        # st.rerun() # Não é necessário chamar rerun aqui, Streamlit já faz automaticamente

with col2:
    if st.button("✈️ Visitante (V)", key="Visitante (V)", use_container_width=True, help="Vitória do Visitante"):
        adicionar_resultado('V')
        # st.rerun()

with col3:
    if st.button("⚖️ Empate (E)", key="Empate (E)", use_container_width=True, help="Empate"):
        adicionar_resultado('E')
        # st.rerun()

with col4:
    if st.button("↩️ Desfazer", key="Desfazer", use_container_width=True, help="Desfazer último resultado"):
        desfazer_ultimo()
        # st.rerun()

with col5:
    if st.button("🗑️ Limpar Tudo", key="Limpar Tudo", use_container_width=True, help="Limpar todo o histórico e estatísticas"):
        limpar_historico()
        # st.rerun()

# --- EXIBIÇÃO DO HISTÓRICO (AGORA CORRETO) ---
st.markdown('<div class="section-header"><h2>📈 Histórico de Resultados</h2></div>', unsafe_allow_html=True)

if not st.session_state.historico:
    st.info("🎮 Nenhum resultado registrado. Comece inserindo os resultados dos jogos!")
else:
    st.markdown('<div class="historic-container">', unsafe_allow_html=True)
    
    # Exibir em linhas de 9 resultados
    num_per_row = 9
    for i in range(0, len(st.session_state.historico), num_per_row):
        row_results = st.session_state.historico[i : i + num_per_row]
        cols = st.columns(num_per_row) # Cria 9 colunas
        for j, resultado in enumerate(row_results):
            with cols[j]:
                st.markdown(get_resultado_html(resultado), unsafe_allow_html=True)
    
    st.markdown(f"**Total:** {len(st.session_state.historico)} jogos (máx. 50)", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ANÁLISE PRINCIPAL ---
if len(st.session_state.historico) >= 3: # Mínimo de 3 para iniciar qualquer análise de padrão simples
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
        st.warning(f"🤔 Confiança insuficiente ({sugestao['confianca']}%) ou nenhum padrão detectado acima do limite. Não há sugestão forte no momento. Confiança Mínima: {confidence_threshold}%.")
    
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
    st.info("🎮 Insira pelo menos 3 resultados para começar a análise de padrões e 18 para a tendência completa!")

# --- RODAPÉ ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; margin-top: 2rem;">
    <p>⚽ Football Studio Live Analyzer v3.0 | Análise Inteligente de Padrões</p>
    <p><small>Desenvolvido para Evolution Gaming Football Studio</small></p>
</div>
""", unsafe_allow_html=True)
