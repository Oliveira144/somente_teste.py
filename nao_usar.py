import streamlit as st
import collections
import random
import numpy as np
import pandas as pd
from datetime import datetime
# --- CLASSE ANALISEPADROES REFINADA E AJUSTADA ---
    Classe para analisar padrões em um histórico de resultados de jogos
    (ex: 'C' para Casa, 'F' para Fora, 'E' para Empate) e gerar sugestões.
    """
    def __init__(self, histórico: lista):
        """
        Inicializa uma aula com um histórico de resultados.
        O histórico é truncado para os últimos 50 jogos para foco na análise recente.

        Argumentos:
            histórico (lista): Uma lista de strings representando os resultados dos jogos.
                               Exemplo: ['Dó', 'Fá', 'Mi', 'Dó', 'Dó']
        """
        # Limita o histórico aos últimos 50 jogos para análise.
        # Suponha que o histórico esteja sempre com o mais recente primeiro (insert(0))
        self.histórico = histórico[-54:]
        self.historico.reverse() if len(histórico) > 50 else histórico[:]

        self.padroes_ativos_map = {
            #Padres Básicos
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
            "Padrão Dragão Tigre": self._padrao_dragon_tiger,
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

        # Pesos dos padrões para calcular uma sugestão de confiança.
        # Ajustei os pesos para os padrões novos darem mais relevância ao "surf"
        self.pesos_padroes = {
            "Sequência (Surf de Cor)": 1.2,
            "Zig-Zag Perfeito": 1.0,
            "Quebra de Surf": 1.1,
            "Quebra de Zig-Zag": 1.0,
            "Duplas Repetidas": 0,8,
            "Empate Recorrente": 1.3,
            "Padrão Escada": 0.7,
            "Espelho": 0,9,
            "Alternância com Empate": 0,9,
            "Padrão Onda": 0.8,
            "Padrão Fibonacci": 1.0,
            "Sequência Dourada": 1.0,
            "Padrão Triangular": 0,8,
            "Ciclo de Empates": 1.4,
            "Padrão Martingale": 1.1,
            "Sequência de Fibonacci Invertida": 1.0,
            "Padrão Dragão Tigre": 1,2,
            "Sequência de Paroli": 0,9,
            "Padrão de Ondas Longas": 1.3,
            "Ciclo de Dominância": 1.1,
            "Padrão de Tensão": 1.0,
            "Sequência de Labouchere": 0,7,
            "Padrão Ritmo Cardíaco": 0,8,
            "Ciclo de Pressão": 0,9,
            "Padrão de Clusters": 0,8,
            "Sequência Polar": 1.0,
            "Padrão de Momentum": 1.2,
            "Ciclo de Respiração": 0,9,
            "Padrão de Resistência": 1.1,
            "Sequência de Breakout": 1.2,
            
            # Pesos para os novos padrões (aumentados para priorizar o "surf")
            "Padrão 2x1x2": 1.6, # Peso alto para indicar continuidade (AA B AA)
            "Padrão 2x2": 1.4, # Relevância para o 2x2
            "Padrão 3x3": 1.7, # Peso mais alto para sequências mais longas de duplas
            "Padrão 4x4": 1.9, # Peso ainda mais alto
        }

    def analisar_todos(self) -> dict:
        """
        Analise o histórico para detectar quais padrões são ativos.
        Devoluções:
            dict: Um dicionário onde as chaves são os nomes dos padrões e os valores
                  sÃ£o True se o padrÃ£o for detectado, False caso contrario.
        """
        resultados = {}
        para nome, func em self.padroes_ativos_map.items():
            tentar:
                resultados[nome] = func()
            exceto Exceção como e:
                #É bom manter toras embutidas para depuração, mesmo que Streamlit capture exceções
                st.session_state.log_messages.append(f"[{datetime.now().strftime('%H:%M:%S')}] [ERROR] Erro ao analisar o padrão '{nome}': {e}")
                resultados[nome] = False
        retornar resultados

    # --- Métodos Auxiliares Internos ---
    def _get_last_result(self) -> str | Nenhum:
        """Retorna o último resultado do histórico, se houver."""
        retornar self.historico[0] se self.historico senão Nenhum
    
    def _get_second_last_result(self) -> str | Nenhum:
        """Retorna o penúltimo resultado do histórico, se houver."""
        retornar self.historico[1] se len(self.historico) >= 2 senão Nenhum

    def _get_result_counts_in_window(self, window_size: int) -> coleções.Contador:
        """
        Retorna a contagem de cada resultado em uma janela recente do histórico.
        """
        se len(self.historico) < window_size:
            retornar coleções.Counter(self.historico)
        retornar coleções.Counter(self.historico[:window_size])

    # --- PADRÕES BÁSICOS EXISTENTES ---
    def _sequencia_simples(self) -> bool:
        if len(self.historico) < 3: return False
        retornar self.historico[0] == self.historico[1] == self.historico[2]

    def _zig_zag(self) -> bool:
        if len(self.historico) < 6: return False
        para i no intervalo(5):
            se self.historico[i] == self.historico[i+1]: retornar Falso
        retornar Verdadeiro

    def _quebra_de_surf(self) -> bool:
        if len(self.historico) < 4: return False
        retornar (self.historico[0] == self.historico[1] == self.historico[2] e
                self.histórico[2] != self.histórico[3])

    def _quebra_de_zig_zag(self) -> bool:
        if len(self.historico) < 5: return False
        retornar (self.historico[0] != self.historico[1] e
                self.historico[1] != self.historico[2] e
                self.historico[2] != self.historico[3] e
                self.histórico[3] == self.histórico[4])

    def _duplas_repetidas(self) -> bool:
        if len(self.historico) < 4: return False
        # Este padrão específico é CCFF
        retornar (self.historico[0] == self.historico[1] e
                self.historico[2] == self.historico[3] e
                self.histórico[0] != self.histórico[2])

    def _empate_recorrente(self) -> bool:
        empates_indices = [i para i, r em enumerate(self.historico) se r == 'E']
        se len(empates_indices) < 3: retornar Falso
        intervals = np.diff(empates_indices) # Corrigido para usar empates_indices
        se len(intervalos) >= 2:
            media_intervalo = np.mean(intervalos)
            # Ajustando a tolerância para ser mais flexível em "recorrente"
            retornar 2 <= media_intervalo <= 8 e np.std(intervals) <media_intervalo * 0,8
        retornar Falso

    def _padrao_escada(self) -> bool:
        if len(self.historico) < 6: return False
        retornar (self.historico[0] != self.historico[1] e
                self.historico[1] == self.historico[2] e
                self.historico[3] == self.historico[4] == self.historico[5] e
                self.histórico[1] != self.histórico[3])

    def _espelho(self) -> bool:
        para tamanho no intervalo(4, min(len(self.historico) + 1, 13), 2):
            metade = tamanho // 2
            segmento = self.historico[:tamanho]
            if segmento[:metade] == segmento[metade:][::-1]:
                retornar Verdadeiro
        retornar Falso

    def _alternancia_empate_meio(self) -> bool:
        if len(self.historico) < 3: return False
        return (self.historico[0] != 'E' e self.historico[1] == 'E' e
                self.historico[2] != 'E' e self.historico[0] != self.historico[2])

    def _padrao_onda(self) -> bool:
        if len(self.historico) < 6: return False
        retornar (self.historico[0] == self.historico[2] == self.historico[4] e
                self.historico[1] == self.historico[3] == self.historico[5] e
                self.histórico[0] != self.histórico[1])

    # --- NOVOS PADRÕES ESPECÍFICOS DO FOOTBALL STUDIO ---
    def _padrao_fibonacci(self) -> bool:
        if len(self.historico) < 8: return False
        fib_lengths = [1, 1, 2, 3] # Representa C, F, CC, FFF (alternando)
        idx_atual = 0
        resultados_a_verificar = self.historico[:]
        tentar:
            para comprimento em fib_lengths:
                se current_idx + comprimento > len(resultados_a_verificar): retornar Falso
                bloco = resultados_a_verificar[idx_atual : idx_atual + comprimento]
                se não bloquear ou não todos(x == bloco[0] para x no bloco): retornar Falso # Verifica se o bloco é uniforme
                # Verifique se o bloco atual é diferente do anterior, garantindo alternância
                se current_idx > 0 e block[0] == results_to_check[current_idx - 1]: retornar Falso
                current_idx += comprimento
            retornar Verdadeiro
        exceto IndexError: retornar False
        
    def _sequencia_dourada(self) -> bool:
        if len(self.historico) < 8: return False
        return (self.historico[0] == self.historico[1] == self.historico[2] e # 3 do mesmo
                self.historico[3] == self.historico[4] == self.historico[5] == self.historico[6] == self.historico[7] e # 5 do mesmo
                self.historico[0] != self.historico[3]) # Mais diferentes entre si

    def _padrao_triangular(self) -> bool:
        if len(self.historico) < 9: return False
        segmento = self.historico[:9]
        # Padrão: ABCDCBAEA (onde A é o resultado mais externo, e E é o do meio)
        # Ajuste para verificar se o centro (segment[4]) é o mesmo da base (segment[0])
        # e se a parte central é uniforme (ex: CCC)
        retornar (segmento[0] == segmento[8] e segmento[1] == segmento[7] e
                segmento[2] == segmento[6] e segmento[3] == segmento[5] e
                segment[0] != segment[4]) # A base é diferente do pico/centro do triângulo

    def _ciclo_empates(self) -> bool:
        empates = [i para i, x em enumerate(self.historico) se x == 'E']
        se len(empates) <3: retorne Falso
        # Procura por intervalos regulares entre empates
        intervalos = np.diff(empatas)
        se len(intervalos) >= 2:
            media_intervalo = np.mean(intervalos)
            # Um ciclo é mais forte se os intervalos são consistentes
            return np.std(intervals) < 1.5 and 2 <= media_intervalo <= 7 # Intervalos médios entre 2 e 7 jogos

    def _padrao_martingale(self) -> bool:
        if len(self.historico) < 7: return False
        # Ex: ABBCCCC (após uma quebra, uma sequência forte)
        return (self.historico[0] != self.historico[1] e # A quebra
                self.historico[1] == self.historico[2] e # BB
                self.historico[3] == self.historico[4] == self.historico[5] == self.historico[6] e # CCCC
                self.historico[1] != self.historico[3]) # B diferente de C

    def _fibonacci_invertida(self) -> bool:
        if len(self.historico) < 8: return False
        # Ex: CCFFCCFF (sequências curtas e alternadas)
        # Mais genérico: Dupla A, Dupla B, Dupla C, Dupla D, onde A!=B, B!=C, C!=D
        return (self.historico[0] == self.historico[1] e # Dupla 1
                self.historico[2] == self.historico[3] e # Dupla 2
                self.historico[4] == self.historico[5] e # Dupla 3
                self.historico[6] == self.historico[7] e # Dupla 4
                self.historico[0] != self.historico[2] e # Dupla 1 diferente de Dupla 2
                self.historico[2] != self.historico[4] e # Dupla 2 diferente de Dupla 3
                self.historico[4] != self.historico[6]) # Dupla 3 diferente de Dupla 4

    def _padrao_dragon_tiger(self) -> bool:
        if len(self.historico) < 6: return False
        # Ex: CFCEFF (Alternância, um empate, e uma dupla)
        return (self.historico[0] != self.historico[1] e self.historico[1] != self.historico[2] e # Zig-zag inicial
                self.historico[3] == 'E' e # Um empate no meio
                self.historico[4] == self.historico[5] e # Uma dupla
                self.historico[4] != 'E') # E não pode ser o da dupla

    def _sequencia_paroli(self) -> bool:
        if len(self.historico) < 8: return False
        # Ex: CFFCCCCC (Quebra, dupla, sequência longa, e o primeiro e o último são iguais)
        return (self.historico[0] != self.historico[1] e # Quebra
                self.historico[1] == self.historico[2] e # Dupla
                self.historico[3] == self.historico[4] == self.historico[5] == self.historico[6] e # Sequência de 4
                self.historico[0] == self.historico[7]) # O primeiro e o oitavo são iguais

    def _ondas_longas(self) -> bool:
        if len(self.historico) < 5: return False
        contagem = 1
        para i no intervalo(1, len(self.historico)):
            se self.historico[i] == self.historico[i-1]:
                contagem += 1
                if count >= 5: return True # Detecta qualquer sequência de 5 ou mais
            caso contrário: contagem = 1
        retornar Falso

    def _ciclo_dominância(self) -> bool:
        if len(self.historico) < 10: return False
        janela = self.historico[:10]
        contador = coleções.Contador(janela)
        para _, conte em counter.items():
            if count >= 7: return True # Um resultado domina 70% da janela

        retornar Falso

    def _padrao_tensao(self) -> bool:
        if len(self.historico) < 7: return False
        # Ex: CFCFCCC (Alternância que se "quebra" em uma sequência forte)
        alternations_ok = (self.historico[0] != self.historico[1] e
                           self.historico[1] != self.historico[2] e
                           self.historico[2] != self.historico[3]) # As 3 primeiras alternâncias
        
        sequencia_break = (self.historico[3] == self.historico[4] == self.historico[5] == self.historico[6]) # Uma sequência de 4
        
        return alternations_ok and sequencia_break and (self.historico[2] != self.historico[3]) # A alternância quebrada pela sequência

    def _sequencia_labouchere(self) -> bool:
        if len(self.historico) < 6: return False
        # Ex: CFXXFC (primeiro e último igual, segundo e penúltimo igual, meio diferente)
        segmento = self.historico[:6]
        retornar (segmento[0] == segmento[5] e segmento[1] == segmento[4] e
                segment[2] != segment[0] and segment[3] != segment[0] and segment[2] == segment[3]) # Meio é uma dupla diferente

    def _ritmo_cardiaco(self) -> bool:
        if len(self.historico) < 8: return False
        # Ex: CCFCCFFF (Dupla, quebra, dupla, quebra, tripla)
        segmento = self.historico[:8]
        retornar (segmento[0] == segmento[1] e segmento[2] != segmento[0] e # Dupla A, Quebra
                segmento[3] == segmento[4] e segmento[5] != segmento[3] e # Dupla B, Quebra
                segmento[5] == segmento[6] == segmento[7]) # Tripla C, B diferente de C

    def _ciclo_pressão(self) -> bool:
        if len(self.historico) < 9: return False
        # Ex: ABBCCCABB (repetição de padrões pequenos em um ciclo)
        return (self.historico[0] != self.historico[1] e self.historico[1] == self.historico[2] e # ABB
                self.historico[3] == self.historico[4] == self.historico[5] e # CCC
                self.historico[6] == self.historico[0] e # Repete A
                self.historico[7] == self.historico[1] e self.historico[8] == self.historico[2]) # Repete BB

    def _padrao_clusters(self) -> bool:
        if len(self.historico) < 12: return False
        # Procura por "blocos" densos de resultados do mesmo tipo
        janela = self.historico[:12]
        cluster1 = janela[0:4]
        cluster2 = janela[4:8]
        cluster3 = janela[8:12]
        # Pelo menos 3 do mesmo em cada cluster de 4
        retornar (collections.Counter(cluster1).most_common(1)[0][1] >= 3 e
                coleções.Counter(cluster2).most_common(1)[0][1] >= 3 e
                coleções.Contador(cluster3).most_common(1)[0][1] >= 3)

    def _sequencia_polar(self) -> bool:
        if len(self.historico) < 10: return False
        #Alternância extrema entre dois resultados sem empates
        janela = self.historico[:10]
        resultados_únicos = definir(janela)
        se len(unique_results) == 2 e 'E' não estiver em unique_results:
            alterações = soma(1 para j no intervalo(len(janela)-1) se janela[j] != janela[j+1])
            return change >= 6 # Pelo menos 6 mudanças em 9 possíveis (alta alternância)
        retornar Falso

    def _padrao_momentum(self) -> bool:
        if len(self.historico) < 10: return False
        # Ex: ABBCCCDDDD (sequências crescentes de resultados diferentes)
        retornar (self.historico[0] != self.historico[1] e self.historico[1] == self.historico[2] e # 1x A, 2x B
                self.historico[3] == self.historico[4] == self.historico[5] e # 3x C
                self.historico[6] == self.historico[7] == self.historico[8] == self.historico[9] e # 4x D
                self.historico[1] != self.historico[3] e self.historico[3] != self.historico[6]) # B != C != D

    def _ciclo_respiracao(self) -> bool:
        if len(self.historico) < 8: return False
        # Ex: AAAABCCC (Sequência longa, quebra e nova sequência)
        return (self.historico[0] == self.historico[1] == self.historico[2] == self.historico[3] e # Sequência de 4
                self.historico[4] != self.historico[0] e # Quebra
                self.historico[5] == self.historico[6] == self.historico[7] e # Nova sequência de 3
                self.historico[5] != self.historico[4]) # E a nova sequência é diferente da quebra

    def _padrao_resistencia(self) -> bool:
        if len(self.historico) < 6: return False
        # Ex: ABACAA (um resultado 'A' aparece e 'resiste' a interrupções)
        return (self.historico[0] == self.historico[2] == self.historico[4] == self.historico[5] e # A em posições específicas
                self.historico[1] != self.historico[0] and self.historico[3] != self.historico[0]) # Interrupções são diferentes de A

    def _sequencia_breakout(self) -> bool:
        if len(self.historico) < 8: return False
        # Ex: AAAABBBB (sequência longa, quebra e nova sequência longa do tipo da quebra)
        return (self.historico[0] == self.historico[1] == self.historico[2] == self.historico[3] e # Sequência AAAA
                self.historico[4] != self.historico[0] e # Quebra para B
                self.historico[5] == self.historico[6] == self.historico[7] e #Sequência BBB
                self.historico[5] == self.historico[4]) # O resultado da quebra inicia uma nova sequência

    # --- NOVOS PADRÕES SOLICITADOS ---
    def _padrao_2x1x2(self) -> bool:
        if len(self.historico) < 5: return False
        # Ex: CCFCC ou FFCF F.
        # Verifique se os dois primeiros são iguais, o terceiro é diferente,
        # e o quarto e quinto são iguais ao primeiro e segundo.
        return (self.historico[0] == self.historico[1] e # Dois do mesmo (primeira dupla)
                self.historico[2] != self.historico[0] e # Um diferente
                self.historico[3] == self.historico[4] e # Dois do mesmo (segunda dupla)
                self.historico[0] == self.historico[3]) # As duplas são do mesmo tipo

    def _padrao_2x2(self) -> bool:
        if len(self.historico) < 4: return False
        # Ex: CCFF ou FFC C.
        # Verifique se os dois primeiros são iguais e os dois próximos são iguais, mas diferentes entre si.
        return (self.historico[0] == self.historico[1] e # Dois do mesmo
                self.historico[2] == self.historico[3] e # Dois do outro
                self.historico[0] != self.historico[2]) # Os pares são de tipos diferentes

    def _padrao_3x3(self) -> bool:
        if len(self.historico) < 6: return False
        # Ex: CCCFFF ou FFFCC C.
        # Verifique se os três primeiros são iguais e os três próximos são iguais, mas diferentes entre si.
        return (self.historico[0] == self.historico[1] == self.historico[2] e # Três do mesmo
                self.historico[3] == self.historico[4] == self.historico[5] e # Três do outro
                self.historico[0] != self.historico[3]) # Os trios são de tipos diferentes

    def _padrao_4x4(self) -> bool:
        if len(self.historico) < 8: return False
        # Ex: CCCCFFFF ou FFFFCCC C.
        # Verifique se os quatro primeiros são iguais e os quatro próximos são iguais, mas diferentes entre si.
        return (self.historico[0] == self.historico[1] == self.historico[2] == self.historico[3] e # Quatro do mesmo
                self.historico[4] == self.historico[5] == self.historico[6] == self.historico[7] e # Quatro do outro
                self.historico[0] != self.historico[4]) # Os quartetos são de tipos diferentes


    def_calcularfrequências(self):
        """Calcula frequências dos resultados"""
        contador = coleções.Contador(self.histórico)
        total = len(self.historico)
        se total == 0: retorne {'C': 0, 'F': 0, 'E': 0}
        
        resultado = {k: round(v / total * 100, 1) para k, v em contador.items()}
        para tipo em ['C', 'F', 'E']:
            se tipo não estiver no resultado:
                resultado[tipo] = 0
        retornar resultado

    def calcular_tendencia(self):
        """Calcula tendência dos últimos resultados"""
        if len(self.historico) < 5: return "Dados insuficientes"
        
        últimos_5 = self.histórico[:5]
        contador = coleções.Contador(últimos_5)
        
        # Considere a tendência se um resultado aparece 3 ou mais vezes nos últimos 5.
        # Ajustado para ser mais sensato
        se contador.most_common(1)[0][1] >= 4:
            return f"Forte tendência: {contador.most_common(1)[0][0]}"
        elif contador.most_common(1)[0][1] == 3:
            return f"Tendência moderada: {contador.most_common(1)[0][0]}"
        outro:
            return "Sem tendência clara"

    def gerar_sugestao(self) -> dict: # CORRIGIDO: Nome do método de 'generar_sugestao' para 'gerar_sugestao'
        """
        Gera uma sugestão de próximo resultado com base em padrões ativos e seus pesos,
        além de considerar a tendência mais recente.
        """
        se não auto.histórico:
            retornar {
                "sugerir": Falso, "entrada": Nenhum, "entrada_codigo": Nenhum,
                "motivos": ["Nenhum histórico para análise."], "confianca": 0.0,
                "frequências": self.calcular_frequencias(), "tendência": "Sem dados",
                "últimos_resultados": [], "analise_detalhada": {}, "pontuacoes_brutas": {'C':0, 'F':0, 'E':0}
            }

        padroes_ativos = self.analisar_todos()
        
        pontuações = {'C': 0,0, 'F': 0,0, 'E': 0,0}
        
        último_resultado = self._get_last_result()
        segundo_último_resultado = self._obter_segundo_último_resultado()
        
        motivos_sugestao = []
        total_peso_padroes = 0,0
        
        for nome_padrao, ativo em padroes_ativos.items():
            se ativo:
                peso = self.pesos_padroes.get(nome_padrao, 0,5)
                motivos_sugestao.append(nome_padrao)
                total_peso_padroes += peso

                # Lógica de pontuação para cada padrão ativo
                if nome_padrao == "Sequência (Surf de Cor)":
                    if last_result: pontuacoes[last_result] += peso * 2.0 # Peso maior para continuar o surf

                elif nome_padrao == "Zig-Zag Perfeito":
                    if último_resultado == 'C': pontuacoes['F'] += peso
                    elif último_resultado == 'F': pontuacoes['C'] += peso
                    
                elif nome_padrao == "Quebra de Surf":
                    # Este padrão indica que a sequência anterior de 3 foi quebrada pelo 4º resultado.
                    # A sugestão seria apostar NO resultado que QUEBROU a sequência.
                    if len(self.historico) >= 4 e self.historico[0] == self.historico[1] == self.historico[2] e self.historico[2] != self.historico[3]:
                        pontuacoes[self.historico[3]] += peso * 0.8 # Menor peso, pois é uma quebra

                elif nome_padrao == "Quebra de Zig-Zag":
                    # Este padrão indica que o zig-zag foi quebrado.
                    # A sugestão é seguir o resultado que corte a alternância.
                    se len(self.historico) >= 5 e self.historico[3] == self.historico[4]:
                        pontuacoes[self.historico[3]] += peso * 0.8 # Menor peso para quebra

                elif nome_padrao == "Duplas Repetidas": #CCFF
                    if len(self.historico) >= 4 e self.historico[0] == self.historico[1] e self.historico[2] == self.historico[3] e self.historico[0] != self.historico[2]:
                        pontuacoes[self.historico[0]] += peso # Sugere a continuação da primeira dupla

                elif nome_padrao == "Empate Recorrente":
                    pontuacoes['E'] += peso * 1,5

                elif nome_padrao == "Padrão Escada":
                    # Ex: ABBCC C. Sugere quebrar o CCC e voltar para B (ou E se aplicável)
                    se len(self.historico) >= 6 e self.historico[1] == self.historico[2] e self.historico[3] == self.historico[4] == self.historico[5]:
                        if self.historico[0] == 'C': pontuacoes['F'] += peso # Se A foi C, sugerindo F
                        elif self.historico[0] == 'F': pontuacoes['C'] += peso # Se A foi F, sugerindo C
                        else: pontuacoes['E'] += peso # Se A foi E, sugerindo E (menos provável)
                        
                elif nome_padrao == "Espelho":
                    # Se há um espelho (por exemplo, CFEFC), o próximo seria a 'continuação' do espelho.
                    # Para simplificar, pode-se sugerir o oposto do último para manter a simetria ou o próximo do "espelho"
                    if último_resultado == 'C': pontuacoes['F'] += peso * 0,7
                    elif último_resultado == 'F': pontuações['C'] += peso * 0.7
                    elif last_result == 'E': pontuacoes['E'] += peso * 0.5 # Empates podem quebrar espelhos facilmente

                elif nome_padrao == "Alternância com Empate":
                    # Ex: CE F. O próximo seria C.
                    if len(self.historico) >= 3 e self.historico[1] == 'E' e self.historico[0] != self.historico[2]:
                        pontuacoes[self.historico[0]] += peso * 1.0 # Sugere o que alternou com E

                elif nome_padrao == "Padrão Onda": # CFCFCF
                    if len(self.historico) >= 6 e self.historico[0] == self.historico[2] == self.historico[4] e self.historico[1] == self.historico[3] == self.historico[5]:
                        pontuacoes[self.historico[1]] += peso # Sugere o oposto do último resultado

                elif nome_padrao == "Padrão Fibonacci": # 1, 1, 2, 3 (alternando)
                    # Se terminou em uma sequência de 3 (ex: FFF), ou próximo seria C (inversão)
                    if último_resultado == 'C': pontuacoes['F'] += peso * 1.1
                    elif último_resultado == 'F': pontuações['C'] += peso * 1.1
                    elif último_resultado == 'E': pontuacoes['E'] += peso * 0.8

                elif nome_padrao == "Sequência Dourada": # 3 de um, 5 do outro
                    se len(self.historico) >= 8 e self.historico[3] == self.historico[4]:
                        pontuacoes[self.historico[3]] += peso * 1.2 # Sugere continuar a sequência de 5

                elif nome_padrao == "Padrão Triangular": # ABCDCBAEA
                    se len(self.historico) >= 9 e self.historico[0] == self.historico[8]:
                        if self.historico[4] == 'C': pontuações['F'] += peso # Sugere o oposto do meio
                        elif self.historico[4] == 'F': pontuacoes['C'] += peso
                        elif self.historico[4] == 'E': pontuacoes['E'] += peso * 0.8

                elif nome_padrao == "Ciclo de Empates":
                    pontuacoes['E'] += peso * 1.8 # Forte sugestão de Empate

                elif nome_padrao == "Padrão Martingale": # ABBCCCC
                    se len(self.historico) >= 7 e self.historico[3] == self.historico[4]:
                        pontuacoes[self.historico[3]] += peso * 1.5 # Sugere continuar a sequência forte

                elif nome_padrao == "Sequência de Fibonacci Invertida": # 2x, 1x, 2x, 1x
                    if último_resultado == 'C': pontuacoes['F'] += peso * 1.1
                    elif último_resultado == 'F': pontuações['C'] += peso * 1.1
                    elif último_resultado == 'E': pontuacoes['E'] += peso * 0.8

                elif nome_padrao == "Padrão Dragão Tigre": # CFCEFF
                    se len(self.historico) >= 6 e self.historico[4] == self.historico[5]:
                        pontuacoes[self.historico[4]] += peso * 1.3 # Sugere continuar a última dupla

                elif nome_padrao == "Sequência de Paroli": # CFFCCCCC
                    se len(self.historico) >= 8 e self.historico[0] == self.historico[7]:
                        pontuacoes[self.historico[0]] += peso * 1.2 # Sugere o resultado que "fechou" a sequência

                elif nome_padrao == "Padrão de Ondas Longas":
                    if último_resultado: pontuacoes[último_resultado] += peso * 2.0 # Muito forte para continuar a onda

                elif nome_padrao == "Ciclo de Dominância":
                    resultado_dominante = coleções.Contador(self.historico[:10]).mais_comum(1)[0][0]
                    pontuacoes[dominant_result] += peso * 1.1 # Sugere o dominante

                elif nome_padrao == "Padrão de Tensão": # CFCFCCC
                    se len(self.historico) >= 7 e self.historico[4] == self.historico[5] == self.historico[6]:
                        pontuacoes[self.historico[4]] += peso * 1.2 # Sugere continuar a sequência final

                elif nome_padrao == "Sequência de Labouchere": # CFXXFC
                    se len(self.historico) >= 6 e self.historico[0] == self.historico[5]:
                        if last_result == 'C': pontuacoes['F'] += peso * 0.8 # Sugere alternância se o padrão para espelho
                        elif último_resultado == 'F': pontuações['C'] += peso * 0.8
                        elif último_resultado == 'E': pontuacoes['E'] += peso * 0.5

                elif nome_padrao == "Padrão Ritmo Cardíaco": # CCFCCFFF
                    if len(self.historico) < 8: return False # Já selecionado na função do padrão
                    outro:
                        if self.historico[5] == self.historico[6] == self.historico[7]:
                            if self.historico[5] == 'C': pontuações['F'] += peso * 0.7 # Sugere o oposto da última sequência
                            elif self.historico[5] == 'F': pontuacoes['C'] += peso * 0.7
                            elif self.historico[5] == 'E': pontuacoes['E'] += peso * 0.7

                elif nome_padrao == "Ciclo de Pressão": # ABBCCCABB
                    se len(self.historico) >= 9 e self.historico[6] == self.historico[0]:
                        pontuacoes[self.historico[0]] += peso * 1.1 # Sugere a continuação do ciclo

                elif nome_padrao == "Padrão de Clusters":
                    se len(self.historico) >= 12:
                        último_cluster_dominante = coleções.Contador(self.historico[8:12]).mais_comum(1)[0][0]
                        pontuacoes[last_cluster_dominant] += peso * 1.0 # Sugere continuar o último cluster

                elif nome_padrao == "Sequência Polar":
                    se len(self.historico) >= 10:
                        if last_result == 'C': pontuações['F'] += peso * 1.0 # Sugira o oposto para manter a polaridade
                        elif último_resultado == 'F': pontuações['C'] += peso * 1.0

                elif nome_padrao == "Padrão de Momentum": # ABBCCCDDDD
                    se len(self.historico) >= 10 e self.historico[6] == self.historico[7]:
                        pontuacoes[self.historico[6]] += peso * 1.4 # Sugere continuar a Última sequência forte

                elif nome_padrao == "Ciclo de Respiração": # AAAABCCC
                    if len(self.historico) < 8: pass # Já selecionado na função do padrão
                    outro:
                        pontuacoes[self.historico[5]] += peso * 1.1 # Sugere continuar a última sequência

                elif nome_padrao == "Padrão de Resistência": # ABACAA
                    if len(self.historico) < 6: pass # Já selecionado na função do padrão
                    outro:
                        pontuacoes[self.historico[0]] += peso * 1.2 # Sugere continuar o resultado "resistente"

                elif nome_padrao == "Sequência de Breakout": # AAAABBBB
                    if len(self.historico) < 8: pass # Já selecionado na função do padrão
                    outro:
                        pontuacoes[self.historico[5]] += peso * 1.5 # Sugere continuar a sequência que se "consolidou"

                # Lógica de pontuação para os NOVOS PADRÕES SOLICITADOS
                elif nome_padrao == "Padrão 2x1x2": # CCFCC -> Sugere C (o tipo que se repete)
                    se len(self.historico) >= 4 e self.historico[0] == self.historico[1] e self.historico[0] == self.historico[3]:
                        pontuacoes[self.historico[0]] += peso * 1.5 # Forte sugestão de continuar o resultado dominante

                elif nome_padrao == "Padrão 2x2": # CCFF -> Sugere C (o tipo da primeira dupla para reiniciar o ciclo)
                    se len(self.historico) >= 4 e self.historico[0] == self.historico[1] e self.historico[2] == self.historico[3]:
                        pontuacoes[self.historico[0]] += peso * 1.0
                        
                elif nome_padrao == "Padrão 3x3": # CCCFFF -> Sugere C (o tipo da primeira tripla para reiniciar o ciclo)
                    if len(self.historico) >= 6 e self.historico[0] == self.historico[1] == self.historico[2] e self.historico[3] == self.historico[4] == self.historico[5]:
                        pontuacoes[self.historico[0]] += peso * 1.2

                elif nome_padrao == "Padrão 4x4": # CCCCFFFF -> Sugere C (o tipo da primeira sequência de 4 para reiniciar o ciclo)
                    if len(self.historico) >= 8 e self.historico[0] == self.historico[1] == self.historico[2] == self.historico[3] e \
                       self.historico[4] == self.historico[5] == self.historico[6] == self.historico[7]:
                        pontuacoes[self.historico[0]] += peso * 1.4
        
        # 2. Adicionar uma pontuação baseada na tendência mais recente (últimos 3-5 jogos)
        recentes_window = self.histórico[:min(len(self.histórico), 5)]
        se recentes_window:
            contagem_recentes = coleções.Contador(janela_recentes)
            para resultado, conte em contagem_recentes.items():
                se o resultado for pontuacoes:
                    pontuacoes[resultado] += contagem * 0,2

        #3. Determinar a sugestão final
        melhor_sugestao_codigo = "N/A"
        maior_pontuacao = -1.0

        se houver(pontuacoes.values()):
            resultados_ordenados = ordenados(pontuacoes.items(), key=lambda item: item[1], reverso=True)
            melhor_sugestao_codigo = resultados_ordenados[0][0]
            maior_pontuacao = resultados_ordenados[0][1]

            # Lógica para favorecer Empate se a pontuação para próxima (ajuste delicado)
            # if 'E' em pontuacoes e pontuacoes['E'] > 0 e \
            # (maior_pontuacao > 0 e (pontuacoes['E'] >= maior_pontuacao * 0.9 e pontuacoes['E'] < maior_pontuacao)):
            # melhor_sugestao_codigo = 'E'
        outro:
            # Se nenhuma pontuação for gerada pelos padrões, use a frequência mais baixa como sugestão
            frequências = self.calcular_frequencias()
            se frequências:
                # Sugere o resultado com menor frequência (equilíbrio)
                melhor_sugestao_codigo = min(frequências, key=frequências.get)
            outro:
                melhor_sugestao_codigo = random.choice(['C', 'F', 'E'])
                
        total_pontuacao_geral = soma(pontuacoes.valores())
        confianca_percentual = (maior_pontuacao / total_pontuacao_geral) * 100 if total_pontuacao_geral > 0 else 0

        mapeamento_legivel = {"C": "Casa", "F": "Visitante", "E": "Empate"}
        
        retornar {
            "sugerir": Verdade,
            "entrada": mapeamento_legivel.get(melhor_sugestao_codigo, "N/A"),
            "entrada_codigo": melhor_sugestao_codigo,
            "motivos": motives_sugestao,
            "confianca": min(99, int(confianca_percentual)),
            "frequências": self.calcular_frequencias(),
            "tendência": self.calcular_tendencia(),
            "últimos_resultados": self.historico[:5],
            "analise_detalhada": self._gerar_analise_detalhada(motivos_sugestao),
            "pontuacoes_brutas": pontuacoes # Adicionado para depuração
        }

    def _gerar_analise_detalhada(self, padrões):
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
        
        analisar = {}
        para categoria, palavras-chave em categorias.items():
            padroes_categoria = [p para p em padroes se houver(k.lower() em p.lower() para k em palavras-chave)]
            se padrões_categoria:
                analise[categoria] = padroes_categoria
        
        retornar análise

# --- FUNÇÕES DE INTERFACE E LÓGICA DE HISTÓRICO ---

# Inicializa o estado da sessão
se 'historico' não estiver em st.session_state:
    # Histórico de exemplo, pode ser vazio ou com alguns dados para começar
    # st.session_state.historico = [] # Se quiser começar completamente vazio
    st.session_state.historico = ['C', 'F', 'C', 'E', 'F', 'F', 'C', 'C', 'E', 'F']
    
se 'estatisticas' não estiver em st.session_state:
    st.session_state.estatisticas = {
        'total_jogos': 0,
        'acertos': 0,
        'erros': 0,
        'ultima_sugestao': None # Guarda a última sugestão para validação
    }

# Para capturar e exibir logs/erros na UI (opcional)
se 'log_messages' não estiver em st.session_state:
    st.session_state.log_messages = []

def log_message(tipo, mensagem):
    st.session_state.log_messages.append(f"[{datetime.now().strftime('%H:%M:%S')}] [{type.upper()}] {mensagem}")
    if len(st.session_state.log_messages) > 50: # Limite de tamanho do log
        st.session_state.log_messages.pop(0)

def adicionar_resultado(resultado):
    """Adiciona novo resultado ao histórico e valida a sugestão anterior."""
    # Valida a sugestão anterior ANTES de adicionar o novo resultado ao histórico principal.
    # Isso garante que a validação use o estado do histórico anterior ao novo jogo.
    if st.session_state.get('ultima_sugestao') e st.session_state.get('sugestao_processada'):
        # A sugestão é validada se foi gerada na rodada anterior
        validar_sugestao(st.session_state.ultima_sugestao, resultado)
        # Limpe a bandeira e a sugestão após a validação
        st.session_state.sugestao_processada = Falso
        st.session_state.ultima_sugestao = Nenhum
    
    st.session_state.historico.insert(0, resultado) # Adicionado no início
    se len(st.session_state.historico) > 50:
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
        'ultima_sugestao': Nenhum
    }
    st.session_state.log_messages = []
    st.session_state.sugestao_processada = False # Redefinir uma flag
    log_message("info", "Histórico e estatísticas limpas.")


def desfazer_ultimo():
    """Remover o último resultado e ajustar as estatísticas."""
    se st.session_state.historico:
        resultado_removido = st.session_state.historico.pop(0)
        # Ao desfazer, também zera uma sugestão para evitar a validação de um jogo que não existe mais.
        st.session_state.ultima_sugestao = Nenhum
        st.session_state.sugestao_processada = Falso
        st.session_state.estatisticas['total_jogos'] = len(st.session_state.historico)
        log_message("info", f"Último resultado '{removed_result}' desejado. Histórico ajustado.")
    outro:
        log_message("warn", "Tentativa de desfazer com histórico vazio.")


def validar_sugestao(sugestao_obj, resultado_real):
    """Valida se a sugestão anterior estava correta"""
    if sugestao_obj e sugestao_obj['entrada_codigo'] == resultado_real:
        st.session_state.estatisticas['acertos'] += 1
        log_message("sucesso", f"Sugestão anterior ACERTADA! Sugerido: {sugestao_obj['entrada_codigo']}, Real: {resultado_real}")
        retornar Verdadeiro
    outro:
        st.session_state.estatisticas['erros'] += 1
        log_message("erro", f"Sugestão anterior ERRADA! Sugerido: {sugestao_obj['entrada_codigo'] if sugestao_obj else 'N/A'}, Real: {resultado_real}")
        retornar Falso

def get_resultado_html(resultado):
    """Retorna HTML para visualização do resultado"""
    mapa de cores = {'C': '#FF4B4B', 'F': '#4B4BFF', 'E': '#FFD700'}
    symbol_map = {'C': 'ðŸ ', 'F': 'âœˆï¸ ', 'E': 'âš–ï¸ '}
    
    retornar f"""
    <div estilo='
        display: inline-flex; /* Use inline-flex para o próprio círculo */
        largura: 32px; /* Um pouco maior para melhor toque no celular */
        altura: 32px;
        raio da borda: 50%;
        background-color: {color_map.get(resultado, 'gray')};
        margin: 2px; /* Manter margem para espaçamento entre círculos */
        align-items: center; /* Centralizar conteúdo verticalmente */
        justify-content: center; /* Centralizar o conteúdo horizontalmente */
        tamanho da fonte: 14px;
        cor: {"preto" if resultado == "E" else "branco"};
        caixa-sombra: 0 2px 4px rgba(0,0,0,0.2);
        flex-shrink: 0; /* Evitar encolhimento */
    '>
        {symbol_map.get(resultado, '?')}
    </div>
    """

def get_confianca_color(confianca):
    """Retorna cor baseada no número de confiança"""
    se confianca >= 80:
        retornar "#4CAF50" # Verde
    elif confianca >= 60:
        retornar "#FF9800" # Laranja
    elif confianca >= 40:
        retornar "#FFC107" # Amarelo
    outro:
        retornar "#F44336" # Vermelho

# --- CONFIGURAÇAO DA PÁ GINA ---
st.set_page_config(
    layout="amplo",
    page_title="ðŸŽ¯ Analisador ao vivo do Football Studio",
    page_icon="âš½",
    initial_sidebar_state="expandido"
)

# CSS Aprimorado
st.markdown("""
<estilo>
/* Estilo geral */
.cabeçalho-principal {
    fundo: gradiente linear (135 graus, #667eea 0%, #764ba2 100%);
    preenchimento: 2rem;
    raio da borda: 10px;
    margem inferior: 2rem;
    alinhamento de texto: centro;
}

.cabeçalho principal h1 {
    cor: branco;
    tamanho da fonte: 2,5 rem;
    margem: 0;
}

.cabeçalho principal p {
    cor: branco;
    tamanho da fonte: 1,2rem;
    margem: 0,5rem 0 0 0;
    opacidade: 0,9;
}

/* BotÃµes */
div.stButton > botão:primeiro-filho {
    tamanho da fonte: 16px;
    preenchimento: 12px 24px;
    raio da borda: 8px;
    cursor: ponteiro;
    margem: 5px;
    cor: branco;
    borda: nenhuma;
    espessura da fonte: negrito;
    transição: todos os 0,3s de facilidade;
    caixa-sombra: 0 4px 8px rgba(0,0,0,0.2);
}

div.stButton > botão:primeiro-filho:hover {
    transformar: translateY(-2px);
    caixa-sombra: 0 6px 12px rgba(0,0,0,0.3);
}

/* Botões específicos */
div.stButton > botão[data-testid="stButton-ðŸ Casa (C)"] {
    fundo: gradiente linear (135 graus, #FF6B6B, #FF4B4B);
}

div.stButton > botão[data-testid="stButton-âœˆï¸ Visitante (F)"] {
    fundo: gradiente linear (135 graus, #4ECDC4, #4B4BFF);
}

div.stButton > botão[data-testid="stButton-âš–ï¸ Empate (E)"] {
    fundo: gradiente linear (135 graus, #FFE66D, #FFD700);
    cor: preto;
}

div.stButton > botão[data-testid="stButton-†©ï¸ Desfazer"],
div.stButton > botão[data-testid="stButton-ðŸ—'ï¸ Limpar"] {
    fundo: gradiente linear (135 graus, #95A5A6, #7F8C8D);
}

/* Cartões de estatísticas */
.cartão-métrico {
    fundo: branco;
    preenchimento: 1,5rem;
    raio da borda: 10px;
    caixa-sombra: 0 4px 6px rgba(0, 0, 0, 0.1);
    borda esquerda: 4px sólido #667eea;
    margem: 1rem 0;
}

.cartão métrico h3 {
    margem: 0 0 0,5rem 0;
    cor: #2C3E50;
}

.cartão métrico p {
    margem: 0;
    tamanho da fonte: 1.1rem;
    espessura da fonte: negrito;
}

/* Sessões */
.cabeçalho-de-seção {
    fundo: gradiente linear (135 graus, #74b9ff, #0984e3);
    cor: branco;
    preenchimento: 1rem;
    raio da borda: 8px;
    margem: 1rem 0;
    alinhamento de texto: centro;
}

.padrão-encontrado {
    fundo: gradiente linear (135 graus, #00b894, #55a3ff);
    cor: branco;
    preenchimento: 0,5rem 1rem;
    raio da borda: 6px;
    margem: 0,25rem 0;
    espessura da fonte: negrito;
}

.padrão-não-encontrado {
    fundo: #f8f9fa;
    cor: #6c757d;
    preenchimento: 0,5rem 1rem;
    raio da borda: 6px;
    margem: 0,25rem 0;
    borda: 1px sólido #dee2e6;
}

.caixa de sugestões {
    fundo: gradiente linear(135 graus, #a8edea, #fed6e3);
    preenchimento: 2rem;
    raio da borda: 12px;
    margem: 1rem 0;
    borda: 2px sólido #667eea;
}

.confiança-alta { cor: #27AE60; peso da fonte: negrito; }
.confiança-médio { cor: #F39C12; peso da fonte: negrito; }
.confiança-baixa { cor: #E74C3C; peso da fonte: negrito; }

/* Histórico de resultados - NOVO ESTILO PARA LINHAS */
.linha histórica {
    exibição: flexível;
    flex-wrap: wrap; /* Alterado de nowrap para wrap */
    justificar-conteúdo: flex-start;
    alinhar-itens: centro;
    margin-bottom: 5px; /* Espaçamento entre linhas */
}

.contêiner histórico {
    fundo: #f8f9fa;
    preenchimento: 1,5rem;
    raio da borda: 10px;
    margem: 1rem 0;
    borda: 1px sólido #dee2e6;
}

/* Garanta que os círculos estejam em bloco para um fluxo adequado dentro do flex */
.historic-container div { /* Segmentando os círculos de resultados */
    display: inline-flex; /* Use inline-flex para o próprio círculo */
    largura: 32px;
    altura: 32px;
    raio da borda: 50%;
    margin: 2px; /* Espaçamento entre círculos */
    alinhar-itens: centro;
    justificar-conteúdo: centro;
    tamanho da fonte: 14px;
    cor: branco;
    caixa-sombra: 0 2px 4px rgba(0,0,0,0.2);
    flex-encolhimento: 0;
}
</estilo>
""", unsafe_allow_html=True)

# --- CABEÇALHO PRINCIPAL ---
st.markdown("""
<div class="cabeçalho-principal">
    <h1>™ Analisador ao vivo do Football Studio</h1>
    <p>Análise Inteligente de PadrÃµes - Evolution Gaming</p>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR COM ESTATÍSTICAS ---
com st.sidebar:
    st.markdown("## ðŸ“Š Estatísticas da Sessão")
    
    total_jogos = st.session_state.estatisticas['total_jogos']
    acertos = st.session_state.estatisticas['acertos']
    erros = st.session_state.estatisticas['erros']
    
    se total_jogos > 0:
        taxa_acerto = (acertos / total_jogos) * 100
        st.metric("Total de Jogos", total_jogos)
        st.metric("Taxa de Acerto", f"{taxa_acerto:.1f}%")
        st.metric("Acertos", acertos)
        st.metric("Erros", erros)
    outro:
        st.info("Nenhum jogo explorado ainda")
    
    st.markdown("---")
    st.markdown("## Configurações")
    
    # auto_suggest = st.checkbox("Sugestão Automática", value=True) # Removido, pois a sugestão é sempre exibida se a confiança for suficiente
    show_advanced = st.checkbox("Análise Avançada", value=True)
    confidence_threshold = st.slider("Limite de Confiança", 0, 100, 60)

    st.markdown("---")
    st.markdown("## ðŸ“ Logs de Depuração")
    log_area = st.empty()
    se st.session_state.log_messages:
        # Exibe os logs mais recentes primeiro
        para logar em reversed(st.session_state.log_messages):
            log_area.texto(log)
    outro:
        log_area.info("Nenhum log ainda.")


# --- SEÇÃO DE INSERÇÃO DE RESULTADOS ---
st.markdown('<div class="section-header"><h2>ðŸŽ¯ Inserir Resultado do Jogo</h2></div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

com col1:
    if st.button("ðŸ Casa (C)", key="CasaC", use_container_width=True, help="Vitória da Casa"):
        adicionar_resultado('C')
        st.rerun()

com col2:
    if st.button("âœˆï¸ Visitante (F)", key="VisitanteF", use_container_width=True, help="Vitória do Visitante"):
        adicionar_resultado('F')
        st.rerun()

com col3:
    se st.button("âš–ï¸ Empate (E)", key="EmpateE", use_container_width=True, help="Empate"):
        adicionar_resultado('E')
        st.rerun()

com col4:
    if st.button("†©ï¸ Desfazer", key="Desfazer", use_container_width=True, help="Desfazer último resultado"):
        desfazer_ultimo()
        st.rerun()

com col5:
    if st.button("ðŸ—'ï¸ Limpar", key="Limpar", use_container_width=True, help="Limpar todo o histórico"):
        limpar_histórico()
        st.rerun()

# --- ANÃ LISE PRINCIPAL (MOVIDA PARA CIMA DO HISTÓRICO) ---
st.markdown('<div class="section-header"><h2>™ Próxima Sugestão</h2></div>', unsafe_allow_html=True)

if len(st.session_state.historico) >= 5: # Mínimo de 5 para algumas análises
    tentar:
        analisador = AnalisePadroes(st.session_state.historico)
        log_message("info", "Objeto AnalisePadroes criado com histórico atual.")
        
        # Gera uma sugestão
        sugestao = analyzer.gerar_sugestao() # CORRIGIDO: Chamando o método com o nome correto
        log_message("info", f"Sugestão gerada: {sugestao['entrada_codigo']} (Confiança: {sugestao['confianca']}%)")
        
        # Armazena a sugestão e defina uma bandeira para que ela seja processada na próxima adição de resultado
        st.session_state.ultima_sugestao = sugestão
        st.session_state.sugestao_processada = True # Flag para indicar que uma sugestão foi gerada e aguarda validação

        if sugestao['sugerir'] e sugestao['confianca'] >= limite_deconfiança:
            confianca_color = get_confianca_color(sugestão['confianca'])
            
            st.markdown(f"""
            <div class="caixa-de-sugestão">
                <h3>ðŸŽ¯ Sugestão para o Próximo Jogo:</h3>
                <h2 style="color: {confianca_color}; margem: 1rem 0;">
                    {sugestão['entrada']} ({sugestão['entrada_codigo']})
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
            
            se mostrar_avançado:
                with st.expander("ðŸ“‹ Detalhes da Análise"):
                    st.write("**Padrões Identificados que Contribuíram:**")
                    se sugestão['motivos']:
                        for motivo in sugestao['motivos']:
                            st.write(f"â€¢ {motivo}")
                    outro:
                        st.info("Nenhum padrão específico contribuiu para a sugestão com peso suficiente.")
                    
                    if 'analise_detalhada' em sugestao e sugestao['analise_detalhada']:
                        st.write("**Análise por Categoria de Padrões:**")
                        para categoria, padroes_list em sugestao['analise_detalhada'].items():
                            st.write(f"**{categoria}:** {', '.join(padroes_list)}")
                    outro:
                        st.info("Nenhuma análise detalhada de categorias de padrões disponíveis.")
                    
                    st.write("**Pontuações Brutas por Resultado:**")
                    st.json(sugestao['pontuacoes_brutas']) # Para depuração

        outro:
            st.warning(f"ðŸ¤” Confiança insuficiente ({sugestao['confianca']}%) para uma sugestão forte. Limite: {confidence_threshold}%.")
            st.info("Continue inserindo resultados para aumentar a precisão da análise.")
            log_message("warn", f"Sugestão não exibida: Confiança {sugestao['confianca']}% abaixo do limite {confidence_threshold}%.")

    exceto Exceção como e:
        st.error(f"Ocorreu um erro inesperado durante a análise da sugestão. Por favor, verifique os logs na barra lateral.")
        st.exception(e) # Exibe o traceback completo para depuração em desenvolvimento
        log_message("critical", f"Erro crítico na análise: {e}")

outro:
    st.info("ðŸŽ® Insira pelo menos 5 resultados para começar a analisar inteligente e gerar sugestões!")


# --- EXIBIÇÃO DO HISTÓRICO (AGORA ABAIXO DA SUGESTÃO) ​​---
st.markdown('<div class="section-header"><h2>ðŸ“ˆ Histórico de Resultados</h2></div>', unsafe_allow_html=True)

se não st.session_state.historico:
    st.info("ðŸŽ® Nenhum resultado registrado. Comece inserindo os resultados dos jogos!")
outro:
    st.markdown('<div class="historic-container">', unsafe_allow_html=True)
    
    # Renderiza o histórico em linhas com quebra automática
    # A classe CSS 'historic-row' já usa 'flex-wrap: wrap;' para quebrar automaticamente.
    st.markdown('<div class="historic-row">', unsafe_allow_html=True)
    para i, resultado em enumerate(st.session_state.historico):
        st.markdown(get_resultado_html(resultado), unsafe_allow_html=True)
        se (i + 1) % 9 == 0:
            st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) # Data para div historic-row
            
    st.markdown(f"**Total:** {len(st.session_state.historico)} jogos (máx. 50)", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ANÃ LISE DE PADRÃ•ES (DETALHADA) - SÃ“ SE show_advanced ESTIVER ATIVO ---
se show_advanced e len(st.session_state.historico) >= 5:
    tentar:
        analyzer = AnalisePadroes(st.session_state.historico) # Crie o analisador para esta sessão, se necessário
        st.markdown('<div class="section-header"><h2>ðŸ” Padrões Detectados (Todos)</h2></div>', unsafe_allow_html=True)
        
        padroes_encontrados = analyzer.analisar_todos()
        
        coluna_esquerda, coluna_direita = st.columns(2)
        
        com col_left:
            st.markdown("### âœ…Padrões Ativos")
            encontrado = [nome para nome, status em padroes_encontrados.items() if status]
            
            se encontrado:
                para padrão em encontrado:
                    peso = analyzer.pesos_padroes.get(padrão, 0,5)
                    st.markdown(f'<div class="pattern-found">âœ… {padrao} (Peso: {peso})</div>', unsafe_allow_html=True)
            outro:
                st.info("Nenhum padrão detectado no histórico atual.")
        
        com col_right:
            st.markdown("### â Œ Padrões Inativos")
            nao_encontrados = [nome para nome, status em padroes_encontrados.items() se não for status]
            
            se nao_encontrados:
                # Exibir apenas os primeiros X inativos para não poluir a tela
                para padrão em nao_encontrados[:15]:
                    st.markdown(f'<div class="pattern-not-found">â Œ {padrao}</div>', unsafe_allow_html=True)
                se len(nao_encontrados) > 15:
                    st.markdown(f'<div class="pattern-not-found">... e mais {len(nao_encontrados) - 15}</div>', unsafe_allow_html=True)
            outro:
                st.info("Todos os padrões foram encontrados (muito raros).")
        
    exceto Exceção como e:
        st.error(f"Ocorreu um erro inesperado durante uma análise específica dos padrões. Por favor, verifique os logs na barra lateral.")
        st.exception(e)
        log_message("critical", f"Erro crítico na análise específica de padrões: {e}")

# --- ANÁ LISE ESTATÍSTICA GERAL ---
st.markdown('<div class="section-header"><h2>ðŸ“Š Análise Estatística Geral</h2></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

# Garante que o analisador foi criado para esta temporada, caso a sugestão não tenha sido gerada
se 'analyzer' não estiver em locals() ou analyzer for None:
    analisador = AnalisePadroes(st.session_state.historico)

frequências = analyzer.calcular_frequencias()

com col1:
    st.markdown(f"""
    <div class="cartão-métrico">
        <h3>ðŸ Casa</h3>
        <p style="color: #FF4B4B;">{frequencias.get('C', 0.0)}%</p>
    </div>
    """, unsafe_allow_html=True)

com col2:
    st.markdown(f"""
    <div class="cartão-métrico">
        <h3>Visitante</h3>
        <p style="color: #4B4BFF;">{frequencias.get('F', 0.0)}%</p>
    </div>
    """, unsafe_allow_html=True)

com col3:
    st.markdown(f"""
    <div class="cartão-métrico">
        <h3>âš–ï¸ Empatia</h3>
        <p style="color: #FFD700;">{frequencias.get('E', 0.0)}%</p>
    </div>
    """, unsafe_allow_html=True)

# Gráfico de frequências
se mostrar_avançado:
    st.markdown("### ðŸ“ˆ Distribuição dos Resultados no Histórico Completo")
    chart_data = pd.DataFrame({
        'Resultado': ['Casa', 'Visitante', 'Empate'],
        'Frequência': [frequências.get('C', 0.0), frequências.get('F', 0.0), frequências.get('E', 0.0)],
        'Cor': ['#FF4B4B', '#4B4BFF', '#FFD700']
    })
    
    st.bar_chart(chart_data.set_index('Resultado')['Frequência'])

# --- RODAPÉ ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; margin-top: 2rem;">
    <p>âš½ Football Studio Live Analyzer v2.5 | Análise Inteligente de Padrées</p>
    <p><small>Desenvolvido para Evolution Gaming Football Studio</small></p>
</div>
""", unsafe_allow_html=True)
