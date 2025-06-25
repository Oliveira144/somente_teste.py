import streamlit as st
import collections
import streamlit as st
import collections
import numpy as np
import pandas as pd
from datetime import datetime

# --- CLASSE ANALISEPADROES REFINADA E AJUSTADA ---
class AnalisePadroes:
    """
    Classe para analisar padrÃµes em um histÃ³rico de resultados de jogos
    (ex: 'C' para Casa, 'F' para Fora, 'E' para Empate) e gerar sugestÃµes.
    """
    def __init__(self, historico: list):
        """
        Inicializa a classe com um histÃ³rico de resultados.
        O histÃ³rico Ã© truncado para os Ãºltimos 50 jogos para foco na anÃ¡lise recente.

        Args:
            historico (list): Uma lista de strings representando os resultados dos jogos.
                               Ex: ['C', 'F', 'E', 'C', 'C']
        """
        # Limita o histÃ³rico aos Ãºltimos 50 jogos para anÃ¡lise.
        # Assume que o histÃ³rico estÃ¡ sempre com o mais recente primeiro (insert(0))
        self.historico = historico[-54:] if len(historico) > 54 else historico[:]
        self.historico.reverse()

        self.padroes_ativos_map = {
            # PadrÃµes BÃ¡sicos
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

            # Novos PadrÃµes EspecÃ­ficos do Football Studio
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
            
            # PadrÃµes solicitados pelo usuÃ¡rio
            "PadrÃ£o 2x1x2": self._padrao_2x1x2,
            "PadrÃ£o 2x2": self._padrao_2x2,
            "PadrÃ£o 3x3": self._padrao_3x3,
            "PadrÃ£o 4x4": self._padrao_4x4,
        }

        # Pesos dos padrÃµes para calcular a confianÃ§a e sugestÃ£o.
        # Ajustei os pesos para os padrÃµes novos darem mais relevÃ¢ncia ao "surf"
        self.pesos_padroes = {
            "SequÃªncia (Surf de Cor)": 1.2,
            "Zig-Zag Perfeito": 1.0,
            "Quebra de Surf": 1.1,
            "Quebra de Zig-Zag": 1.0,
            "Duplas Repetidas": 0.8,
            "Empate Recorrente": 1.3,
            "PadrÃ£o Escada": 0.7,
            "Espelho": 0.9,
            "AlternÃ¢ncia com Empate": 0.9,
            "PadrÃ£o Onda": 0.8,
            "PadrÃ£o Fibonacci": 1.0,
            "SequÃªncia Dourada": 1.0,
            "PadrÃ£o Triangular": 0.8,
            "Ciclo de Empates": 1.4,
            "PadrÃ£o Martingale": 1.1,
            "SequÃªncia de Fibonacci Invertida": 1.0,
            "PadrÃ£o Dragon Tiger": 1.2,
            "SequÃªncia de Paroli": 0.9,
            "PadrÃ£o de Ondas Longas": 1.3,
            "Ciclo de DominÃ¢ncia": 1.1,
            "PadrÃ£o de TensÃ£o": 1.0,
            "SequÃªncia de Labouchere": 0.7,
            "PadrÃ£o Ritmo CardÃ­aco": 0.8,
            "Ciclo de PressÃ£o": 0.9,
            "PadrÃ£o de Clusters": 0.8,
            "SequÃªncia Polar": 1.0,
            "PadrÃ£o de Momentum": 1.2,
            "Ciclo de RespiraÃ§Ã£o": 0.9,
            "PadrÃ£o de ResistÃªncia": 1.1,
            "SequÃªncia de Breakout": 1.2,
            
            # Pesos para os novos padrÃµes (aumentados para priorizar o "surf")
            "PadrÃ£o 2x1x2": 1.6, # Peso alto para indicar continuidade (AA B AA)
            "PadrÃ£o 2x2": 1.4,   # RelevÃ¢ncia para o 2x2
            "PadrÃ£o 3x3": 1.7,   # Peso mais alto para sequÃªncias mais longas de duplas
            "PadrÃ£o 4x4": 1.9,   # Peso ainda mais alto
        }

    def analisar_todos(self) -> dict:
        """
        Analisa o histÃ³rico para detectar quais padrÃµes estÃ£o ativos.
        Returns:
            dict: Um dicionÃ¡rio onde as chaves sÃ£o os nomes dos padrÃµes e os valores
                  sÃ£o True se o padrÃ£o for detectado, False caso contrÃ¡rio.
        """
        resultados = {}
        for nome, func in self.padroes_ativos_map.items():
            try:
                resultados[nome] = func()
            except Exception as e:
                # Ã‰ bom manter logs embutidos para depuraÃ§Ã£o, mesmo que Streamlit capture exceÃ§Ãµes
                st.session_state.log_messages.append(f"[{datetime.now().strftime('%H:%M:%S')}] [ERROR] Erro ao analisar o padrÃ£o '{nome}': {e}")
                resultados[nome] = False
        return resultados

    # --- MÃ©todos Auxiliares Internos ---
    def _get_last_result(self) -> str | None:
        """Retorna o Ãºltimo resultado do histÃ³rico, se houver."""
        return self.historico[0] if self.historico else None
    
    def _get_second_last_result(self) -> str | None:
        """Retorna o penÃºltimo resultado do histÃ³rico, se houver."""
        return self.historico[1] if len(self.historico) >= 2 else None

    def _get_result_counts_in_window(self, window_size: int) -> collections.Counter:
        """
        Retorna a contagem de cada resultado em uma janela recente do histÃ³rico.
        """
        if len(self.historico) < window_size:
            return collections.Counter(self.historico)
        return collections.Counter(self.historico[:window_size])

    # --- PADRÃ•ES BÃSICOS EXISTENTES ---
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
        # Este padrÃ£o especÃ­fico Ã© C C F F
        return (self.historico[0] == self.historico[1] and
                self.historico[2] == self.historico[3] and
                self.historico[0] != self.historico[2])

    def _empate_recorrente(self) -> bool:
        empates_indices = [i for i, r in enumerate(self.historico) if r == 'E']
        if len(empates_indices) < 3: return False
        intervals = np.diff(empates_indices) # Corrigido para usar empates_indices
        if len(intervals) >= 2:
            media_intervalo = np.mean(intervals)
            # Ajustando a tolerÃ¢ncia para ser mais flexÃ­vel em "recorrente"
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

    # --- NOVOS PADRÃ•ES ESPECÃFICOS DO FOOTBALL STUDIO ---
    def _padrao_fibonacci(self) -> bool:
        if len(self.historico) < 8: return False
        fib_lengths = [1, 1, 2, 3] # Representa C, F, C C, F F F (alternando)
        current_idx = 0
        results_to_check = self.historico[:]
        try:
            for length in fib_lengths:
                if current_idx + length > len(results_to_check): return False
                block = results_to_check[current_idx : current_idx + length]
                if not block or not all(x == block[0] for x in block): return False # Verifica se o bloco Ã© uniforme
                # Verifica se o bloco atual Ã© diferente do anterior, garantindo alternÃ¢ncia
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
        # PadrÃ£o: A B C D C B A E A (onde A Ã© o resultado mais externo, e E Ã© o do meio)
        # Ajuste para verificar se o centro (segment[4]) Ã© o mesmo da base (segment[0])
        # e se a parte central Ã© uniforme (ex: C C C)
        return (segment[0] == segment[8] and segment[1] == segment[7] and 
                segment[2] == segment[6] and segment[3] == segment[5] and
                segment[0] != segment[4]) # A base Ã© diferente do pico/centro do triÃ¢ngulo

    def _ciclo_empates(self) -> bool:
        empates = [i for i, x in enumerate(self.historico) if x == 'E']
        if len(empates) < 3: return False
        # Procura por intervalos regulares entre empates
        intervals = np.diff(empates)
        if len(intervals) >= 2:
            media_intervalo = np.mean(intervals)
            # Um ciclo Ã© mais forte se os intervalos sÃ£o consistentes
            return np.std(intervals) < 1.5 and 2 <= media_intervalo <= 7 # Intervalos mÃ©dios entre 2 e 7 jogos

    def _padrao_martingale(self) -> bool:
        if len(self.historico) < 7: return False
        # Ex: A B B C C C C (apÃ³s uma quebra, uma sequÃªncia forte)
        return (self.historico[0] != self.historico[1] and # A quebra
                self.historico[1] == self.historico[2] and # B B
                self.historico[3] == self.historico[4] == self.historico[5] == self.historico[6] and # C C C C
                self.historico[1] != self.historico[3]) # B diferente de C

    def _fibonacci_invertida(self) -> bool:
        if len(self.historico) < 8: return False
        # Ex: C C F F C C F F (sequÃªncias curtas e alternadas)
        # Mais genÃ©rico: Dupla A, Dupla B, Dupla C, Dupla D, onde A!=B, B!=C, C!=D
        return (self.historico[0] == self.historico[1] and           # Dupla 1
                self.historico[2] == self.historico[3] and           # Dupla 2
                self.historico[4] == self.historico[5] and           # Dupla 3
                self.historico[6] == self.historico[7] and           # Dupla 4
                self.historico[0] != self.historico[2] and           # Dupla 1 diferente de Dupla 2
                self.historico[2] != self.historico[4] and           # Dupla 2 diferente de Dupla 3
                self.historico[4] != self.historico[6])              # Dupla 3 diferente de Dupla 4

    def _padrao_dragon_tiger(self) -> bool:
        if len(self.historico) < 6: return False
        # Ex: C F C E F F (AlternÃ¢ncia, um empate, e uma dupla)
        return (self.historico[0] != self.historico[1] and self.historico[1] != self.historico[2] and # Zig-zag inicial
                self.historico[3] == 'E' and # Um empate no meio
                self.historico[4] == self.historico[5] and # Uma dupla
                self.historico[4] != 'E') # E nÃ£o pode ser o da dupla

    def _sequencia_paroli(self) -> bool:
        if len(self.historico) < 8: return False
        # Ex: C F F C C C C C (Quebra, dupla, sequÃªncia longa, e o primeiro e o Ãºltimo sÃ£o iguais)
        return (self.historico[0] != self.historico[1] and # Quebra
                self.historico[1] == self.historico[2] and # Dupla
                self.historico[3] == self.historico[4] == self.historico[5] == self.historico[6] and # SequÃªncia de 4
                self.historico[0] == self.historico[7]) # O primeiro e o oitavo sÃ£o iguais

    def _ondas_longas(self) -> bool:
        if len(self.historico) < 5: return False
        count = 1
        for i in range(1, len(self.historico)):
            if self.historico[i] == self.historico[i-1]:
                count += 1
                if count >= 5: return True # Detecta qualquer sequÃªncia de 5 ou mais
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
        # Ex: C F C F C C C (AlternÃ¢ncia que se "quebra" em uma sequÃªncia forte)
        alternations_ok = (self.historico[0] != self.historico[1] and
                           self.historico[1] != self.historico[2] and
                           self.historico[2] != self.historico[3]) # As 3 primeiras alternÃ¢ncias
        
        sequence_break = (self.historico[3] == self.historico[4] == self.historico[5] == self.historico[6]) # Uma sequÃªncia de 4
        
        return alternations_ok and sequence_break and (self.historico[2] != self.historico[3]) # A alternÃ¢ncia Ã© quebrada pela sequÃªncia

    def _sequencia_labouchere(self) -> bool:
        if len(self.historico) < 6: return False
        # Ex: C F X X F C (primeiro e Ãºltimo iguais, segundo e penÃºltimo iguais, meio diferente)
        segment = self.historico[:6]
        return (segment[0] == segment[5] and segment[1] == segment[4] and
                segment[2] != segment[0] and segment[3] != segment[0] and segment[2] == segment[3]) # Meio Ã© uma dupla diferente

    def _ritmo_cardiaco(self) -> bool:
        if len(self.historico) < 8: return False
        # Ex: C C F C C F F F (Dupla, quebra, dupla, quebra, tripla)
        segment = self.historico[:8]
        return (segment[0] == segment[1] and segment[2] != segment[0] and # Dupla A, Quebra
                segment[3] == segment[4] and segment[5] != segment[3] and # Dupla B, Quebra
                segment[5] == segment[6] == segment[7]) # Tripla C, B diferente de C

    def _ciclo_pressao(self) -> bool:
        if len(self.historico) < 9: return False
        # Ex: A B B C C C A B B (repetiÃ§Ã£o de padrÃµes pequenos em um ciclo)
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
        # AlternÃ¢ncia extrema entre dois resultados sem empates
        window = self.historico[:10]
        unique_results = set(window)
        if len(unique_results) == 2 and 'E' not in unique_results:
            changes = sum(1 for j in range(len(window)-1) if window[j] != window[j+1])
            return changes >= 6 # Pelo menos 6 mudanÃ§as em 9 possÃ­veis (alta alternÃ¢ncia)
        return False

    def _padrao_momentum(self) -> bool:
        if len(self.historico) < 10: return False
        # Ex: A B B C C C D D D D (sequÃªncias crescentes de diferentes resultados)
        return (self.historico[0] != self.historico[1] and self.historico[1] == self.historico[2] and # 1x A, 2x B
                self.historico[3] == self.historico[4] == self.historico[5] and # 3x C
                self.historico[6] == self.historico[7] == self.historico[8] == self.historico[9] and # 4x D
                self.historico[1] != self.historico[3] and self.historico[3] != self.historico[6]) # B != C != D

    def _ciclo_respiracao(self) -> bool:
        if len(self.historico) < 8: return False
        # Ex: A A A A B C C C (SequÃªncia longa, quebra, e nova sequÃªncia)
        return (self.historico[0] == self.historico[1] == self.historico[2] == self.historico[3] and # SequÃªncia de 4
                self.historico[4] != self.historico[0] and # Quebra
                self.historico[5] == self.historico[6] == self.historico[7] and # Nova sequÃªncia de 3
                self.historico[5] != self.historico[4]) # E a nova sequÃªncia Ã© diferente da quebra

    def _padrao_resistencia(self) -> bool:
        if len(self.historico) < 6: return False
        # Ex: A B A C A A (um resultado 'A' aparece e 'resiste' a interrupÃ§Ãµes)
        return (self.historico[0] == self.historico[2] == self.historico[4] == self.historico[5] and # A em posiÃ§Ãµes especÃ­ficas
                self.historico[1] != self.historico[0] and self.historico[3] != self.historico[0]) # InterrupÃ§Ãµes sÃ£o diferentes de A

    def _sequencia_breakout(self) -> bool:
        if len(self.historico) < 8: return False
        # Ex: A A A A B B B B (sequÃªncia longa, quebra e nova sequÃªncia longa do tipo da quebra)
        return (self.historico[0] == self.historico[1] == self.historico[2] == self.historico[3] and # SequÃªncia AAAA
                self.historico[4] != self.historico[0] and # Quebra para B
                self.historico[5] == self.historico[6] == self.historico[7] and # SequÃªncia BBB
                self.historico[5] == self.historico[4]) # O resultado da quebra inicia a nova sequÃªncia

    # --- NOVOS PADRÃ•ES SOLICITADOS ---
    def _padrao_2x1x2(self) -> bool:
        if len(self.historico) < 5: return False
        # Ex: C C F C C ou F F C F F.
        # Verifica se os dois primeiros sÃ£o iguais, o terceiro Ã© diferente,
        # e o quarto e quinto sÃ£o iguais ao primeiro e segundo.
        return (self.historico[0] == self.historico[1] and           # Dois do mesmo (primeira dupla)
                self.historico[2] != self.historico[0] and          # Um diferente
                self.historico[3] == self.historico[4] and           # Dois do mesmo (segunda dupla)
                self.historico[0] == self.historico[3])              # As duplas sÃ£o do mesmo tipo

    def _padrao_2x2(self) -> bool:
        if len(self.historico) < 4: return False
        # Ex: C C F F ou F F C C.
        # Verifica se os dois primeiros sÃ£o iguais e os dois prÃ³ximos sÃ£o iguais, mas diferentes entre si.
        return (self.historico[0] == self.historico[1] and           # Dois do mesmo
                self.historico[2] == self.historico[3] and           # Dois do outro
                self.historico[0] != self.historico[2])              # Os pares sÃ£o de tipos diferentes

    def _padrao_3x3(self) -> bool:
        if len(self.historico) < 6: return False
        # Ex: C C C F F F ou F F F C C C.
        # Verifica se os trÃªs primeiros sÃ£o iguais e os trÃªs prÃ³ximos sÃ£o iguais, mas diferentes entre si.
        return (self.historico[0] == self.historico[1] == self.historico[2] and # TrÃªs do mesmo
                self.historico[3] == self.historico[4] == self.historico[5] and # TrÃªs do outro
                self.historico[0] != self.historico[3])             # Os trios sÃ£o de tipos diferentes

    def _padrao_4x4(self) -> bool:
        if len(self.historico) < 8: return False
        # Ex: C C C C F F F F ou F F F F C C C C.
        # Verifica se os quatro primeiros sÃ£o iguais e os quatro prÃ³ximos sÃ£o iguais, mas diferentes entre si.
        return (self.historico[0] == self.historico[1] == self.historico[2] == self.historico[3] and # Quatro do mesmo
                self.historico[4] == self.historico[5] == self.historico[6] == self.historico[7] and # Quatro do outro
                self.historico[0] != self.historico[4])             # Os quartetos sÃ£o de tipos diferentes


    def calcular_frequencias(self):
        """Calcula frequÃªncias dos resultados"""
        contador = collections.Counter(self.historico)
        total = len(self.historico)
        if total == 0: return {'C': 0, 'F': 0, 'E': 0}
        
        result = {k: round(v / total * 100, 1) for k, v in contador.items()}
        for tipo in ['C', 'F', 'E']:
            if tipo not in result:
                result[tipo] = 0
        return result

    def calcular_tendencia(self):
        """Calcula tendÃªncia dos Ãºltimos resultados"""
        if len(self.historico) < 5: return "Dados insuficientes"
        
        ultimos_5 = self.historico[:5]
        contador = collections.Counter(ultimos_5)
        
        # Considera a tendÃªncia se um resultado aparece 3 ou mais vezes nos Ãºltimos 5.
        # Ajustado para ser mais sensÃ­vel
        if contador.most_common(1)[0][1] >= 4: 
            return f"Forte tendÃªncia: {contador.most_common(1)[0][0]}"
        elif contador.most_common(1)[0][1] == 3: 
            return f"TendÃªncia moderada: {contador.most_common(1)[0][0]}"
        else: 
            return "Sem tendÃªncia clara"

    def gerar_sugestao(self) -> dict: # CORRIGIDO: Nome do mÃ©todo de 'generar_sugestao' para 'gerar_sugestao'
        """
        Gera uma sugestÃ£o de prÃ³ximo resultado com base nos padrÃµes ativos e seus pesos,
        alÃ©m de considerar a tendÃªncia mais recente.
        """
        if not self.historico:
            return {
                "sugerir": False, "entrada": None, "entrada_codigo": None,
                "motivos": ["Nenhum histÃ³rico para anÃ¡lise."], "confianca": 0.0,
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

                # LÃ³gica de pontuaÃ§Ã£o para cada padrÃ£o ativo
                if nome_padrao == "SequÃªncia (Surf de Cor)":
                    if last_result: pontuacoes[last_result] += peso * 2.0 # Maior peso para continuar o surf

                elif nome_padrao == "Zig-Zag Perfeito":
                    if last_result == 'C': pontuacoes['F'] += peso
                    elif last_result == 'F': pontuacoes['C'] += peso
                    
                elif nome_padrao == "Quebra de Surf":
                    # Este padrÃ£o indica que a sequÃªncia anterior de 3 foi quebrada pelo 4Âº resultado.
                    # A sugestÃ£o seria apostar NO resultado que QUEBROU a sequÃªncia.
                    if len(self.historico) >= 4 and self.historico[0] == self.historico[1] == self.historico[2] and self.historico[2] != self.historico[3]:
                        pontuacoes[self.historico[3]] += peso * 0.8 # Menor peso, pois Ã© uma quebra

                elif nome_padrao == "Quebra de Zig-Zag":
                    # Este padrÃ£o indica que o zig-zag foi quebrado.
                    # A sugestÃ£o Ã© seguir o resultado que quebrou a alternÃ¢ncia.
                    if len(self.historico) >= 5 and self.historico[3] == self.historico[4]:
                        pontuacoes[self.historico[3]] += peso * 0.8 # Menor peso para quebra

                elif nome_padrao == "Duplas Repetidas": # C C F F
                    if len(self.historico) >= 4 and self.historico[0] == self.historico[1] and self.historico[2] == self.historico[3] and self.historico[0] != self.historico[2]:
                        pontuacoes[self.historico[0]] += peso # Sugere a continuaÃ§Ã£o da primeira dupla

                elif nome_padrao == "Empate Recorrente":
                    pontuacoes['E'] += peso * 1.5

                elif nome_padrao == "PadrÃ£o Escada":
                    # Ex: A B B C C C. Sugere quebrar o C C C e voltar para B (ou E se aplicÃ¡vel)
                    if len(self.historico) >= 6 and self.historico[1] == self.historico[2] and self.historico[3] == self.historico[4] == self.historico[5]:
                        if self.historico[0] == 'C': pontuacoes['F'] += peso # Se A foi C, sugerir F
                        elif self.historico[0] == 'F': pontuacoes['C'] += peso # Se A foi F, sugerir C
                        else: pontuacoes['E'] += peso # Se A foi E, sugerir E (menos provÃ¡vel)
                        
                elif nome_padrao == "Espelho":
                    # Se hÃ¡ um espelho (e.g., C F E F C), o prÃ³ximo seria a 'continuaÃ§Ã£o' do espelho.
                    # Para simplificar, pode-se sugerir o oposto do Ãºltimo para manter a simetria ou o prÃ³ximo do "espelho"
                    if last_result == 'C': pontuacoes['F'] += peso * 0.7
                    elif last_result == 'F': pontuacoes['C'] += peso * 0.7
                    elif last_result == 'E': pontuacoes['E'] += peso * 0.5 # Empates podem quebrar espelhos facilmente

                elif nome_padrao == "AlternÃ¢ncia com Empate":
                    # Ex: C E F. O prÃ³ximo seria C.
                    if len(self.historico) >= 3 and self.historico[1] == 'E' and self.historico[0] != self.historico[2]:
                        pontuacoes[self.historico[0]] += peso * 1.0 # Sugere o que alternou com E

                elif nome_padrao == "PadrÃ£o Onda": # C F C F C F
                    if len(self.historico) >= 6 and self.historico[0] == self.historico[2] == self.historico[4] and self.historico[1] == self.historico[3] == self.historico[5]:
                        pontuacoes[self.historico[1]] += peso # Sugere o oposto do Ãºltimo resultado

                elif nome_padrao == "PadrÃ£o Fibonacci": # 1, 1, 2, 3 (alternando)
                    # Se terminou em uma sequÃªncia de 3 (ex: F F F), o prÃ³ximo seria C (inversÃ£o)
                    if last_result == 'C': pontuacoes['F'] += peso * 1.1
                    elif last_result == 'F': pontuacoes['C'] += peso * 1.1
                    elif last_result == 'E': pontuacoes['E'] += peso * 0.8

                elif nome_padrao == "SequÃªncia Dourada": # 3 de um, 5 do outro
                    if len(self.historico) >= 8 and self.historico[3] == self.historico[4]:
                        pontuacoes[self.historico[3]] += peso * 1.2 # Sugere continuar a sequÃªncia de 5

                elif nome_padrao == "PadrÃ£o Triangular": # A B C D C B A E A
                    if len(self.historico) >= 9 and self.historico[0] == self.historico[8]:
                        if self.historico[4] == 'C': pontuacoes['F'] += peso # Sugere o oposto do meio
                        elif self.historico[4] == 'F': pontuacoes['C'] += peso
                        elif self.historico[4] == 'E': pontuacoes['E'] += peso * 0.8

                elif nome_padrao == "Ciclo de Empates":
                    pontuacoes['E'] += peso * 1.8 # Forte sugestÃ£o de Empate

                elif nome_padrao == "PadrÃ£o Martingale": # A B B C C C C
                    if len(self.historico) >= 7 and self.historico[3] == self.historico[4]:
                        pontuacoes[self.historico[3]] += peso * 1.5 # Sugere continuar a sequÃªncia forte

                elif nome_padrao == "SequÃªncia de Fibonacci Invertida": # 2x, 1x, 2x, 1x
                    if last_result == 'C': pontuacoes['F'] += peso * 1.1
                    elif last_result == 'F': pontuacoes['C'] += peso * 1.1
                    elif last_result == 'E': pontuacoes['E'] += peso * 0.8

                elif nome_padrao == "PadrÃ£o Dragon Tiger": # C F C E F F
                    if len(self.historico) >= 6 and self.historico[4] == self.historico[5]:
                        pontuacoes[self.historico[4]] += peso * 1.3 # Sugere continuar a Ãºltima dupla

                elif nome_padrao == "SequÃªncia de Paroli": # C F F C C C C C
                    if len(self.historico) >= 8 and self.historico[0] == self.historico[7]:
                        pontuacoes[self.historico[0]] += peso * 1.2 # Sugere o resultado que "fechou" a sequÃªncia

                elif nome_padrao == "PadrÃ£o de Ondas Longas":
                    if last_result: pontuacoes[last_result] += peso * 2.0 # Muito forte para continuar a onda

                elif nome_padrao == "Ciclo de DominÃ¢ncia":
                    dominant_result = collections.Counter(self.historico[:10]).most_common(1)[0][0]
                    pontuacoes[dominant_result] += peso * 1.1 # Sugere o dominante

                elif nome_padrao == "PadrÃ£o de TensÃ£o": # C F C F C C C
                    if len(self.historico) >= 7 and self.historico[4] == self.historico[5] == self.historico[6]:
                        pontuacoes[self.historico[4]] += peso * 1.2 # Sugere continuar a sequÃªncia final

                elif nome_padrao == "SequÃªncia de Labouchere": # C F X X F C
                    if len(self.historico) >= 6 and self.historico[0] == self.historico[5]:
                        if last_result == 'C': pontuacoes['F'] += peso * 0.8 # Sugere alternÃ¢ncia se o padrÃ£o for de espelho
                        elif last_result == 'F': pontuacoes['C'] += peso * 0.8
                        elif last_result == 'E': pontuacoes['E'] += peso * 0.5

                elif nome_padrao == "PadrÃ£o Ritmo CardÃ­aco": # C C F C C F F F
                    if len(self.historico) < 8: return False # JÃ¡ verificado na funÃ§Ã£o do padrÃ£o
                    else:
                        if self.historico[5] == self.historico[6] == self.historico[7]:
                            if self.historico[5] == 'C': pontuacoes['F'] += peso * 0.7 # Sugere o oposto da Ãºltima sequÃªncia
                            elif self.historico[5] == 'F': pontuacoes['C'] += peso * 0.7
                            elif self.historico[5] == 'E': pontuacoes['E'] += peso * 0.7

                elif nome_padrao == "Ciclo de PressÃ£o": # A B B C C C A B B
                    if len(self.historico) >= 9 and self.historico[6] == self.historico[0]:
                        pontuacoes[self.historico[0]] += peso * 1.1 # Sugere a continuaÃ§Ã£o do ciclo

                elif nome_padrao == "PadrÃ£o de Clusters":
                    if len(self.historico) >= 12:
                        last_cluster_dominant = collections.Counter(self.historico[8:12]).most_common(1)[0][0]
                        pontuacoes[last_cluster_dominant] += peso * 1.0 # Sugere continuar o Ãºltimo cluster

                elif nome_padrao == "SequÃªncia Polar":
                    if len(self.historico) >= 10:
                        if last_result == 'C': pontuacoes['F'] += peso * 1.0 # Sugere o oposto para manter a polaridade
                        elif last_result == 'F': pontuacoes['C'] += peso * 1.0

                elif nome_padrao == "PadrÃ£o de Momentum": # A B B C C C D D D D
                    if len(self.historico) >= 10 and self.historico[6] == self.historico[7]:
                        pontuacoes[self.historico[6]] += peso * 1.4 # Sugere continuar a Ãºltima sequÃªncia forte

                elif nome_padrao == "Ciclo de RespiraÃ§Ã£o": # A A A A B C C C
                    if len(self.historico) < 8: pass # JÃ¡ verificado na funÃ§Ã£o do padrÃ£o
                    else:
                        pontuacoes[self.historico[5]] += peso * 1.1 # Sugere continuar a Ãºltima sequÃªncia

                elif nome_padrao == "PadrÃ£o de ResistÃªncia": # A B A C A A
                    if len(self.historico) < 6: pass # JÃ¡ verificado na funÃ§Ã£o do padrÃ£o
                    else:
                        pontuacoes[self.historico[0]] += peso * 1.2 # Sugere continuar o resultado "resistente"

                elif nome_padrao == "SequÃªncia de Breakout": # A A A A B B B B
                    if len(self.historico) < 8: pass # JÃ¡ verificado na funÃ§Ã£o do padrÃ£o
                    else:
                        pontuacoes[self.historico[5]] += peso * 1.5 # Sugere continuar a sequÃªncia que se "consolidou"

                # LÃ³gica de pontuaÃ§Ã£o para os NOVOS PADRÃ•ES SOLICITADOS
                elif nome_padrao == "PadrÃ£o 2x1x2": # C C F C C -> Sugere C (o tipo que se repete)
                    if len(self.historico) >= 4 and self.historico[0] == self.historico[1] and self.historico[0] == self.historico[3]:
                        pontuacoes[self.historico[0]] += peso * 1.5 # Forte sugestÃ£o de continuar o resultado dominante

                elif nome_padrao == "PadrÃ£o 2x2": # C C F F -> Sugere C (o tipo da primeira dupla para reiniciar o ciclo)
                    if len(self.historico) >= 4 and self.historico[0] == self.historico[1] and self.historico[2] == self.historico[3]:
                        pontuacoes[self.historico[0]] += peso * 1.0
                        
                elif nome_padrao == "PadrÃ£o 3x3": # C C C F F F -> Sugere C (o tipo da primeira tripla para reiniciar o ciclo)
                    if len(self.historico) >= 6 and self.historico[0] == self.historico[1] == self.historico[2] and self.historico[3] == self.historico[4] == self.historico[5]:
                        pontuacoes[self.historico[0]] += peso * 1.2

                elif nome_padrao == "PadrÃ£o 4x4": # C C C C F F F F -> Sugere C (o tipo da primeira sequÃªncia de 4 para reiniciar o ciclo)
                    if len(self.historico) >= 8 and self.historico[0] == self.historico[1] == self.historico[2] == self.historico[3] and \
                       self.historico[4] == self.historico[5] == self.historico[6] == self.historico[7]:
                        pontuacoes[self.historico[0]] += peso * 1.4
        
        # 2. Adicionar uma pontuaÃ§Ã£o baseada na tendÃªncia mais recente (Ãºltimos 3-5 jogos)
        recentes_window = self.historico[:min(len(self.historico), 5)]
        if recentes_window:
            contagem_recentes = collections.Counter(recentes_window)
            for resultado, count in contagem_recentes.items():
                if resultado in pontuacoes:
                    pontuacoes[resultado] += count * 0.2

        # 3. Determinar a sugestÃ£o final
        melhor_sugestao_codigo = "N/A"
        maior_pontuacao = -1.0

        if any(pontuacoes.values()):
            resultados_ordenados = sorted(pontuacoes.items(), key=lambda item: item[1], reverse=True)
            melhor_sugestao_codigo = resultados_ordenados[0][0]
            maior_pontuacao = resultados_ordenados[0][1]

            # LÃ³gica para favorecer Empate se a pontuaÃ§Ã£o for prÃ³xima (ajuste delicado)
            # if 'E' in pontuacoes and pontuacoes['E'] > 0 and \
            #    (maior_pontuacao > 0 and (pontuacoes['E'] >= maior_pontuacao * 0.9 and pontuacoes['E'] < maior_pontuacao)):
            #     melhor_sugestao_codigo = 'E'
        else:
            # Se nenhuma pontuaÃ§Ã£o for gerada pelos padrÃµes, use a frequÃªncia mais baixa como sugestÃ£o
            frequencias = self.calcular_frequencias()
            if frequencias:
                # Sugere o resultado com menor frequÃªncia (equilÃ­brio)
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
            "pontuacoes_brutas": pontuacoes # Adicionado para depuraÃ§Ã£o
        }

    def _gerar_analise_detalhada(self, padroes):
        """Gera anÃ¡lise detalhada dos padrÃµes encontrados"""
        # Adicionando uma nova categoria para "PadrÃµes de Bloco/Duplas"
        categorias = {
            "PadrÃµes de SequÃªncia": ["SequÃªncia", "Surf", "Ondas", "Fibonacci", "Momentum", "Paroli", "Ciclo de RespiraÃ§Ã£o", "SequÃªncia Dourada"],
            "PadrÃµes de Quebra": ["Quebra", "Breakout", "TensÃ£o"],
            "PadrÃµes CÃ­clicos": ["Ciclo", "RespiraÃ§Ã£o", "Ritmo", "PressÃ£o", "Empate Recorrente"],
            "PadrÃµes de Simetria/AlternÃ¢ncia": ["Espelho", "AlternÃ¢ncia", "Zig-Zag", "Escada", "Duplas", "Polar", "Labouchere", "Triangular", "Fibonacci Invertida", "Dragon Tiger"],
            "PadrÃµes de DominÃ¢ncia": ["Clusters", "ResistÃªncia", "DominÃ¢ncia", "Martingale"],
            "PadrÃµes de Bloco/Duplas": ["2x1x2", "2x2", "3x3", "4x4"] # Nova categoria
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
    # HistÃ³rico de exemplo, pode ser vazio ou com alguns dados para comeÃ§ar
    # st.session_state.historico = [] # Se quiser comeÃ§ar completamente vazio
    st.session_state.historico = ['C', 'F', 'C', 'E', 'F', 'F', 'C', 'C', 'E', 'F'] 
    
if 'estatisticas' not in st.session_state:
    st.session_state.estatisticas = {
        'total_jogos': 0,
        'acertos': 0,
        'erros': 0,
        'ultima_sugestao': None # Guarda a Ãºltima sugestÃ£o para validaÃ§Ã£o
    }

# Para capturar e exibir logs/erros na UI (opcional)
if 'log_messages' not in st.session_state:
    st.session_state.log_messages = []

def log_message(type, message):
    st.session_state.log_messages.append(f"[{datetime.now().strftime('%H:%M:%S')}] [{type.upper()}] {message}")
    if len(st.session_state.log_messages) > 50: # Limita o tamanho do log
        st.session_state.log_messages.pop(0)

def adicionar_resultado(resultado):
    """Adiciona novo resultado ao histÃ³rico e valida a sugestÃ£o anterior."""
    # Valida a sugestÃ£o anterior ANTES de adicionar o novo resultado ao histÃ³rico principal.
    # Isso garante que a validaÃ§Ã£o usa o estado do histÃ³rico anterior ao novo jogo.
    if st.session_state.get('ultima_sugestao') and st.session_state.get('sugestao_processada'):
        # A sugestÃ£o sÃ³ Ã© validada se foi gerada na rodada anterior
        validar_sugestao(st.session_state.ultima_sugestao, resultado)
        # Limpa a flag e a sugestÃ£o apÃ³s a validaÃ§Ã£o
        st.session_state.sugestao_processada = False
        st.session_state.ultima_sugestao = None
    
    st.session_state.historico.insert(0, resultado) # Adiciona no inÃ­cio
    if len(st.session_state.historico) > 50:
        st.session_state.historico = st.session_state.historico[:50]
    st.session_state.estatisticas['total_jogos'] = len(st.session_state.historico) # Atualiza total de jogos
    log_message("info", f"Resultado '{resultado}' adicionado. HistÃ³rico atualizado.")


def limpar_historico():
    """Limpa todo o histÃ³rico e estatÃ­sticas."""
    st.session_state.historico = []
    st.session_state.estatisticas = {
        'total_jogos': 0,
        'acertos': 0,
        'erros': 0,
        'ultima_sugestao': None
    }
    st.session_state.log_messages = []
    st.session_state.sugestao_processada = False # Reseta a flag
    log_message("info", "HistÃ³rico e estatÃ­sticas limpos.")


def desfazer_ultimo():
    """Remove o Ãºltimo resultado e ajusta as estatÃ­sticas."""
    if st.session_state.historico:
        removed_result = st.session_state.historico.pop(0)
        # Ao desfazer, tambÃ©m zera a sugestÃ£o para evitar validaÃ§Ã£o de um jogo que nÃ£o existe mais.
        st.session_state.ultima_sugestao = None
        st.session_state.sugestao_processada = False
        st.session_state.estatisticas['total_jogos'] = len(st.session_state.historico)
        log_message("info", f"Ãšltimo resultado '{removed_result}' desfeito. HistÃ³rico ajustado.")
    else:
        log_message("warn", "Tentativa de desfazer com histÃ³rico vazio.")


def validar_sugestao(sugestao_obj, resultado_real):
    """Valida se a sugestÃ£o anterior estava correta"""
    if sugestao_obj and sugestao_obj['entrada_codigo'] == resultado_real:
        st.session_state.estatisticas['acertos'] += 1
        log_message("success", f"SugestÃ£o anterior ACERTADA! Sugerido: {sugestao_obj['entrada_codigo']}, Real: {resultado_real}")
        return True
    else:
        st.session_state.estatisticas['erros'] += 1
        log_message("error", f"SugestÃ£o anterior ERRADA! Sugerido: {sugestao_obj['entrada_codigo'] if sugestao_obj else 'N/A'}, Real: {resultado_real}")
        return False

def get_resultado_html(resultado):
    """Retorna HTML para visualizaÃ§Ã£o do resultado"""
    color_map = {'C': '#FF4B4B', 'F': '#4B4BFF', 'E': '#FFD700'}
    symbol_map = {'C': 'ðŸ ', 'F': 'âœˆï¸', 'E': 'âš–ï¸'}
    
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
    """Retorna cor baseada no nÃ­vel de confianÃ§a"""
    if confianca >= 80:
        return "#4CAF50"  # Verde
    elif confianca >= 60:
        return "#FF9800"  # Laranja
    elif confianca >= 40:
        return "#FFC107"  # Amarelo
    else:
        return "#F44336"  # Vermelho

# --- CONFIGURAÃ‡ÃƒO DA PÃGINA ---
st.set_page_config(
    layout="wide", 
    page_title="ðŸŽ¯ Football Studio Live Analyzer",
    page_icon="âš½",
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

/* BotÃµes */
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

/* BotÃµes especÃ­ficos */
div.stButton > button[data-testid="stButton-ðŸ  Casa (C)"] {
    background: linear-gradient(135deg, #FF6B6B, #FF4B4B);
}

div.stButton > button[data-testid="stButton-âœˆï¸ Visitante (F)"] {
    background: linear-gradient(135deg, #4ECDC4, #4B4BFF);
}

div.stButton > button[data-testid="stButton-âš–ï¸ Empate (E)"] {
    background: linear-gradient(135deg, #FFE66D, #FFD700);
    color: black;
}

div.stButton > button[data-testid="stButton-â†©ï¸ Desfazer"],
div.stButton > button[data-testid="stButton-ðŸ—‘ï¸ Limpar"] {
    background: linear-gradient(135deg, #95A5A6, #7F8C8D);
}

/* Cards de estatÃ­sticas */
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

/* SeÃ§Ãµes */
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

/* HistÃ³rico de resultados - NOVO ESTILO PARA LINHAS */
.historic-row {
    display: flex;
    flex-wrap: wrap; /* Changed from nowrap to wrap */
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

# --- CABEÃ‡ALHO PRINCIPAL ---
st.markdown("""
<div class="main-header">
    <h1>âš½ Football Studio Live Analyzer</h1>
    <p>AnÃ¡lise Inteligente de PadrÃµes - Evolution Gaming</p>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR COM ESTATÃSTICAS ---
with st.sidebar:
    st.markdown("## ðŸ“Š EstatÃ­sticas da SessÃ£o")
    
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
    st.markdown("## âš™ï¸ ConfiguraÃ§Ãµes")
    
    # auto_suggest = st.checkbox("SugestÃ£o AutomÃ¡tica", value=True) # Removido, pois a sugestÃ£o Ã© sempre exibida se a confianÃ§a for suficiente
    show_advanced = st.checkbox("AnÃ¡lise AvanÃ§ada", value=True)
    confidence_threshold = st.slider("Limite de ConfianÃ§a", 0, 100, 60)

    st.markdown("---")
    st.markdown("## ðŸ“ Logs de DepuraÃ§Ã£o")
    log_area = st.empty()
    if st.session_state.log_messages:
        # Exibe os logs mais recentes primeiro
        for log in reversed(st.session_state.log_messages):
            log_area.text(log)
    else:
        log_area.info("Nenhum log ainda.")


# --- SEÃ‡ÃƒO DE INSERÃ‡ÃƒO DE RESULTADOS ---
st.markdown('<div class="section-header"><h2>ðŸŽ¯ Inserir Resultado do Jogo</h2></div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("ðŸ  Casa (C)", key="CasaC", use_container_width=True, help="VitÃ³ria da Casa"):
        adicionar_resultado('C')
        st.rerun()

with col2:
    if st.button("âœˆï¸ Visitante (F)", key="VisitanteF", use_container_width=True, help="VitÃ³ria do Visitante"):
        adicionar_resultado('F')
        st.rerun()

with col3:
    if st.button("âš–ï¸ Empate (E)", key="EmpateE", use_container_width=True, help="Empate"):
        adicionar_resultado('E')
        st.rerun()

with col4:
    if st.button("â†©ï¸ Desfazer", key="Desfazer", use_container_width=True, help="Desfazer Ãºltimo resultado"):
        desfazer_ultimo()
        st.rerun()

with col5:
    if st.button("ðŸ—‘ï¸ Limpar", key="Limpar", use_container_width=True, help="Limpar todo o histÃ³rico"):
        limpar_historico()
        st.rerun()

# --- ANÃLISE PRINCIPAL (MOVIDA PARA CIMA DO HISTÃ“RICO) ---
st.markdown('<div class="section-header"><h2>âœ¨ PrÃ³xima SugestÃ£o</h2></div>', unsafe_allow_html=True)

if len(st.session_state.historico) >= 5: # MÃ­nimo de 5 para algumas anÃ¡lises
    try:
        analyzer = AnalisePadroes(st.session_state.historico)
        log_message("info", "Objeto AnalisePadroes criado com histÃ³rico atual.")
        
        # Gera a sugestÃ£o
        sugestao = analyzer.gerar_sugestao() # CORRIGIDO: Chamando o mÃ©todo com o nome correto
        log_message("info", f"SugestÃ£o gerada: {sugestao['entrada_codigo']} (ConfianÃ§a: {sugestao['confianca']}%)")
        
        # Armazena a sugestÃ£o e define uma flag para que ela seja processada na prÃ³xima adiÃ§Ã£o de resultado
        st.session_state.ultima_sugestao = sugestao
        st.session_state.sugestao_processada = True # Flag para indicar que uma sugestÃ£o foi gerada e aguarda validaÃ§Ã£o

        if sugestao['sugerir'] and sugestao['confianca'] >= confidence_threshold:
            confianca_color = get_confianca_color(sugestao['confianca'])
            
            st.markdown(f"""
            <div class="suggestion-box">
                <h3>ðŸŽ¯ SugestÃ£o para o PrÃ³ximo Jogo:</h3>
                <h2 style="color: {confianca_color}; margin: 1rem 0;">
                    {sugestao['entrada']} ({sugestao['entrada_codigo']})
                </h2>
                <p><strong>ConfianÃ§a:</strong> 
                    <span style="color: {confianca_color}; font-weight: bold;">
                        {sugestao['confianca']}%
                    </span>
                </p>
                <p><strong>TendÃªncia Recente:</strong> {sugestao['tendencia']}</p>
                <p><strong>FrequÃªncias (C/F/E):</strong> {sugestao['frequencias'].get('C',0)}% / {sugestao['frequencias'].get('F',0)}% / {sugestao['frequencias'].get('E',0)}%</p>
            </div>
            """, unsafe_allow_html=True)
            
            if show_advanced:
                with st.expander("ðŸ“‹ Detalhes da AnÃ¡lise"):
                    st.write("**PadrÃµes Identificados que ContribuÃ­ram:**")
                    if sugestao['motivos']:
                        for motivo in sugestao['motivos']:
                            st.write(f"â€¢ {motivo}")
                    else:
                        st.info("Nenhum padrÃ£o especÃ­fico contribuiu para a sugestÃ£o com peso suficiente.")
                    
                    if 'analise_detalhada' in sugestao and sugestao['analise_detalhada']:
                        st.write("**AnÃ¡lise por Categoria de PadrÃµes:**")
                        for categoria, padroes_list in sugestao['analise_detalhada'].items():
                            st.write(f"**{categoria}:** {', '.join(padroes_list)}")
                    else:
                        st.info("Nenhuma anÃ¡lise detalhada de categorias de padrÃµes disponÃ­vel.")
                    
                    st.write("**PontuaÃ§Ãµes Brutas por Resultado:**")
                    st.json(sugestao['pontuacoes_brutas']) # Para depuraÃ§Ã£o

        else:
            st.warning(f"ðŸ¤” ConfianÃ§a insuficiente ({sugestao['confianca']}%) para uma sugestÃ£o forte. Limite: {confidence_threshold}%.")
            st.info("Continue inserindo resultados para aumentar a precisÃ£o da anÃ¡lise.")
            log_message("warn", f"SugestÃ£o nÃ£o exibida: ConfianÃ§a {sugestao['confianca']}% abaixo do limite {confidence_threshold}%.")

    except Exception as e:
        st.error(f"Ocorreu um erro inesperado durante a anÃ¡lise da sugestÃ£o. Por favor, verifique os logs na barra lateral.")
        st.exception(e) # Exibe o traceback completo para depuraÃ§Ã£o em desenvolvimento
        log_message("critical", f"Erro crÃ­tico na anÃ¡lise: {e}")

else:
    st.info("ðŸŽ® Insira pelo menos 5 resultados para comeÃ§ar a anÃ¡lise inteligente e gerar sugestÃµes!")


# --- EXIBIÃ‡ÃƒO DO HISTÃ“RICO (AGORA ABAIXO DA SUGESTÃƒO) ---
st.markdown('<div class="section-header"><h2>ðŸ“ˆ HistÃ³rico de Resultados</h2></div>', unsafe_allow_html=True)

if not st.session_state.historico:
    st.info("ðŸŽ® Nenhum resultado registrado. Comece inserindo os resultados dos jogos!")
else:
    st.markdown('<div class="historic-container">', unsafe_allow_html=True)
    
    # Renderiza o histÃ³rico em linhas com quebra automÃ¡tica
    # A classe CSS 'historic-row' jÃ¡ usa 'flex-wrap: wrap;' para quebrar automaticamente.
    st.markdown('<div class="historic-row">', unsafe_allow_html=True)
    for i, resultado in enumerate(st.session_state.historico):
        st.markdown(get_resultado_html(resultado), unsafe_allow_html=True)
        if (i + 1) % 9 == 0:
            st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) # Fecha a div historic-row
            
    st.markdown(f"**Total:** {len(st.session_state.historico)} jogos (mÃ¡x. 50)", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ANÃLISE DE PADRÃ•ES (DETALHADA) - SÃ“ SE show_advanced ESTIVER ATIVO ---
if show_advanced and len(st.session_state.historico) >= 5:
    try:
        analyzer = AnalisePadroes(st.session_state.historico) # Recria o analyzer para esta seÃ§Ã£o, se necessÃ¡rio
        st.markdown('<div class="section-header"><h2>ðŸ” PadrÃµes Detectados (Todos)</h2></div>', unsafe_allow_html=True)
        
        padroes_encontrados = analyzer.analisar_todos()
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("### âœ… PadrÃµes Ativos")
            encontrados = [nome for nome, status in padroes_encontrados.items() if status]
            
            if encontrados:
                for padrao in encontrados:
                    peso = analyzer.pesos_padroes.get(padrao, 0.5)
                    st.markdown(f'<div class="pattern-found">âœ… {padrao} (Peso: {peso})</div>', unsafe_allow_html=True)
            else:
                st.info("Nenhum padrÃ£o detectado no histÃ³rico atual.")
        
        with col_right:
            st.markdown("### âŒ PadrÃµes Inativos")
            nao_encontrados = [nome for nome, status in padroes_encontrados.items() if not status]
            
            if nao_encontrados:
                # Exibir apenas os primeiros X inativos para nÃ£o poluir a tela
                for padrao in nao_encontrados[:15]: 
                    st.markdown(f'<div class="pattern-not-found">âŒ {padrao}</div>', unsafe_allow_html=True)
                if len(nao_encontrados) > 15:
                    st.markdown(f'<div class="pattern-not-found">... e mais {len(nao_encontrados) - 15}</div>', unsafe_allow_html=True)
            else:
                st.info("Todos os padrÃµes foram encontrados (muito raro).")
        
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado durante a anÃ¡lise detalhada dos padrÃµes. Por favor, verifique os logs na barra lateral.")
        st.exception(e)
        log_message("critical", f"Erro crÃ­tico na anÃ¡lise detalhada de padrÃµes: {e}")

# --- ANÃLISE ESTATÃSTICA GERAL ---
st.markdown('<div class="section-header"><h2>ðŸ“Š AnÃ¡lise EstatÃ­stica Geral</h2></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

# Garante que o analyzer Ã© criado para esta seÃ§Ã£o, caso a sugestÃ£o nÃ£o tenha sido gerada
if 'analyzer' not in locals() or analyzer is None:
    analyzer = AnalisePadroes(st.session_state.historico)

frequencias = analyzer.calcular_frequencias()

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>ðŸ  Casa</h3>
        <p style="color: #FF4B4B;">{frequencias.get('C', 0.0)}%</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>âœˆï¸ Visitante</h3>
        <p style="color: #4B4BFF;">{frequencias.get('F', 0.0)}%</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>âš–ï¸ Empate</h3>
        <p style="color: #FFD700;">{frequencias.get('E', 0.0)}%</p>
    </div>
    """, unsafe_allow_html=True)

# GrÃ¡fico de frequÃªncias
if show_advanced:
    st.markdown("### ðŸ“ˆ DistribuiÃ§Ã£o dos Resultados no HistÃ³rico Completo")
    chart_data = pd.DataFrame({
        'Resultado': ['Casa', 'Visitante', 'Empate'],
        'FrequÃªncia': [frequencias.get('C', 0.0), frequencias.get('F', 0.0), frequencias.get('E', 0.0)],
        'Cor': ['#FF4B4B', '#4B4BFF', '#FFD700']
    })
    
    st.bar_chart(chart_data.set_index('Resultado')['FrequÃªncia'])

# --- RODAPÃ‰ ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; margin-top: 2rem;">
    <p>âš½ Football Studio Live Analyzer v2.5 | AnÃ¡lise Inteligente de PadrÃµes</p>
    <p><small>Desenvolvido para Evolution Gaming Football Studio</small></p>
</div>
""", unsafe_allow_html=True)
