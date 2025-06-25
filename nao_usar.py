import streamlit as st
import collections
import random
import numpy as np
from datetime import datetime
import pandas as pd

# --- CLASSE ANALISEPADROES REFINADA ---
class AnalisePadroes:
    def __init__(self, historico):
        # Limita o histórico para análise, sempre os 54 mais recentes
        self.historico = historico[:54] # Máximo de 54 resultados para o roadmap
        
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
            "Padrão 3x1": self._padrao_3x1, # Novo
            "Padrão 4x1": self._padrao_4x1, # Novo
            "Empate em Zonas de Frequência": self._empate_zonas_frequencia, # Novo
        }
        
        # Pesos dos padrões para calcular confiança (podem ser ajustados conforme performance real)
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
                # print(f"Erro ao analisar padrão {nome}: {e}") # Para depuração
                resultados[nome] = False
        return resultados

    # --- PADRÕES BÁSICOS EXISTENTES ---
    def _sequencia_simples(self):
        # 1. Sequência (Surf de Cor): 3+ vezes a mesma cor seguida
        for i in range(len(self.historico) - 2):
            if self.historico[i] == self.historico[i+1] == self.historico[i+2]:
                return True
        return False

    def _zig_zag(self):
        # 2. Zig-Zag Perfeito: alternância constante por 5+ resultados
        if len(self.historico) < 6:
            return False
        count = 0
        for i in range(len(self.historico) - 1):
            if self.historico[i] != self.historico[i+1]:
                count += 1
            else:
                if count >= 5: # Pelo menos 5 alternâncias seguidas
                    return True
                count = 0
        return count >= 5

    def _quebra_de_surf(self):
        # 3. Quebra de Surf: sequência que é interrompida (3+ iguais, depois diferente)
        for i in range(len(self.historico) - 3):
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] and 
                self.historico[i+2] != self.historico[i+3]):
                return True
        return False

    def _quebra_de_zig_zag(self):
        # 4. Quebra de Zig-Zag: padrão alternado que quebra
        if len(self.historico) < 4:
            return False
        for i in range(len(self.historico) - 3):
            if (self.historico[i] != self.historico[i+1] and 
                self.historico[i+1] != self.historico[i+2] and # Verifica que não é tripla igual
                self.historico[i+2] == self.historico[i+3]): # O próximo quebra a alternância
                return True
        return False

    def _duplas_repetidas(self):
        # 5. Duplas Repetidas: Casa, Casa, Visitante, Visitante...
        if len(self.historico) < 4:
            return False
        for i in range(len(self.historico) - 3):
            if (self.historico[i] == self.historico[i+1] and 
                self.historico[i+2] == self.historico[i+3] and 
                self.historico[i] != self.historico[i+2]):
                return True
        return False

    def _empate_recorrente(self):
        # 6. Empate Recorrente: Empates aparecendo em intervalos curtos
        empates_indices = [i for i, r in enumerate(self.historico) if r == 'E']
        if len(empates_indices) < 3:
            return False
        
        intervalos = []
        for i in range(len(empates_indices) - 1):
            intervalos.append(empates_indices[i+1] - empates_indices[i])
        
        # Verifica se os intervalos são relativamente consistentes e curtos
        if len(intervalos) >= 2:
            # Por exemplo, se a maioria dos intervalos está dentro de uma pequena margem da média
            media_intervalo = sum(intervalos) / len(intervalos)
            if 2 <= media_intervalo <= 8: # Intervalos curtos
                # Verifica a consistência
                consistent_intervals = [x for x in intervalos if abs(x - media_intervalo) <= 2]
                return len(consistent_intervals) / len(intervalos) >= 0.75 # Pelo menos 75% dos intervalos são consistentes
        return False

    def _padrao_escada(self):
        # 7. Padrão Escada: 1 Casa, 2 Visitantes, 3 Casas (adaptar para cores/resultados)
        if len(self.historico) < 6:
            return False
        for i in range(len(self.historico) - 5):
            if (self.historico[i] != self.historico[i+1] and # 1 diferente do 2
                self.historico[i+1] == self.historico[i+2] and # 2 iguais
                self.historico[i+2] != self.historico[i+3] and # 3 diferente do 2
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5]): # 3 iguais
                return True
        return False

    def _espelho(self):
        # 8. Espelho: Ex: Casa, Visitante, Visitante, Casa
        if len(self.historico) < 4:
            return False
        # Busca por padrões de espelho de 4 a 12 resultados
        for tamanho in range(4, min(len(self.historico) + 1, 13)):
            if tamanho % 2 == 0: # Deve ser tamanho par
                metade = tamanho // 2
                for start in range(len(self.historico) - tamanho + 1):
                    primeira_metade = self.historico[start:start + metade]
                    segunda_metade = self.historico[start + metade:start + tamanho]
                    if primeira_metade == segunda_metade[::-1]: # Verifica se é espelho
                        return True
        return False

    def _alternancia_empate_meio(self):
        # 9. Alternância com Empate no meio: Casa, Empate, Visitante (Adaptar para cores/resultados)
        if len(self.historico) < 3:
            return False
        for i in range(len(self.historico) - 2):
            if (self.historico[i] != 'E' and self.historico[i+1] == 'E' and 
                self.historico[i+2] != 'E' and self.historico[i] != self.historico[i+2]):
                return True
        return False

    def _padrao_onda(self):
        # 10. Padrão "onda": Ex: 1-2-1-2 de núcleos (Adaptar para 1 ou 2 sequências de resultados)
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
        # 11. Padrão Fibonacci
        if len(self.historico) < 8: # Mínimo para começar a ver 1,1,2,3
            return False
        
        fib_sequence = [1, 1, 2, 3, 5] # Simplificado para os primeiros números
        
        # Converte o histórico para uma sequência de comprimentos de sequências de resultados iguais
        # Ex: C,C,V,V,V,E,E -> [2, 3, 2]
        current_seq_len = []
        if self.historico:
            count = 1
            for i in range(1, len(self.historico)):
                if self.historico[i] == self.historico[i-1]:
                    count += 1
                else:
                    current_seq_len.append(count)
                    count = 1
            current_seq_len.append(count) # Adiciona o último
        
        # Verifica se há a sequência Fibonacci dentro dos comprimentos de sequências
        for i in range(len(current_seq_len) - len(fib_sequence) + 1):
            if current_seq_len[i:i+len(fib_sequence)] == fib_sequence:
                return True
        return False

    def _sequencia_dourada(self):
        # 12. Sequência Dourada: 3, 5
        if len(self.historico) < 8:
            return False
        for i in range(len(self.historico) - 7):
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] and # 3 iguais
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] == self.historico[i+6] == self.historico[i+7] and # 5 iguais
                self.historico[i] != self.historico[i+3]): # e são diferentes entre si
                return True
        return False

    def _padrao_triangular(self):
        # 13. Padrão Triangular: 1, 2, 3, 2, 1
        if len(self.historico) < 9:
            return False
        for i in range(len(self.historico) - 8):
            segment = self.historico[i:i+9]
            if (segment[0] == segment[8] and # Extremidades iguais (1)
                segment[1] == segment[7] and # Próximos iguais (2)
                segment[0] != segment[1] and # Extremidades diferentes dos próximos
                segment[2] == segment[3] == segment[4] == segment[5] == segment[6] and # Meio com 5 iguais (3)
                segment[1] != segment[2]): # Diferente do meio
                return True
        return False

    def _ciclo_empates(self):
        # 14. Ciclo de Empates
        empates = [i for i, x in enumerate(self.historico) if x == 'E']
        if len(empates) < 3:
            return False
        
        # Verifica se empates aparecem em intervalos cíclicos (3 a 10)
        for cycle_length in range(3, 11): # Incluindo 10
            is_cyclic = True
            if len(empates) >= 2: # Precisa de pelo menos 2 empates para verificar intervalo
                for i in range(len(empates) - 1):
                    actual_interval = empates[i+1] - empates[i]
                    if not (cycle_length - 2 <= actual_interval <= cycle_length + 2): # Margem de tolerância
                        is_cyclic = False
                        break
            else:
                is_cyclic = False # Menos de 2 empates não forma ciclo
            if is_cyclic:
                return True
        return False

    def _padrao_martingale(self):
        # 15. Padrão Martingale: 1, 2, 4 (1 resultado, 2 iguais, 4 iguais)
        if len(self.historico) < 7:
            return False
        for i in range(len(self.historico) - 6):
            if (self.historico[i] != self.historico[i+1] and # 1 diferente do 2
                self.historico[i+1] == self.historico[i+2] and # 2 iguais
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] == self.historico[i+6] and # 4 iguais
                self.historico[i+1] != self.historico[i+3]): # e o segundo bloco diferente do terceiro
                return True
        return False

    def _fibonacci_invertida(self):
        # 16. Sequência de Fibonacci Invertida: 8, 5, 3, 2, 1, 1 (simulação)
        if len(self.historico) < 8:
            return False
        # Este é um padrão mais abstrato. Simulação: longa sequência, seguida por uma menor, etc.
        # Ex: C,C,C,C,C,C,C,C (8), V,V,V,V,V (5), C,C,C (3), V,V (2), E (1), C (1)
        # O código tenta detectar um padrão com segmentos de comprimentos decrescentes
        for i in range(len(self.historico) - 7):
            segment = self.historico[i:i+8]
            # Uma possível interpretação: longo, médio, curto e alternâncias no final
            if (len(set(segment[0:4])) == 1 and # 4 primeiros iguais (representando a parte "longa")
                segment[4] != segment[0] and    # Quebra
                len(set(segment[5:7])) == 1 and # Próximos 2 iguais
                segment[7] != segment[5] and    # Quebra
                segment[4] == segment[7]):      # Alterna e volta para o mesmo tipo
                return True
        return False

    def _padrao_dragon_tiger(self):
        # 17. Padrão Dragon Tiger: Alternância forte seguida de empate e par
        if len(self.historico) < 6:
            return False
        for i in range(len(self.historico) - 5):
            if (self.historico[i] != self.historico[i+1] and # Alterna
                self.historico[i+1] != self.historico[i+2] and # Alterna de novo
                self.historico[i] != self.historico[i+2] and # Garante 3 alternados (C,V,C ou V,C,V)
                self.historico[i+3] == 'E' and # Seguido por um empate
                self.historico[i+4] == self.historico[i+5] and # Seguido por dois iguais
                self.historico[i+4] != 'E'): # E esses não são empates
                return True
        return False

    def _sequencia_paroli(self):
        # 18. Sequência de Paroli: 1, 2, 4, volta ao 1
        if len(self.historico) < 7:
            return False
        for i in range(len(self.historico) - 6):
            if (self.historico[i] != self.historico[i+1] and # 1 singular
                self.historico[i+1] == self.historico[i+2] and # 2 iguais
                self.historico[i+3] == self.historico[i+4] == self.historico[i+5] == self.historico[i+6] and # 4 iguais
                self.historico[i] == self.historico[i+3]): # O primeiro é o mesmo tipo do início da sequência de 4
                return True
        return False

    def _ondas_longas(self):
        # 19. Padrão de Ondas Longas: sequências de 5+ do mesmo resultado
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
        # 20. Ciclo de Dominância: um resultado domina (70%+) em janela de 10
        if len(self.historico) < 10:
            return False
        for i in range(len(self.historico) - 9):
            window = self.historico[i:i+10]
            counter = collections.Counter(window)
            
            for resultado, count in counter.items():
                if count >= 7: # 70% de 10 jogos
                    return True
        return False

    def _padrao_tensao(self):
        # 21. Padrão de Tensão: alternância seguida de explosão (sequência)
        if len(self.historico) < 8:
            return False
        for i in range(len(self.historico) - 7):
            alternations = 0
            # Verifica 4+ alternâncias nos primeiros 4 ou 5
            for j in range(i, i+4): # Verifica 4 jogos (3 alternâncias)
                if j+1 < len(self.historico) and self.historico[j] != self.historico[j+1]:
                    alternations += 1
            
            if alternations >= 3: # Se houve pelo menos 3 alternâncias (ex: C,V,C,V)
                # Verifica se há uma sequência após as alternâncias
                if (i+4 < len(self.historico) and 
                    self.historico[i+4] == self.historico[i+5] == self.historico[i+6]): # Três iguais em sequência
                    return True
        return False

    def _sequencia_labouchere(self):
        # 22. Sequência de Labouchere: início e fim iguais, meio diferente (cancelamento)
        if len(self.historico) < 6:
            return False
        for i in range(len(self.historico) - 5):
            if (self.historico[i] == self.historico[i+5] and # Primeiro e último iguais
                self.historico[i+1] == self.historico[i+4] and # Segundo e penúltimo iguais
                self.historico[i] != self.historico[i+1] and # E diferentes do exterior
                self.historico[i+2] != self.historico[i+3] and # Meio diferentes
                self.historico[i+2] != self.historico[i] and # Meio diferente do exterior
                self.historico[i+3] != self.historico[i]):
                return True
        return False

    def _ritmo_cardiaco(self):
        # 23. Padrão Ritmo Cardíaco: batimentos irregulares (2, 1, 2, 3, 2, 1, 2)
        if len(self.historico) < 8:
            return False
        for i in range(len(self.historico) - 7):
            segment = self.historico[i:i+8]
            if (segment[0] == segment[1] and # Dois iguais
                segment[2] != segment[0] and # Um diferente
                segment[3] == segment[4] and # Dois iguais
                segment[5] == segment[6] == segment[7] and # Três iguais
                segment[0] != segment[3] and # Quebras entre os blocos
                segment[3] != segment[5]):
                return True
        return False

    def _ciclo_pressao(self):
        # 24. Ciclo de Pressão: 1, 2, 3, 1, 2, 3
        if len(self.historico) < 9:
            return False
        for i in range(len(self.historico) - 8):
            segment = self.historico[i:i+9]
            if (segment[0] != segment[1] and # 1 singular
                segment[1] == segment[2] and # 2 iguais
                segment[3] == segment[4] == segment[5] and # 3 iguais
                segment[6] == segment[0] and # Volta ao primeiro do ciclo
                segment[7] == segment[8] and # E segue o padrão do segundo (dupla)
                segment[6] != segment[7]): # O novo singular é diferente da nova dupla
                return True
        return False

    def _padrao_clusters(self):
        # 25. Padrão de Clusters: agrupamentos (clusters) de resultados
        if len(self.historico) < 12:
            return False
        for i in range(len(self.historico) - 11):
            window = self.historico[i:i+12]
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
        # 26. Sequência Polar: extremos (só 2 tipos de resultado, muitas alternâncias)
        if len(self.historico) < 10:
            return False
        for i in range(len(self.historico) - 9):
            window = self.historico[i:i+10]
            unique_results = set(window)
            if len(unique_results) == 2 and 'E' not in unique_results: # Apenas Casa e Visitante
                changes = sum(1 for j in range(len(window)-1) if window[j] != window[j+1])
                if changes >= 6: # Muitas mudanças (6+ alternâncias em 10 jogos)
                    return True
        return False

    def _padrao_momentum(self):
        # 27. Padrão de Momentum: aceleração (1, 2, 3, 4 crescimento)
        if len(self.historico) < 10:
            return False
        for i in range(len(self.historico) - 9):
            segment = self.historico[i:i+10]
            if (segment[0] != segment[1] and # Singular
                segment[1] == segment[2] and # Dupla
                segment[3] == segment[4] == segment[5] and # Tripla
                segment[6] == segment[7] == segment[8] == segment[9] and # Quádrupla
                segment[0] != segment[1] and segment[1] != segment[3] and segment[3] != segment[6]): # Certifica-se que os blocos são diferentes
                return True
        return False

    def _ciclo_respiracao(self):
        # 28. Ciclo de Respiração: expansão e contração
        if len(self.historico) < 8:
            return False
        for i in range(len(self.historico) - 7):
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] == self.historico[i+3] and # Expansão (4 iguais)
                self.historico[i+4] != self.historico[i] and # Quebra
                self.historico[i+5] == self.historico[i+6] == self.historico[i+7] and # Contração (3 iguais)
                self.historico[i+5] == self.historico[i+4]): # A nova estabilidade é do tipo da quebra
                return True
        return False

    def _padrao_resistencia(self):
        # 29. Padrão de Resistência: resultado dominante resiste a mudanças
        if len(self.historico) < 6:
            return False
        for i in range(len(self.historico) - 5):
            # Ex: C,V,C,E,C,C - C resiste a quebras de V e E
            if (self.historico[i] == self.historico[i+2] == self.historico[i+4] == self.historico[i+5] and # Padrão de resistência
                self.historico[i+1] != self.historico[i] and # Quebra 1
                self.historico[i+3] != self.historico[i]): # Quebra 2
                return True
        return False

    def _sequencia_breakout(self):
        # 30. Sequência de Breakout: estabilidade seguida de mudança abrupta e nova estabilidade
        if len(self.historico) < 8:
            return False
        for i in range(len(self.historico) - 7):
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] == self.historico[i+3] and # 4 iguais (estabilidade)
                self.historico[i+4] != self.historico[i] and # Quebra abrupta
                self.historico[i+5] == self.historico[i+6] == self.historico[i+7] and # Nova estabilidade (3 iguais)
                self.historico[i+5] == self.historico[i+4]): # A nova estabilidade é do tipo da quebra
                return True
        return False

    def _padrao_3x1(self):
        # 31. Padrão 3x1: Três ocorrências de um tipo, seguidas por uma de outro.
        if len(self.historico) < 4:
            return False
        for i in range(len(self.historico) - 3):
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] and
                self.historico[i+2] != self.historico[i+3]):
                return True
        return False
        
    def _padrao_4x1(self):
        # 32. Padrão 4x1: Quatro ocorrências de um tipo, seguidas por uma de outro.
        if len(self.historico) < 5:
            return False
        for i in range(len(self.historico) - 4):
            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] == self.historico[i+3] and
                self.historico[i+3] != self.historico[i+4]):
                return True
        return False

    def _empate_zonas_frequencia(self):
        # 33. Empate em Zonas de Frequência: Empates após ausência ou em ciclos de 9-10/15-35 rodadas.
        empates_indices = [i for i, r in enumerate(self.historico) if r == 'E']
        if len(empates_indices) < 2:
            return False

        # Verifica intervalos entre empates
        intervals = []
        for i in range(len(empates_indices) - 1):
            intervals.append(empates_indices[i+1] - empates_indices[i])

        # Se há empates em duplas
        if len(self.historico) >= 2 and self.historico[0] == 'E' and self.historico[1] == 'E':
            return True # Empate em dupla

        # Verifica recorrência em intervalos próximos aos sugeridos (9-10 ou 15-35)
        for interval in intervals:
            if (8 <= interval <= 11) or (14 <= interval <= 36):
                return True
        
        # Verifica se o último empate foi há muito tempo (mais de 15 jogos) e agora um novo empate ocorreu
        # Note: self.historico[0] é o mais recente. indices são em ordem crescente, então empates_indices[0] é o mais antigo no histórico exibido.
        # Queremos saber se o *intervalo* até o empate mais recente (que é historico[0] se for um E) foi grande.
        # Isso é mais bem abordado pelo calculo de `intervals` e a verificação do último intervalo.
        if len(intervals) > 0 and intervals[0] > 15: # Se o intervalo até o empate mais recente é grande
             return True # Pode indicar um reaparecimento
        
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
        
        # Encontra o resultado mais comum e sua contagem
        most_common_result, most_common_count = contador.most_common(1)[0]
        
        if most_common_count >= 4:
            return f"Forte tendência: {most_common_result}"
        elif most_common_count >= 3:
            return f"Tendência moderada: {most_common_result}"
        else:
            return "Sem tendência clara"

    def sugestao_inteligente(self):
        """Gera sugestão inteligente baseada em múltiplos fatores e pesos dos padrões"""
        # Só sugere a partir de 9 entradas
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
        
        # Calcula confiança baseada nos pesos dos padrões
        confianca_total = 0
        peso_total = 0
        
        for padrao in padroes_identificados:
            peso = self.pesos_padroes.get(padrao, 0.5) # Padrões não mapeados tem peso padrão de 0.5
            confianca_total += peso
            peso_total += peso
        
        confianca_media = (confianca_total / peso_total) * 100 if peso_total > 0 else 0
        
        # Ajusta confiança baseada na quantidade de padrões
        bonus_quantidade = min(20, len(padroes_identificados) * 3) # Bônus menor para não inflar muito
        confianca_final = min(99, int(confianca_media + bonus_quantidade)) # Limite superior
        
        # Análise de frequências e tendências
        frequencias = self.calcular_frequencias()
        tendencia = self.calcular_tendencia()
        
        opcoes = ["V", "C", "E"] # Ordem padrão
        
        # Lógica de sugestão aprimorada
        # 1. Padrões de Quebra/Inversão (prioridade alta)
        padroes_quebra = [p for p in padroes_identificados if "quebra" in p.lower() or "breakout" in p.lower()]
        if padroes_quebra:
            # Se um padrão de quebra é detectado, sugere o oposto do último resultado dominante
            ultimo_resultado = self.historico[0] if self.historico else None
            if ultimo_resultado:
                # Se o último foi empate, sugere o mais comum entre C e V
                if ultimo_resultado == 'E':
                    # Pega o mais frequente entre C e V no histórico geral, e sugere o oposto
                    freq_cv = {k: v for k, v in frequencias.items() if k != 'E'}
                    if freq_cv:
                        sugerido = min(freq_cv, key=freq_cv.get) # Sugere o menos frequente entre C/V
                    else:
                        sugerido = random.choice(['C', 'V'])
                else: # Se o último não foi empate, sugere o oposto direto
                    opcoes_opostas = [op for op in ['C', 'V'] if op != ultimo_resultado]
                    if opcoes_opostas:
                        sugerido = random.choice(opcoes_opostas)
                    else:
                        sugerido = random.choice(opcoes) # Fallback
            else:
                sugerido = random.choice(opcoes) # Fallback
        
        # 2. Padrões de Sequência/Dominância
        elif any(p for p in padroes_identificados if "sequência" in p.lower() or "dominância" in p.lower() or "onda" in p.lower() or "momentum" in p.lower() or "surf" in p.lower()):
            # Se há padrões de sequência, sugere continuar a sequência
            # Sugere o resultado mais frequente recentemente
            ultimos_resultados_para_tendencia = self.historico[:min(len(self.historico), 5)] # últimos 5
            if ultimos_resultados_para_tendencia:
                sugerido = collections.Counter(ultimos_resultados_para_tendencia).most_common(1)[0][0]
            else:
                sugerido = random.choice(opcoes)
        
        # 3. Padrões de Empate (se houver, e não houve quebra ou sequência forte)
        elif any(p for p in padroes_identificados if "empate" in p.lower()):
            sugerido = 'E' # Se detectou padrão de empate, sugere empate
        
        # 4. Nenhum dos acima (ou múltiplos padrões conflitantes): usa frequência geral do histórico
        else:
            # Sugere o que menos saiu (mais "devendo" estatisticamente)
            sugerido = min(opcoes, key=lambda x: frequencias.get(x, 0))

            # Se todas as frequências são iguais, ou muito próximas, usa momentum mais recente
            freq_values = list(frequencias.values())
            if len(set(freq_values)) == 1 or (max(freq_values) - min(freq_values) < 5): # Se a diferença é menor que 5%
                ultimos_3 = self.historico[:3]
                if ultimos_3:
                    contador_recente = collections.Counter(ultimos_3)
                    # Se há repetição recente, sugere mudança (para evitar sequências longas inesperadas)
                    if contador_recente.most_common(1)[0][1] >= 2 and len(set(ultimos_3)) < 3: # Se houve repetição e não é tudo diferente
                        resultado_frequente = contador_recente.most_common(1)[0][0]
                        opcoes_mudanca = [op for op in opcoes if op != resultado_frequente]
                        if opcoes_mudanca:
                            sugerido = random.choice(opcoes_mudanca)
                        else:
                            sugerido = random.choice(opcoes) # Fallback
                    else: # Se os últimos resultados são variados, aposta no menos frequente geral
                        sugerido = min(opcoes, key=lambda x: frequencias.get(x, 0))
                else:
                    sugerido = random.choice(opcoes) # Fallback

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
        """Gera análise detalhada dos padrões encontrados"""
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
        'historico_sugestoes': [] # Para registrar sugestões e resultados reais para auditoria
    }

def adicionar_resultado(resultado):
    """Adiciona novo resultado ao histórico e registra validação da sugestão anterior, se houver"""
    if 'ultima_sugestao' in st.session_state and st.session_state.ultima_sugestao['sugerir']:
        sugestao_anterior = st.session_state.ultima_sugestao
        # Valida a sugestão anterior com o resultado real agora inserido
        if sugestao_anterior['entrada_codigo'] == resultado:
            st.session_state.estatisticas['acertos'] += 1
            acertou = True
        else:
            st.session_state.estatisticas['erros'] += 1
            acertou = False
        
        # Adiciona ao histórico de sugestões para auditoria
        st.session_state.estatisticas['historico_sugestoes'].append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'sugerido': sugestao_anterior['entrada_codigo'],
            'real': resultado,
            'confianca': sugestao_anterior['confianca'],
            'acertou': acertou,
            'motivos': sugestao_anterior['motivos']
        })
        # Limpa a última sugestão após a validação
        del st.session_state.ultima_sugestao

    st.session_state.historico.insert(0, resultado) # Adiciona no início (mais recente)
    if len(st.session_state.historico) > 54: # Limita a 54 resultados (9 colunas x 6 linhas)
        st.session_state.historico = st.session_state.historico[:54]
    st.session_state.estatisticas['total_jogos'] += 1

def limpar_historico():
    """Limpa todo o histórico e estatísticas"""
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
    """Remove o último resultado e ajusta as estatísticas se aplicável"""
    if st.session_state.historico:
        # Se houve uma sugestão ativa antes do resultado que será desfeito, não ajustamos estatísticas
        # pois a sugestão não foi validada por este resultado específico.
        # A complexidade de desfazer a validação exigiria um controle mais granular das sugestões.
        # Por simplicidade, desfazer remove apenas o resultado do histórico principal.
        st.session_state.historico.pop(0)
        if st.session_state.estatisticas['total_jogos'] > 0:
            st.session_state.estatisticas['total_jogos'] -= 1
        
        # Se a última sugestão foi armazenada e não validada, ela é "perdida"
        # para evitar confusão nas estatísticas de acerto/erro.
        if 'ultima_sugestao' in st.session_state:
             del st.session_state.ultima_sugestao

def get_resultado_html(resultado):
    """Retorna HTML para visualização do resultado com cores e símbolos"""
    color_map = {'C': '#FF4B4B', 'V': '#4B4BFF', 'E': '#FFD700'} # Vermelho, Azul, Amarelo
    symbol_map = {'C': '🏠', 'V': '✈️', 'E': '⚖️'} # Símbolos simples, se quiser mais próximos dos da imagem (C e V em círculo)
                                               # Pode usar ícones de imagem ou CSS mais complexo
    
    # Para se parecer mais com a imagem, os símbolos podem ser substituídos por círculos vazios
    # e apenas a cor do background ser usada, ou um ponto central.
    
    # Exemplo para se parecer mais com a imagem, apenas a cor:
    return f"""
    <div style='
        display: flex;
        align-items: center;
        justify-content: center;
        width: 25px; /* Tamanho do círculo */
        height: 25px;
        border-radius: 50%; 
        background-color: {color_map.get(resultado, 'gray')}; 
        margin: 2px; /* Espaçamento entre os círculos */
        font-size: 14px;
        color: {"black" if resultado == "E" else "white"};
        border: 1px solid rgba(255,255,255,0.3); /* Borda sutil */
    '>
        {"E" if resultado == "E" else ""} </div>
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
div.stButton > button[data-testid*="stButton-CASA"] {
    background: linear-gradient(135deg, #FF6B6B, #FF4B4B); /* Vermelho */
}

div.stButton > button[data-testid*="stButton-EMPATE"] {
    background: linear-gradient(135deg, #FFE66D, #FFD700); /* Amarelo */
    color: black;
}

div.stButton > button[data-testid*="stButton-VISITANTE"] {
    background: linear-gradient(135deg, #4ECDC4, #4B4BFF); /* Azul */
}

div.stButton > button[data-testid*="stButton-Desfazer"],
div.stButton > button[data-testid*="stButton-Limpar"] {
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
    display: flex; /* Para roadmap */
    overflow-x: auto; /* Permite rolagem horizontal se muitas colunas */
    scroll-behavior: smooth;
    padding-bottom: 10px; /* Espaço para barra de rolagem */
}

.historic-column {
    display: flex;
    flex-direction: column; /* Resultados em coluna */
    align-items: center;
    margin: 0 2px; /* Espaçamento entre colunas */
}
.historic-column div {
    margin-bottom: 2px; /* Espaçamento entre itens na coluna */
}

/* Ajuste para o texto dentro dos botões de resultado */
.stButton > button[data-testid*="stButton-CASA"] div,
.stButton > button[data-testid*="stButton-EMPATE"] div,
.stButton > button[data-testid*="stButton-VISITANTE"] div {
    white-space: nowrap; /* Impede que o texto quebre em várias linhas */
    overflow: hidden;
    text-overflow: ellipsis;
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

# --- EXIBIÇÃO DO HISTÓRICO NO FORMATO ROADMAP ---
st.markdown('<div class="section-header"><h2>📈 Histórico de Resultados</h2></div>', unsafe_allow_html=True)

if not st.session_state.historico:
    st.info("🎮 Nenhum resultado registrado. Comece inserindo os resultados dos jogos!")
else:
    # Parâmetros para o roadmap
    NUM_LINHAS_ROADMAP = 6 # Fixado em 6 linhas como no placar
    MAX_COLUNAS_ROADMAP = 9 # Para um total de 54 resultados (9 colunas * 6 linhas)
    
    # Preparar os dados para exibição no formato de colunas
    # O histórico está em ordem inversa (mais recente no índice 0)
    # Precisamos preencher as colunas do mais novo para o mais antigo, de cima para baixo
    
    # Preenche um grid com None para os espaços vazios
    grid_resultados = [['' for _ in range(MAX_COLUNAS_ROADMAP)] for _ in range(NUM_LINHAS_ROADMAP)]
    
    col_idx = 0
    row_idx = 0
    
    # Percorre o histórico e preenche a grid, simulando o preenchimento do roadmap
    for i, res in enumerate(st.session_state.historico):
        if row_idx >= NUM_LINHAS_ROADMAP:
            # Se a coluna está cheia, move para a próxima coluna
            col_idx += 1
            row_idx = 0 # Reinicia a linha
            # Se chegamos ao fim das colunas visíveis, paramos
            if col_idx >= MAX_COLUNAS_ROADMAP:
                break
        
        grid_resultados[row_idx][col_idx] = res
        row_idx += 1
    
    # Inverte as colunas para que as mais recentes fiquem à esquerda na exibição
    # A imagem mostra os resultados mais recentes nas colunas da esquerda,
    # e os mais antigos nas colunas da direita, com as colunas sendo preenchidas de cima para baixo.
    # Nossa lógica preenche da esquerda para a direita, de cima para baixo,
    # então precisamos inverter as colunas para a exibição.
    
    # Se você quiser que o placar "empurre" da direita para a esquerda:
    # A maneira mais fácil de simular é criar as colunas da direita para a esquerda
    # no HTML, ou renderizar o grid invertido.
    
    # Para o formato da imagem (mais recente à esquerda, preenchido de cima para baixo)
    # A lista `st.session_state.historico` já está do mais recente (índice 0) para o mais antigo.
    # O preenchimento da grid deve simular a rolagem para a esquerda.
    
    # Crio um container flex para as colunas
    st.markdown('<div class="historic-container">', unsafe_allow_html=True)
    
    # As colunas mais recentes ficam à esquerda.
    # Itero de MAX_COLUNAS_ROADMAP - 1 até 0 para exibir da direita para a esquerda,
    # mas os resultados são do mais recente (índice 0) para o mais antigo.
    # Isso significa que a primeira coluna exibida (mais à esquerda) deve conter
    # os resultados mais recentes.
    
    # Vamos re-pensar o preenchimento para ser mais direto com o visual:
    # Imagine o histórico como uma fila. O item 0 é o mais recente.
    # A primeira coluna (mais à esquerda) do roadmap deve conter os itens 0, 1, 2, 3, 4, 5.
    # A segunda coluna deve conter 6, 7, 8, 9, 10, 11, e assim por diante.
    
    roadmap_columns = [[] for _ in range(MAX_COLUNAS_ROADMAP)]
    
    for i, res in enumerate(st.session_state.historico):
        col = i // NUM_LINHAS_ROADMAP # Qual coluna este resultado pertence
        row = i % NUM_LINHAS_ROADMAP # Qual linha dentro da coluna
        
        if col < MAX_COLUNAS_ROADMAP: # Garante que não excede o número de colunas
            roadmap_columns[col].append(res)
    
    # Renderiza as colunas da esquerda para a direita (mais recentes para os mais antigos visíveis)
    for col_data in roadmap_columns:
        if not col_data: # Não renderiza colunas vazias
            continue
        
        st.markdown('<div class="historic-column">', unsafe_allow_html=True)
        for res in col_data:
            st.markdown(get_resultado_html(res), unsafe_allow_html=True)
        # Preenche os espaços vazios na coluna se ela não estiver cheia (6 resultados)
        for _ in range(NUM_LINHAS_ROADMAP - len(col_data)):
            st.markdown(get_resultado_html(''), unsafe_allow_html=True) # Renderiza um círculo vazio
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # Fecha historic-container
    
    st.markdown(f"**Total:** {len(st.session_state.historico)} jogos (máx. 54)", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ANÁLISE PRINCIPAL ---
st.markdown('<div class="section-header"><h2>🧠 Análise e Sugestão</h2></div>', unsafe_allow_html=True)

if len(st.session_state.historico) >= 9: # Começa a sugerir a partir de 9 entradas
    analyzer = AnalisePadroes(st.session_state.historico)
    sugestao = analyzer.sugestao_inteligente()
    
    # Armazena a última sugestão para validação futura
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
        
        # Detalhes da análise
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
    
    # --- ANÁLISE DE PADRÕES (DETALHADA) ---
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
                for padrao in nao_encontrados[:15]: # Limita a exibição para não sobrecarregar
                    st.markdown(f'<div class="pattern-not-found">❌ {padrao}</div>', unsafe_allow_html=True)
                if len(nao_encontrados) > 15:
                    st.write(f"E mais {len(nao_encontrados) - 15} padrões inativos...")
            else:
                st.info("Todos os padrões estão ativos (improvável).")
        
    # --- ANÁLISE ESTATÍSTICA GERAL ---
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
        # Mapeamento de cores para o gráfico
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

# --- RODAPÉ ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; margin-top: 2rem;">
    <p>⚽ Football Studio Live Analyzer v2.2 | Análise Inteligente de Padrões</p>
    <p><small>Desenvolvido para Evolution Gaming Football Studio</small></p>
</div>
""", unsafe_allow_html=True)
