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
    st.session_state.estatisticas = {
        'total_jogos': 0,
        'acertos': 0,
        'erros': 0,
        'historico_sugestoes': []
    }

def adicionar_resultado(resultado):
    """Adiciona novo resultado ao histórico"""
    st.session_state.historico.insert(0, resultado)
    if len(st.session_state.historico) > 50:
        st.session_state.historico = st.session_state.historico[:50]
    st.session_state.estatisticas['total_jogos'] += 1

def limpar_historico():
    """Limpa todo o histórico"""
    st.session_state.historico = []
    st.session_state.estatisticas = {
        'total_jogos': 0,
        'acertos': 0,
        'erros': 0,
        'historico_sugestoes': []
    }

def desfazer_ultimo():
    """Remove o último resultado"""
    if st.session_state.historico:
        st.session_state.historico.pop(0)
        if st.session_state.estatisticas['total_jogos'] > 0:
            st.session_state.estatisticas['total_jogos'] -= 1

def validar_sugestao(sugestao_anterior, resultado_real):
    """Valida se a sugestão anterior estava correta"""
    if sugestao_anterior['entrada_codigo'] == resultado_real:
        st.session_state.estatisticas['acertos'] += 1
        return True
    else:
        st.session_state.estatisticas['erros'] += 1
        return False

def get_resultado_html(resultado):
    """Retorna HTML para visualização do resultado"""
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

div.stButton > button[data-testid="stButton-✈️ Visitante (V)"] {
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
    if st.button("🗑️ Limpar", key="🗑️ Limpar", use_container_width=True, help="Limpar todo o histórico"):
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
    analyzer = AnalisePadroes(st.session_state.historico)
    
    # --- SUGESTÃO INTELIGENTE ---
    st.markdown('<div class="section-header"><h2>🎯 Sugestão Inteligente</h2></div>', unsafe_allow_html=True)
    
    sugestao = analyzer.sugestao_inteligente()
    
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
        </div>
        """, unsafe_allow_html=True)
        
        # Detalhes da análise
        if show_advanced:
            with st.expander("📋 Detalhes da Análise"):
                st.write("**Padrões Identificados:**")
                for motivo in sugestao['motivos']:
                    st.write(f"• {motivo}")
                
                if 'analise_detalhada' in sugestao:
                    st.write("**Análise por Categoria:**")
                    for categoria, padroes in sugestao['analise_detalhada'].items():
                        st.write(f"**{categoria}:** {', '.join(padroes)}")
    else:
        st.warning(f"🤔 Confiança insuficiente ({sugestao['confianca']}%) ou nenhum padrão detectado")
    
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
        
        for padrao in nao_encontrados[:10]:  # Limita a exibição
            st.markdown(f'<div class="pattern-not-found">❌ {padrao}</div>', unsafe_allow_html=True)
    
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
        st.markdown("### 📈 Distribuição dos Resultados")
        chart_data = pd.DataFrame({
            'Resultado': ['Casa', 'Visitante', 'Empate'],
            'Frequência': [frequencias['C'], frequencias['V'], frequencias['E']],
            'Cor': ['#FF4B4B', '#4B4BFF', '#FFD700']
        })
        
        st.bar_chart(chart_data.set_index('Resultado')['Frequência'])

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
