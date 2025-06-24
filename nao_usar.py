import streamlit as st
import collections
import r
import streamlit as st
import collections
import random
import numpy as np
from datetime import datetime
import pandas as pd

# --- CLASSE ANALISEPADROES REFINADA ---
class AnalisePadroes:
    def __init__(self, historico):
        self.historico = historico[:50]  # Aumentado para 50 jogos para melhor anÃ¡lise
        self.padroes_ativos = {
            # PadrÃµes bÃ¡sicos existentes
            "SequÃªncia (Surf de Cor)": self._sequencia_simples,
            "Zig-Zag Perfeito": self._zig_zag,
            "Quebra de Surf": self._quebra_de_surf,
            "Quebra de Zig-Zag": self._quebra_de_zig_zag,
            "Duplas Repetidas": self._duplas_repetidas,
            "Empate Recorrente": self._empate_recorrente,
            "PadrÃ£o Escada": self._padrao_escada,
            "Espelho": self._espelho,
            "AlternÃ¢ncia com Empate": self._alternancia_empate_meio,
            "PadrÃ£o Onda": self._padrao_onda,
            
            # Novos padrÃµes especÃ­ficos do Football Studio
            "PadrÃ£o Fibonacci": self._padrao_fibonacci,
            "SequÃªncia Dourada": self._sequencia_dourada,
            "PadrÃ£o Triangular": self._padrao_triangular,
            "Ciclo de Empates": self._ciclo_empates,
            "PadrÃ£o Martingale": self._padrao_martingale,
            "SequÃªncia de Fibonacci Invertida": self._fibonacci_invertida,
            "PadrÃ£o Dragon Tiger": self._padrao_dragon_tiger,
            "SequÃªncia de Paroli": self._sequencia_paroli,
            "PadrÃ£o de Ondas Longas": self._ondas_longas,
            "Ciclo de DominÃ¢ncia": self._ciclo_dominancia,
            "PadrÃ£o de TensÃ£o": self._padrao_tensao,
            "SequÃªncia de Labouchere": self._sequencia_labouchere,
            "PadrÃ£o Ritmo CardÃ­aco": self._ritmo_cardiaco,
            "Ciclo de PressÃ£o": self._ciclo_pressao,
            "PadrÃ£o de Clusters": self._padrao_clusters,
            "SequÃªncia Polar": self._sequencia_polar,
            "PadrÃ£o de Momentum": self._padrao_momentum,
            "Ciclo de RespiraÃ§Ã£o": self._ciclo_respiracao,
            "PadrÃ£o de ResistÃªncia": self._padrao_resistencia,
            "SequÃªncia de Breakout": self._sequencia_breakout,
        }
        
        # Pesos dos padrÃµes para calcular confianÃ§a
        self.pesos_padroes = {
            "SequÃªncia (Surf de Cor)": 0.9,
            "Zig-Zag Perfeito": 0.8,
            "Quebra de Surf": 0.85,
            "Quebra de Zig-Zag": 0.8,
            "PadrÃ£o Fibonacci": 0.95,
            "SequÃªncia Dourada": 0.9,
            "PadrÃ£o Dragon Tiger": 0.85,
            "Ciclo de DominÃ¢ncia": 0.8,
            "PadrÃ£o de Momentum": 0.9,
            "SequÃªncia de Breakout": 0.95,
        }

    def analisar_todos(self):
        resultados = {}
        for nome, func in self.padroes_ativos.items():
            try:
                resultados[nome] = func()
            except Exception as e:
                resultados[nome] = False
        return resultados

    # --- PADRÃ•ES BÃSICOS EXISTENTES ---
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
        
        # Verifica se hÃ¡ um padrÃ£o de intervalos regulares entre empates
        intervalos = []
        for i in range(len(empates_indices) - 1):
            intervalos.append(empates_indices[i+1] - empates_indices[i])
        
        if len(intervalos) >= 2:
            # Verifica se os intervalos seguem um padrÃ£o
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

    # --- NOVOS PADRÃ•ES ESPECÃFICOS DO FOOTBALL STUDIO ---
    
    def _padrao_fibonacci(self):
        """Detecta padrÃµes baseados na sequÃªncia de Fibonacci"""
        if len(self.historico) < 8:
            return False
        
        fib_sequence = [1, 1, 2, 3, 5, 8]
        
        for i in range(len(self.historico) - 7):
            # Verifica se hÃ¡ uma sequÃªncia que segue o padrÃ£o Fibonacci
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
        """Detecta sequÃªncias baseadas na proporÃ§Ã£o Ã¡urea"""
        if len(self.historico) < 8:
            return False
        
        # PadrÃ£o dourado: 3, 5, 8, 13...
        for i in range(len(self.historico) - 7):
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] and
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] == self.historico[i+6] == self.historico[i+7] and
                self.historico[i] != self.historico[i+3]):
                return True
        return False

    def _padrao_triangular(self):
        """Detecta padrÃµes triangulares: 1, 2, 3, 2, 1"""
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
        """Detecta ciclos especÃ­ficos de empates"""
        empates = [i for i, x in enumerate(self.historico) if x == 'E']
        if len(empates) < 3:
            return False
        
        # Verifica se empates aparecem em intervalos cÃ­clicos
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
        """Detecta padrÃµes de duplicaÃ§Ã£o (Martingale)"""
        if len(self.historico) < 7:
            return False
        
        for i in range(len(self.historico) - 6):
            # PadrÃ£o: 1, 2, 4 (1 resultado, 2 iguais, 4 iguais)
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
        
        # PadrÃ£o: 8, 5, 3, 2, 1, 1
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
        """PadrÃ£o especÃ­fico de Dragon Tiger adaptado"""
        if len(self.historico) < 6:
            return False
        
        for i in range(len(self.historico) - 5):
            # PadrÃ£o: AlternÃ¢ncia forte seguida de empate
            if (self.historico[i] != self.historico[i+1] != self.historico[i+2] and
                self.historico[i+3] == 'E' and
                self.historico[i+4] == self.historico[i+5] and
                self.historico[i+4] != 'E'):
                return True
        return False

    def _sequencia_paroli(self):
        """Detecta padrÃµes de progressÃ£o positiva"""
        if len(self.historico) < 7:
            return False
        
        for i in range(len(self.historico) - 6):
            # PadrÃ£o: 1, 2, 4, volta ao 1
            if (self.historico[i] != self.historico[i+1] and
                self.historico[i+1] == self.historico[i+2] and
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] == self.historico[i+6] and
                self.historico[i] == self.historico[i+3]):
                return True
        return False

    def _ondas_longas(self):
        """Detecta ondas longas (sequÃªncias de 5+ do mesmo resultado)"""
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
        """Detecta ciclos de dominÃ¢ncia de um resultado"""
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
        """Detecta padrÃµes de tensÃ£o (alternÃ¢ncia seguida de explosÃ£o)"""
        if len(self.historico) < 8:
            return False
        
        for i in range(len(self.historico) - 7):
            # PadrÃ£o: 4+ alternÃ¢ncias seguidas de sequÃªncia
            alternations = 0
            for j in range(i, i+4):
                if j+1 < len(self.historico) and self.historico[j] != self.historico[j+1]:
                    alternations += 1
            
            if alternations >= 3:
                # Verifica se hÃ¡ sequÃªncia apÃ³s as alternÃ¢ncias
                if (i+5 < len(self.historico) and 
                    self.historico[i+4] == self.historico[i+5] == self.historico[i+6]):
                    return True
        return False

    def _sequencia_labouchere(self):
        """Detecta padrÃµes de cancelamento"""
        if len(self.historico) < 6:
            return False
        
        for i in range(len(self.historico) - 5):
            # PadrÃ£o: inÃ­cio e fim iguais, meio diferente
            if (self.historico[i] == self.historico[i+5] and
                self.historico[i+1] == self.historico[i+4] and
                self.historico[i+2] != self.historico[i] and
                self.historico[i+3] != self.historico[i]):
                return True
        return False

    def _ritmo_cardiaco(self):
        """Detecta padrÃµes de ritmo cardÃ­aco (batimentos irregulares)"""
        if len(self.historico) < 8:
            return False
        
        for i in range(len(self.historico) - 7):
            # PadrÃ£o: 2, 1, 2, 3, 2, 1, 2
            segment = self.historico[i:i+8]
            if (segment[0] == segment[1] and
                segment[2] != segment[0] and
                segment[3] == segment[4] and
                segment[5] == segment[6] == segment[7] and
                segment[3] != segment[5]):
                return True
        return False

    def _ciclo_pressao(self):
        """Detecta ciclos de pressÃ£o crescente"""
        if len(self.historico) < 9:
            return False
        
        for i in range(len(self.historico) - 8):
            # PadrÃ£o: 1, 2, 3, 1, 2, 3
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
            
            # Verifica se cada cluster tem dominÃ¢ncia (3+ iguais)
            if (collections.Counter(cluster1).most_common(1)[0][1] >= 3 and
                collections.Counter(cluster2).most_common(1)[0][1] >= 3 and
                collections.Counter(cluster3).most_common(1)[0][1] >= 3):
                return True
        return False

    def _sequencia_polar(self):
        """Detecta sequÃªncias polares (extremos)"""
        if len(self.historico) < 10:
            return False
        
        for i in range(len(self.historico) - 9):
            window = self.historico[i:i+10]
            
            # Verifica se hÃ¡ polarizaÃ§Ã£o (sÃ³ 2 tipos de resultado, sem empates)
            unique_results = set(window)
            if len(unique_results) == 2 and 'E' not in unique_results:
                # Verifica alternÃ¢ncia polar
                changes = sum(1 for j in range(len(window)-1) if window[j] != window[j+1])
                if changes >= 6:  # Muitas mudanÃ§as
                    return True
        return False

    def _padrao_momentum(self):
        """Detecta padrÃµes de momentum (aceleraÃ§Ã£o)"""
        if len(self.historico) < 10:
            return False
        
        for i in range(len(self.historico) - 9):
            # PadrÃ£o: 1, 2, 3, 4 (crescimento)
            if (self.historico[i] != self.historico[i+1] and
                self.historico[i+1] == self.historico[i+2] and
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] and
                self.historico[i+6] == self.historico[i+7] == self.historico[i+8] == self.historico[i+9]):
                return True
        return False

    def _ciclo_respiracao(self):
        """Detecta padrÃµes de respiraÃ§Ã£o (inspiraÃ§Ã£o/expiraÃ§Ã£o)"""
        if len(self.historico) < 8:
            return False
        
        for i in range(len(self.historico) - 7):
            # PadrÃ£o: expansÃ£o e contraÃ§Ã£o
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] == self.historico[i+3] and
                self.historico[i+4] != self.historico[i] and
                self.historico[i+5] == self.historico[i+6] == self.historico[i+7] and
                self.historico[i+5] != self.historico[i+4]):
                return True
        return False

    def _padrao_resistencia(self):
        """Detecta padrÃµes de resistÃªncia (tentativas de quebra)"""
        if len(self.historico) < 6:
            return False
        
        for i in range(len(self.historico) - 5):
            # PadrÃ£o: resultado dominante resiste a mudanÃ§as
            if (self.historico[i] == self.historico[i+2] == self.historico[i+4] == self.historico[i+5] and
                self.historico[i+1] != self.historico[i] and
                self.historico[i+3] != self.historico[i]):
                return True
        return False

    def _sequencia_breakout(self):
        """Detecta sequÃªncias de breakout (quebra de padrÃ£o)"""
        if len(self.historico) < 8:
            return False
        
        for i in range(len(self.historico) - 7):
            # PadrÃ£o: estabilidade seguida de mudanÃ§a abrupta
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] == self.historico[i+3] and
                self.historico[i+4] != self.historico[i] and
                self.historico[i+5] == self.historico[i+6] == self.historico[i+7] and
                self.historico[i+5] == self.historico[i+4]):
                return True
        return False

    def calcular_frequencias(self):
        """Calcula frequÃªncias dos resultados"""
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
        """Calcula tendÃªncia dos Ãºltimos resultados"""
        if len(self.historico) < 5:
            return "Dados insuficientes"
        
        ultimos_5 = self.historico[:5]
        contador = collections.Counter(ultimos_5)
        
        if contador.most_common(1)[0][1] >= 4:
            return f"Forte tendÃªncia: {contador.most_common(1)[0][0]}"
        elif contador.most_common(1)[0][1] >= 3:
            return f"TendÃªncia moderada: {contador.most_common(1)[0][0]}"
        else:
            return "Sem tendÃªncia clara"

    def sugestao_inteligente(self):
        """Gera sugestÃ£o inteligente baseada em mÃºltiplos fatores"""
        analise = self.analisar_todos()
        padroes_identificados = [nome for nome, ok in analise.items() if ok]
        
        if not padroes_identificados:
            return {
                "sugerir": False,
                "entrada": None,
                "entrada_codigo": None,
                "motivos": ["Nenhum padrÃ£o confiÃ¡vel identificado"],
                "confianca": 0,
                "frequencias": self.calcular_frequencias(),
                "tendencia": self.calcular_tendencia(),
                "ultimos_resultados": self.historico[:5]
            }
        
        # Calcula confianÃ§a baseada nos pesos dos padrÃµes
        confianca_total = 0
        peso_total = 0
        
        for padrao in padroes_identificados:
            peso = self.pesos_padroes.get(padrao, 0.5)
            confianca_total += peso
            peso_total += peso
        
        confianca_media = (confianca_total / peso_total) * 100 if peso_total > 0 else 0
        
        # Ajusta confianÃ§a baseada na quantidade de padrÃµes
        bonus_quantidade = min(20, len(padroes_identificados) * 5)
        confianca_final = min(95, int(confianca_media + bonus_quantidade))
        
        # AnÃ¡lise de frequÃªncias e tendÃªncias
        frequencias = self.calcular_frequencias()
        tendencia = self.calcular_tendencia()
        
        # LÃ³gica de sugestÃ£o aprimorada
        opcoes = ["V", "C", "E"]
        
        # Considera padrÃµes de quebra
        padroes_quebra = [p for p in padroes_identificados if "quebra" in p.lower() or "breakout" in p.lower()]
        
        if padroes_quebra:
            # Se hÃ¡ padrÃµes de quebra, sugere o oposto da tendÃªncia
            ultimo_resultado = self.historico[0] if self.historico else None
            if ultimo_resultado:
                opcoes_sem_ultimo = [op for op in opcoes if op != ultimo_resultado]
                entrada_sugerida = min(opcoes_sem_ultimo, key=lambda x: frequencias.get(x, 0))
            else:
                entrada_sugerida = min(opcoes, key=lambda x: frequencias.get(x, 0))
        else:
            # LÃ³gica normal: sugere baseado em frequÃªncias
            entrada_sugerida = min(opcoes, key=lambda x: frequencias.get(x, 0))
        
        # Se todas as frequÃªncias sÃ£o iguais, usa anÃ¡lise de momentum
        if len(set(frequencias.values())) == 1:
            # Analisa momentum dos Ãºltimos 3 resultados
            ultimos_3 = self.historico[:3]
            contador_recente = collections.Counter(ultimos_3)
            if contador_recente.most_common(1)[0][1] >= 2:
                # Se hÃ¡ repetiÃ§Ã£o recente, sugere mudanÃ§a
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
        """Gera anÃ¡lise detalhada dos padrÃµes encontrados"""
        categorias = {
            "PadrÃµes de SequÃªncia": ["SequÃªncia", "Surf", "Ondas", "Fibonacci"],
            "PadrÃµes de Quebra": ["Quebra", "Breakout", "TensÃ£o"],
            "PadrÃµes CÃ­clicos": ["Ciclo", "RespiraÃ§Ã£o", "Momentum"],
            "PadrÃµes Especiais": ["Dragon", "Martingale", "Dourada", "Triangular"]
        }
        
        analise = {}
        for categoria, keywords in categorias.items():
            padroes_categoria = [p for p in padroes if any(k.lower() in p.lower() for k in keywords)]
            if padroes_categoria:
                analise[categoria] = padroes_categoria
        
        return analise

# --- FUNÃ‡Ã•ES DE INTERFACE E LÃ“GICA DE HISTÃ“RICO ---

# Inicializa o estado da sessÃ£o
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
    """Adiciona resultado ao histÃ³rico"""
    st.session_state.historico.insert(0, resultado)
    if len(st.session_state.historico) > 50:
        st.session_state.historico = st.session_state.historico[:50]
    st.session_state.estatisticas['total_jogos'] += 1

def limpar_historico():
    """Limpa todo o histÃ³rico"""
    st.session_state.historico = []
    st.session_state.estatisticas = {
        'total_jogos': 0,
        'acertos': 0,
        'erros': 0,
        'historico_sugestoes': []
    }

def desfazer_ultimo():
    """Remove o Ãºltimo resultado"""
    if st.session_state.historico:
        st.session_state.historico.pop(0)
        if st.session_state.estatisticas['total_jogos'] > 0:
            st.session_state.estatisticas['total_jogos'] -= 1

def verificar_sugestao(resultado_real, sugestao_codigo):
    """Verifica se a sugestÃ£o estava correta"""
    if sugestao_codigo == resultado_real:
        st.session_state.estatisticas['acertos'] += 1
        return True
    else:
        st.session_state.estatisticas['erros'] += 1
        return False

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
    """Retorna seta de tendÃªncia baseada nas frequÃªncias"""
    valores = list(frequencias.values())
    max_val = max(valores)
    resultado_dominante = [k for k, v in frequencias.items() if v == max_val][0]
    
    arrows = {'C': 'ðŸ”´', 'V': 'ðŸ”µ', 'E': 'ðŸŸ¡'}
    return arrows.get(resultado_dominante, 'âšª')

# --- CONFIGURAÃ‡ÃƒO DA PÃGINA ---
st.set_page_config(
    layout="wide", 
    page_title="Football Studio Live Analyzer Pro",
    page_icon="âš½"
)

# CSS melhorado
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

/* BotÃµes coloridos */
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

/* BotÃµes de aÃ§Ã£o */
div.stButton > button[kind="primary"]:not([style*="background"]) {
    background: linear-gradient(135deg, #28a745, #20c997);
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
}

</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<h1 class="main-header">âš½ Football Studio Live Analyzer Pro</h1>', unsafe_allow_html=True)
st.markdown("---")

# --- ESTATÃSTICAS RÃPIDAS ---
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>ðŸŽ¯ Total de Jogos</h3>
        <h2>{st.session_state.estatisticas['total_jogos']}</h2>
    </div>
    """, unsafe_allow_html=True)

with col_stat2:
    acertos = st.session_state.estatisticas['acertos']
    st.markdown(f"""
    <div class="metric-card">
        <h3>âœ… Acertos</h3>
        <h2>{acertos}</h2>
    </div>
    """, unsafe_allow_html=True)

with col_stat3:
    erros = st.session_state.estatisticas['erros']
    st.markdown(f"""
    <div class="metric-card">
        <h3>âŒ Erros</h3>
        <h2>{erros}</h2>
    </div>
    """, unsafe_allow_html=True)

with col_stat4:
    total_sugestoes = acertos + erros
    precisao = round((acertos / total_sugestoes * 100), 1) if total_sugestoes > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <h3>ðŸ“Š PrecisÃ£o</h3>
        <h2>{precisao}%</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- INSERÃ‡ÃƒO DE RESULTADOS ---
st.subheader("ðŸŽ® Inserir Novo Resultado")

col_btn1, col_btn2, col_btn3, col_btn4, col_btn5 = st.columns(5)

with col_btn1:
    if st.button("ðŸ”´ Casa (C)", help="VitÃ³ria da Casa", key="casa", use_container_width=True):
        adicionar_resultado('C')
        st.rerun()

with col_btn2:
    if st.button("ðŸ”µ Visitante (V)", help="VitÃ³ria do Visitante", key="visitante", use_container_width=True):
        adicionar_resultado('V')
        st.rerun()

with col_btn3:
    if st.button("ðŸŸ¡ Empate (E)", help="Resultado Empate", key="empate", use_container_width=True):
        adicionar_resultado('E')
        st.rerun()

with col_btn4:
    if st.button("â†©ï¸ Desfazer", help="Remove Ãºltimo resultado", key="desfazer", use_container_width=True):
        desfazer_ultimo()
        st.rerun()

with col_btn5:
    if st.button("ðŸ—‘ï¸ Limpar Tudo", help="Limpa histÃ³rico completo", key="limpar", use_container_width=True):
        limpar_historico()
        st.rerun()

st.markdown("---")

# --- HISTÃ“RICO ---
st.subheader("ðŸ“ˆ HistÃ³rico de Resultados")

if not st.session_state.historico:
    st.info("ðŸŽ¯ HistÃ³rico vazio. Comece inserindo alguns resultados para ver a mÃ¡gica acontecer!")
else:
    # Exibe histÃ³rico com styling
    historico_html = "<div class='history-container'>"
    historico_html += "<h4>Ãšltimos Resultados (mais recente Ã  esquerda):</h4>"

    for i, resultado in enumerate(st.session_state.historico):
        historico_html += get_resultado_html(resultado)
        if (i + 1) % 9 == 0 and (i + 1) < len(st.session_state.historico):
            historico_html += "<br><br>"

    historico_html += f"<br><br><small>Total: {len(st.session_state.historico)} resultados</small>"
    historico_html += "</div>"

    st.markdown(historico_html, unsafe_allow_html=True)

st.markdown("---")

# --- ANÃLISE PRINCIPAL ---
if len(st.session_state.historico) >= 9:
    analyzer = AnalisePadroes(st.session_state.historico)
    
    # --- SUGESTÃƒO PRINCIPAL ---
    st.header("ðŸ”® SugestÃ£o Inteligente")
    
    sugestao = analyzer.sugestao_inteligente()
    
    if sugestao['sugerir']:
        # Determina cor da confianÃ§a
        if sugestao['confianca'] >= 75:
            conf_class = "confidence-high"
            conf_emoji = "ðŸŸ¢"
        elif sugestao['confianca'] >= 50:
            conf_class = "confidence-medium"
            conf_emoji = "ðŸŸ¡"
        else:
            conf_class = "confidence-low"
            conf_emoji = "ðŸ”´"
        
        # Box de sugestÃ£o
        st.markdown(f"""
        <div class="suggestion-box">
            <h2>ðŸŽ¯ PrÃ³xima Jogada Sugerida: <strong>{sugestao['entrada']}</strong></h2>
            <h3>{conf_emoji} ConfianÃ§a: <span class="{conf_class}">{sugestao['confianca']}%</span></h3>
            <p><strong>TendÃªncia:</strong> {sugestao['tendencia']}</p>
            <p><strong>Ãšltimos 5:</strong> {' â†’ '.join(sugestao['ultimos_resultados'])}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # AnÃ¡lise detalhada
        if 'analise_detalhada' in sugestao and sugestao['analise_detalhada']:
            st.subheader("ðŸ” AnÃ¡lise Detalhada por Categoria")
            for categoria, padroes in sugestao['analise_detalhada'].items():
                st.write(f"**{categoria}:**")
                for padrao in padroes:
                    st.markdown(f"<span class='pattern-found'>âœ“ {padrao}</span>", unsafe_allow_html=True)
                st.write("")
    
    else:
        st.warning("âš ï¸ Dados insuficientes para sugestÃ£o confiÃ¡vel. Continue jogando!")
    
    st.markdown("---")
    
    # --- PADRÃ•ES DETECTADOS ---
    st.header("ðŸŽ¨ PadrÃµes Detectados")
    
    padroes_encontrados = analyzer.analisar_todos()
    
    col_found, col_not_found = st.columns(2)
    
    with col_found:
        st.subheader("âœ… PadrÃµes Ativos")
        encontrados = [nome for nome, found in padroes_encontrados.items() if found]
        
        if encontrados:
            for padrao in encontrados:
                st.markdown(f"<span class='pattern-found'>âœ“ {padrao}</span>", unsafe_allow_html=True)
        else:
            st.info("Nenhum padrÃ£o especÃ­fico ativo no momento.")
    
    with col_not_found:
        st.subheader("â³ PadrÃµes Inativos")
        nao_encontrados = [nome for nome, found in padroes_encontrados.items() if not found]
        
        if nao_encontrados:
            # Mostra apenas os primeiros 10 para nÃ£o sobrecarregar
            for padrao in nao_encontrados[:10]:
                st.markdown(f"<span class='pattern-not-found'>â—‹ {padrao}</span>", unsafe_allow_html=True)
            
            if len(nao_encontrados) > 10:
                st.write(f"... e mais {len(nao_encontrados) - 10} padrÃµes")
    
    st.markdown("---")
    
    # --- ANÃLISE FREQUENCIAL ---
    st.header("ðŸ“Š AnÃ¡lise de FrequÃªncias")
    
    frequencias = analyzer.calcular_frequencias()
    
    col_freq1, col_freq2 = st.columns(2)
    
    with col_freq1:
        # GrÃ¡fico de barras
        df_freq = pd.DataFrame([
            {'Resultado': 'Casa', 'FrequÃªncia': frequencias['C'], 'Cor': '#FF4B4B'},
            {'Resultado': 'Visitante', 'FrequÃªncia': frequencias['V'], 'Cor': '#4B4BFF'},
            {'Resultado': 'Empate', 'FrequÃªncia': frequencias['E'], 'Cor': '#FFD700'}
        ])
        
        st.bar_chart(df_freq.set_index('Resultado')['FrequÃªncia'])
    
    with col_freq2:
        # MÃ©tricas detalhadas
        st.metric("ðŸ”´ Casa", f"{frequencias['C']}%")
        st.metric("ðŸ”µ Visitante", f"{frequencias['V']}%")
        st.metric("ðŸŸ¡ Empate", f"{frequencias['E']}%")
        
        # Indicador de tendÃªncia
        trend_arrow = get_trend_arrow(frequencias)
        st.markdown(f"**TendÃªncia Atual:** {trend_arrow}")

else:
    st.warning(f"ðŸ“Š AnÃ¡lise serÃ¡ exibida com pelo menos 9 resultados. Atual: **{len(st.session_state.historico)}**")
    
    progress = len(st.session_state.historico) / 9
    st.progress(progress)
    st.write(f"Progresso: {len(st.session_state.historico)}/9 resultados")

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; margin-top: 50px;'>
    <h4>âš½ Football Studio Live Analyzer Pro</h4>
    <p>AnÃ¡lise inteligente de padrÃµes para Football Studio da Evolution Gaming</p>
    <p><small>Desenvolvido com algoritmos avanÃ§ados de detecÃ§Ã£o de padrÃµes</small></p>
</div>
""", unsafe_allow_html=True)
