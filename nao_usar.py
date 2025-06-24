import collections
import random
import numpy as np

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

        self.padroes_ativos_map = { # Renomeado para evitar conflito com método `analisar_todos`
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
                print(f"Erro ao analisar o padrão '{nome}': {e}") # Para depuração
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
        fib_lengths = [1, 1, 2, 3, 5]
        current_idx = 0
        results_to_check = self.historico[:]
        try:
            for length in fib_lengths:
                if current_idx + length > len(results_to_check): return False
                block = results_to_check[current_idx : current_idx + length]
                if not block or not all(x == block[0] for x in block): return False
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

    # O método `sugestao_inteligente` será substituído/complementado por `gerar_sugestao`
    # Você pode manter `calcular_frequencias` e `calcular_tendencia` como auxiliares
    def calcular_frequencias(self):
        """Calcula frequências dos resultados"""
        contador = collections.Counter(self.historico)
        total = len(self.historico)
        if total == 0: return {'C': 0, 'V': 0, 'E': 0}
        
        result = {k: round(v / total * 100, 1) for k, v in contador.items()}
        for tipo in ['C', 'V', 'E']: # 'V' deve ser 'F' para Fora
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
        
        pontuacoes = {'C': 0.0, 'F': 0.0, 'E': 0.0} # Usando 'F' para Fora/Visitante, como no seu padrão
        
        last_result = self._get_last_result()
        second_last_result = self._get_second_last_result()
        
        # 1. Pontuação baseada nos padrões ativos
        motivos_sugestao = []
        for nome_padrao, ativo in padroes_ativos.items():
            if ativo:
                peso = self.pesos_padroes.get(nome_padrao, 0.5)
                motivos_sugestao.append(nome_padrao)

                # --- Lógica de Sugestão para CADA PADRÃO ---
                # Aumente os pesos aqui para os padrões que você confia mais.
                # Lembre-se: 'V' do seu Streamlit precisa ser 'F' aqui para 'Fora/Visitante'

                if nome_padrao == "Sequência (Surf de Cor)" and last_result == second_last_result:
                    pontuacoes[last_result] += peso * 1.5

                elif nome_padrao == "Zig-Zag Perfeito" and last_result != second_last_result:
                    if last_result == 'C': pontuacoes['F'] += peso
                    elif last_result == 'F': pontuacoes['C'] += peso
                    
                elif nome_padrao == "Quebra de Surf" and len(self.historico) >= 4 and \
                     self.historico[0] == self.historico[1] == self.historico[2] and self.historico[2] != self.historico[3]:
                    pontuacoes[self.historico[3]] += peso * 1.2
                    
                elif nome_padrao == "Quebra de Zig-Zag" and len(self.historico) >= 5 and \
                     self.historico[3] == self.historico[4]:
                    pontuacoes[self.historico[3]] += peso * 1.2

                elif nome_padrao == "Duplas Repetidas" and len(self.historico) >= 4 and \
                     self.historico[0] == self.historico[1] and self.historico[2] == self.historico[3]:
                    pontuacoes[self.historico[0]] += peso

                elif nome_padrao == "Empate Recorrente":
                    pontuacoes['E'] += peso * 1.5

                elif nome_padrao == "Padrão Escada" and len(self.historico) >= 6 and \
                     self.historico[1] == self.historico[2] and self.historico[3] == self.historico[4] == self.historico[5]:
                    pontuacoes[self.historico[0]] += peso

                elif nome_padrao == "Espelho":
                    if last_result == 'C': pontuacoes['F'] += peso * 0.5
                    elif last_result == 'F': pontuacoes['C'] += peso * 0.5
                    elif last_result == 'E': pontuacoes['E'] += peso * 0.5

                elif nome_padrao == "Alternância com Empate" and len(self.historico) >= 3 and \
                     self.historico[1] == 'E' and self.historico[0] != self.historico[2]:
                    if self.historico[0] == 'C': pontuacoes['F'] += peso
                    elif self.historico[0] == 'F': pontuacoes['C'] += peso

                elif nome_padrao == "Padrão Onda" and len(self.historico) >= 6 and \
                     self.historico[0] == self.historico[2] == self.historico[4] and \
                     self.historico[1] == self.historico[3] == self.historico[5]:
                    pontuacoes[self.historico[1]] += peso

                elif nome_padrao == "Padrão Fibonacci":
                    if last_result == 'C': pontuacoes['F'] += peso
                    elif last_result == 'F': pontuacoes['C'] += peso
                    elif last_result == 'E': pontuacoes['E'] += peso * 0.5

                elif nome_padrao == "Sequência Dourada" and len(self.historico) >= 8 and \
                     self.historico[3] == self.historico[4]:
                    pontuacoes[self.historico[3]] += peso * 1.2

                elif nome_padrao == "Padrão Triangular" and len(self.historico) >= 9 and \
                     self.historico[0] == self.historico[8]:
                    if self.historico[4] == 'C': pontuacoes['F'] += peso
                    elif self.historico[4] == 'F': pontuacoes['C'] += peso
                    elif self.historico[4] == 'E': pontuacoes['E'] += peso * 0.8

                elif nome_padrao == "Ciclo de Empates":
                    pontuacoes['E'] += peso * 1.8

                elif nome_padrao == "Padrão Martingale" and len(self.historico) >= 7 and \
                     self.historico[3] == self.historico[4]:
                    pontuacoes[self.historico[3]] += peso * 1.5

                elif nome_padrao == "Sequência de Fibonacci Invertida" and len(self.historico) >= 8:
                    if last_result == 'C': pontuacoes['F'] += peso
                    elif last_result == 'F': pontuacoes['C'] += peso
                    elif last_result == 'E': pontuacoes['E'] += peso * 0.5

                elif nome_padrao == "Padrão Dragon Tiger" and len(self.historico) >= 6 and \
                     self.historico[4] == self.historico[5]:
                    pontuacoes[self.historico[4]] += peso * 1.3

                elif nome_padrao == "Sequência de Paroli" and len(self.historico) >= 8 and \
                     self.historico[0] == self.historico[7]:
                    pontuacoes[self.historico[0]] += peso * 1.2

                elif nome_padrao == "Padrão de Ondas Longas":
                    pontuacoes[last_result] += peso * 1.6

                elif nome_padrao == "Ciclo de Dominância":
                    dominant_result = collections.Counter(self.historico[:10]).most_common(1)[0][0]
                    pontuacoes[dominant_result] += peso * 1.1

                elif nome_padrao == "Padrão de Tensão" and len(self.historico) >= 7 and \
                     self.historico[4] == self.historico[5] == self.historico[6]:
                    pontuacoes[self.historico[4]] += peso * 1.2

                elif nome_padrao == "Sequência de Labouchere" and len(self.historico) >= 6 and \
                     self.historico[0] == self.historico[5]:
                    pontuacoes[self.historico[0]] += peso

                elif nome_padrao == "Padrão Ritmo Cardíaco" and len(self.historico) >= 8:
                    if self.historico[5] == self.historico[6] == self.historico[7]:
                        if self.historico[5] == 'C': pontuacoes['F'] += peso * 0.7
                        elif self.historico[5] == 'F': pontuacoes['C'] += peso * 0.7
                        elif self.historico[5] == 'E': pontuacoes['E'] += peso * 0.7

                elif nome_padrao == "Ciclo de Pressao" and len(self.historico) >= 9 and \
                     self.historico[6] == self.historico[0]:
                    pontuacoes[self.historico[0]] += peso * 1.1

                elif nome_padrao == "Padrão de Clusters" and len(self.historico) >= 12:
                    last_cluster_dominant = collections.Counter(self.historico[8:12]).most_common(1)[0][0]
                    pontuacoes[last_cluster_dominant] += peso * 1.0

                elif nome_padrao == "Sequencia Polar" and len(self.historico) >= 10:
                    if last_result == 'C': pontuacoes['F'] += peso * 1.0
                    elif last_result == 'F': pontuacoes['C'] += peso * 1.0

                elif nome_padrao == "Padrão de Momentum" and len(self.historico) >= 10 and \
                     self.historico[6] == self.historico[7]:
                    pontuacoes[self.historico[6]] += peso * 1.4

                elif nome_padrao == "Ciclo de Respiracao" and len(self.historico) >= 8 and \
                     self.historico[5] == self.historico[6] == self.historico[7]:
                    pontuacoes[self.historico[5]] += peso * 1.1

                elif nome_padrao == "Padrão de Resistencia" and len(self.historico) >= 6 and \
                     self.historico[0] == self.historico[2]:
                    pontuacoes[self.historico[0]] += peso * 1.2

                elif nome_padrao == "Sequencia de Breakout" and len(self.historico) >= 8 and \
                     self.historico[5] == self.historico[6] == self.historico[7]:
                    pontuacoes[self.historico[5]] += peso * 1.5
        
        # 2. Adicionar uma pontuação baseada na tendência recente (últimos 5 jogos mais recentes)
        recentes = self.historico[:5] 
        contagem_recentes = collections.Counter(recentes)
        for resultado, count in contagem_recentes.items():
            if resultado in pontuacoes: # Garante que 'V' não cause erro se não mapeado
                pontuacoes[resultado] += count * 0.2

        # 3. Determinar a sugestão final
        melhor_sugestao_codigo = "N/A"
        maior_pontuacao = -1.0

        resultados_ordenados = sorted(pontuacoes.items(), key=lambda item: item[1], reverse=True)

        if resultados_ordenados:
            melhor_sugestao_codigo = resultados_ordenados[0][0]
            maior_pontuacao = resultados_ordenados[0][1]

            # Lógica para desempatar, favorecendo o empate se as pontuações forem muito próximas
            if 'E' in pontuacoes and pontuacoes['E'] > 0 and \
               (pontuacoes['E'] >= maior_pontuacao * 0.95 and pontuacoes['E'] < maior_pontuacao):
                melhor_sugestao_codigo = 'E'

        # Calcular uma confiança percentual simples
        total_pontuacao = sum(pontuacoes.values())
        confianca_percentual = (maior_pontuacao / total_pontuacao) * 100 if total_pontuacao > 0 else 0

        # Mapeamento para nomes legíveis
        mapeamento_legivel = {"C": "Casa", "F": "Visitante", "E": "Empate", "V": "Visitante"} # Adicione 'V' aqui
        
        return {
            "sugerir": True,
            "entrada": mapeamento_legivel.get(melhor_sugestao_codigo, "N/A"),
            "entrada_codigo": melhor_sugestao_codigo,
            "motivos": motivos_sugestao,
            "confianca": min(95, int(confianca_percentual)), # Limita a confiança a 95%
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

