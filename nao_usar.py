import streamlit as st
import collections
import random
import numpy as np
from datetime import datetime
import pandas as pd

# --- CLASSE ANALISEPADROES REFINADA (mantida a mesma, foco no CSS) ---
class AnalisePadroes:
    def __init__(self, historico):
        self.historico = historico[:54] # Limita o histórico para análise, sempre os 54 mais recentes
        
        self.padroes_ativos = {
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
            "Padrão 3x1": self._padrao_3x1,
            "Padrão 4x1": self._padrao_4x1,
            "Empate em Zonas de Frequência": self._empate_zonas_frequencia,
        }
        
        self.pesos_padroes = {
            "Sequência (Surf de Cor)": 0.9,
            "Zig-Zag Perfeito": 0.8,
            "Quebra de Surf": 0.85,
            "Quebra de Zig-Zag": 0.8,
            "Duplas Repetidas": 0.7,
            "Empate Recorrente": 0.75,
            "Padrão Escada": 0.6,
            "Espelho": 0.7,
            "Alternância com Empate": 0.65,
            "Padrão Onda": 0.75,
            "Padrão Fibonacci": 0.95,
            "Sequência Dourada": 0.9,
            "Padrão Triangular": 0.8,
            "Ciclo de Empates": 0.85,
            "Padrão Martingale": 0.85,
            "Sequência de Fibonacci Invertida": 0.8,
            "Padrão Dragon Tiger": 0.85,
            "Sequência de Paroli": 0.75,
            "Padrão de Ondas Longas": 0.9,
            "Ciclo de Dominância": 0.8,
            "Padrão de Tensão": 0.7,
            "Sequência de Labouchere": 0.6,
            "Padrão Ritmo Cardíaco": 0.65,
            "Ciclo de Pressão": 0.75,
            "Padrão de Clusters": 0.7,
            "Sequência Polar": 0.7,
            "Padrão de Momentum": 0.9,
            "Ciclo de Respiração": 0.65,
            "Padrão de Resistência": 0.6,
            "Sequência de Breakout": 0.95,
            "Padrão 3x1": 0.7,
            "Padrão 4x1": 0.75,
            "Empate em Zonas de Frequência": 0.8,
        }

    def analisar_todos(self):
        resultados = {}
        for nome, func in self.padroes_ativos.items():
            try:
                resultados[nome] = func()
            except Exception as e:
                resultados[nome] = False
        return resultados

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
        if len(self.historico) < 4:
            return False
        for i in range(len(self.historico) - 3):
            if (self.historico[i] != self.historico[i+1] and 
                self.historico[i+1] != self.historico[i+2] and
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
        
        intervalos = []
        for i in range(len(empates_indices) - 1):
            intervalos.append(empates_indices[i+1] - empates_indices[i])
        
        if len(intervalos) >= 2:
            media_intervalo = sum(intervalos) / len(intervalos)
            if 2 <= media_intervalo <= 8:
                consistent_intervals = [x for x in intervalos if abs(x - media_intervalo) <= 2]
                return len(consistent_intervals) / len(intervalos) >= 0.75
        return False

    def _padrao_escada(self):
        if len(self.historico) < 6:
            return False
        for i in range(len(self.historico) - 5):
            if (self.historico[i] != self.historico[i+1] and
                self.historico[i+1] == self.historico[i+2] and
                self.historico[i+2] != self.historico[i+3] and
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5]):
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

    def _padrao_fibonacci(self):
        if len(self.historico) < 8:
            return False
        
        fib_sequence = [1, 1, 2, 3, 5]
        
        current_seq_len = []
        if self.historico:
            count = 1
            for i in range(1, len(self.historico)):
                if self.historico[i] == self.historico[i-1]:
                    count += 1
                else:
                    current_seq_len.append(count)
                    count = 1
            current_seq_len.append(count)
        
        for i in range(len(current_seq_len) - len(fib_sequence) + 1):
            if current_seq_len[i:i+len(fib_sequence)] == fib_sequence:
                return True
        return False

    def _sequencia_dourada(self):
        if len(self.historico) < 8:
            return False
        for i in range(len(self.historico) - 7):
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] and
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] == self.historico[i+6] == self.historico[i+7] and
                self.historico[i] != self.historico[i+3]):
                return True
        return False

    def _padrao_triangular(self):
        if len(self.historico) < 9:
            return False
        for i in range(len(self.historico) - 8):
            segment = self.historico[i:i+9]
            if (segment[0] == segment[8] and
                segment[1] == segment[7] and
                segment[0] != segment[1] and
                segment[2] == segment[3] == segment[4] == segment[5] == segment[6] and
                segment[1] != segment[2]):
                return True
        return False

    def _ciclo_empates(self):
        empates = [i for i, x in enumerate(self.historico) if x == 'E']
        if len(empates) < 3:
            return False
        
        for cycle_length in range(3, 11):
            is_cyclic = True
            if len(empates) >= 2:
                for i in range(len(empates) - 1):
                    actual_interval = empates[i+1] - empates[i]
                    if not (cycle_length - 2 <= actual_interval <= cycle_length + 2):
                        is_cyclic = False
                        break
            else:
                is_cyclic = False
            if is_cyclic:
                return True
        return False

    def _padrao_martingale(self):
        if len(self.historico) < 7:
            return False
        for i in range(len(self.historico) - 6):
            if (self.historico[i] != self.historico[i+1] and
                self.historico[i+1] == self.historico[i+2] and
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] == self.historico[i+6] and
                self.historico[i+1] != self.historico[i+3]):
                return True
        return False

    def _fibonacci_invertida(self):
        if len(self.historico) < 8:
            return False
        for i in range(len(self.historico) - 7):
            segment = self.historico[i:i+8]
            if (len(set(segment[0:4])) == 1 and
                segment[4] != segment[0] and
                len(set(segment[5:7])) == 1 and
                segment[7] != segment[5] and
                segment[4] == segment[7]):
                return True
        return False

    def _padrao_dragon_tiger(self):
        if len(self.historico) < 6:
            return False
        for i in range(len(self.historico) - 5):
            if (self.historico[i] != self.historico[i+1] and
                self.historico[i+1] != self.historico[i+2] and
                self.historico[i] != self.historico[i+2] and
                self.historico[i+3] == 'E' and
                self.historico[i+4] == self.historico[i+5] and
                self.historico[i+4] != 'E'):
                return True
        return False

    def _sequencia_paroli(self):
        if len(self.historico) < 7:
            return False
        for i in range(len(self.historico) - 6):
            if (self.historico[i] != self.historico[i+1] and
                self.historico[i+1] == self.historico[i+2] and
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] == self.historico[i+6] and
                self.historico[i] == self.historico[i+3]):
                return True
        return False

    def _ondas_longas(self):
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
        if len(self.historico) < 10:
            return False
        for i in range(len(self.historico) - 9):
            window = self.historico[i:i+10]
            counter = collections.Counter(window)
            
            for resultado, count in counter.items():
                if count >= 7:
                    return True
        return False

    def _padrao_tensao(self):
        if len(self.historico) < 8:
            return False
        for i in range(len(self.historico) - 7):
            alternations = 0
            for j in range(i, i+4):
                if j+1 < len(self.historico) and self.historico[j] != self.historico[j+1]:
                    alternations += 1
            
            if alternations >= 3:
                if (i+4 < len(self.historico) and 
                    self.historico[i+4] == self.historico[i+5] == self.historico[i+6]):
                    return True
        return False

    def _sequencia_labouchere(self):
        if len(self.historico) < 6:
            return False
        for i in range(len(self.historico) - 5):
            if (self.historico[i] == self.historico[i+5] and
                self.historico[i+1] == self.historico[i+4] and
                self.historico[i] != self.historico[i+1] and
                self.historico[i+2] != self.historico[i+3] and
                self.historico[i+2] != self.historico[i] and
                self.historico[i+3] != self.historico[i]):
                return True
        return False

    def _ritmo_cardiaco(self):
        if len(self.historico) < 8:
            return False
        for i in range(len(self.historico) - 7):
            segment = self.historico[i:i+8]
            if (segment[0] == segment[1] and
                segment[2] != segment[0] and
                segment[3] == segment[4] and
                segment[5] == segment[6] == segment[7] and
                segment[0] != segment[3] and
                segment[3] != segment[5]):
                return True
        return False

    def _ciclo_pressao(self):
        if len(self.historico) < 9:
            return False
        for i in range(len(self.historico) - 8):
            segment = self.historico[i:i+9]
            if (segment[0] != segment[1] and
                segment[1] == segment[2] and
                segment[3] == segment[4] == segment[5] and
                segment[6] == segment[0] and
                segment[7] == segment[8] and
                segment[6] != segment[7]):
                return True
        return False

    def _padrao_clusters(self):
        if len(self.historico) < 12:
            return False
        for i in range(len(self.historico) - 11):
            window = self.historico[i:i+12]
            cluster1 = window[:4]
            cluster2 = window[4:8]
            cluster3 = window[8:12]
            
            if (collections.Counter(cluster1).most_common(1)[0][1] >= 3 and
                collections.Counter(cluster2).most_common(1)[0][1] >= 3 and
                collections.Counter(cluster3).most_common(1)[0][1] >= 3):
                return True
        return False

    def _sequencia_polar(self):
        if len(self.historico) < 10:
            return False
        for i in range(len(self.historico) - 9):
            window = self.historico[i:i+10]
            unique_results = set(window)
            if len(unique_results) == 2 and 'E' not in unique_results:
                changes = sum(1 for j in range(len(window)-1) if window[j] != window[j+1])
                if changes >= 6:
                    return True
        return False

    def _padrao_momentum(self):
        if len(self.historico) < 10:
            return False
        for i in range(len(self.historico) - 9):
            segment = self.historico[i:i+10]
            if (segment[0] != segment[1] and
                segment[1] == segment[2] and
                segment[3] == segment[4] == segment[5] and
                segment[6] == segment[7] == segment[8] == segment[9] and
                segment[0] != segment[1] and segment[1] != segment[3] and segment[3] != segment[6]):
                return True
        return False

    def _ciclo_respiracao(self):
        if len(self.historico) < 8:
            return False
        for i in range(len(self.historico) - 7):
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] == self.historico[i+3] and
                self.historico[i+4] != self.historico[i] and
                self.historico[i+5] == self.historico[i+6] == self.historico[i+7] and
                self.historico[i+5] == self.historico[i+4]):
                return True
        return False

    def _padrao_resistencia(self):
        if len(self.historico) < 6:
            return False
        for i in range(len(self.historico) - 5):
            if (self.historico[i] == self.historico[i+2] == self.historico[i+4] == self.historico[i+5] and
                self.historico[i+1] != self.historico[i] and
                self.historico[i+3] != self.historico[i]):
                return True
        return False

    def _sequencia_breakout(self):
        if len(self.historico) < 8:
            return False
        for i in range(len(self.historico) - 7):
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] == self.historico[i+3] and
                self.historico[i+4] != self.historico[i] and
                self.historico[i+5] == self.historico[i+6] == self.historico[i+7] and
                self.historico[i+5] == self.historico[i+4]):
                return True
        return False

    def _padrao_3x1(self):
        if len(self.historico) < 4:
            return False
        for i in range(len(self.historico) - 3):
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] and
                self.historico[i+2] != self.historico[i+3]):
                return True
        return False
        
    def _padrao_4x1(self):
        if len(self.historico) < 5:
            return False
        for i in range(len(self.historico) - 4):
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] == self.historico[i+3] and
                self.historico[i+3] != self.historico[i+4]):
                return True
        return False

    def _empate_zonas_frequencia(self):
        empates_indices = [i for i, r in enumerate(self.historico) if r == 'E']
        if len(empates_indices) < 2:
            return False

        intervals = []
        for i in range(len(empates_indices) - 1):
            intervals.append(empates_indices[i+1] - empates_indices[i])

        if len(self.historico) >= 2 and self.historico[0] == 'E' and self.historico[1] == 'E':
            return True

        for interval in intervals:
            if (8 <= interval <= 11) or (14 <= interval <= 36):
                return True
        
        if len(intervals) > 0 and intervals[0] > 15:
             return True
        
        return False

    def calcular_frequencias(self):
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
        if len(self.historico) < 9:
            return {
                "sugerir": False,
                "entrada": None,
                "entrada_codigo": None,
                "motivos": ["Histórico insuficiente (mínimo 9 jogos para sugestão)"],
                "confianca": 0,
                "frequencias": self.calcular_frequencias(),
                "tendencia": self.calcular_tendencia(),
                "ultimos_resultados": self.historico[:5]
            }

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
        
        confianca_total = 0
        peso_total = 0
        
        for padrao in padroes_identificados:
            peso = self.pesos_padroes.get(padrao, 0.5)
            confianca_total += peso
            peso_total += peso
        
        confianca_media = (confianca_total / peso_total) * 100 if peso_total > 0 else 0
        
        bonus_quantidade = min(20, len(padroes_identificados) * 3)
        confianca_final = min(99, int(confianca_media + bonus_quantidade))
        
        frequencias = self.calcular_frequencias()
        tendencia = self.calcular_tendencia()
        
        opcoes = ["V", "C", "E"]
        
        padroes_quebra = [p for p in padroes_identificados if "quebra" in p.lower() or "breakout" in p.lower()]
        if padroes_quebra:
            ultimo_resultado = self.historico[0] if self.historico else None
            if ultimo_resultado:
                if ultimo_resultado == 'E':
                    freq_cv = {k: v for k, v in frequencias.items() if k != 'E'}
                    if freq_cv:
                        sugerido = min(freq_cv, key=freq_cv.get)
                    else:
                        sugerido = random.choice(['C', 'V'])
                else:
                    opcoes_opostas = [op for op in ['C', 'V'] if op != ultimo_resultado]
                    if opcoes_opostas:
                        sugerido = random.choice(opcoes_opostas)
                    else:
                        sugerido = random.choice(opcoes)
            else:
                sugerido = random.choice(opcoes)
        
        elif any(p for p in padroes_identificados if "sequência" in p.lower() or "dominância" in p.lower() or "onda" in p.lower() or "momentum" in p.lower() or "surf" in p.lower()):
            ultimos_resultados_para_tendencia = self.historico[:min(len(self.historico), 5)]
            if ultimos_resultados_para_tendencia:
                sugerido = collections.Counter(ultimos_resultados_para_tendencia).most_common(1)[0][0]
            else:
                sugerido = random.choice(opcoes)
        
        elif any(p for p in padroes_identificados if "empate" in p.lower()):
            sugerido = 'E'
        
        else:
            sugerido = min(opcoes, key=lambda x: frequencias.get(x, 0))

            freq_values = list(frequencias.values())
            if len(set(freq_values)) == 1 or (max(freq_values) - min(freq_values) < 5):
                ultimos_3 = self.historico[:3]
                if ultimos_3:
                    contador_recente = collections.Counter(ultimos_3)
                    if contador_recente.most_common(1)[0][1] >= 2 and len(set(ultimos_3)) < 3:
                        resultado_frequente = contador_recente.most_common(1)[0][0]
                        opcoes_mudanca = [op for op in opcoes if op != resultado_frequente]
                        if opcoes_mudanca:
                            sugerido = random.choice(opcoes_mudanca)
                        else:
                            sugerido = random.choice(opcoes)
                    else:
                        sugerido = min(opcoes, key=lambda x: frequencias.get(x, 0))
                else:
                    sugerido = random.choice(opcoes)

        mapeamento = {"C": "Casa", "V": "Visitante", "E": "Empate"}
        entrada_legivel = mapeamento[sugerido]
        
        return {
            "sugerir": True,
            "entrada": entrada_legivel,
            "entrada_codigo": sugerido,
            "motivos": padroes_identificados,
            "confianca": confianca_final,
            "frequencias": frequencias,
            "tendencia": tendencia,
            "ultimos_resultados": self.historico[:5],
            "analise_detalhada": self._gerar_analise_detalhada(padroes_identificados)
        }

    def _gerar_analise_detalhada(self, padroes):
        categorias = {
            "Padrões de Sequência e Repetição": ["Sequência", "Surf", "Ondas", "Martingale", "Paroli", "Momentum", "Clusters", "3x1", "4x1"],
            "Padrões de Quebra e Inversão": ["Quebra", "Breakout", "Tensão", "Resistência"],
            "Padrões Cíclicos e Recorrência": ["Ciclo", "Empate Recorrente", "Zonas de Frequência", "Respiração", "Ritmo Cardíaco", "Pressão"],
            "Padrões Estruturais Especiais": ["Espelho", "Escada", "Alternância com Empate", "Triangular", "Labouchere", "Dragon Tiger", "Polar"],
            "Padrões Fibonacci/Proporção": ["Fibonacci", "Dourada", "Fibonacci Invertida"],
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
        'historico_sugestoes': []
    }

def adicionar_resultado(resultado):
    if (
        'ultima_sugestao' in st.session_state and
        st.session_state.ultima_sugestao['sugerir'] and
        st.session_state.estatisticas['total_jogos'] == len(st.session_state.estatisticas['historico_sugestoes'])
    ):
        sugestao_anterior = st.session_state.ultima_sugestao

        if sugestao_anterior['entrada_codigo'] == resultado:
            st.session_state.estatisticas['acertos'] += 1
            acertou = True
        else:
            st.session_state.estatisticas['erros'] += 1
            acertou = False
        
        st.session_state.estatisticas['historico_sugestoes'].append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'sugerido': sugestao_anterior['entrada_codigo'],
            'real': resultado,
            'confianca': sugestao_anterior['confianca'],
            'acertou': acertou,
            'motivos': sugestao_anterior['motivos']
        })

        del st.session_state.ultima_sugestao

    st.session_state.historico.insert(0, resultado)
    st.session_state.estatisticas['total_jogos'] += 1
 
def limpar_historico():
    st.session_state.historico = []
    st.session_state.estatisticas = {
        'total_jogos': 0,
        'acertos': 0,
        'erros': 0,
        'historico_sugestoes': []
    }
    if 'ultima_sugestao' in st.session_state:
        del st.session_state.ultima_sugestao


def desfazer_ultimo():
    if st.session_state.historico:
        st.session_state.historico.pop(0)
        if st.session_state.estatisticas['total_jogos'] > 0:
            st.session_state.estatisticas['total_jogos'] -= 1
        
        if 'ultima_sugestao' in st.session_state:
             del st.session_state.ultima_sugestao

def get_resultado_html(resultado):
    color_map = {'C': '#FF4B4B', 'V': '#4B4BFF', 'E': '#FFD700'}

    return f"""
    <div class='roadmap-item' style='
        background-color: {color_map.get(resultado, 'gray')} !important;
        width: 25px !important;
        height: 25px !important;
        border-radius: 50% !important;
        display: inline-block !important;
        margin: 2px !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    '>
    </div>
    """
def get_confianca_color(confianca):
    if confianca >= 80:
        return "#4CAF50"
    elif confianca >= 60:
        return "#FF9800"
    elif confianca >= 40:
        return "#FFC107"
    else:
        return "#F44336"

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    layout="wide", 
    page_title="🎯 Football Studio Live Analyzer",
    page_icon="⚽",
    initial_sidebar_state="expanded"
)

# CSS Aprimorado com st.html para melhor injeção
st.html("""
<style>
/* Estilo geral */
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    padding: 2rem !important;
    border-radius: 10px !important;
    margin-bottom: 2rem !important;
    text-align: center !important;
}

.main-header h1 {
    color: white !important;
    font-size: 2.5rem !important;
    margin: 0 !important;
}

.main-header p {
    color: white !important;
    font-size: 1.2rem !important;
    margin: 0.5rem 0 0 0 !important;
    opacity: 0.9 !important;
}

/* Botões */
div.stButton > button:first-child {
    font-size: 16px !important;
    padding: 12px 24px !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    margin: 5px !important;
    color: white !important;
    border: none !important;
    font-weight: bold !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
}

div.stButton > button:first-child:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 12px rgba(0,0,0,0.3) !important;
}

/* Botões específicos */
div.stButton > button[data-testid*="stButton-CASA"] {
    background: linear-gradient(135deg, #FF6B6B, #FF4B4B) !important; /* Vermelho */
}

div.stButton > button[data-testid*="stButton-EMPATE"] {
    background: linear-gradient(135deg, #FFE66D, #FFD700) !important; /* Amarelo */
    color: black !important;
}

div.stButton > button[data-testid*="stButton-VISITANTE"] {
    background: linear-gradient(135deg, #4ECDC4, #4B4BFF) !important; /* Azul */
}

div.stButton > button[data-testid*="stButton-Desfazer"],
div.stButton > button[data-testid*="stButton-Limpar"] {
    background: linear-gradient(135deg, #95A5A6, #7F8C8D) !important;
}

/* Cards de estatísticas */
.metric-card {
    background: white !important;
    padding: 1.5rem !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    border-left: 4px solid #667eea !important;
    margin: 1rem 0 !important;
}

.metric-card h3 {
    margin: 0 0 0.5rem 0 !important;
    color: #2C3E50 !important;
}

.metric-card p {
    margin: 0 !important;
    font-size: 1.1rem !important;
    font-weight: bold !important;
}

/* Seções */
.section-header {
    background: linear-gradient(135deg, #74b9ff, #0984e3) !important;
    color: white !important;
    padding: 1rem !important;
    border-radius: 8px !important;
    margin: 1rem 0 !important;
    text-align: center !important;
}

.pattern-found {
    background: linear-gradient(135deg, #00b894, #55a3ff) !important;
    color: white !important;
    padding: 0.5rem 1rem !important;
    border-radius: 6px !important;
    margin: 0.25rem 0 !important;
    font-weight: bold !important;
}

.pattern-not-found {
    background: #f8f9fa !important;
    color: #6c757d !important;
    padding: 0.5rem 1rem !important;
    border-radius: 6px !important;
    margin: 0.25rem 0 !important;
    border: 1px solid #dee2e6 !important;
}

.suggestion-box {
    background: linear-gradient(135deg, #a8edea, #fed6e3) !important;
    padding: 2rem !important;
    border-radius: 12px !important;
    margin: 1rem 0 !important;
    border: 2px solid #667eea !important;
}

.confidence-high { color: #27AE60 !important; font-weight: bold !important; }
.confidence-medium { color: #F39C12 !important; font-weight: bold !important; }
.confidence-low { color: #E74C3C !important; font-weight: bold !important; }

/* Styles for the roadmap grid - APLICAR AO CONTAINER PAI */
.roadmap-grid-container {
    display: grid !important;
    grid-template-columns: repeat(9, 28px) !important; /* Ajustado para 9 colunas de 28px */
    gap: 2px !important; /* Espaçamento entre os círculos */
    justify-content: start !important;
    align-items: start !important;
    padding: 5px !important;
    border: 1px solid #333 !important;
    border-radius: 5px !important;
    background-color: #1a1a1a !important;
    max-width: fit-content !important; /* Ajusta a largura ao conteúdo */
    overflow-x: hidden !important; /* Garante que não haja scroll horizontal */
}

/* Styles for each roadmap item (the circles) */
.roadmap-item {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 25px !important; /* Tamanho do círculo */
    height: 25px !important;
    border-radius: 50% !important; /* Faz o item ser um círculo */
    font-size: 14px !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    flex-shrink: 0 !important; /* Impede que os itens encolham */
    box-sizing: border-box !important; /* Garante que padding e border não aumentem o tamanho total */
}

/* Ajuste para o texto dentro dos botões de resultado */
div.stButton > button[data-testid*="stButton-CASA"] div,
div.stButton > button[data-testid*="stButton-EMPATE"] div,
div.stButton > button[data-testid*="stButton-VISITANTE"] div {
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}

</style>
""") # Fechamento do st.html

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
        taxa_acerto = (acertos / (acertos + erros)) * 100 if (acertos + erros) > 0 else 0
        st.metric("Total de Jogos Registrados", total_jogos)
        st.metric("Total de Sugestões Validadas", acertos + erros)
        st.metric("Taxa de Acerto das Sugestões", f"{taxa_acerto:.1f}%")
        st.metric("Acertos", acertos, delta=acertos-erros)
        st.metric("Erros", erros)
    else:
        st.info("Nenhum jogo analisado ainda.")
    
    st.markdown("---")
    st.markdown("## ⚙️ Configurações")
    
    show_advanced = st.checkbox("Análise Avançada e Detalhes", value=True)
    confidence_threshold = st.slider("Limite Mínimo de Confiança para Sugestão", 0, 100, 60)

# --- SEÇÃO DE INSERÇÃO DE RESULTADOS ---
st.markdown('<div class="section-header"><h2>🎯 Inserir Resultado do Jogo</h2></div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🔴 CASA (C)", key="stButton-CASA", use_container_width=True, help="Vitória da Casa"):
        adicionar_resultado('C')
        st.rerun()

with col2:
    if st.button("🟡 EMPATE (E)", key="stButton-EMPATE", use_container_width=True, help="Empate"):
        adicionar_resultado('E')
        st.rerun()

with col3:
    if st.button("🔵 VISITANTE (V)", key="stButton-VISITANTE", use_container_width=True, help="Vitória do Visitante"):
        adicionar_resultado('V')
        st.rerun()

with col4:
    if st.button("↩️ DESFAZER ÚLTIMO", key="stButton-Desfazer", use_container_width=True, help="Remove o último resultado inserido"):
        desfazer_ultimo()
        st.rerun()

with col5:
    if st.button("🗑️ LIMPAR TUDO", key="stButton-Limpar", use_container_width=True, help="Limpa todo o histórico e estatísticas"):
        limpar_historico()
        st.rerun()

import streamlit.components.v1 as components

# --- EXIBIÇÃO DO HISTÓRICO EM LINHAS DE 9 ---
st.markdown('<div class="section-header"><h2>📈 Histórico de Resultados</h2></div>', unsafe_allow_html=True)

if not st.session_state.historico:
    st.info("🎮 Nenhum resultado registrado. Comece inserindo os resultados dos jogos!")
else:
    grid_html_content = ""
    for resultado_cell in st.session_state.historico:
        grid_html_content += get_resultado_html(resultado_cell)

    components.html(f"""
    <div class="roadmap-grid-container">
        {grid_html_content}
    </div>
    """, height=300, scrolling=False)

    st.markdown(f"**Total:** {len(st.session_state.historico)} jogos", unsafe_allow_html=True)


    st.markdown(f"**Total:** {len(st.session_state.historico)} jogos", unsafe_allow_html=True)


# --- ANÁLISE PRINCIPAL ---
st.markdown('<div class="section-header"><h2>🧠 Análise e Sugestão</h2></div>', unsafe_allow_html=True)

if len(st.session_state.historico) >= 9:
    analyzer = AnalisePadroes(st.session_state.historico[::-1])
    sugestao = analyzer.sugestao_inteligente()
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
            <p><strong>Tendência Atual:</strong> {sugestao['tendencia']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if show_advanced:
            with st.expander("📋 Detalhes da Análise"):
                st.write("**Padrões Identificados que influenciaram a sugestão:**")
                if sugestao['motivos']:
                    for motivo in sugestao['motivos']:
                        st.write(f"• {motivo}")
                else:
                    st.info("Nenhum padrão específico detectado, sugestão baseada em estatísticas gerais.")
                
                if 'analise_detalhada' in sugestao and sugestao['analise_detalhada']:
                    st.write("**Análise por Categoria de Padrões:**")
                    for categoria, padroes_list in sugestao['analise_detalhada'].items():
                        st.write(f"**{categoria}:** {', '.join(padroes_list)}")
    else:
        if len(st.session_state.historico) < 9:
             st.info(f"🤔 Insira mais {9 - len(st.session_state.historico)} resultados para iniciar a sugestão inteligente.")
        else:
             st.warning(f"🤔 Confiança insuficiente ({sugestao['confianca']}%) para uma sugestão, ou nenhum padrão relevante detectado no momento.")
    
    if show_advanced:
        st.markdown('<div class="section-header"><h2>🔍 Padrões Detectados (Detalhado)</h2></div>', unsafe_allow_html=True)
        
        padroes_encontrados = analyzer.analisar_todos()
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("### ✅ Padrões Ativos")
            encontrados = [nome for nome, status in padroes_encontrados.items() if status]
            
            if encontrados:
                for padrao in encontrados:
                    peso = analyzer.pesos_padroes.get(padrao, 0.5)
                    st.markdown(f'<div class="pattern-found">✅ {padrao} (Peso: {peso})</div>', unsafe_allow_html=True)
            else:
                st.info("Nenhum padrão específico detectado no histórico atual.")
        
        with col_right:
            st.markdown("### ❌ Outros Padrões (Inativos)")
            nao_encontrados = [nome for nome, status in padroes_encontrados.items() if not status]
            
            if nao_encontrados:
                for padrao in nao_encontrados[:15]:
                    st.markdown(f'<div class="pattern-not-found">❌ {padrao}</div>', unsafe_allow_html=True)
                if len(nao_encontrados) > 15:
                    st.write(f"E mais {len(nao_encontrados) - 15} padrões inativos...")
            else:
                st.info("Todos os padrões estão ativos (improvável).")
        
    if show_advanced:
        st.markdown('<div class="section-header"><h2>📊 Análise Estatística Geral</h2></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        frequencias = analyzer.calcular_frequencias()
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🔴 Casa</h3>
                <p style="color: #FF4B4B;">{frequencias['C']}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🔵 Visitante</h3>
                <p style="color: #4B4BFF;">{frequencias['V']}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🟡 Empate</h3>
                <p style="color: #FFD700;">{frequencias['E']}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 📈 Distribuição de Frequências (Gráfico)")
        chart_data = pd.DataFrame({
            'Resultado': ['Casa', 'Visitante', 'Empate'],
            'Frequência': [frequencias['C'], frequencias['V'], frequencias['E']]
        })
        chart_colors = {
            'Casa': '#FF4B4B',
            'Visitante': '#4B4BFF',
            'Empate': '#FFD700'
        }
        
        st.bar_chart(chart_data.set_index('Resultado').T, color=[chart_colors[col] for col in chart_data['Resultado']])
        
        with st.expander("Histórico de Sugestões e Resultados Reais"):
            if st.session_state.estatisticas['historico_sugestoes']:
                df_sugestoes = pd.DataFrame(st.session_state.estatisticas['historico_sugestoes'])
                df_sugestoes['Acertou?'] = df_sugestoes['acertou'].apply(lambda x: '✅ Sim' if x else '❌ Não')
                df_sugestoes_display = df_sugestoes[['timestamp', 'sugerido', 'real', 'confianca', 'Acertou?', 'motivos']]
                st.dataframe(df_sugestoes_display, use_container_width=True)
            else:
                st.info("Nenhuma sugestão foi validada ainda.")

else:
    st.info(f"🎮 Insira pelo menos 9 resultados para começar a análise inteligente e as sugestões!")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; margin-top: 2rem;">
    <p>⚽ Football Studio Live Analyzer v2.2 | Análise Inteligente de Padrões</p>
    <p><small>Desenvolvido para Evolution Gaming Football Studio</small></p>
</div>
""", unsafe_allow_html=True)
