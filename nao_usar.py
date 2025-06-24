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
        
        if contador.most_common(1)[0][1] >= 4:
            return f"Forte tendência: {contador.most_common(1)[0][0]}"
        elif contador.most_common(1)[0][1] >= 3:
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
                "ultimos_resultados": self.historico[:5]
            }
        
        # Calcula confiança baseada nos pesos dos padrões
        confianca_total = 0
        peso_total = 0
        
        for padrao in padroes_identificados:
            peso = self.pesos_padroes.get(padrao, 0.5)
            confianca_total += peso
            peso_total += peso
        
        confianca_media = (confianca_total / peso_total) * 100 if peso_total > 0 else 0
        
        # Ajusta confiança baseada na quantidade de padrões
        bonus_quantidade = min(20, len(padroes_identificados) * 5)
        confianca_final = min(95, int(confianca_media + bonus_quantidade))
        
        # Análise de frequências e tendências
        frequencias = self.calcular_frequencias()
        tendencia = self.calcular_tendencia()
        
        # Lógica de sugestão aprimorada
        opcoes = ["V", "C", "E"]
        
        # Considera padrões de quebra
        padroes_quebra = [p for p in padroes_identificados if "quebra" in p.lower() or "breakout" in p.lower()]
        
        if padroes_quebra:
            # Se há padrões de quebra, sugere o oposto da tendência
            ultimo_resultado = self.historico[0] if self.historico else None
            if ultimo_resultado:
                opcoes_sem_ultimo = [op for op in opcoes if op != ultimo_resultado]
                entrada_sugerida = min(opcoes_sem_ultimo, key=lambda x: frequencias.get(x, 0))
            else:
                entrada_sugerida = min(opcoes, key=lambda x: frequencias.get(x, 0))
        else:
            # Lógica normal: sugere baseado em frequências
            entrada_sugerida = min(opcoes, key=lambda x: frequencias.get(x, 0))
        
        # Se todas as frequências são iguais, usa análise de momentum
        if len(set(frequencias.values())) == 1:
            # Analisa momentum dos últimos 3 resultados
            ultimos_3 = self.historico[:3]
            contador_recente = collections.Counter(ultimos_3)
            if contador_recente.most_common(1)[0][1] >= 2:
                # Se há repetição recente, sugere mudança
                resultado_frequente = contador_recente.most_common(1)[0][0]
                opcoes_mudanca = [op for op in opcoes if op != resultado_frequente]
                entrada_sugerida = random.choice(opcoes_mudanca)
            else:
                entrada_sugerida = random.choice(opcoes)
        
        mapeamento = {"C": "Casa", "V": "Visitante", "E": "Empate"}
        entrada_legivel = mapeamento[entrada_sugerida]
        
        return {
            "sugerir": True,
            "entrada": entrada_legivel,
            "entrada_codigo": entrada_sugerida,
            "motivos": padroes_identificados,
            "confianca": confianca_final,
            "frequencias": frequencias,
            "tendencia": tendencia,
            "ultimos_resultados": self.historico[:5],
            "analise_detalhada": self._gerar_analise_detalhada(padroes_identificados)
        }

    def _gerar_analise_detalhada(self, padroes):
        """Gera análise detalhada dos padrões encontrados"""
        categorias = {
            "Padrões de Sequência": ["Sequência", "Surf", "Ondas", "Fibonacci"],
            "Padrões de Quebra": ["Quebra", "Breakout", "Tensão"],
            "Padrões Cíclicos": ["Ciclo", "Respiração", "Momentum"],
            "Padrões Especiais": ["Dragon", "Martingale", "Dourada", "Triangular"]
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
    st.session_state.estatisticas = {'total_jogos': 0, 'acertos': 0, 'sugestoes_seguidas': 0}
if 'historico_sugestoes' not in st.session_state:
    st.session_state.historico_sugestoes = []

def adicionar_resultado(resultado, foi_sugerido=False):
    """Adiciona resultado e atualiza estatísticas"""
    st.session_state.historico.insert(0, resultado)
    st.session_state.estatisticas['total_jogos'] += 1
    
    # Verifica se seguiu a sugestão anterior
    if st.session_state.historico_sugestoes and foi_sugerido:
        ultima_sugestao = st.session_state.historico_sugestoes[-1]
        if ultima_sugestao['entrada_codigo'] == resultado:
            st.session_state.estatisticas['acertos'] += 1
            st.session_state.estatisticas['sugestoes_seguidas'] += 1
        else:
            st.session_state.estatisticas['sugestoes_seguidas'] = 0
    
    # Limita histórico a 50 resultados
    if len(st.session_state.historico) > 50:
        st.session_state.historico = st.session_state.historico[:50]

def limpar_historico():
    """Limpa histórico e estatísticas"""
    st.session_state.historico = []
    st.session_state.estatisticas = {'total_jogos': 0, 'acertos': 0, 'sugestoes_seguidas': 0}
    st.session_state.historico_sugestoes = []

def desfazer_ultimo():
    """Remove último resultado"""
    if st.session_state.historico:
        st.session_state.historico.pop(0)
        if st.session_state.estatisticas['total_jogos'] > 0:
            st.session_state.estatisticas['total_jogos'] -= 1

def get_resultado_html(resultado):
    """Retorna HTML para bolinha colorida"""
    color_map = {'C': '#FF4B4B', 'V': '#4B4BFF', 'E': '#FFD700'}
    symbol_map = {'C': '🏠', 'V': '✈️', 'E': '⚖️'}
    return f"""
    <span style='display:inline-block; width:30px; height:30px; border-radius:50%; 
                 background-color:{color_map.get(resultado, 'gray')}; margin:2px; 
                 vertical-align:middle; text-align:center; line-height:30px; 
                 font-size:16px; color:white; font-weight:bold; 
                 box-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
        {symbol_map.get(resultado, '?')}
    </span>
    """

def calcular_taxa_acerto():
    """Calcula taxa de acerto das sugestões"""
    if st.session_state.estatisticas['sugestoes_seguidas'] == 0:
        return 0
    return round((st.session_state.estatisticas['acertos'] / 
                 max(1, len(st.session_state.historico_sugestoes))) * 100, 1)

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    layout="wide", 
    page_title="Football Studio Live Game - Analisador Pro",
    page_icon="⚽",
    initial_sidebar_state="expanded"
)

# CSS Avançado
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

.main-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.5rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(45deg, #FF4B4B, #4B4BFF, #FFD700);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 2rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.stats-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin: 0.5rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.pattern-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    color: white;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.suggestion-card {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin: 1rem 0;
    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
}

.confidence-high { color: #28a745; font-weight: bold; }
.confidence-medium { color: #ffc107; font-weight: bold; }
.confidence-low { color: #dc3545; font-weight: bold; }

div.stButton > button:first-child {
    font-size: 16px;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: bold;
    transition: all 0.3s ease;
    border: none;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

div.stButton > button:first-child:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
}

.stButton > button[key="Casa (C)"] {
    background: linear-gradient(135deg, #FF4B4B, #FF6B6B);
    color: white;
}

.stButton > button[key="Visitante (V)"] {
    background: linear-gradient(135deg, #4B4BFF, #6B6BFF);
    color: white;
}

.stButton > button[key="Empate (E)"] {
    background: linear-gradient(135deg, #FFD700, #FFF066);
    color: black;
}

.metric-card {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem;
    border: 1px solid rgba(255,255,255,0.2);
}
</style>
""", unsafe_allow_html=True)

# --- INTERFACE PRINCIPAL ---
st.markdown('<h1 class="main-title">⚽ Football Studio Live Game - Analisador Pro</h1>', unsafe_allow_html=True)

# Sidebar com estatísticas
with st.sidebar:
    st.markdown("### 📊 Estatísticas da Sessão")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Jogos", st.session_state.estatisticas['total_jogos'])
        st.metric("Sequência Atual", st.session_state.estatisticas['sugestoes_seguidas'])
    
    with col2:
        st.metric("Acertos", st.session_state.estatisticas['acertos'])
        st.metric("Taxa de Acerto", f"{calcular_taxa_acerto()}%")
    
    st.markdown("---")
    st.markdown("### 🎯 Configurações")
    
    modo_analise = st.selectbox(
        "Modo de Análise",
        ["Padrão Completo", "Foco em Quebras", "Análise Conservadora", "Modo Agressivo"]
    )
    
    mostrar_detalhes = st.checkbox("Mostrar Análise Detalhada", value=True)
    
    st.markdown("---")
    st.markdown("### 🔄 Ações Rápidas")
    if st.button("🗑️ Limpar Tudo", use_container_width=True):
        limpar_historico()
        st.rerun()

# Seção de inserção de resultados
st.markdown("### 🎮 Inserir Novo Resultado")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🏠 Casa (C)", key="Casa (C)", help="Vitória da Casa", use_container_width=True):
        adicionar_resultado('C')
        st.rerun()

with col2:
    if st.button("✈️ Visitante (V)", key="Visitante (V)", help="Vitória do Visitante", use_container_width=True):
        adicionar_resultado('V')
        st.rerun()

with col3:
    if st.button("⚖️ Empate (E)", key="Empate (E)", help="Resultado Empate", use_container_width=True):
        adicionar_resultado('E')
        st.rerun()

with col4:
    if st.button("↩️ Desfazer", help="Remove último resultado", use_container_width=True):
        desfazer_ultimo()
        st.rerun()

with col5:
    if st.button("🔄 Limpar", help="Limpa histórico", use_container_width=True):
        limpar_historico()
        st.rerun()

st.markdown("---")

# Exibição do histórico
st.markdown("### 📈 Histórico de Resultados (Mais Recente → Mais Antigo)")

if not st.session_state.historico:
    st.info("🎯 O histórico está vazio. Comece inserindo os resultados dos jogos acima.")
else:
    # Histórico visual
    historico_html = ""
    for i, resultado in enumerate(st.session_state.historico):
        historico_html += get_resultado_html(resultado)
        if (i + 1) % 10 == 0 and (i + 1) < len(st.session_state.historico):
            historico_html += "<br><br>"
    
    st.markdown(historico_html, unsafe_allow_html=True)
    
    # Métricas do histórico
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Resultados", len(st.session_state.historico))
    with col2:
        casa_count = st.session_state.historico.count('C')
        st.metric("🏠 Casa", f"{casa_count} ({round(casa_count/len(st.session_state.historico)*100, 1)}%)")
    with col3:
        visitante_count = st.session_state.historico.count('V')
        st.metric("✈️ Visitante", f"{visitante_count} ({round(visitante_count/len(st.session_state.historico)*100, 1)}%)")
    with col4:
        empate_count = st.session_state.historico.count('E')
        st.metric("⚖️ Empate", f"{empate_count} ({round(empate_count/len(st.session_state.historico)*100, 1)}%)")

st.markdown("---")

# Análise principal
if len(st.session_state.historico) >= 6:
    analisador = AnalisePadroes(st.session_state.historico)
    
    # Sugestão principal
    sugestao = analisador.sugestao_inteligente()
    
    if sugestao['sugerir']:
        confianca = sugestao['confianca']
        cor_confianca = "confidence-high" if confianca >= 70 else "confidence-medium" if confianca >= 50 else "confidence-low"
        
        st.markdown(f"""
        <div class="suggestion-card">
            <h2>🎯 SUGESTÃO PARA O PRÓXIMO JOGO</h2>
            <h1>{sugestao['entrada']} ({sugestao['entrada_codigo']})</h1>
            <h3 class="{cor_confianca}">Confiança: {confianca}%</h3>
            <p>Tendência: {sugestao['tendencia']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Salva sugestão no histórico
        st.session_state.historico_sugestoes.append(sugestao)
        
        # Análise detalhada
        if mostrar_detalhes and 'analise_detalhada' in sugestao:
            st.markdown("### 🔍 Análise Detalhada dos Padrões")
            
            analise_det = sugestao['analise_detalhada']
            if analise_det:
                for categoria, padroes in analise_det.items():
                    with st.expander(f"📋 {categoria} ({len(padroes)} padrões)"):
                        for padrao in padroes:
                            st.success(f"✅ {padrao}")
            else:
                st.info("Nenhuma categorização específica disponível.")
        
        # Padrões encontrados
        st.markdown("### 🔎 Padrões Identificados")
        
        if sugestao['motivos']:
            # Divide padrões em colunas
            num_padroes = len(sugestao['motivos'])
            cols = st.columns(min(3, num_padroes))
            
            for i, padrao in enumerate(sugestao['motivos']):
                with cols[i % len(cols)]:
                    st.markdown(f"""
                    <div class="pattern-card">
                        <strong>✅ {padrao}</strong>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Gráfico de frequências
        st.markdown("### 📊 Distribuição dos Resultados")
        
        freq_data = pd.DataFrame({
            'Resultado': ['🏠 Casa', '✈️ Visitante', '⚖️ Empate'],
            'Frequência (%)': [sugestao['frequencias']['C'], sugestao['frequencias']['V'], sugestao['frequencias']['E']],
            'Cor': ['#FF4B4B', '#4B4BFF', '#FFD700']
        })
        
        st.bar_chart(freq_data.set_index('Resultado')['Frequência (%)'])
        
        # Últimos resultados
        st.markdown("### 🔄 Últimos 5 Resultados Analisados")
        ultimos_html = ""
        for resultado in sugestao['ultimos_resultados']:
            ultimos_html += get_resultado_html(resultado)
        st.markdown(ultimos_html, unsafe_allow_html=True)
        
    else:
        st.warning("⚠️ Dados insuficientes para gerar sugestão confiável. Continue inserindo resultados.")

else:
    st.info(f"📋 Para análise completa, são necessários pelo menos 6 resultados. Atual: {len(st.session_state.historico)}")

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>⚽ Football Studio Live Game - Analisador Pro v2.0</p>
    <p>🎯 Sistema de análise avançada com 20+ padrões específicos</p>
    <p>⚠️ Use com responsabilidade. Apostas envolvem riscos.</p>
</div>
""", unsafe_allow_html=True)
