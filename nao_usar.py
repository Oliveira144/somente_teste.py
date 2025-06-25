import streamlit as st
import collections
import random
import numpy as np
import pandas as pd
from datetime import datetime

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
        # Assume que o histórico está sempre com o mais recente primeiro (insert(0))
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
            
            # Padrões solicitados pelo usuário
            "Padrão 2x1x2": self._padrao_2x1x2,
            "Padrão 2x2": self._padrao_2x2,
            "Padrão 3x3": self._padrao_3x3,
            "Padrão 4x4": self._padrao_4x4,
        }

        # Pesos dos padrões para calcular a confiança e sugestão.
        # Ajustei os pesos para os padrões novos darem mais relevância ao "surf"
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
            
            # Pesos para os novos padrões (aumentados para priorizar o "surf")
            "Padrão 2x1x2": 1.6, # Peso alto para indicar continuidade (AA B AA)
            "Padrão 2x2": 1.4,   # Relevância para o 2x2
            "Padrão 3x3": 1.7,   # Peso mais alto para sequências mais longas de duplas
            "Padrão 4x4": 1.9,   # Peso ainda mais alto
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
                # É bom manter logs embutidos para depuração, mesmo que Streamlit capture exceções
                st.session_state.log_messages.append(f"[{datetime.now().strftime('%H:%M:%S')}] [ERROR] Erro ao analisar o padrão '{nome}': {e}")
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
        # Este padrão específico é C C F F
        return (self.historico[0] == self.historico[1] and
                self.historico[2] == self.historico[3] and
                self.historico[0] != self.historico[2])

    def _empate_recorrente(self) -> bool:
        empates_indices = [i for i, r in enumerate(self.historico) if r == 'E']
        if len(empates_indices) < 3: return False
        intervals = np.diff(empates_indices) # Corrigido para usar empates_indices
        if len(intervals) >= 2:
            media_intervalo = np.mean(intervals)
            # Ajustando a tolerância para ser mais flexível em "recorrente"
            return 2 <= media_intervalo <= 8 and np.std(intervals) < media_intervalo * 0.8
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
        fib_lengths = [1, 1, 2, 3] # Representa C, F, C C, F F F (alternando)
        current_idx = 0
        results_to_check = self.historico[:]
        try:
            for length in fib_lengths:
                if current_idx + length > len(results_to_check): return False
                block = results_to_check[current_idx : current_idx + length]
                if not block or not all(x == block[0] for x in block): return False # Verifica se o bloco é uniforme
                # Verifica se o bloco atual é diferente do anterior, garantindo alternância
                if current_idx > 0 and block[0] == results_to_check[current_idx - 1]: return False
                current_idx += length
            return True
        except IndexError: return False
        
    def _sequencia_dourada(self) -> bool:
        if len(self.historico) < 8: return False
        return (self.historico[0] == self.historico[1] == self.historico[2] and # 3 do mesmo
                self.historico[3] == self.historico[4] == self.historico[5] == self.historico[6] == self.historico[7] and # 5 do mesmo
                self.historico[0] != self.historico[3]) # Mas diferentes entre si

    def _padrao_triangular(self) -> bool:
        if len(self.historico) < 9: return False
        segment = self.historico[:9]
        # Padrão: A B C D C B A E A (onde A é o resultado mais externo, e E é o do meio)
        # Ajuste para verificar se o centro (segment[4]) é o mesmo da base (segment[0])
        # e se a parte central é uniforme (ex: C C C)
        return (segment[0] == segment[8] and segment[1] == segment[7] and 
                segment[2] == segment[6] and segment[3] == segment[5] and
                segment[0] != segment[4]) # A base é diferente do pico/centro do triângulo

    def _ciclo_empates(self) -> bool:
        empates = [i for i, x in enumerate(self.historico) if x == 'E']
        if len(empates) < 3: return False
        # Procura por intervalos regulares entre empates
        intervals = np.diff(empates)
        if len(intervals) >= 2:
            media_intervalo = np.mean(intervals)
            # Um ciclo é mais forte se os intervalos são consistentes
            return np.std(intervals) < 1.5 and 2 <= media_intervalo <= 7 # Intervalos médios entre 2 e 7 jogos

    def _padrao_martingale(self) -> bool:
        if len(self.historico) < 7: return False
        # Ex: A B B C C C C (após uma quebra, uma sequência forte)
        return (self.historico[0] != self.historico[1] and # A quebra
                self.historico[1] == self.historico[2] and # B B
                self.historico[3] == self.historico[4] == self.historico[5] == self.historico[6] and # C C C C
                self.historico[1] != self.historico[3]) # B diferente de C

    def _fibonacci_invertida(self) -> bool:
        if len(self.historico) < 8: return False
        # Ex: C C F F C C F F (sequências curtas e alternadas)
        # Mais genérico: Dupla A, Dupla B, Dupla C, Dupla D, onde A!=B, B!=C, C!=D
        return (self.historico[0] == self.historico[1] and           # Dupla 1
                self.historico[2] == self.historico[3] and           # Dupla 2
                self.historico[4] == self.historico[5] and           # Dupla 3
                self.historico[6] == self.historico[7] and           # Dupla 4
                self.historico[0] != self.historico[2] and           # Dupla 1 diferente de Dupla 2
                self.historico[2] != self.historico[4] and           # Dupla 2 diferente de Dupla 3
                self.historico[4] != self.historico[6])              # Dupla 3 diferente de Dupla 4

    def _padrao_dragon_tiger(self) -> bool:
        if len(self.historico) < 6: return False
        # Ex: C F C E F F (Alternância, um empate, e uma dupla)
        return (self.historico[0] != self.historico[1] and self.historico[1] != self.historico[2] and # Zig-zag inicial
                self.historico[3] == 'E' and # Um empate no meio
                self.historico[4] == self.historico[5] and # Uma dupla
                self.historico[4] != 'E') # E não pode ser o da dupla

    def _sequencia_paroli(self) -> bool:
        if len(self.historico) < 8: return False
        # Ex: C F F C C C C C (Quebra, dupla, sequência longa, e o primeiro e o último são iguais)
        return (self.historico[0] != self.historico[1] and # Quebra
                self.historico[1] == self.historico[2] and # Dupla
                self.historico[3] == self.historico[4] == self.historico[5] == self.historico[6] and # Sequência de 4
                self.historico[0] == self.historico[7]) # O primeiro e o oitavo são iguais

    def _ondas_longas(self) -> bool:
        if len(self.historico) < 5: return False
        count = 1
        for i in range(1, len(self.historico)):
            if self.historico[i] == self.historico[i-1]:
                count += 1
                if count >= 5: return True # Detecta qualquer sequência de 5 ou mais
            else: count = 1
        return False

    def _ciclo_dominancia(self) -> bool:
        if len(self.historico) < 10: return False
        window = self.historico[:10]
        counter = collections.Counter(window)
        for _, count in counter.items():
            if count >= 7: return True # Um resultado domina 70% da janela

        return False

    def _padrao_tensao(self) -> bool:
        if len(self.historico) < 7: return False
        # Ex: C F C F C C C (Alternância que se "quebra" em uma sequência forte)
        alternations_ok = (self.historico[0] != self.historico[1] and
                           self.historico[1] != self.historico[2] and
                           self.historico[2] != self.historico[3]) # As 3 primeiras alternâncias
        
        sequence_break = (self.historico[3] == self.historico[4] == self.historico[5] == self.historico[6]) # Uma sequência de 4
        
        return alternations_ok and sequence_break and (self.historico[2] != self.historico[3]) # A alternância é quebrada pela sequência

    def _sequencia_labouchere(self) -> bool:
        if len(self.historico) < 6: return False
        # Ex: C F X X F C (primeiro e último iguais, segundo e penúltimo iguais, meio diferente)
        segment = self.historico[:6]
        return (segment[0] == segment[5] and segment[1] == segment[4] and
                segment[2] != segment[0] and segment[3] != segment[0] and segment[2] == segment[3]) # Meio é uma dupla diferente

    def _ritmo_cardiaco(self) -> bool:
        if len(self.historico) < 8: return False
        # Ex: C C F C C F F F (Dupla, quebra, dupla, quebra, tripla)
        segment = self.historico[:8]
        return (segment[0] == segment[1] and segment[2] != segment[0] and # Dupla A, Quebra
                segment[3] == segment[4] and segment[5] != segment[3] and # Dupla B, Quebra
                segment[5] == segment[6] == segment[7]) # Tripla C, B diferente de C

    def _ciclo_pressao(self) -> bool:
        if len(self.historico) < 9: return False
        # Ex: A B B C C C A B B (repetição de padrões pequenos em um ciclo)
        return (self.historico[0] != self.historico[1] and self.historico[1] == self.historico[2] and # A B B
                self.historico[3] == self.historico[4] == self.historico[5] and # C C C
                self.historico[6] == self.historico[0] and # Repete A
                self.historico[7] == self.historico[1] and self.historico[8] == self.historico[2]) # Repete B B

    def _padrao_clusters(self) -> bool:
        if len(self.historico) < 12: return False
        # Procura por "blocos" densos de resultados do mesmo tipo
        window = self.historico[:12]
        cluster1 = window[0:4]
        cluster2 = window[4:8]
        cluster3 = window[8:12]
        # Pelo menos 3 do mesmo em cada cluster de 4
        return (collections.Counter(cluster1).most_common(1)[0][1] >= 3 and
                collections.Counter(cluster2).most_common(1)[0][1] >= 3 and
                collections.Counter(cluster3).most_common(1)[0][1] >= 3)

    def _sequencia_polar(self) -> bool:
        if len(self.historico) < 10: return False
        # Alternância extrema entre dois resultados sem empates
        window = self.historico[:10]
        unique_results = set(window)
        if len(unique_results) == 2 and 'E' not in unique_results:
            changes = sum(1 for j in range(len(window)-1) if window[j] != window[j+1])
            return changes >= 6 # Pelo menos 6 mudanças em 9 possíveis (alta alternância)
        return False

    def _padrao_momentum(self) -> bool:
        if len(self.historico) < 10: return False
        # Ex: A B B C C C D D D D (sequências crescentes de diferentes resultados)
        return (self.historico[0] != self.historico[1] and self.historico[1] == self.historico[2] and # 1x A, 2x B
                self.historico[3] == self.historico[4] == self.historico[5] and # 3x C
                self.historico[6] == self.historico[7] == self.historico[8] == self.historico[9] and # 4x D
                self.historico[1] != self.historico[3] and self.historico[3] != self.historico[6]) # B != C != D

    def _ciclo_respiracao(self) -> bool:
        if len(self.historico) < 8: return False
        # Ex: A A A A B C C C (Sequência longa, quebra, e nova sequência)
        return (self.historico[0] == self.historico[1] == self.historico[2] == self.historico[3] and # Sequência de 4
                self.historico[4] != self.historico[0] and # Quebra
                self.historico[5] == self.historico[6] == self.historico[7] and # Nova sequência de 3
                self.historico[5] != self.historico[4]) # E a nova sequência é diferente da quebra

    def _padrao_resistencia(self) -> bool:
        if len(self.historico) < 6: return False
        # Ex: A B A C A A (um resultado 'A' aparece e 'resiste' a interrupções)
        return (self.historico[0] == self.historico[2] == self.historico[4] == self.historico[5] and # A em posições específicas
                self.historico[1] != self.historico[0] and self.historico[3] != self.historico[0]) # Interrupções são diferentes de A

    def _sequencia_breakout(self) -> bool:
        if len(self.historico) < 8: return False
        # Ex: A A A A B B B B (sequência longa, quebra e nova sequência longa do tipo da quebra)
        return (self.historico[0] == self.historico[1] == self.historico[2] == self.historico[3] and # Sequência AAAA
                self.historico[4] != self.historico[0] and # Quebra para B
                self.historico[5] == self.historico[6] == self.historico[7] and # Sequência BBB
                self.historico[5] == self.historico[4]) # O resultado da quebra inicia a nova sequência

    # --- NOVOS PADRÕES SOLICITADOS ---
    def _padrao_2x1x2(self) -> bool:
        if len(self.historico) < 5: return False
        # Ex: C C F C C ou F F C F F.
        # Verifica se os dois primeiros são iguais, o terceiro é diferente,
        # e o quarto e quinto são iguais ao primeiro e segundo.
        return (self.historico[0] == self.historico[1] and           # Dois do mesmo (primeira dupla)
                self.historico[2] != self.historico[0] and          # Um diferente
                self.historico[3] == self.historico[4] and           # Dois do mesmo (segunda dupla)
                self.historico[0] == self.historico[3])              # As duplas são do mesmo tipo

    def _padrao_2x2(self) -> bool:
        if len(self.historico) < 4: return False
        # Ex: C C F F ou F F C C.
        # Verifica se os dois primeiros são iguais e os dois próximos são iguais, mas diferentes entre si.
        return (self.historico[0] == self.historico[1] and           # Dois do mesmo
                self.historico[2] == self.historico[3] and           # Dois do outro
                self.historico[0] != self.historico[2])              # Os pares são de tipos diferentes

    def _padrao_3x3(self) -> bool:
        if len(self.historico) < 6: return False
        # Ex: C C C F F F ou F F F C C C.
        # Verifica se os três primeiros são iguais e os três próximos são iguais, mas diferentes entre si.
        return (self.historico[0] == self.historico[1] == self.historico[2] and # Três do mesmo
                self.historico[3] == self.historico[4] == self.historico[5] and # Três do outro
                self.historico[0] != self.historico[3])             # Os trios são de tipos diferentes

    def _padrao_4x4(self) -> bool:
        if len(self.historico) < 8: return False
        # Ex: C C C C F F F F ou F F F F C C C C.
        # Verifica se os quatro primeiros são iguais e os quatro próximos são iguais, mas diferentes entre si.
        return (self.historico[0] == self.historico[1] == self.historico[2] == self.historico[3] and # Quatro do mesmo
                self.historico[4] == self.historico[5] == self.historico[6] == self.historico[7] and # Quatro do outro
                self.historico[0] != self.historico[4])             # Os quartetos são de tipos diferentes


    def calcular_frequencias(self):
        """Calcula frequências dos resultados"""
        contador = collections.Counter(self.historico)
        total = len(self.historico)
        if total == 0: return {'C': 0, 'F': 0, 'E': 0}
        
        result = {k: round(v / total * 100, 1) for k, v in contador.items()}
        for tipo in ['C', 'F', 'E']:
            if tipo not in result:
                result[tipo] = 0
        return result

    def calcular_tendencia(self):
        """Calcula tendência dos últimos resultados"""
        if len(self.historico) < 5: return "Dados insuficientes"
        
        ultimos_5 = self.historico[:5]
        contador = collections.Counter(ultimos_5)
        
        # Considera a tendência se um resultado aparece 3 ou mais vezes nos últimos 5.
        # Ajustado para ser mais sensível
        if contador.most_common(1)[0][1] >= 4: 
            return f"Forte tendência: {contador.most_common(1)[0][0]}"
        elif contador.most_common(1)[0][1] == 3: 
            return f"Tendência moderada: {contador.most_common(1)[0][0]}"
        else: 
            return "Sem tendência clara"

    def gerar_sugestao(self) -> dict: # CORRIGIDO: Nome do método de 'generar_sugestao' para 'gerar_sugestao'
        """
        Gera uma sugestão de próximo resultado com base nos padrões ativos e seus pesos,
        além de considerar a tendência mais recente.
        """
        if not self.historico:
            return {
                "sugerir": False, "entrada": None, "entrada_codigo": None,
                "motivos": ["Nenhum histórico para análise."], "confianca": 0.0,
                "frequencias": self.calcular_frequencias(), "tendencia": "Sem dados",
                "ultimos_resultados": [], "analise_detalhada": {}, "pontuacoes_brutas": {'C':0, 'F':0, 'E':0}
            }

        padroes_ativos = self.analisar_todos()
        
        pontuacoes = {'C': 0.0, 'F': 0.0, 'E': 0.0}
        
        last_result = self._get_last_result()
        second_last_result = self._get_second_last_result()
        
        motives_sugestao = []
        total_peso_padroes = 0.0
        
        for nome_padrao, ativo in padroes_ativos.items():
            if ativo:
                peso = self.pesos_padroes.get(nome_padrao, 0.5)
                motives_sugestao.append(nome_padrao)
                total_peso_padroes += peso

                # Lógica de pontuação para cada padrão ativo
                if nome_padrao == "Sequência (Surf de Cor)":
                    if last_result: pontuacoes[last_result] += peso * 2.0 # Maior peso para continuar o surf

                elif nome_padrao == "Zig-Zag Perfeito":
                    if last_result == 'C': pontuacoes['F'] += peso
                    elif last_result == 'F': pontuacoes['C'] += peso
                    
                elif nome_padrao == "Quebra de Surf":
                    # Este padrão indica que a sequência anterior de 3 foi quebrada pelo 4º resultado.
                    # A sugestão seria apostar NO resultado que QUEBROU a sequência.
                    if len(self.historico) >= 4 and self.historico[0] == self.historico[1] == self.historico[2] and self.historico[2] != self.historico[3]:
                        pontuacoes[self.historico[3]] += peso * 0.8 # Menor peso, pois é uma quebra

                elif nome_padrao == "Quebra de Zig-Zag":
                    # Este padrão indica que o zig-zag foi quebrado.
                    # A sugestão é seguir o resultado que quebrou a alternância.
                    if len(self.historico) >= 5 and self.historico[3] == self.historico[4]:
                        pontuacoes[self.historico[3]] += peso * 0.8 # Menor peso para quebra

                elif nome_padrao == "Duplas Repetidas": # C C F F
                    if len(self.historico) >= 4 and self.historico[0] == self.historico[1] and self.historico[2] == self.historico[3] and self.historico[0] != self.historico[2]:
                        pontuacoes[self.historico[0]] += peso # Sugere a continuação da primeira dupla

                elif nome_padrao == "Empate Recorrente":
                    pontuacoes['E'] += peso * 1.5

                elif nome_padrao == "Padrão Escada":
                    # Ex: A B B C C C. Sugere quebrar o C C C e voltar para B (ou E se aplicável)
                    if len(self.historico) >= 6 and self.historico[1] == self.historico[2] and self.historico[3] == self.historico[4] == self.historico[5]:
                        if self.historico[0] == 'C': pontuacoes['F'] += peso # Se A foi C, sugerir F
                        elif self.historico[0] == 'F': pontuacoes['C'] += peso # Se A foi F, sugerir C
                        else: pontuacoes['E'] += peso # Se A foi E, sugerir E (menos provável)
                        
                elif nome_padrao == "Espelho":
                    # Se há um espelho (e.g., C F E F C), o próximo seria a 'continuação' do espelho.
                    # Para simplificar, pode-se sugerir o oposto do último para manter a simetria ou o próximo do "espelho"
                    if last_result == 'C': pontuacoes['F'] += peso * 0.7
                    elif last_result == 'F': pontuacoes['C'] += peso * 0.7
                    elif last_result == 'E': pontuacoes['E'] += peso * 0.5 # Empates podem quebrar espelhos facilmente

                elif nome_padrao == "Alternância com Empate":
                    # Ex: C E F. O próximo seria C.
                    if len(self.historico) >= 3 and self.historico[1] == 'E' and self.historico[0] != self.historico[2]:
                        pontuacoes[self.historico[0]] += peso * 1.0 # Sugere o que alternou com E

                elif nome_padrao == "Padrão Onda": # C F C F C F
                    if len(self.historico) >= 6 and self.historico[0] == self.historico[2] == self.historico[4] and self.historico[1] == self.historico[3] == self.historico[5]:
                        pontuacoes[self.historico[1]] += peso # Sugere o oposto do último resultado

                elif nome_padrao == "Padrão Fibonacci": # 1, 1, 2, 3 (alternando)
                    # Se terminou em uma sequência de 3 (ex: F F F), o próximo seria C (inversão)
                    if last_result == 'C': pontuacoes['F'] += peso * 1.1
                    elif last_result == 'F': pontuacoes['C'] += peso * 1.1
                    elif last_result == 'E': pontuacoes['E'] += peso * 0.8

                elif nome_padrao == "Sequência Dourada": # 3 de um, 5 do outro
                    if len(self.historico) >= 8 and self.historico[3] == self.historico[4]:
                        pontuacoes[self.historico[3]] += peso * 1.2 # Sugere continuar a sequência de 5

                elif nome_padrao == "Padrão Triangular": # A B C D C B A E A
                    if len(self.historico) >= 9 and self.historico[0] == self.historico[8]:
                        if self.historico[4] == 'C': pontuacoes['F'] += peso # Sugere o oposto do meio
                        elif self.historico[4] == 'F': pontuacoes['C'] += peso
                        elif self.historico[4] == 'E': pontuacoes['E'] += peso * 0.8

                elif nome_padrao == "Ciclo de Empates":
                    pontuacoes['E'] += peso * 1.8 # Forte sugestão de Empate

                elif nome_padrao == "Padrão Martingale": # A B B C C C C
                    if len(self.historico) >= 7 and self.historico[3] == self.historico[4]:
                        pontuacoes[self.historico[3]] += peso * 1.5 # Sugere continuar a sequência forte

                elif nome_padrao == "Sequência de Fibonacci Invertida": # 2x, 1x, 2x, 1x
                    if last_result == 'C': pontuacoes['F'] += peso * 1.1
                    elif last_result == 'F': pontuacoes['C'] += peso * 1.1
                    elif last_result == 'E': pontuacoes['E'] += peso * 0.8

                elif nome_padrao == "Padrão Dragon Tiger": # C F C E F F
                    if len(self.historico) >= 6 and self.historico[4] == self.historico[5]:
                        pontuacoes[self.historico[4]] += peso * 1.3 # Sugere continuar a última dupla

                elif nome_padrao == "Sequência de Paroli": # C F F C C C C C
                    if len(self.historico) >= 8 and self.historico[0] == self.historico[7]:
                        pontuacoes[self.historico[0]] += peso * 1.2 # Sugere o resultado que "fechou" a sequência

                elif nome_padrao == "Padrão de Ondas Longas":
                    if last_result: pontuacoes[last_result] += peso * 2.0 # Muito forte para continuar a onda

                elif nome_padrao == "Ciclo de Dominância":
                    dominant_result = collections.Counter(self.historico[:10]).most_common(1)[0][0]
                    pontuacoes[dominant_result] += peso * 1.1 # Sugere o dominante

                elif nome_padrao == "Padrão de Tensão": # C F C F C C C
                    if len(self.historico) >= 7 and self.historico[4] == self.historico[5] == self.historico[6]:
                        pontuacoes[self.historico[4]] += peso * 1.2 # Sugere continuar a sequência final

                elif nome_padrao == "Sequência de Labouchere": # C F X X F C
                    if len(self.historico) >= 6 and self.historico[0] == self.historico[5]:
                        if last_result == 'C': pontuacoes['F'] += peso * 0.8 # Sugere alternância se o padrão for de espelho
                        elif last_result == 'F': pontuacoes['C'] += peso * 0.8
                        elif last_result == 'E': pontuacoes['E'] += peso * 0.5

                elif nome_padrao == "Padrão Ritmo Cardíaco": # C C F C C F F F
                    if len(self.historico) < 8: return False # Já verificado na função do padrão
                    else:
                        if self.historico[5] == self.historico[6] == self.historico[7]:
                            if self.historico[5] == 'C': pontuacoes['F'] += peso * 0.7 # Sugere o oposto da última sequência
                            elif self.historico[5] == 'F': pontuacoes['C'] += peso * 0.7
                            elif self.historico[5] == 'E': pontuacoes['E'] += peso * 0.7

                elif nome_padrao == "Ciclo de Pressão": # A B B C C C A B B
                    if len(self.historico) >= 9 and self.historico[6] == self.historico[0]:
                        pontuacoes[self.historico[0]] += peso * 1.1 # Sugere a continuação do ciclo

                elif nome_padrao == "Padrão de Clusters":
                    if len(self.historico) >= 12:
                        last_cluster_dominant = collections.Counter(self.historico[8:12]).most_common(1)[0][0]
                        pontuacoes[last_cluster_dominant] += peso * 1.0 # Sugere continuar o último cluster

                elif nome_padrao == "Sequência Polar":
                    if len(self.historico) >= 10:
                        if last_result == 'C': pontuacoes['F'] += peso * 1.0 # Sugere o oposto para manter a polaridade
                        elif last_result == 'F': pontuacoes['C'] += peso * 1.0

                elif nome_padrao == "Padrão de Momentum": # A B B C C C D D D D
                    if len(self.historico) >= 10 and self.historico[6] == self.historico[7]:
                        pontuacoes[self.historico[6]] += peso * 1.4 # Sugere continuar a última sequência forte

                elif nome_padrao == "Ciclo de Respiração": # A A A A B C C C
                    if len(self.historico) < 8: pass # Já verificado na função do padrão
                    else:
                        pontuacoes[self.historico[5]] += peso * 1.1 # Sugere continuar a última sequência

                elif nome_padrao == "Padrão de Resistência": # A B A C A A
                    if len(self.historico) < 6: pass # Já verificado na função do padrão
                    else:
                        pontuacoes[self.historico[0]] += peso * 1.2 # Sugere continuar o resultado "resistente"

                elif nome_padrao == "Sequência de Breakout": # A A A A B B B B
                    if len(self.historico) < 8: pass # Já verificado na função do padrão
                    else:
                        pontuacoes[self.historico[5]] += peso * 1.5 # Sugere continuar a sequência que se "consolidou"

                # Lógica de pontuação para os NOVOS PADRÕES SOLICITADOS
                elif nome_padrao == "Padrão 2x1x2": # C C F C C -> Sugere C (o tipo que se repete)
                    if len(self.historico) >= 4 and self.historico[0] == self.historico[1] and self.historico[0] == self.historico[3]:
                        pontuacoes[self.historico[0]] += peso * 1.5 # Forte sugestão de continuar o resultado dominante

                elif nome_padrao == "Padrão 2x2": # C C F F -> Sugere C (o tipo da primeira dupla para reiniciar o ciclo)
                    if len(self.historico) >= 4 and self.historico[0] == self.historico[1] and self.historico[2] == self.historico[3]:
                        pontuacoes[self.historico[0]] += peso * 1.0
                        
                elif nome_padrao == "Padrão 3x3": # C C C F F F -> Sugere C (o tipo da primeira tripla para reiniciar o ciclo)
                    if len(self.historico) >= 6 and self.historico[0] == self.historico[1] == self.historico[2] and self.historico[3] == self.historico[4] == self.historico[5]:
                        pontuacoes[self.historico[0]] += peso * 1.2

                elif nome_padrao == "Padrão 4x4": # C C C C F F F F -> Sugere C (o tipo da primeira sequência de 4 para reiniciar o ciclo)
                    if len(self.historico) >= 8 and self.historico[0] == self.historico[1] == self.historico[2] == self.historico[3] and \
                       self.historico[4] == self.historico[5] == self.historico[6] == self.historico[7]:
                        pontuacoes[self.historico[0]] += peso * 1.4
        
        # 2. Adicionar uma pontuação baseada na tendência mais recente (últimos 3-5 jogos)
        recentes_window = self.historico[:min(len(self.historico), 5)]
        if recentes_window:
            contagem_recentes = collections.Counter(recentes_window)
            for resultado, count in contagem_recentes.items():
                if resultado in pontuacoes:
                    pontuacoes[resultado] += count * 0.2

        # 3. Determinar a sugestão final
        melhor_sugestao_codigo = "N/A"
        maior_pontuacao = -1.0

        if any(pontuacoes.values()):
            resultados_ordenados = sorted(pontuacoes.items(), key=lambda item: item[1], reverse=True)
            melhor_sugestao_codigo = resultados_ordenados[0][0]
            maior_pontuacao = resultados_ordenados[0][1]

            # Lógica para favorecer Empate se a pontuação for próxima (ajuste delicado)
            # if 'E' in pontuacoes and pontuacoes['E'] > 0 and \
            #    (maior_pontuacao > 0 and (pontuacoes['E'] >= maior_pontuacao * 0.9 and pontuacoes['E'] < maior_pontuacao)):
            #     melhor_sugestao_codigo = 'E'
        else:
            # Se nenhuma pontuação for gerada pelos padrões, use a frequência mais baixa como sugestão
            frequencias = self.calcular_frequencias()
            if frequencias:
                # Sugere o resultado com menor frequência (equilíbrio)
                melhor_sugestao_codigo = min(frequencias, key=frequencias.get)
            else:
                melhor_sugestao_codigo = random.choice(['C', 'F', 'E'])
                
        total_pontuacao_geral = sum(pontuacoes.values())
        confianca_percentual = (maior_pontuacao / total_pontuacao_geral) * 100 if total_pontuacao_geral > 0 else 0

        mapeamento_legivel = {"C": "Casa", "F": "Visitante", "E": "Empate"}
        
        return {
            "sugerir": True,
            "entrada": mapeamento_legivel.get(melhor_sugestao_codigo, "N/A"),
            "entrada_codigo": melhor_sugestao_codigo,
            "motivos": motives_sugestao,
            "confianca": min(99, int(confianca_percentual)),
            "frequencias": self.calcular_frequencias(),
            "tendencia": self.calcular_tendencia(),
            "ultimos_resultados": self.historico[:5],
            "analise_detalhada": self._gerar_analise_detalhada(motives_sugestao),
            "pontuacoes_brutas": pontuacoes # Adicionado para depuração
        }

    def _gerar_analise_detalhada(self, padroes):
        """Gera análise detalhada dos padrões encontrados"""
        # Adicionando uma nova categoria para "Padrões de Bloco/Duplas"
        categorias = {
            "Padrões de Sequência": ["Sequência", "Surf", "Ondas", "Fibonacci", "Momentum", "Paroli", "Ciclo de Respiração", "Sequência Dourada"],
            "Padrões de Quebra": ["Quebra", "Breakout", "Tensão"],
            "Padrões Cíclicos": ["Ciclo", "Respiração", "Ritmo", "Pressão", "Empate Recorrente"],
            "Padrões de Simetria/Alternância": ["Espelho", "Alternância", "Zig-Zag", "Escada", "Duplas", "Polar", "Labouchere", "Triangular", "Fibonacci Invertida", "Dragon Tiger"],
            "Padrões de Dominância": ["Clusters", "Resistência", "Dominância", "Martingale"],
            "Padrões de Bloco/Duplas": ["2x1x2", "2x2", "3x3", "4x4"] # Nova categoria
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
    # Histórico de exemplo, pode ser vazio ou com alguns dados para começar
    # st.session_state.historico = [] # Se quiser começar completamente vazio
    st.session_state.historico = ['C', 'F', 'C', 'E', 'F', 'F', 'C', 'C', 'E', 'F'] 
    
if 'estatisticas' not in st.session_state:
    st.session_state.estatisticas = {
        'total_jogos': 0,
        'acertos': 0,
        'erros': 0,
        'ultima_sugestao': None # Guarda a última sugestão para validação
    }

# Para capturar e exibir logs/erros na UI (opcional)
if 'log_messages' not in st.session_state:
    st.session_state.log_messages = []

def log_message(type, message):
    st.session_state.log_messages.append(f"[{datetime.now().strftime('%H:%M:%S')}] [{type.upper()}] {message}")
    if len(st.session_state.log_messages) > 50: # Limita o tamanho do log
        st.session_state.log_messages.pop(0)

def adicionar_resultado(resultado):
    """Adiciona novo resultado ao histórico e valida a sugestão anterior."""
    # Valida a sugestão anterior ANTES de adicionar o novo resultado ao histórico principal.
    # Isso garante que a validação usa o estado do histórico anterior ao novo jogo.
    if st.session_state.get('ultima_sugestao') and st.session_state.get('sugestao_processada'):
        # A sugestão só é validada se foi gerada na rodada anterior
        validar_sugestao(st.session_state.ultima_sugestao, resultado)
        # Limpa a flag e a sugestão após a validação
        st.session_state.sugestao_processada = False
        st.session_state.ultima_sugestao = None
    
    st.session_state.historico.insert(0, resultado) # Adiciona no início
    if len(st.session_state.historico) > 50:
        st.session_state.historico = st.session_state.historico[:50]
    st.session_state.estatisticas['total_jogos'] = len(st.session_state.historico) # Atualiza total de jogos
    log_message("info", f"Resultado '{resultado}' adicionado. Histórico atualizado.")


def limpar_historico():
    """Limpa todo o histórico e estatísticas."""
    st.session_state.historico = []
    st.session_state.estatisticas = {
        'total_jogos': 0,
        'acertos': 0,
        'erros': 0,
        'ultima_sugestao': None
    }
    st.session_state.log_messages = []
    st.session_state.sugestao_processada = False # Reseta a flag
    log_message("info", "Histórico e estatísticas limpos.")


def desfazer_ultimo():
    """Remove o último resultado e ajusta as estatísticas."""
    if st.session_state.historico:
        removed_result = st.session_state.historico.pop(0)
        # Ao desfazer, também zera a sugestão para evitar validação de um jogo que não existe mais.
        st.session_state.ultima_sugestao = None
        st.session_state.sugestao_processada = False
        st.session_state.estatisticas['total_jogos'] = len(st.session_state.historico)
        log_message("info", f"Último resultado '{removed_result}' desfeito. Histórico ajustado.")
    else:
        log_message("warn", "Tentativa de desfazer com histórico vazio.")


def validar_sugestao(sugestao_obj, resultado_real):
    """Valida se a sugestão anterior estava correta"""
    if sugestao_obj and sugestao_obj['entrada_codigo'] == resultado_real:
        st.session_state.estatisticas['acertos'] += 1
        log_message("success", f"Sugestão anterior ACERTADA! Sugerido: {sugestao_obj['entrada_codigo']}, Real: {resultado_real}")
        return True
    else:
        st.session_state.estatisticas['erros'] += 1
        log_message("error", f"Sugestão anterior ERRADA! Sugerido: {sugestao_obj['entrada_codigo'] if sugestao_obj else 'N/A'}, Real: {resultado_real}")
        return False

def get_resultado_html(resultado):
    """Retorna HTML para visualização do resultado"""
    color_map = {'C': '#FF4B4B', 'F': '#4B4BFF', 'E': '#FFD700'}
    symbol_map = {'C': '🏠', 'F': '✈️', 'E': '⚖️'}
    
    return f"""
    <div style='
        display: inline-flex; /* Use inline-flex for the circle itself */
        width: 32px; /* Slightly larger for better touch on mobile */
        height: 32px; 
        border-radius: 50%; 
        background-color: {color_map.get(resultado, 'gray')}; 
        margin: 2px; /* Keep margin for spacing between circles */
        align-items: center; /* Center content vertically */
        justify-content: center; /* Center content horizontally */
        font-size: 14px;
        color: {"black" if resultado == "E" else "white"};
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        flex-shrink: 0; /* Prevent shrinking */
    '>
        {symbol_map.get(resultado, '?')}
    </div>
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

div.stButton > button[data-testid="stButton-✈️ Visitante (F)"] {
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

/* Histórico de resultados - NOVO ESTILO PARA LINHAS */
.historic-row {
    display: flex;
    flex-wrap: nowrap; /* Prevent wrapping within a row */
    justify-content: flex-start;
    align-items: center;
    margin-bottom: 5px; /* Spacing between rows */
}

.historic-container {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    margin: 1rem 0;
    border: 1px solid #dee2e6;
}

/* Ensure circles are inline-block for proper flow within flex */
.historic-container div { /* Targeting the result circles */
    display: inline-flex; /* Use inline-flex for the circle itself */
    width: 32px; 
    height: 32px; 
    border-radius: 50%; 
    margin: 2px; /* Spacing between circles */
    align-items: center; 
    justify-content: center; 
    font-size: 14px;
    color: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    flex-shrink: 0; 
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
    
    # auto_suggest = st.checkbox("Sugestão Automática", value=True) # Removido, pois a sugestão é sempre exibida se a confiança for suficiente
    show_advanced = st.checkbox("Análise Avançada", value=True)
    confidence_threshold = st.slider("Limite de Confiança", 0, 100, 60)

    st.markdown("---")
    st.markdown("## 📝 Logs de Depuração")
    log_area = st.empty()
    if st.session_state.log_messages:
        # Exibe os logs mais recentes primeiro
        for log in reversed(st.session_state.log_messages):
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
    if st.button("✈️ Visitante (F)", key="VisitanteF", use_container_width=True, help="Vitória do Visitante"):
        adicionar_resultado('F')
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

# --- ANÁLISE PRINCIPAL (MOVIDA PARA CIMA DO HISTÓRICO) ---
st.markdown('<div class="section-header"><h2>✨ Próxima Sugestão</h2></div>', unsafe_allow_html=True)

if len(st.session_state.historico) >= 5: # Mínimo de 5 para algumas análises
    try:
        analyzer = AnalisePadroes(st.session_state.historico)
        log_message("info", "Objeto AnalisePadroes criado com histórico atual.")
        
        # Gera a sugestão
        sugestao = analyzer.gerar_sugestao() # CORRIGIDO: Chamando o método com o nome correto
        log_message("info", f"Sugestão gerada: {sugestao['entrada_codigo']} (Confiança: {sugestao['confianca']}%)")
        
        # Armazena a sugestão e define uma flag para que ela seja processada na próxima adição de resultado
        st.session_state.ultima_sugestao = sugestao
        st.session_state.sugestao_processada = True # Flag para indicar que uma sugestão foi gerada e aguarda validação

        if sugestao['sugerir'] and sugestao['confianca'] >= confidence_threshold:
            confianca_color = get_confianca_color(sugestao['confianca'])
            
            st.markdown(f"""
            <div class="suggestion-box">
                <h3>🎯 Sugestão para o Próximo Jogo:</h3>
                <h2 style="color: {confianca_color}; margin: 1rem 0;">
                    {sugestao['entrada']} ({sugestao['entrada_codigo']})
                </h2>
                <p><strong>Confiança:</strong> 
                    <span style="color: {confianca_color}; font-weight: bold;">
                        {sugestao['confianca']}%
                    </span>
                </p>
                <p><strong>Tendência Recente:</strong> {sugestao['tendencia']}</p>
                <p><strong>Frequências (C/F/E):</strong> {sugestao['frequencias'].get('C',0)}% / {sugestao['frequencias'].get('F',0)}% / {sugestao['frequencias'].get('E',0)}%</p>
            </div>
            """, unsafe_allow_html=True)
            
            if show_advanced:
                with st.expander("📋 Detalhes da Análise"):
                    st.write("**Padrões Identificados que Contribuíram:**")
                    if sugestao['motivos']:
                        for motivo in sugestao['motivos']:
                            st.write(f"• {motivo}")
                    else:
                        st.info("Nenhum padrão específico contribuiu para a sugestão com peso suficiente.")
                    
                    if 'analise_detalhada' in sugestao and sugestao['analise_detalhada']:
                        st.write("**Análise por Categoria de Padrões:**")
                        for categoria, padroes_list in sugestao['analise_detalhada'].items():
                            st.write(f"**{categoria}:** {', '.join(padrores_list)}")
                    else:
                        st.info("Nenhuma análise detalhada de categorias de padrões disponível.")
                    
                    st.write("**Pontuações Brutas por Resultado:**")
                    st.json(sugestao['pontuacoes_brutas']) # Para depuração

        else:
            st.warning(f"🤔 Confiança insuficiente ({sugestao['confianca']}%) para uma sugestão forte. Limite: {confidence_threshold}%.")
            st.info("Continue inserindo resultados para aumentar a precisão da análise.")
            log_message("warn", f"Sugestão não exibida: Confiança {sugestao['confianca']}% abaixo do limite {confidence_threshold}%.")

    except Exception as e:
        st.error(f"Ocorreu um erro inesperado durante a análise da sugestão. Por favor, verifique os logs na barra lateral.")
        st.exception(e) # Exibe o traceback completo para depuração em desenvolvimento
        log_message("critical", f"Erro crítico na análise: {e}")

else:
    st.info("🎮 Insira pelo menos 5 resultados para começar a análise inteligente e gerar sugestões!")


# --- EXIBIÇÃO DO HISTÓRICO (AGORA ABAIXO DA SUGESTÃO) ---
st.markdown('<div class="section-header"><h2>📈 Histórico de Resultados</h2></div>', unsafe_allow_html=True)

if not st.session_state.historico:
    st.info("🎮 Nenhum resultado registrado. Comece inserindo os resultados dos jogos!")
else:
    st.markdown('<div class="historic-container">', unsafe_allow_html=True)
    
    # Renderiza o histórico em linhas de 9
    results_per_row = 9
    for i in range(0, len(st.session_state.historico), results_per_row):
        row_results = st.session_state.historico[i:i + results_per_row]
        row_html = '<div class="historic-row">'
        for resultado in row_results:
            row_html += get_resultado_html(resultado)
        row_html += '</div>'
        st.markdown(row_html, unsafe_allow_html=True)
            
    st.markdown(f"**Total:** {len(st.session_state.historico)} jogos (máx. 50)", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ANÁLISE DE PADRÕES (DETALHADA) - SÓ SE show_advanced ESTIVER ATIVO ---
if show_advanced and len(st.session_state.historico) >= 5:
    try:
        analyzer = AnalisePadroes(st.session_state.historico) # Recria o analyzer para esta seção, se necessário
        st.markdown('<div class="section-header"><h2>🔍 Padrões Detectados (Todos)</h2></div>', unsafe_allow_html=True)
        
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
                st.info("Nenhum padrão detectado no histórico atual.")
        
        with col_right:
            st.markdown("### ❌ Padrões Inativos")
            nao_encontrados = [nome for nome, status in padroes_encontrados.items() if not status]
            
            if nao_encontrados:
                for padrao in nao_encontrados[:15]:
                    st.markdown(f'<div class="pattern-not-found">❌ {padrao}</div>', unsafe_allow_html=True)
                if len(nao_encontrados) > 15:
                    st.markdown(f'<div class="pattern-not-found">... e mais {len(nao_encontrados) - 15}</div>', unsafe_allow_html=True)
            else:
                st.info("Todos os padrões foram encontrados (muito raro).")
        
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado durante a análise detalhada dos padrões. Por favor, verifique os logs na barra lateral.")
        st.exception(e)
        log_message("critical", f"Erro crítico na análise detalhada de padrões: {e}")

# --- ANÁLISE ESTATÍSTICA GERAL ---
st.markdown('<div class="section-header"><h2>📊 Análise Estatística Geral</h2></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

# Garante que o analyzer é criado para esta seção, caso a sugestão não tenha sido gerada
if 'analyzer' not in locals() or analyzer is None:
    analyzer = AnalisePadroes(st.session_state.historico)

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
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>⚖️ Empate</h3>
        <p style="color: #FFD700;">{frequencias.get('E', 0.0)}%</p>
    </div>
    """, unsafe_allow_html=True)

# Gráfico de frequências
if show_advanced:
    st.markdown("### 📈 Distribuição dos Resultados no Histórico Completo")
    chart_data = pd.DataFrame({
        'Resultado': ['Casa', 'Visitante', 'Empate'],
        'Frequência': [frequencias.get('C', 0.0), frequencias.get('F', 0.0), frequencias.get('E', 0.0)],
        'Cor': ['#FF4B4B', '#4B4BFF', '#FFD700']
    })
    
    st.bar_chart(chart_data.set_index('Resultado')['Frequência'])

# --- RODAPÉ ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; margin-top: 2rem;">
    <p>⚽ Football Studio Live Analyzer v2.5 | Análise Inteligente de Padrões</p>
    <p><small>Desenvolvido para Evolution Gaming Football Studio</small></p>
</div>
""", unsafe_allow_html=True)
