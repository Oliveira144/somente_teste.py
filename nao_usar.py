import streamlit as st
import collections
import random
import numpy as np
import pandas as pd
from datetime import datetime # Mantido caso você o use em outras partes do seu projeto

# --- CLASSE ANALISEPADROES REFINADA E AJUSTADA ---
class AnalisePadroes:
    """
    Classe para analisar padrões em um histórico de resultados de jogos
    (ex: 'C' para Casa, 'F' para Fora, 'E' para Empate) e gerar sugestões.
    """
    def __init__(self, historico: list):
        """
        Inicializa a classe com um histórico de resultados.
        O histórico é truncado para os últimos 50 jogos para foco na análise recente.

        Args:
            historico (list): Uma lista de strings representando os resultados dos jogos.
                               Ex: ['C', 'F', 'E', 'C', 'C']
        """
        # Limita o histórico aos últimos 50 jogos para análise.
        self.historico = historico[:50] if len(historico) > 50 else historico[:]

        self.padroes_ativos_map = {
            # Padrões Básicos
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

            # Novos Padrões Específicos do Football Studio
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

        # Pesos dos padrões para calcular a confiança e sugestão.
        # Ajuste esses pesos para dar mais importância a padrões que você considera mais preditivos.
        self.pesos_padroes = {
            "Sequência (Surf de Cor)": 1.2,
            "Zig-Zag Perfeito": 1.0,
            "Quebra de Surf": 1.1,
            "Quebra de Zig-Zag": 1.0,
            "Duplas Repetidas": 0.8,
            "Empate Recorrente": 1.3,
            "Padrão Escada": 0.7,
            "Espelho": 0.9,
            "Alternância com Empate": 0.9,
            "Padrão Onda": 0.8,
            "Padrão Fibonacci": 1.0,
            "Sequência Dourada": 1.0,
            "Padrão Triangular": 0.8,
            "Ciclo de Empates": 1.4,
            "Padrão Martingale": 1.1,
            "Sequência de Fibonacci Invertida": 1.0,
            "Padrão Dragon Tiger": 1.2,
            "Sequência de Paroli": 0.9,
            "Padrão de Ondas Longas": 1.3,
            "Ciclo de Dominância": 1.1,
            "Padrão de Tensão": 1.0,
            "Sequência de Labouchere": 0.7,
            "Padrão Ritmo Cardíaco": 0.8,
            "Ciclo de Pressão": 0.9,
            "Padrão de Clusters": 0.8,
            "Sequência Polar": 1.0,
            "Padrão de Momentum": 1.2,
            "Ciclo de Respiração": 0.9,
            "Padrão de Resistência": 1.1,
            "Sequência de Breakout": 1.2,
        }

    def analisar_todos(self) -> dict:
        """
        Analisa o histórico para detectar quais padrões estão ativos.
        Returns:
            dict: Um dicionário onde as chaves são os nomes dos padrões e os valores
                  são True se o padrão for detectado, False caso contrário.
        """
        resultados = {}
        for nome, func in self.padroes_ativos_map.items():
            try:
                resultados[nome] = func()
            except Exception as e:
                #st.error(f"Erro ao analisar o padrão '{nome}': {e}") # Usar em Streamlit para visualização
                resultados[nome] = False
        return resultados

    # --- Métodos Auxiliares Internos ---
    def _get_last_result(self) -> str | None:
        """Retorna o último resultado do histórico, se houver."""
        return self.historico[0] if self.historico else None
    
    def _get_second_last_result(self) -> str | None:
        """Retorna o penúltimo resultado do histórico, se houver."""
        return self.historico[1] if len(self.historico) >= 2 else None

    def _get_result_counts_in_window(self, window_size: int) -> collections.Counter:
        """
        Retorna a contagem de cada resultado em uma janela recente do histórico.
        """
        if len(self.historico) < window_size:
            return collections.Counter(self.historico)
        return collections.Counter(self.historico[:window_size])

    # --- PADRÕES BÁSICOS EXISTENTES ---
    def _sequencia_simples(self) -> bool:
        if len(self.historico) < 3: return False
        return self.historico[0] == self.historico[1] == self.historico[2]

    def _zig_zag(self) -> bool:
        if len(self.historico) < 6: return False
        for i in range(5):
            if self.historico[i] == self.historico[i+1]: return False
        return True

    def _quebra_de_surf(self) -> bool:
        if len(self.historico) < 4: return False
        return (self.historico[0] == self.historico[1] == self.historico[2] and
                self.historico[2] != self.historico[3])

    def _quebra_de_zig_zag(self) -> bool:
        if len(self.historico) < 5: return False
        return (self.historico[0] != self.historico[1] and
                self.historico[1] != self.historico[2] and
                self.historico[2] != self.historico[3] and
                self.historico[3] == self.historico[4])

    def _duplas_repetidas(self) -> bool:
        if len(self.historico) < 4: return False
        return (self.historico[0] == self.historico[1] and
                self.historico[2] == self.historico[3] and
                self.historico[0] != self.historico[2])

    def _empate_recorrente(self) -> bool:
        empates_indices = [i for i, r in enumerate(self.historico) if r == 'E']
        if len(empates_indices) < 3: return False
        intervals = np.diff(empates_indices)
        if len(intervals) >= 2:
            media_intervalo = np.mean(intervals)
            # Adicionado uma tolerância para o desvio padrão
            return 2 <= media_intervalo <= 8 and np.std(intervals) < media_intervalo * 0.5
        return False

    def _padrao_escada(self) -> bool:
        if len(self.historico) < 6: return False
        return (self.historico[0] != self.historico[1] and
                self.historico[1] == self.historico[2] and
                self.historico[3] == self.historico[4] == self.historico[5] and
                self.historico[1] != self.historico[3])

    def _espelho(self) -> bool:
        for tamanho in range(4, min(len(self.historico) + 1, 13), 2):
            metade = tamanho // 2
            segmento = self.historico[:tamanho]
            if segmento[:metade] == segmento[metade:][::-1]:
                return True
        return False

    def _alternancia_empate_meio(self) -> bool:
        if len(self.historico) < 3: return False
        return (self.historico[0] != 'E' and self.historico[1] == 'E' and
                self.historico[2] != 'E' and self.historico[0] != self.historico[2])

    def _padrao_onda(self) -> bool:
        if len(self.historico) < 6: return False
        return (self.historico[0] == self.historico[2] == self.historico[4] and
                self.historico[1] == self.historico[3] == self.historico[5] and
                self.historico[0] != self.historico[1])

    # --- NOVOS PADRÕES ESPECÍFICOS DO FOOTBALL STUDIO ---
    def _padrao_fibonacci(self) -> bool:
        if len(self.historico) < 8: return False
        fib_lengths = [1, 1, 2, 3] # Ajustado para um comprimento mais razoável para análise em 8 elementos
        current_idx = 0
        results_to_check = self.historico[:]
        try:
            for length in fib_lengths:
                if current_idx + length > len(results_to_check): return False
                block = results_to_check[current_idx : current_idx + length]
                if not block or not all(x == block[0] for x in block): return False
                # A condição abaixo verifica se o bloco atual é diferente do anterior,
                # essencial para o padrão Fibonacci de resultados alternados.
                if current_idx > 0 and block[0] == results_to_check[current_idx - 1]: return False
                current_idx += length
            return True
        except IndexError: return False
        
    def _sequencia_dourada(self) -> bool:
        if len(self.historico) < 8: return False
        return (self.historico[0] == self.historico[1] == self.historico[2] and
                self.historico[3] == self.historico[4] == self.historico[5] == self.historico[6] == self.historico[7] and
                self.historico[0] != self.historico[3])

    def _padrao_triangular(self) -> bool:
        if len(self.historico) < 9: return False
        segment = self.historico[:9]
        return (segment[0] == segment[8] and segment[1] == segment[7] and 
                segment[2] == segment[6] and segment[3] == segment[5] and
                len(set(segment[2:7])) == 1 and segment[0] != segment[4])

    def _ciclo_empates(self) -> bool:
        empates = [i for i, x in enumerate(self.historico) if x == 'E']
        if len(empates) < 3: return False
        if len(empates) >= 3:
            intervals = np.diff(empates)
            if np.mean(intervals) >= 2 and np.std(intervals) < 2: return True
        return False

    def _padrao_martingale(self) -> bool:
        if len(self.historico) < 7: return False
        return (self.historico[0] != self.historico[1] and
                self.historico[1] == self.historico[2] and
                self.historico[3] == self.historico[4] == self.historico[5] == self.historico[6] and
                self.historico[1] != self.historico[3])

    def _fibonacci_invertida(self) -> bool:
        if len(self.historico) < 8: return False
        return (self.historico[0] == self.historico[1] and self.historico[2] != self.historico[0] and
                self.historico[3] == self.historico[4] and self.historico[5] != self.historico[3] and
                self.historico[6] == self.historico[7] and self.historico[0] != self.historico[3])

    def _padrao_dragon_tiger(self) -> bool:
        if len(self.historico) < 6: return False
        return (self.historico[0] != self.historico[1] and self.historico[1] != self.historico[2] and
                self.historico[3] == 'E' and self.historico[4] == self.historico[5] and
                self.historico[4] != 'E')

    def _sequencia_paroli(self) -> bool:
        if len(self.historico) < 8: return False
        return (self.historico[0] != self.historico[1] and self.historico[1] == self.historico[2] and
                self.historico[3] == self.historico[4] == self.historico[5] == self.historico[6] and
                self.historico[0] == self.historico[7])

    def _ondas_longas(self) -> bool:
        if len(self.historico) < 5: return False
        count = 1
        for i in range(1, len(self.historico)):
            if self.historico[i] == self.historico[i-1]:
                count += 1
                if count >= 5: return True
            else: count = 1
        return False

    def _ciclo_dominancia(self) -> bool:
        if len(self.historico) < 10: return False
        window = self.historico[:10]
        counter = collections.Counter(window)
        for _, count in counter.items():
            if count >= 7: return True
        return False

    def _padrao_tensao(self) -> bool:
        if len(self.historico) < 7: return False
        alternations = 0
        for i in range(3):
            if self.historico[i] != self.historico[i+1]: alternations += 1
            else: return False
        return (alternations == 3 and self.historico[4] == self.historico[5] == self.historico[6])

    def _sequencia_labouchere(self) -> bool:
        if len(self.historico) < 6: return False
        segment = self.historico[:6]
        return (segment[0] == segment[5] and segment[1] == segment[4] and
                segment[2] != segment[0] and segment[3] != segment[0] and segment[2] == segment[3])

    def _ritmo_cardiaco(self) -> bool:
        if len(self.historico) < 8: return False
        segment = self.historico[:8]
        return (segment[0] == segment[1] and segment[2] != segment[0] and
                segment[3] == segment[4] and segment[5] == segment[6] == segment[7] and
                segment[3] != segment[5])

    def _ciclo_pressao(self) -> bool:
        if len(self.historico) < 9: return False
        return (self.historico[0] != self.historico[1] and self.historico[1] == self.historico[2] and
                self.historico[3] == self.historico[4] == self.historico[5] and self.historico[6] == self.historico[0] and
                self.historico[7] == self.historico[1] and self.historico[8] == self.historico[2])

    def _padrao_clusters(self) -> bool:
        if len(self.historico) < 12: return False
        window = self.historico[:12]
        cluster1 = window[0:4]
        cluster2 = window[4:8]
        cluster3 = window[8:12]
        return (collections.Counter(cluster1).most_common(1)[0][1] >= 3 and
                collections.Counter(cluster2).most_common(1)[0][1] >= 3 and
                collections.Counter(cluster3).most_common(1)[0][1] >= 3)

    def _sequencia_polar(self) -> bool:
        if len(self.historico) < 10: return False
        window = self.historico[:10]
        unique_results = set(window)
        if len(unique_results) == 2 and 'E' not in unique_results:
            changes = sum(1 for j in range(len(window)-1) if window[j] != window[j+1])
            return changes >= 6
        return False

    def _padrao_momentum(self) -> bool:
        if len(self.historico) < 10: return False
        return (self.historico[0] != self.historico[1] and self.historico[1] == self.historico[2] and
                self.historico[3] == self.historico[4] == self.historico[5] and
                self.historico[6] == self.historico[7] == self.historico[8] == self.historico[9] and
                self.historico[1] != self.historico[3] and self.historico[3] != self.historico[6])

    def _ciclo_respiracao(self) -> bool:
        if len(self.historico) < 8: return False
        return (self.historico[0] == self.historico[1] == self.historico[2] == self.historico[3] and
                self.historico[4] != self.historico[0] and self.historico[5] == self.historico[6] == self.historico[7] and
                self.historico[5] != self.historico[4])

    def _padrao_resistencia(self) -> bool:
        if len(self.historico) < 6: return False
        return (self.historico[0] == self.historico[2] == self.historico[4] == self.historico[5] and
                self.historico[1] != self.historico[0] and self.historico[3] != self.historico[0])

    def _sequencia_breakout(self) -> bool:
        if len(self.historico) < 8: return False
        return (self.historico[0] == self.historico[1] == self.historico[2] == self.historico[3] and
                self.historico[4] != self.historico[0] and self.historico[5] == self.historico[6] == self.historico[7] and
                self.historico[5] == self.historico[4])

    def calcular_frequencias(self):
        """Calcula frequências dos resultados"""
        contador = collections.Counter(self.historico)
        total = len(self.historico)
        if total == 0: return {'C': 0, 'F': 0, 'E': 0} # Alterado 'V' para 'F'
        
        result = {k: round(v / total * 100, 1) for k, v in contador.items()}
        for tipo in ['C', 'F', 'E']: # 'V' alterado para 'F'
            if tipo not in result:
                result[tipo] = 0
        return result

    def calcular_tendencia(self):
        """Calcula tendência dos últimos resultados"""
        if len(self.historico) < 5: return "Dados insuficientes"
        
        ultimos_5 = self.historico[:5]
        contador = collections.Counter(ultimos_5)
        
        if contador.most_common(1)[0][1] >= 4: return f"Forte tendência: {contador.most_common(1)[0][0]}"
        elif contador.most_common(1)[0][1] >= 3: return f"Tendência moderada: {contador.most_common(1)[0][0]}"
        else: return "Sem tendência clara"

    def gerar_sugestao(self) -> dict:
        """
        Gera uma sugestão de próximo resultado com base nos padrões ativos e seus pesos,
        além de considerar a tendência mais recente.
        """
        if not self.historico:
            return {
                "sugerir": False, "entrada": None, "entrada_codigo": None,
                "motivos": ["Nenhum histórico para análise."], "confianca": 0.0,
                "frequencias": self.calcular_frequencias(), "tendencia": "Sem dados",
                "ultimos_resultados": [], "analise_detalhada": {}
            }

        padroes_ativos = self.analisar_todos()
        
        pontuacoes = {'C': 0.0, 'F': 0.0, 'E': 0.0} # Usando 'F' para Fora/Visitante
        
        last_result = self._get_last_result()
        second_last_result = self._get_second_last_result()
        
        # 1. Pontuação baseada nos padrões ativos
        motivos_sugestao = []
        total_peso_padroes = 0.0 # Para calcular a confiança
        
        for nome_padrao, ativo in padroes_ativos.items():
            if ativo:
                peso = self.pesos_padroes.get(nome_padrao, 0.5)
                motivos_sugestao.append(nome_padrao)
                total_peso_padroes += peso

                # --- Lógica de Sugestão para CADA PADRÃO ---
                # Aumente os pesos aqui para os padrões que você confia mais.
                # 'V' no Streamlit é mapeado para 'F' (Fora) aqui

                if nome_padrao == "Sequência (Surf de Cor)":
                    if last_result: pontuacoes[last_result] += peso * 1.5

                elif nome_padrao == "Zig-Zag Perfeito":
                    if last_result == 'C': pontuacoes['F'] += peso
                    elif last_result == 'F': pontuacoes['C'] += peso
                    
                elif nome_padrao == "Quebra de Surf":
                    if len(self.historico) >= 4 and self.historico[0] == self.historico[1] == self.historico[2] and self.historico[2] != self.historico[3]:
                        pontuacoes[self.historico[3]] += peso * 1.2
                    
                elif nome_padrao == "Quebra de Zig-Zag":
                    if len(self.historico) >= 5 and self.historico[3] == self.historico[4]:
                        pontuacoes[self.historico[3]] += peso * 1.2

                elif nome_padrao == "Duplas Repetidas":
                    if len(self.historico) >= 4 and self.historico[0] == self.historico[1] and self.historico[2] == self.historico[3]:
                        pontuacoes[self.historico[0]] += peso

                elif nome_padrao == "Empate Recorrente":
                    pontuacoes['E'] += peso * 1.5

                elif nome_padrao == "Padrão Escada":
                    if len(self.historico) >= 6 and self.historico[1] == self.historico[2] and self.historico[3] == self.historico[4] == self.historico[5]:
                        if self.historico[0] == 'C': pontuacoes['F'] += peso
                        elif self.historico[0] == 'F': pontuacoes['C'] += peso
                        else: pontuacoes['E'] += peso # Se for E, tenta o oposto do que quebrou a escada
                        
                elif nome_padrao == "Espelho":
                    if last_result == 'C': pontuacoes['F'] += peso * 0.5
                    elif last_result == 'F': pontuacoes['C'] += peso * 0.5
                    elif last_result == 'E': pontuacoes['E'] += peso * 0.5

                elif nome_padrao == "Alternância com Empate":
                    if len(self.historico) >= 3 and self.historico[1] == 'E' and self.historico[0] != self.historico[2]:
                        if self.historico[0] == 'C': pontuacoes['F'] += peso
                        elif self.historico[0] == 'F': pontuacoes['C'] += peso

                elif nome_padrao == "Padrão Onda":
                    if len(self.historico) >= 6 and self.historico[0] == self.historico[2] == self.historico[4] and self.historico[1] == self.historico[3] == self.historico[5]:
                        pontuacoes[self.historico[1]] += peso

                elif nome_padrao == "Padrão Fibonacci":
                    if last_result == 'C': pontuacoes['F'] += peso * 1.1
                    elif last_result == 'F': pontuacoes['C'] += peso * 1.1
                    elif last_result == 'E': pontuacoes['E'] += peso * 0.8

                elif nome_padrao == "Sequência Dourada":
                    if len(self.historico) >= 8 and self.historico[3] == self.historico[4]:
                        pontuacoes[self.historico[3]] += peso * 1.2

                elif nome_padrao == "Padrão Triangular":
                    if len(self.historico) >= 9 and self.historico[0] == self.historico[8]:
                        if self.historico[4] == 'C': pontuacoes['F'] += peso
                        elif self.historico[4] == 'F': pontuacoes['C'] += peso
                        elif self.historico[4] == 'E': pontuacoes['E'] += peso * 0.8

                elif nome_padrao == "Ciclo de Empates":
                    pontuacoes['E'] += peso * 1.8

                elif nome_padrao == "Padrão Martingale":
                    if len(self.historico) >= 7 and self.historico[3] == self.historico[4]:
                        pontuacoes[self.historico[3]] += peso * 1.5 # Sugere a continuação da sequência

                elif nome_padrao == "Sequência de Fibonacci Invertida":
                    if last_result == 'C': pontuacoes['F'] += peso * 1.1
                    elif last_result == 'F': pontuacoes['C'] += peso * 1.1
                    elif last_result == 'E': pontuacoes['E'] += peso * 0.8

                elif nome_padrao == "Padrão Dragon Tiger":
                    if len(self.historico) >= 6 and self.historico[4] == self.historico[5]:
                        pontuacoes[self.historico[4]] += peso * 1.3

                elif nome_padrao == "Sequência de Paroli":
                    if len(self.historico) >= 8 and self.historico[0] == self.historico[7]:
                        pontuacoes[self.historico[0]] += peso * 1.2

                elif nome_padrao == "Padrão de Ondas Longas":
                    if last_result: pontuacoes[last_result] += peso * 1.6 # Sugere continuação da onda

                elif nome_padrao == "Ciclo de Dominância":
                    dominant_result = collections.Counter(self.historico[:10]).most_common(1)[0][0]
                    pontuacoes[dominant_result] += peso * 1.1

                elif nome_padrao == "Padrão de Tensão":
                    if len(self.historico) >= 7 and self.historico[4] == self.historico[5] == self.historico[6]:
                        pontuacoes[self.historico[4]] += peso * 1.2

                elif nome_padrao == "Sequência de Labouchere":
                    if len(self.historico) >= 6 and self.historico[0] == self.historico[5]:
                        if last_result == 'C': pontuacoes['F'] += peso
                        elif last_result == 'F': pontuacoes['C'] += peso
                        elif last_result == 'E': pontuacoes['E'] += peso

                elif nome_padrao == "Padrão Ritmo Cardíaco":
                    if len(self.historico) >= 8:
                        if self.historico[5] == self.historico[6] == self.historico[7]:
                            if self.historico[5] == 'C': pontuacoes['F'] += peso * 0.7
                            elif self.historico[5] == 'F': pontuacoes['C'] += peso * 0.7
                            elif self.historico[5] == 'E': pontuacoes['E'] += peso * 0.7

                elif nome_padrao == "Ciclo de Pressão":
                    if len(self.historico) >= 9 and self.historico[6] == self.historico[0]:
                        pontuacoes[self.historico[0]] += peso * 1.1

                elif nome_padrao == "Padrão de Clusters":
                    if len(self.historico) >= 12:
                        last_cluster_dominant = collections.Counter(self.historico[8:12]).most_common(1)[0][0]
                        pontuacoes[last_cluster_dominant] += peso * 1.0

                elif nome_padrao == "Sequência Polar":
                    if len(self.historico) >= 10:
                        if last_result == 'C': pontuacoes['F'] += peso * 1.0
                        elif last_result == 'F': pontuacoes['C'] += peso * 1.0

                elif nome_padrao == "Padrão de Momentum":
                    if len(self.historico) >= 10 and self.historico[6] == self.historico[7]:
                        pontuacoes[self.historico[6]] += peso * 1.4

                elif nome_padrao == "Ciclo de Respiração":
                    if len(self.historico) >= 8 and self.historico[5] == self.historico[6] == self.historico[7]:
                        pontuacoes[self.historico[5]] += peso * 1.1

                elif nome_padrao == "Padrão de Resistência":
                    if len(self.historico) >= 6 and self.historico[0] == self.historico[2]:
                        pontuacoes[self.historico[0]] += peso * 1.2

                elif nome_padrao == "Sequência de Breakout":
                    if len(self.historico) >= 8 and self.historico[5] == self.historico[6] == self.historico[7]:
                        # Em um breakout, geralmente se aposta CONTRA o que está sendo quebrado ou a favor da nova tendência
                        # Se a sequência anterior ('C','C','C','C') quebra com 'F', aposta-se 'F'.
                        # Aqui, se o breakout foi com um resultado, sugere-se a continuação daquele.
                        pontuacoes[self.historico[5]] += peso * 1.5
        
        # 2. Adicionar uma pontuação baseada na tendência mais recente (últimos 3-5 jogos)
        recentes_window = self.historico[:min(len(self.historico), 5)] # Últimos 5, ou menos se não houver
        if recentes_window:
            contagem_recentes = collections.Counter(recentes_window)
            for resultado, count in contagem_recentes.items():
                if resultado in pontuacoes:
                    pontuacoes[resultado] += count * 0.2 # Peso menor para a contagem simples

        # 3. Determinar a sugestão final
        melhor_sugestao_codigo = "N/A"
        maior_pontuacao = -1.0

        if any(pontuacoes.values()): # Verifica se há alguma pontuação
            resultados_ordenados = sorted(pontuacoes.items(), key=lambda item: item[1], reverse=True)
            melhor_sugestao_codigo = resultados_ordenados[0][0]
            maior_pontuacao = resultados_ordenados[0][1]

            # Lógica para desempatar, favorecendo o empate se as pontuações forem muito próximas
            # e o empate tiver alguma pontuação relevante.
            if 'E' in pontuacoes and pontuacoes['E'] > 0 and \
               (maior_pontuacao > 0 and (pontuacoes['E'] >= maior_pontuacao * 0.9 and pontuacoes['E'] < maior_pontuacao)):
                melhor_sugestao_codigo = 'E'
        else: # Se nenhuma pontuação foi atribuída por padrões, sugere o que menos saiu
            frequencias = self.calcular_frequencias()
            if frequencias:
                melhor_sugestao_codigo = min(frequencias, key=frequencias.get)
            else:
                melhor_sugestao_codigo = random.choice(['C', 'F', 'E']) # Último recurso
                
        # Calcular uma confiança percentual
        total_pontuacao_geral = sum(pontuacoes.values())
        confianca_percentual = (maior_pontuacao / total_pontuacao_geral) * 100 if total_pontuacao_geral > 0 else 0

        # Mapeamento para nomes legíveis (incluindo 'V' se o botão ainda mostrar 'V' na interface)
        mapeamento_legivel = {"C": "Casa", "F": "Visitante", "E": "Empate"}
        
        return {
            "sugerir": True,
            "entrada": mapeamento_legivel.get(melhor_sugestao_codigo, "N/A"),
            "entrada_codigo": melhor_sugestao_codigo,
            "motivos": motivos_sugestao,
            "confianca": min(99, int(confianca_percentual)), # Limita a confiança para não parecer 100% garantido
            "frequencias": self.calcular_frequencias(),
            "tendencia": self.calcular_tendencia(),
            "ultimos_resultados": self.historico[:5],
            "analise_detalhada": self._gerar_analise_detalhada(motivos_sugestao)
        }

    def _gerar_analise_detalhada(self, padroes):
        """Gera análise detalhada dos padrões encontrados"""
        categorias = {
            "Padrões de Sequência": ["Sequência", "Surf", "Ondas", "Fibonacci", "Momentum", "Paroli"],
            "Padrões de Quebra": ["Quebra", "Breakout", "Tensão"],
            "Padrões Cíclicos": ["Ciclo", "Respiração", "Ritmo", "Pressão", "Empate Recorrente"],
            "Padrões de Simetria/Alternância": ["Espelho", "Alternância", "Zig-Zag", "Escada", "Duplas", "Polar", "Labouchere", "Triangular"],
            "Padrões de Dominância": ["Clusters", "Resistência", "Dominância", "Dragon Tiger"]
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
    # Histórico de exemplo para iniciar com dados válidos
    st.session_state.historico = ['C', 'F', 'C', 'E', 'F', 'F', 'C', 'C', 'E', 'F', 'C', 'F', 'C', 'F', 'E', 'C'] 

if 'estatisticas' not in st.session_state:
    st.session_state.estatisticas = {
        'total_jogos': 0,
        'acertos': 0,
        'erros': 0,
        'historico_sugestoes': []
    }

# Para capturar e exibir logs/erros na UI (opcional)
if 'log_messages' not in st.session_state:
    st.session_state.log_messages = []

def log_message(type, message):
    st.session_state.log_messages.append(f"[{datetime.now().strftime('%H:%M:%S')}] [{type.upper()}] {message}")

def adicionar_resultado(resultado):
    """Adiciona novo resultado ao histórico"""
    st.session_state.historico.insert(0, resultado)
    if len(st.session_state.historico) > 50:
        st.session_state.historico = st.session_state.historico[:50]
    st.session_state.estatisticas['total_jogos'] += 1
    log_message("info", f"Resultado '{resultado}' adicionado. Total: {len(st.session_state.historico)}")


def limpar_historico():
    """Limpa todo o histórico"""
    st.session_state.historico = []
    st.session_state.estatisticas = {
        'total_jogos': 0,
        'acertos': 0,
        'erros': 0,
        'historico_sugestoes': []
    }
    log_message("info", "Histórico limpo.")


def desfazer_ultimo():
    """Remove o último resultado"""
    if st.session_state.historico:
        removed_result = st.session_state.historico.pop(0)
        if st.session_state.estatisticas['total_jogos'] > 0:
            st.session_state.estatisticas['total_jogos'] -= 1
        log_message("info", f"Último resultado '{removed_result}' desfeito.")
    else:
        log_message("warn", "Tentativa de desfazer com histórico vazio.")


def validar_sugestao(sugestao_anterior, resultado_real):
    """Valida se a sugestão anterior estava correta"""
    if sugestao_anterior and sugestao_anterior['entrada_codigo'] == resultado_real:
        st.session_state.estatisticas['acertos'] += 1
        log_message("success", f"Sugestão anterior ACERTADA! Sugerido: {sugestao_anterior['entrada_codigo']}, Real: {resultado_real}")
        return True
    else:
        st.session_state.estatisticas['erros'] += 1
        log_message("error", f"Sugestão anterior ERRADA! Sugerido: {sugestao_anterior['entrada_codigo'] if sugestao_anterior else 'N/A'}, Real: {resultado_real}")
        return False

def get_resultado_html(resultado):
    """Retorna HTML para visualização do resultado"""
    color_map = {'C': '#FF4B4B', 'F': '#4B4BFF', 'E': '#FFD700'} # Mapeado 'F' para azul (Visitante)
    symbol_map = {'C': '🏠', 'F': '✈️', 'E': '⚖️'} # Mapeado 'F' para avião (Visitante)
    
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
    """Retorna cor baseada no nível de confiança"""
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

div.stButton > button[data-testid="stButton-✈️ Visitante (F)"] { /* MUDADO para (F) */
    background: linear-gradient(135deg, #4ECDC4, #4B4BFF);
}

div.stButton > button[data-testid="stButton-⚖️ Empate (E)"] {
    background: linear-gradient(135deg, #FFE66D, #FFD700);
    color: black;
}

div.stButton > button[data-testid="stButton-↩️ Desfazer"],
div.stButton > button[data-testid="stButton-🗑️ Limpar"] {
    background: linear-gradient(135deg, #95A5A6, #7F8C8D);
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
        st.metric("Acertos", acertos, delta=acertos-erros)
    else:
        st.info("Nenhum jogo analisado ainda")
    
    st.markdown("---")
    st.markdown("## ⚙️ Configurações")
    
    auto_suggest = st.checkbox("Sugestão Automática", value=True)
    show_advanced = st.checkbox("Análise Avançada", value=True)
    confidence_threshold = st.slider("Limite de Confiança", 0, 100, 60)

    st.markdown("---")
    st.markdown("## 📝 Logs de Depuração")
    # Exibe logs de depuração na sidebar
    log_area = st.empty()
    if st.session_state.log_messages:
        for log in reversed(st.session_state.log_messages[-10:]): # Mostra os 10 últimos logs
            log_area.text(log)
    else:
        log_area.info("Nenhum log ainda.")


# --- SEÇÃO DE INSERÇÃO DE RESULTADOS ---
st.markdown('<div class="section-header"><h2>🎯 Inserir Resultado do Jogo</h2></div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🏠 Casa (C)", key="CasaC", use_container_width=True, help="Vitória da Casa"):
        adicionar_resultado('C')
        st.rerun()

with col2:
    if st.button("✈️ Visitante (F)", key="VisitanteF", use_container_width=True, help="Vitória do Visitante"): # Alterado para (F) no botão
        adicionar_resultado('F') # Alterado para 'F' aqui
        st.rerun()

with col3:
    if st.button("⚖️ Empate (E)", key="EmpateE", use_container_width=True, help="Empate"):
        adicionar_resultado('E')
        st.rerun()

with col4:
    if st.button("↩️ Desfazer", key="Desfazer", use_container_width=True, help="Desfazer último resultado"):
        desfazer_ultimo()
        st.rerun()

with col5:
    if st.button("🗑️ Limpar", key="Limpar", use_container_width=True, help="Limpar todo o histórico"):
        limpar_historico()
        st.rerun()

# --- EXIBIÇÃO DO HISTÓRICO ---
st.markdown('<div class="section-header"><h2>📈 Histórico de Resultados</h2></div>', unsafe_allow_html=True)

if not st.session_state.historico:
    st.info("🎮 Nenhum resultado registrado. Comece inserindo os resultados dos jogos!")
else:
    st.markdown('<div class="historic-container">', unsafe_allow_html=True)
    
    historico_html = ""
    for i, resultado in enumerate(st.session_state.historico):
        historico_html += get_resultado_html(resultado)
        if (i + 1) % 10 == 0 and (i + 1) < len(st.session_state.historico):
            historico_html += "<br>"
    
    st.markdown(historico_html, unsafe_allow_html=True)
    st.markdown(f"**Total:** {len(st.session_state.historico)} jogos (máx. 50)", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ANÁLISE PRINCIPAL ---
if len(st.session_state.historico) >= 5:
    try:
        analyzer = AnalisePadroes(st.session_state.historico)
        log_message("info", "Objeto AnalisePadroes criado.")
        
        # --- SUGESTÃO INTELIGENTE ---
        st.markdown('<div class="section-header"><h2>🎯 Sugestão Inteligente</h2></div>', unsafe_allow_html=True)
        
        sugestao = analyzer.gerar_sugestao() # Chamada corrigida
        log_message("info", f"Sugestão gerada: {sugestao['entrada_codigo']} (Confiança: {sugestao['confianca']}%)")

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
                <p><strong>Tendência:</strong> {sugestao['tendencia']}</p>
                <p><strong>Frequências (C/F/E):</strong> {sugestao['frequencias'].get('C',0)}% / {sugestao['frequencias'].get('F',0)}% / {sugestao['frequencias'].get('E',0)}%</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Detalhes da análise
            if show_advanced:
                with st.expander("📋 Detalhes da Análise"):
                    st.write("**Padrões Identificados:**")
                    if sugestao['motivos']:
                        for motivo in sugestao['motivos']:
                            st.write(f"• {motivo}")
                    else:
                        st.info("Nenhum padrão específico contribuiu para a sugestão com peso suficiente.")
                    
                    if 'analise_detalhada' in sugestao and sugestao['analise_detalhada']:
                        st.write("**Análise por Categoria:**")
                        for categoria, padroes in sugestao['analise_detalhada'].items():
                            st.write(f"**{categoria}:** {', '.join(padroes)}")
                    else:
                        st.info("Nenhuma análise detalhada de categorias de padrões disponível.")

        else:
            st.warning(f"🤔 Confiança insuficiente ({sugestao['confianca']}%) ou nenhum padrão detectado com peso relevante para sugestão.")
            log_message("warn", f"Sugestão não exibida: Confiança {sugestao['confianca']}% abaixo do limite {confidence_threshold}%.")

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
                st.info("Nenhum padrão específico detectado")
        
        with col_right:
            st.markdown("### ❌ Padrões Não Encontrados")
            nao_encontrados = [nome for nome, status in padroes_encontrados.items() if not status]
            
            if nao_encontrados:
                for padrao in nao_encontrados[:15]:  # Limita a exibição para não sobrecarregar
                    st.markdown(f'<div class="pattern-not-found">❌ {padrao}</div>', unsafe_allow_html=True)
            else:
                st.info("Todos os padrões avaliados foram encontrados (improvável).")
        
        # --- ANÁLISE ESTATÍSTICA ---
        st.markdown('<div class="section-header"><h2>📊 Análise Estatística</h2></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        frequencias = analyzer.calcular_frequencias()
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🏠 Casa</h3>
                <p style="color: #FF4B4B;">{frequencias.get('C', 0.0)}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>✈️ Visitante</h3>
                <p style="color: #4B4BFF;">{frequencias.get('F', 0.0)}%</p>
            </div>
            """, unsafe_allow_html=True) # Alterado para .get('F', 0.0)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>⚖️ Empate</h3>
                <p style="color: #FFD700;">{frequencias.get('E', 0.0)}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráfico de frequências
        if show_advanced:
            st.markdown("### 📈 Distribuição dos Resultados")
            chart_data = pd.DataFrame({
                'Resultado': ['Casa', 'Visitante', 'Empate'],
                'Frequência': [frequencias.get('C', 0.0), frequencias.get('F', 0.0), frequencias.get('E', 0.0)], # Alterado para .get('F', 0.0)
                'Cor': ['#FF4B4B', '#4B4BFF', '#FFD700']
            })
            
            st.bar_chart(chart_data.set_index('Resultado')['Frequência'])

    except Exception as e:
        st.error(f"Ocorreu um erro inesperado durante a análise: {e}")
        st.exception(e) # Exibe o traceback completo para depuração
        log_message("critical", f"Erro crítico: {e}")

else:
    st.info("🎮 Insira pelo menos 5 resultados para começar a análise inteligente!")

# --- RODAPÉ ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; margin-top: 2rem;">
    <p>⚽ Football Studio Live Analyzer v2.0 | Análise Inteligente de Padrões</p>
    <p><small>Desenvolvido para Evolution Gaming Football Studio</small></p>
</div>
""", unsafe_allow_html=True)

