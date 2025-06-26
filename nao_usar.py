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
        # Inverte a ordem para que o resultado mais recente esteja na posição 0
        self.historico = list(reversed(historico))[:54] 
        
        # Mapeamento de nomes de padrões para seus métodos correspondentes
        self.padroes_ativos = {
            "Sequência (Surf de Cor)": self._sequencia_simples, # Detecta 3+ sequências simples
            "Zig-Zag Perfeito": self._zig_zag,
            "Quebra de Surf": self._quebra_de_surf,
            "Quebra de Zig-Zag": self._quebra_de_zig_zag,
            "Duplas Repetidas": self._duplas_repetidas,
            "Empate Recorrente": self._empate_recorrente,
            "Padrão Escada": self._padrao_escada,
            "Espelho": self._espelho, # Mantido como lógica de palíndromo
            "Alternância com Empate": self._alternancia_empate_meio,
            "Padrão Onda": self._padrao_onda, # Zig-zag de 5
            "Padrão Fibonacci": self._padrao_fibonacci,
            "Sequência Dourada": self._sequencia_dourada, # 3X, 1Y, 1X
            "Padrão Triangular": self._padrao_triangular,
            "Ciclo de Empates": self._ciclo_empates,
            "Fibonacci Invertida": self._fibonacci_invertida,
            "Alternância Dupla": self._alternancia_dupla,
            "Momento Explosivo": self._momento_explosivo,
        }
        
        # Pesos dos padrões (você pode ajustar estes valores)
        self.pesos_padroes = {
            "Sequência (Surf de Cor)": 0.9, # Era 0.9
            "Zig-Zag Perfeito": 0.8,
            "Quebra de Surf": 0.92,
            "Quebra de Zig-Zag": 0.9,
            "Duplas Repetidas": 0.75,
            "Empate Recorrente": 0.85,
            "Padrão Escada": 0.88,
            "Espelho": 0.8,
            "Alternância com Empate": 0.7,
            "Padrão Onda": 0.85,
            "Padrão Fibonacci": 0.95,
            "Sequência Dourada": 0.9, # Era 0.9
            "Padrão Triangular": 0.82,
            "Ciclo de Empates": 0.78,
            "Fibonacci Invertida": 0.93,
            "Alternância Dupla": 0.8,
            "Momento Explosivo": 0.87,
        }

    def analisar(self):
        # Retorna um dicionário de padrões detectados e suas confianças
        padroes_detectados = {}
        for nome_padrao, metodo_padrao in self.padroes_ativos.items():
            ocorrencias = metodo_padrao()
            if ocorrencias:
                # Cada padrão pode retornar múltiplas ocorrências
                padroes_detectados[nome_padrao] = {
                    "ocorrencias": ocorrencias,
                    "peso": self.pesos_padroes.get(nome_padrao, 0)
                }
        return padroes_detectados

    # --- MÉTODOS DE DETECÇÃO DE PADRÕES ---

    def _sequencia_simples(self):
        # Detecta 3 ou mais resultados iguais (C,C,C ou V,V,V)
        padroes = []
        for i in range(len(self.historico) - 2):
            if (self.historico[i] != 'E' and # Ignora sequências de empates para este padrão
                self.historico[i] == self.historico[i+1] == self.historico[i+2]):
                
                # Detecta o comprimento da sequência
                current_len = 3
                while (i + current_len < len(self.historico) and 
                       self.historico[i + current_len] == self.historico[i]):
                    current_len += 1
                
                padroes.append({
                    "nome": "Sequência (Surf de Cor)",
                    "segmento": self.historico[i : i + current_len],
                    "posicao_final": i + current_len - 1,
                    "comprimento": current_len
                })
        return padroes

    def _zig_zag(self):
        # Detecta uma alternância perfeita de C e V (min_len_zigzag de 6 alternâncias)
        padroes = []
        min_len_zigzag = 6 # Mínimo de 6 alternâncias (ex: C,V,C,V,C,V)
        for i in range(len(self.historico) - min_len_zigzag + 1):
            segment = self.historico[i : i + min_len_zigzag]
            is_zig_zag = True
            if 'E' in segment: # Zig-zag perfeito não pode ter empates
                is_zig_zag = False
            else:
                for j in range(min_len_zigzag - 1):
                    if segment[j] == segment[j+1]:
                        is_zig_zag = False
                        break
            if is_zig_zag:
                padroes.append({
                    "nome": "Zig-Zag Perfeito",
                    "segmento": segment,
                    "posicao_final": i + min_len_zigzag - 1
                })
        return padroes

    def _quebra_de_surf(self):
        # Padrão: 3+ da mesma cor, seguido por 2 da cor oposta. Ex: C,C,C,V,V
        padroes = []
        for i in range(len(self.historico) - 4): # Pelo menos 5 posições (3+2)
            cor_base = self.historico[i]
            
            if cor_base == 'E': continue # Ignora se a base é empate

            # Verifica sequência de 3+ da cor base
            if (self.historico[i+1] == cor_base and self.historico[i+2] == cor_base):
                # Detecta o comprimento da sequência inicial
                len_seq_base = 3
                while (i + len_seq_base < len(self.historico) and 
                       self.historico[i + len_seq_base] == cor_base):
                    len_seq_base += 1
                
                # A quebra começa após a sequência base
                if (i + len_seq_base + 1 < len(self.historico)): # Precisa de pelo menos 2 para a quebra
                    cor_oposta = 'C' if cor_base == 'V' else 'V'
                    
                    if (self.historico[i + len_seq_base] == cor_oposta and 
                        self.historico[i + len_seq_base + 1] == cor_oposta):
                        
                        padroes.append({
                            "nome": "Quebra de Surf",
                            "segmento": self.historico[i : i + len_seq_base + 2],
                            "posicao_final": i + len_seq_base + 1
                        })
        return padroes

    def _quebra_de_zig_zag(self):
        # Padrão: Alternância de 4 (X,Y,X,Y), seguida por uma quebra (Y ou E). Ex: C,V,C,V,V ou C,V,C,V,E
        padroes = []
        min_len_zigzag_base = 4 # Ex: C,V,C,V

        for i in range(len(self.historico) - (min_len_zigzag_base + 1)): # +1 para a quebra
            segmento_base = self.historico[i : i + min_len_zigzag_base]
            
            is_zigzag_base = True
            if 'E' in segmento_base: # Zig-zag base não pode ter empates
                is_zigzag_base = False
            else:
                for j in range(min_len_zigzag_base - 1):
                    if segmento_base[j] == segmento_base[j+1]:
                        is_zigzag_base = False
                        break
            
            if is_zigzag_base:
                cor_esperada_zigzag = segmento_base[min_len_zigzag_base - 2] # Ex: C,V,C,V -> espera C
                cor_da_quebra = self.historico[i + min_len_zigzag_base]
                
                # A quebra ocorre se a próxima cor não é a esperada para continuar o zig-zag
                # ou se é um empate.
                if (cor_da_quebra == 'E' or cor_da_quebra != cor_esperada_zigzag):
                    padroes.append({
                        "nome": "Quebra de Zig-Zag",
                        "segmento": self.historico[i : i + min_len_zigzag_base + 1],
                        "posicao_final": i + min_len_zigzag_base
                    })
        return padroes


    def _duplas_repetidas(self):
        # Padrão: X,X,Y,Y (Ex: C,C,V,V)
        padroes = []
        for i in range(len(self.historico) - 3):
            if (self.historico[i] != 'E' and self.historico[i+1] != 'E' and
                self.historico[i] == self.historico[i+1] and
                self.historico[i+2] == self.historico[i+3] and
                self.historico[i] != self.historico[i+2]):
                padroes.append({
                    "nome": "Duplas Repetidas",
                    "segmento": self.historico[i:i+4],
                    "posicao_final": i+3
                })
        return padroes

    def _empate_recorrente(self):
        # Padrão: E, X, E ou E, X, Y, E ou E, X, Y, Z, E
        padroes = []
        for i in range(len(self.historico) - 4): # Max de 4 espaços entre empates
            if self.historico[i] == 'E':
                # E _ E (intervalo de 1)
                if self.historico[i+2] == 'E':
                    padroes.append({
                        "nome": "Empate Recorrente",
                        "segmento": self.historico[i:i+3],
                        "posicao_final": i+2
                    })
                # E _ _ E (intervalo de 2)
                if i + 3 < len(self.historico) and self.historico[i+3] == 'E':
                    padroes.append({
                        "nome": "Empate Recorrente",
                        "segmento": self.historico[i:i+4],
                        "posicao_final": i+3
                    })
                # E _ _ _ E (intervalo de 3)
                if i + 4 < len(self.historico) and self.historico[i+4] == 'E':
                    padroes.append({
                        "nome": "Empate Recorrente",
                        "segmento": self.historico[i:i+5],
                        "posicao_final": i+4
                    })
        return padroes

    def _padrao_escada(self):
        # Padrão: X,X,Y,Y,Y,X,X,X,X (2,3,4)
        padroes = []
        for i in range(len(self.historico) - 8): # Necessita de 9 posições
            s = self.historico[i:i+9]
            if (s[0] != 'E' and s[1] != 'E' and s[2] != 'E' and s[3] != 'E' and
                s[4] != 'E' and s[5] != 'E' and s[6] != 'E' and s[7] != 'E' and s[8] != 'E' and
                s[0] == s[1] and s[0] != s[2] and
                s[2] == s[3] == s[4] and s[2] != s[5] and
                s[5] == s[6] == s[7] == s[8]):
                padroes.append({
                    "nome": "Padrão Escada",
                    "segmento": s,
                    "posicao_final": i+8
                })
        return padroes

    def _espelho(self):
        # Padrão: Palíndromo (ABCBA, ABBA, ABA)
        padroes = []
        for i in range(len(self.historico) - 4): # Para ABCBA
            s = self.historico[i:i+5]
            if s[0] == s[4] and s[1] == s[3]:
                padroes.append({"nome": "Espelho", "segmento": s, "posicao_final": i+4})
        for i in range(len(self.historico) - 3): # Para ABBA
            s = self.historico[i:i+4]
            if s[0] == s[3] and s[1] == s[2]:
                padroes.append({"nome": "Espelho", "segmento": s, "posicao_final": i+3})
        for i in range(len(self.historico) - 2): # Para ABA
            s = self.historico[i:i+3]
            if s[0] == s[2]:
                padroes.append({"nome": "Espelho", "segmento": s, "posicao_final": i+2})
        return padroes

    def _alternancia_empate_meio(self):
        # Padrão: X,E,Y,E,X,E,Y
        padroes = []
        for i in range(len(self.historico) - 6): # Necessita de 7 posições
            s = self.historico[i:i+7]
            if (s[1] == 'E' and s[3] == 'E' and s[5] == 'E' and
                s[0] != 'E' and s[2] != 'E' and s[4] != 'E' and s[6] != 'E' and # Cores não são E
                s[0] == s[4] and s[2] == s[6] and s[0] != s[2]): # Alternância C/V
                padroes.append({
                    "nome": "Alternância com Empate",
                    "segmento": s,
                    "posicao_final": i+6
                })
        return padroes

    def _padrao_onda(self):
        # Padrão: C,V,C,V,C (Zig-zag de 5)
        padroes = []
        for i in range(len(self.historico) - 4): # Necessita de 5 posições
            segment = self.historico[i:i+5]
            is_onda = True
            if 'E' in segment: # Padrão onda não pode ter empates
                is_onda = False
            else:
                for j in range(len(segment) - 1):
                    if segment[j] == segment[j+1]:
                        is_onda = False
                        break
            if is_onda:
                padroes.append({
                    "nome": "Padrão Onda",
                    "segmento": segment,
                    "posicao_final": i+4
                })
        return padroes

    def _padrao_fibonacci(self):
        # Padrão: Sequências de 1,1,2,3,5 (ignora empates)
        padroes = []
        # Para evitar IndexError, garantir que haja histórico suficiente antes de acessar índices
        if len(self.historico) < 12: # Mínimo de 1+1+2+3+5 = 12 resultados C/V
            return padroes

        for i in range(len(self.historico)):
            # Crie um segmento de C/V a partir da posição 'i'
            segmento_c_v = [res for res in self.historico[i:] if res != 'E']
            
            if len(segmento_c_v) < 12: # Não há resultados C/V suficientes para o padrão a partir daqui
                continue

            # Tenta encontrar a sequência 1,1,2,3,5
            # Posições no segmento_c_v:
            # 0: cor1 (len 1)
            # 1: cor2 (len 1)
            # 2,3: cor3 (len 2)
            # 4,5,6: cor4 (len 3)
            # 7,8,9,10,11: cor5 (len 5)

            # Primeiro 1
            cor1 = segmento_c_v[0]
            
            # Segundo 1 (deve ser diferente do primeiro)
            if cor1 == segmento_c_v[1]: continue
            cor2 = segmento_c_v[1]

            # Terceiro 2 (deve ser diferente do segundo, e os dois próximos iguais a ele)
            if cor2 == segmento_c_v[2] or segmento_c_v[2] != segmento_c_v[3]: continue
            cor3 = segmento_c_v[2]

            # Quarto 3 (deve ser diferente do terceiro, e os três próximos iguais a ele)
            if cor3 == segmento_c_v[4] or not (segmento_c_v[4] == segmento_c_v[5] == segmento_c_v[6]): continue
            cor4 = segmento_c_v[4]

            # Quinto 5 (deve ser diferente do quarto, e os cinco próximos iguais a ele)
            if cor4 == segmento_c_v[7] or not (segmento_c_v[7] == segmento_c_v[8] == segmento_c_v[9] == segmento_c_v[10] == segmento_c_v[11]): continue
            cor5 = segmento_c_v[7]

            # Se chegamos até aqui, o padrão foi detectado
            # Encontra o índice final no histórico original para o segmento
            current_idx_in_original_history = i
            count_c_v_found = 0
            required_len_cv = sum([1,1,2,3,5]) # Total de resultados C/V no padrão Fibonacci
            
            # Percorre o histórico original para encontrar a posição final exata do padrão
            for k in range(i, len(self.historico)):
                if self.historico[k] != 'E':
                    count_c_v_found += 1
                if count_c_v_found == required_len_cv:
                    posicao_final = k
                    break
            else: # Caso o loop não encontre, algo deu errado (deveria ter encontrado)
                continue

            padroes.append({
                "nome": "Padrão Fibonacci",
                "segmento": self.historico[i : posicao_final + 1],
                "posicao_final": posicao_final
            })
        return padroes


    def _sequencia_dourada(self):
        # Padrão: X,X,X,Y,X (3 de um, 1 do outro, 1 do primeiro)
        padroes = []
        for i in range(len(self.historico) - 4): # Necessita de 5 posições
            s = self.historico[i:i+5]
            if (s[0] != 'E' and s[1] != 'E' and s[2] != 'E' and s[3] != 'E' and s[4] != 'E' and
                s[0] == s[1] == s[2] and # Primeiros 3 são iguais
                s[0] != s[3] and         # O quarto é diferente
                s[3] != s[4] and s[4] == s[0]): # O quinto é igual ao primeiro
                padroes.append({
                    "nome": "Sequência Dourada",
                    "segmento": s,
                    "posicao_final": i+4
                })
        return padroes

    def _padrao_triangular(self):
        # Padrão: X,Y,Y,X,X,X (1,2,3)
        padroes = []
        for i in range(len(self.historico) - 5): # Necessita de 6 posições
            s = self.historico[i:i+6]
            if (s[0] != 'E' and s[1] != 'E' and s[2] != 'E' and s[3] != 'E' and s[4] != 'E' and s[5] != 'E' and
                s[0] != s[1] and # Primeiro diferente do segundo
                s[1] == s[2] and # Segundo e terceiro iguais
                s[2] != s[3] and # Terceiro diferente do quarto
                s[3] == s[4] == s[5]): # Quarto, quinto e sexto iguais
                padroes.append({
                    "nome": "Padrão Triangular",
                    "segmento": s,
                    "posicao_final": i+5
                })
        return padroes

    def _ciclo_empates(self):
        # Padrão: E,E,X,Y,E,E (Dois empates, duas cores, dois empates)
        padroes = []
        for i in range(len(self.historico) - 5): # Necessita de 6 posições
            s = self.historico[i:i+6]
            if (s[0] == 'E' and s[1] == 'E' and # Dois empates
                s[2] != 'E' and s[3] != 'E' and s[2] != s[3] and # Duas cores diferentes (não empates)
                s[4] == 'E' and s[5] == 'E'): # Mais dois empates
                padroes.append({
                    "nome": "Ciclo de Empates",
                    "segmento": s,
                    "posicao_final": i+5
                })
        return padroes

    def _fibonacci_invertida(self):
        # Padrão: 4 de uma cor, 2 da cor oposta, 1 da primeira cor. Ex: C,C,C,C,V,V,C
        padroes = []
        for i in range(len(self.historico) - 6): # Necessita de 7 posições
            cor_4_base = self.historico[i]
            if cor_4_base == 'E': continue

            if (self.historico[i] == self.historico[i+1] == self.historico[i+2] == self.historico[i+3]):
                cor_2_oposta = 'C' if cor_4_base == 'V' else 'V'
                if (self.historico[i+4] == cor_2_oposta and self.historico[i+5] == cor_2_oposta):
                    if self.historico[i+6] == cor_4_base:
                        padroes.append({
                            "nome": "Fibonacci Invertida",
                            "segmento": self.historico[i:i+7],
                            "posicao_final": i+6
                        })
        return padroes

    def _alternancia_dupla(self):
        # Padrão: X,X,Y,Y,X,X,Y,Y
        padroes = []
        for i in range(len(self.historico) - 7): # Necessita de 8 posições
            s = self.historico[i:i+8]
            if (s[0] != 'E' and s[1] != 'E' and s[2] != 'E' and s[3] != 'E' and
                s[4] != 'E' and s[5] != 'E' and s[6] != 'E' and s[7] != 'E' and
                s[0] == s[1] and s[2] == s[3] and s[4] == s[5] and s[6] == s[7] and # São duplas
                s[0] != s[2] and s[2] != s[4] and s[4] != s[6]): # E as duplas alternam cores
                padroes.append({
                    "nome": "Alternância Dupla",
                    "segmento": s,
                    "posicao_final": i+7
                })
        return padroes

    def _momento_explosivo(self):
        # Padrão: Sequência de X, seguida por uma sequência MAIOR de Y. Ex: C,C,V,V,V,V
        padroes = []
        min_len_explosao_inicial = 2 # Mínimo de 2 da primeira cor
        min_len_explosao_final = 3    # Mínimo de 3 da segunda cor (maior que a primeira)

        for i in range(len(self.historico) - (min_len_explosao_inicial + min_len_explosao_final)):
            cor1 = self.historico[i]
            if cor1 == 'E': continue

            # Detecta o comprimento da primeira sequência
            len1 = 0
            while (i + len1 < len(self.historico) and 
                   self.historico[i + len1] == cor1):
                len1 += 1
            
            if len1 >= min_len_explosao_inicial:
                # Onde a segunda sequência começaria
                start_seq2 = i + len1
                
                if start_seq2 < len(self.historico):
                    cor2 = self.historico[start_seq2]
                    if cor2 == 'E' or cor2 == cor1: # Segunda cor não pode ser empate ou igual à primeira
                        continue

                    # Detecta o comprimento da segunda sequência
                    len2 = 0
                    while (start_seq2 + len2 < len(self.historico) and 
                           self.historico[start_seq2 + len2] == cor2):
                        len2 += 1
                    
                    # A segunda sequência deve ser maior que a primeira e ter pelo menos min_len_explosao_final
                    if len2 > len1 and len2 >= min_len_explosao_final:
                        padroes.append({
                            "nome": "Momento Explosivo",
                            "segmento": self.historico[i : start_seq2 + len2],
                            "posicao_final": start_seq2 + len2 - 1
                        })
        return padroes
        
    def _calcular_frequencias(self, historico_parcial=None):
        # Calcula a frequência de C, V, E em um histórico parcial ou total
        hist = historico_parcial if historico_parcial is not None else self.historico
        frequencias = collections.Counter(hist)
        return {
            'C': frequencias['C'],
            'V': frequencias['V'],
            'E': frequencias['E']
        }

    def _obter_sugestao_com_frequencia(self, frequencias):
        # Sugere o resultado menos frequente ou o oposto do último se a frequência é parecida
        total = sum(frequencias.values())
        if total == 0:
            return 'C' # Default se não há histórico

        # Obter as frequências em porcentagem
        freq_c_pct = (frequencias['C'] / total) * 100
        freq_v_pct = (frequencias['V'] / total) * 100
        freq_e_pct = (frequencias['E'] / total) * 100

        # Encontrar o resultado com menor frequência (ignorando 'E' se há C/V)
        # Se só tem 'E' no histórico, prioriza 'E'
        if frequencias['C'] == 0 and frequencias['V'] == 0 and frequencias['E'] > 0:
            return 'E'
        
        # Considera apenas C e V para a menor frequência se houver ambos
        temp_freq = {k: v for k, v in frequencias.items() if k != 'E'}
        if not temp_freq: # Se só tem 'E' no histórico
            return 'C' # Ou random, ou outra heurística para o caso de só ter E
        
        menor_freq_val = min(temp_freq.values())
        resultados_menor_freq = [k for k, v in temp_freq.items() if v == menor_freq_val]

        if len(resultados_menor_freq) == 1:
            return resultados_menor_freq[0]
        else:
            # Se houver empate na menor frequência entre C e V, sugere o oposto do último C/V
            if self.historico:
                for res in self.historico:
                    if res != 'E':
                        return 'C' if res == 'V' else 'V'
            return random.choice(['C', 'V']) # Fallback seguro

    def sugestao_inteligente(self):
        padroes_detectados = self.analisar()
        
        confianca_final = 0
        sugestao = None
        motivos = []
        
        # Obter as frequências gerais para uso no fallback
        frequencias_gerais = self._calcular_frequencias()

        # Priorização dos padrões para sugestão
        # Prioridade 1: Quebra de Padrão (sugerir o oposto do que estava acontecendo)
        padroes_quebra = ["Quebra de Surf", "Quebra de Zig-Zag"]
        for nome_padrao in padroes_quebra:
            if nome_padrao in padroes_detectados:
                confianca_final += padroes_detectados[nome_padrao]["peso"] * len(padroes_detectados[nome_padrao]["ocorrencias"])
                motivos.append(f"Padrão de Quebra: {nome_padrao}")
                
                # Lógica de sugestão para quebra:
                # Se o último resultado não foi 'E', sugere o oposto dele.
                # Se o último foi 'E', sugere o menos frequente entre C e V.
                if self.historico and self.historico[0] != 'E':
                    sugestao = 'C' if self.historico[0] == 'V' else 'V'
                else:
                    # Se o último é 'E', olha para os últimos resultados não E para decidir
                    ultimos_nao_e = [r for r in self.historico if r != 'E']
                    if ultimos_nao_e:
                        sugestao = 'C' if ultimos_nao_e[0] == 'V' else 'V'
                    else: # Se só tem E no histórico recente
                        sugestao = self._obter_sugestao_com_frequencia(frequencias_gerais) # Fallback
                break # Uma quebra é forte, então se detectada, prioriza

        # Prioridade 2: Padrões de Sequência, Dominância, Onda, Momento, Surf
        padroes_sequencia_dominancia = [
            "Sequência (Surf de Cor)", "Padrão Escada", "Padrão Onda", 
            "Padrão Fibonacci", "Sequência Dourada", "Padrão Triangular",
            "Alternância Dupla", "Momento Explosivo", "Fibonacci Invertida"
        ]
        if sugestao is None: # Só entra se nenhuma quebra foi detectada
            for nome_padrao in padroes_sequencia_dominancia:
                if nome_padrao in padroes_detectados:
                    confianca_final += padroes_detectados[nome_padrao]["peso"] * len(padroes_detectados[nome_padrao]["ocorrencias"])
                    motivos.append(f"Padrão de Sequência/Dominância: {nome_padrao}")
                    
                    # Lógica de sugestão para sequência:
                    # Sugere o resultado mais comum nos últimos 5 (ou menos se não houver 5)
                    ultimos_5 = [res for res in self.historico[:min(len(self.historico), 5)] if res != 'E']
                    frequencias_5 = collections.Counter(ultimos_5)
                    
                    freq_c = frequencias_5['C']
                    freq_v = frequencias_5['V']
                    
                    if freq_c > freq_v:
                        sugestao = 'C'
                    elif freq_v > freq_c:
                        sugestao = 'V'
                    else: # Se empate entre C e V nos últimos 5, volta para a sugestão de frequência geral
                        sugestao = self._obter_sugestao_com_frequencia(frequencias_gerais)
                    break # Se uma sequência é detectada, prioriza

        # Prioridade 3: Padrões de Empate (se não houver sugestão de quebra ou sequência/dominância)
        padroes_empate = ["Empate Recorrente", "Alternância com Empate", "Ciclo de Empates"]
        if sugestao is None:
            for nome_padrao in padroes_empate:
                if nome_padrao in padroes_detectados:
                    confianca_final += padroes_detectados[nome_padrao]["peso"] * len(padroes_detectados[nome_padrao]["ocorrencias"])
                    motivos.append(f"Padrão de Empate: {nome_padrao}")
                    # Lógica de sugestão para empate: se o último não foi E, sugere E. Se foi E, sugere C (como quebra).
                    if self.historico and self.historico[0] != 'E':
                        sugestao = 'E'
                    else:
                        sugestao = 'C' # Tenta quebrar o empate
                    break

        # Prioridade 4: Zig-Zag Perfeito (pode ser uma categoria separada por sua natureza)
        if sugestao is None and "Zig-Zag Perfeito" in padroes_detectados:
            confianca_final += padroes_detectados["Zig-Zag Perfeito"]["peso"] * len(padroes_detectados["Zig-Zag Perfeito"]["ocorrencias"])
            motivos.append("Padrão: Zig-Zag Perfeito")
            # Para zig-zag, sugere a próxima cor na alternância
            if self.historico and self.historico[0] != 'E':
                sugestao = 'C' if self.historico[0] == 'V' else 'V'
            else:
                sugestao = self._obter_sugestao_com_frequencia(frequencias_gerais) # Fallback

        # Prioridade 5: Espelho (se não houver sugestão anterior)
        if sugestao is None and "Espelho" in padroes_detectados:
            confianca_final += padroes_detectados["Espelho"]["peso"] * len(padroes_detectados["Espelho"]["ocorrencias"])
            motivos.append("Padrão: Espelho")
            # Lógica para espelho: geralmente sugere a continuação do espelho
            # Ex: C,V,C -> Sugere V.  C,V,C,V,C -> Sugere V
            if self.historico and len(self.historico) >= 2 and self.historico[0] != 'E' and self.historico[1] != 'E':
                # Se os últimos dois são diferentes, sugere o que for igual ao penúltimo
                if self.historico[0] != self.historico[1]:
                    sugestao = self.historico[1] 
                else: # Se os últimos dois são iguais, sugere o oposto
                    sugestao = 'C' if self.historico[0] == 'V' else 'V'
            else:
                sugestao = self._obter_sugestao_com_frequencia(frequencias_gerais) # Fallback

        # Fallback: Se nenhuma lógica de padrão foi ativada
        if sugestao is None:
            motivos.append("Sugestão baseada em Frequência/Mudança")
            sugestao = self._obter_sugestao_com_frequencia(frequencias_gerais)
            # Para o fallback, a confiança é menor, ou baseada na "intensidade" da menor frequência
            menor_freq_val = min(frequencias_gerais.values())
            total = sum(frequencias_gerais.values())
            if total > 0:
                # Atribui uma confiança base menor para o fallback
                confianca_final = (menor_freq_val / total) * 50 # Max 50% para fallback

        # Bônus por quantidade de padrões detectados (exceto se a confiança já for alta)
        if len(padroes_detectados) > 0:
            # Calcular o bônus de forma mais controlada, para não estourar 100% facilmente
            # Cada padrão extra (além do primeiro) adiciona um pequeno bônus
            bonus_por_padrao = 0.05 # 5% de bônus por cada padrão extra, ou um valor fixo por tipo de padrão
            
            # Sumariza os pesos dos padrões detectados para a confiança base
            soma_pesos = sum(info["peso"] for info in padroes_detectados.values())
            confianca_final = (confianca_final + (soma_pesos * 100)) / (len(padroes_detectados) + 1 if len(padroes_detectados) > 0 else 1)
            
            # Adiciona um bônus adicional se múltiplos padrões são detectados
            if len(padroes_detectados) > 1:
                confianca_final += (len(padroes_detectados) - 1) * bonus_por_padrao * 100
        
        # Garante que a confiança não exceda 100%
        confianca_final = min(100, max(0, confianca_final)) # Garante que esteja entre 0 e 100
            
        # Filtra motivos únicos e inverte a ordem para exibir os mais recentes/relevantes primeiro
        motivos = list(dict.fromkeys(motivos)) # Remove duplicatas mantendo a ordem
        
        return {
            "sugestao": sugestao,
            "confianca": round(confianca_final, 2),
            "motivos": motivos
        }

# --- INÍCIO DO CÓDIGO STREAMLIT ---

st.set_page_config(layout="wide", page_title="Analisador de Padrões de Jogo")

# Inicialização do estado da sessão
if 'historico_resultados' not in st.session_state:
    st.session_state.historico_resultados = []
if 'estatisticas' not in st.session_state:
    st.session_state.estatisticas = {
        'total_sugestoes': 0,
        'acertos': 0,
        'erros': 0,
        'historico_sugestoes': []
    }
if 'ultima_sugestao' not in st.session_state:
    st.session_state.ultima_sugestao = None

# --- CSS Personalizado ---
st.markdown("""
    <style>
    /* Estilos para o cabeçalho */
    h1 {
        color: #4CAF50; /* Verde */
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 0.5em;
    }
    h2 {
        color: #2196F3; /* Azul */
        font-size: 1.8em;
        border-bottom: 2px solid #ddd;
        padding-bottom: 0.3em;
        margin-top: 1.5em;
    }
    h3 {
        color: #FF9800; /* Laranja */
        font-size: 1.4em;
        margin-top: 1em;
    }

    /* Estilos para os botões de resultado */
    .stButton>button {
        width: 100%;
        padding: 10px 0;
        font-size: 1.2em;
        font-weight: bold;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        opacity: 0.9;
    }

    /* Cores específicas para os botões de resultado */
    /* Botão 'C' (Casa) */
    /* Ajustado seletor para evitar conflito com outros botões 'primary' */
    .stButton button[key="add_C"] {
        background-color: #FF4B4B; /* Vermelho */
    }
    /* Botão 'V' (Visitante) */
    .stButton button[key="add_V"] {
        background-color: #4B4BFF; /* Azul */
    }
    /* Botão 'E' (Empate) */
    .stButton button[key="add_E"] {
        background-color: #FFD700; /* Amarelo ouro */
        color: #333; /* Texto escuro para contraste */
    }
    /* Botões de validação (Real) */
    .stButton button[key^="valid_"] {
        background-color: #607D8B; /* Cinza para validação */
        color: white;
    }
    .stButton button[key="clear_history"] {
        background-color: #f44336; /* Vermelho mais suave para limpar */
        color: white;
    }
    
    /* Estilos para cards de informação/sugestão */
    div[data-testid="stAlert"] { /* Seletor geral para alertas do Streamlit */
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
    }
    div[data-testid="stAlert"].stAlert-info {
        background-color: #e3f2fd; /* Azul claro */
        color: #1976d2; /* Azul escuro */
        border-left: 5px solid #2196F3;
    }
    div[data-testid="stAlert"].stAlert-success {
        background-color: #e8f5e9; /* Verde claro */
        color: #2e7d32; /* Verde escuro */
        border-left: 5px solid #4CAF50;
    }
    div[data-testid="stAlert"].stAlert-warning {
        background-color: #fffde7; /* Amarelo claro */
        color: #fbc02d; /* Amarelo escuro */
        border-left: 5px solid #FFC107;
    }
    
    /* Estilos para o container de histórico (se você usar st.container) */
    .stContainer {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
        background-color: #f9f9f9;
    }

    /* Melhorar visualização do dataframe */
    .dataframe {
        font-size: 0.85em;
    }
    
    /* Estilos para as bolhas de resultado */
    .historico-container {
        display: flex;
        flex-wrap: wrap;
        gap: 5px; /* Espaço entre as bolhas */
        margin-top: 10px;
        padding: 10px;
        border: 1px solid #eee;
        border-radius: 8px;
        background-color: #fcfcfc;
    }
    .result-bubble {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px; /* Tamanho da bolha */
        height: 30px;
        border-radius: 50%; /* Torna a forma de bolha */
        color: white;
        font-weight: bold;
        font-size: 0.9em;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .result-bubble.C {
        background-color: #FF4B4B; /* Vermelho */
    }
    .result-bubble.V {
        background-color: #4B4BFF; /* Azul */
    }
    .result-bubble.E {
        background-color: #FFD700; /* Amarelo */
        color: #333; /* Texto escuro para contraste */
    }
    </style>
""", unsafe_allow_html=True)


st.title("⚽ Análise de Padrões para Jogos de Resultado ⚽")

# Sidebar para inserção de resultados
with st.sidebar:
    st.header("Adicionar Resultado")
    col1_side, col2_side, col3_side = st.columns(3)
    
    with col1_side:
        if st.button("Casa (C)", key="add_C"): # Removido type="primary" para aplicar CSS customizado
            st.session_state.historico_resultados.insert(0, 'C') # Adiciona no início para o mais recente ficar em 0
            st.rerun()

    with col2_side:
        if st.button("Visitante (V)", key="add_V"): # Removido type="primary"
            st.session_state.historico_resultados.insert(0, 'V')
            st.rerun()

    with col3_side:
        if st.button("Empate (E)", key="add_E"): # Removido type="primary"
            st.session_state.historico_resultados.insert(0, 'E')
            st.rerun()
            
    st.markdown("---")
    st.header("Validar Última Sugestão")
    # Verifica se há uma última sugestão para validar
    if 'ultima_sugestao' in st.session_state and st.session_state.ultima_sugestao:
        ultima_sugestao = st.session_state.ultima_sugestao
        st.write(f"Última sugestão: **{ultima_sugestao['sugestao']}**")
        st.write(f"Confiança: **{ultima_sugestao['confianca']}%**")
        
        col_valid_c, col_valid_v, col_valid_e = st.columns(3)
        
        with col_valid_c:
            if st.button("Casa (Real)", key="valid_C"):
                acertou = (ultima_sugestao['sugestao'] == 'C')
                st.session_state.estatisticas['total_sugestoes'] += 1
                if acertou:
                    st.session_state.estatisticas['acertos'] += 1
                else:
                    st.session_state.estatisticas['erros'] += 1
                st.session_state.estatisticas['historico_sugestoes'].insert(0, {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'sugerido': ultima_sugestao['sugestao'],
                    'real': 'C',
                    'confianca': ultima_sugestao['confianca'],
                    'acertou': acertou,
                    'motivos': ultima_sugestao['motivos']
                })
                st.session_state.ultima_sugestao = None # Limpa a última sugestão após validação
                st.rerun()
        with col_valid_v:
            if st.button("Visitante (Real)", key="valid_V"):
                acertou = (ultima_sugestao['sugestao'] == 'V')
                st.session_state.estatisticas['total_sugestoes'] += 1
                if acertou:
                    st.session_state.estatisticas['acertos'] += 1
                else:
                    st.session_state.estatisticas['erros'] += 1
                st.session_state.estatisticas['historico_sugestoes'].insert(0, {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'sugerido': ultima_sugestao['sugestao'],
                    'real': 'V',
                    'confianca': ultima_sugestao['confianca'],
                    'acertou': acertou,
                    'motivos': ultima_sugestao['motivos']
                })
                st.session_state.ultima_sugestao = None
                st.rerun()
        with col_valid_e:
            if st.button("Empate (Real)", key="valid_E"):
                acertou = (ultima_sugestao['sugestao'] == 'E')
                st.session_state.estatisticas['total_sugestoes'] += 1
                if acertou:
                    st.session_state.estatisticas['acertos'] += 1
                else:
                    st.session_state.estatisticas['erros'] += 1
                st.session_state.estatisticas['historico_sugestoes'].insert(0, {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'sugerido': ultima_sugestao['sugestao'],
                    'real': 'E',
                    'confianca': ultima_sugestao['confianca'],
                    'acertou': acertou,
                    'motivos': ultima_sugestao['motivos']
                })
                st.session_state.ultima_sugestao = None
                st.rerun()
    else:
        st.info("Adicione resultados para receber sugestões e validá-las.")

    st.markdown("---")
    if st.button("Limpar Histórico", key="clear_history"): # Removido type="secondary"
        st.session_state.historico_resultados = []
        st.session_state.estatisticas = {
            'total_sugestoes': 0,
            'acertos': 0,
            'erros': 0,
            'historico_sugestoes': []
        }
        st.session_state.ultima_sugestao = None
        st.rerun()

# Coluna principal e de estatísticas
col_main, col_stats = st.columns([2, 1])

with col_main:
    st.header("Histórico de Resultados")
    if st.session_state.historico_resultados:
        # Exibe os resultados mais recentes no topo
        # Usa o histórico original (sem o reversed da classe AnalisePadroes) para exibição
        display_historico = "".join([f"<span class='result-bubble {res}'>{res}</span>" for res in st.session_state.historico_resultados])
        st.markdown(f"<div class='historico-container'>{display_historico}</div>", unsafe_allow_html=True)
        st.markdown("---")
    else:
        st.info("Nenhum resultado adicionado ainda.")

    # Análise de Padrões e Sugestão
    # A classe AnalisePadroes inverte o histórico internamente,
    # então passamos o st.session_state.historico_resultados diretamente.
    if len(st.session_state.historico_resultados) >= 9: # Mínimo de 9 resultados para começar a análise
        analisador = AnalisePadroes(st.session_state.historico_resultados)
        sugestao_data = analisador.sugestao_inteligente()
        st.session_state.ultima_sugestao = sugestao_data # Salva a última sugestão

        st.subheader("Sugestão de Próximo Resultado")
        st.success(f"Sugerido: **{sugestao_data['sugestao']}** com confiança de **{sugestao_data['confianca']}%**")
        st.write("Motivos:")
        if sugestao_data['motivos']:
            for motivo in sugestao_data['motivos']:
                st.write(f"- {motivo}")
        else:
            st.info("Nenhum padrão específico forte detectado, usando lógica de frequência/mudança.")

        st.subheader("Padrões Ativos Detectados")
        padroes_detectados_raw = analisador.analisar() # Chamar para exibir todos os detectados
        if padroes_detectados_raw:
            for nome_padrao, info_padrao in padroes_detectados_raw.items():
                st.markdown(f"**{nome_padrao}** (Peso: {analisador.pesos_padroes.get(nome_padrao, 0)}):")
                for ocorrencia in info_padrao["ocorrencias"]:
                    # Inverte o segmento para exibição para coincidir com a ordem do histórico exibido (mais recente à esquerda)
                    segmento_display = list(reversed(ocorrencia['segmento']))
                    st.write(f"    Segmento: `{str(segmento_display)}` (Posição final (relativa ao último resultado): {ocorrencia['posicao_final']})")
        else:
            st.info("Nenhum padrão específico foi detectado no histórico atual.")
            
    else:
        st.info(f"🎮 Insira pelo menos 9 resultados para começar a análise... (Atualmente: {len(st.session_state.historico_resultados)})")

with col_stats:
    st.header("Estatísticas")
    total = st.session_state.estatisticas['total_sugestoes']
    acertos = st.session_state.estatisticas['acertos']
    erros = st.session_state.estatisticas['erros']
    
    col_acc1, col_acc2 = st.columns(2)
    with col_acc1:
        st.metric(label="Total de Sugestões", value=total)
    with col_acc2:
        st.metric(label="Acertos", value=acertos)
    st.metric(label="Erros", value=erros)

    if total > 0:
        taxa_acerto = (acertos / total) * 100
        st.metric(label="Taxa de Acerto", value=f"{taxa_acerto:.2f}%")
    else:
        st.metric(label="Taxa de Acerto", value="N/A")

    st.subheader("Frequência de Resultados")
    frequencias = collections.Counter(st.session_state.historico_resultados)
    frequencias_df = pd.DataFrame({
        'Resultado': ['Casa', 'Visitante', 'Empate'],
        'Frequência': [frequencias['C'], frequencias['V'], frequencias['E']]
    })
    
    chart_colors = {
        'Casa': '#FF4B4B',
        'Visitante': '#4B4BFF',
        'Empate': '#FFD700'
    }
    
    # Criar uma lista de cores na ordem do dataframe
    colors_for_chart = [chart_colors[res] for res in frequencias_df['Resultado']]
    
    # st.bar_chart espera o índice como o eixo X, então Transpõe (T) e usa o Resultado como índice
    # Corrigido para passar a lista de cores corretamente ao st.bar_chart
    st.bar_chart(frequencias_df.set_index('Resultado'), color=colors_for_chart)
    
    with st.expander("Histórico de Sugestões e Resultados Reais"):
        if st.session_state.estatisticas['historico_sugestoes']:
            df_sugestoes = pd.DataFrame(st.session_state.estatisticas['historico_sugestoes'])
            df_sugestoes['Acertou?'] = df_sugestoes['acertou'].apply(lambda x: '✅ Sim' if x else '❌ Não')
            df_sugestoes_display = df_sugestoes[['timestamp', 'sugerido', 'real', 'confianca', 'Acertou?', 'motivos']]
            st.dataframe(df_sugestoes_display, use_container_width=True)
        else:
            st.info("Nenhuma sugestão foi validada ainda.")
