import collections
import random

class AnalisePadroes:
    def __init__(self, historico):
        # Limita o histórico aos últimos 27 resultados, conforme o JS original.
        # Isso garante que a análise sempre considere o mesmo escopo de dados.
        self.historico = historico[-27:]
        self.padroes_ativos = {
            "Sequência (Surf de Cor)": self._sequencia_simples,
            "Zig-Zag": self._zig_zag,
            "Quebra de Surf": self._quebra_de_surf,
            "Quebra de Zig-Zag": self._quebra_de_zig_zag,
            "Duplas repetidas": self._duplas_repetidas,
            "Empate recorrente": self._empate_recorrente,
            "Padrão Escada": self._padrao_escada,
            "Espelho": self._espelho,
            "Alternância com empate no meio": self._alternancia_empate_meio,
            "Padrão 'onda'": self._padrao_onda,
            "Padrões últimos 5/7/10 jogos": self._padroes_ultimos_jogos,
            "Padrão 3x1": self._padrao_3x1,
            "Padrão 3x3": self._padrao_3x3,
            "Padrão 4x4": self._padrao_4x4,
            "Padrão 4x1": self._padrao_4x1
        }

    def analisar_todos(self):
        """
        Executa todos os padrões ativos e retorna um dicionário
        indicando se cada padrão foi encontrado (True/False).
        """
        resultados = {}
        for nome, func in self.padroes_ativos.items():
            try:
                resultados[nome] = func()
            except Exception as e:
                print(f"Erro ao analisar o padrão '{nome}': {e}")
                resultados[nome] = False # Marca como False em caso de erro
        return resultados

    # --- Métodos de Verificação de Padrões ---

    def _sequencia_simples(self):
        """Verifica se há uma sequência de 3 resultados iguais (ex: C-C-C)."""
        for i in range(len(self.historico) - 2):
            if self.historico[i] == self.historico[i+1] and \
               self.historico[i+1] == self.historico[i+2]:
                return True
        return False

    def _zig_zag(self):
        """Verifica se há uma alternância constante de resultados (ex: C-V-C-V)."""
        if len(self.historico) < 4: # Mínimo para um zig-zag claro (A, B, A, B)
            return False
        for i in range(len(self.historico) - 1):
            if self.historico[i] == self.historico[i+1]:
                return False # Se encontrar dois seguidos iguais, não é zig-zag
        return True

    def _quebra_de_surf(self):
        """Verifica se uma sequência de 3 é quebrada por um resultado diferente (ex: C-C-C-V)."""
        for i in range(len(self.historico) - 3):
            if (self.historico[i] == self.historico[i+1] and
                self.historico[i+1] == self.historico[i+2] and
                self.historico[i+2] != self.historico[i+3]):
                return True
        return False

    def _quebra_de_zig_zag(self):
        """Verifica se um zig-zag é quebrado por dois resultados iguais (ex: C-V-C-C)."""
        if len(self.historico) < 5:
            return False
        for i in range(len(self.historico) - 4):
            if (self.historico[i] != self.historico[i+1] and # A != B
                self.historico[i+1] != self.historico[i+2] and # B != C
                self.historico[i+2] == self.historico[i+3]): # C == D, quebra o zig-zag
                return True
        return False

    def _duplas_repetidas(self):
        """Verifica se há repetições de duplas diferentes (ex: C-C-V-V)."""
        if len(self.historico) < 4:
            return False
        for i in range(len(self.historico) - 3):
            if (self.historico[i] == self.historico[i+1] and # A-A
                self.historico[i+2] == self.historico[i+3] and # B-B
                self.historico[i] != self.historico[i+2]): # A != B
                return True
        return False

    def _empate_recorrente(self):
        """Verifica se empates ocorrem a cada 2, 3 ou 4 jogos."""
        empates_indices = [i for i, r in enumerate(self.historico) if r == 'E']
        if len(empates_indices) < 2:
            return False
        for i in range(len(empates_indices) - 1):
            diferenca = empates_indices[i+1] - empates_indices[i]
            if 2 <= diferenca <= 4:
                return True
        return False

    def _padrao_escada(self):
        """Verifica um padrão como A-B-B-C-C-C onde B!=A, C!=B."""
        if len(self.historico) < 6:
            return False
        for i in range(len(self.historico) - 5):
            if (self.historico[i] != self.historico[i+1] and # A != B
                self.historico[i+1] == self.historico[i+2] and # B == C
                self.historico[i+3] == self.historico[i+4] and # D == E
                self.historico[i+4] == self.historico[i+5] and # E == F
                self.historico[i+1] != self.historico[i+3]): # B != D (ex: C V V E E E)
                return True
        return False

    def _espelho(self):
        """Verifica se a primeira metade do histórico é um espelho da segunda metade invertida."""
        if len(self.historico) < 2:
            return False
        metade = len(self.historico) // 2
        primeira_metade = self.historico[:metade]
        # Inverte a segunda metade do histórico para comparação
        segunda_metade_reversa = self.historico[len(self.historico) - metade:][::-1]
        return primeira_metade == segunda_metade_reversa

    def _alternancia_empate_meio(self):
        """Verifica um padrão onde um empate está entre dois resultados diferentes (ex: C-E-V)."""
        if len(self.historico) < 3:
            return False
        for i in range(len(self.historico) - 2):
            if (self.historico[i] != 'E' and
                self.historico[i+1] == 'E' and
                self.historico[i+2] != 'E' and
                self.historico[i] != self.historico[i+2]): # C E V ou V E C
                return True
        return False

    def _padrao_onda(self):
        """Verifica um padrão como A-B-A-B."""
        if len(self.historico) < 4:
            return False
        for i in range(len(self.historico) - 3):
            if (self.historico[i] == self.historico[i+2] and # A _ A
                self.historico[i+1] == self.historico[i+3] and # _ B _ B
                self.historico[i] != self.historico[i+1]): # A != B
                return True
        return False

    def _padroes_ultimos_jogos(self):
        """
        Verifica se há uma predominância de um resultado nos últimos 5 jogos.
        Pode ser estendido para 7, 10, etc., conforme a necessidade.
        """
        if len(self.historico) < 5:
            return False
        ultimos5 = self.historico[-5:]
        contador = collections.Counter(ultimos5)
        # Se um resultado representa 60% ou mais dos últimos 5 jogos
        for resultado, count in contador.items():
            if count / len(ultimos5) >= 0.6:
                return True
        return False

    def _padrao_3x1(self):
        """Verifica um padrão de 3 resultados iguais seguidos por 1 diferente (ex: C-C-C-V)."""
        for i in range(len(self.historico) - 3):
            bloco = self.historico[i:i+4]
            if bloco[0] == bloco[1] == bloco[2] and bloco[3] != bloco[0]:
                return True
        return False

    def _padrao_3x3(self):
        """Verifica um padrão de 3 resultados iguais seguidos por outros 3 resultados iguais, mas diferentes dos primeiros (ex: C-C-C-V-V-V)."""
        for i in range(len(self.historico) - 5):
            bloco = self.historico[i:i+6]
            if (bloco[0] == bloco[1] == bloco[2] and
                bloco[3] == bloco[4] == bloco[5] and
                bloco[0] != bloco[3]):
                return True
        return False

    def _padrao_4x4(self):
        """Verifica um padrão de 4 resultados iguais seguidos por outros 4 resultados iguais, mas diferentes dos primeiros (ex: C-C-C-C-V-V-V-V)."""
        for i in range(len(self.historico) - 7):
            bloco = self.historico[i:i+8]
            if (bloco[0] == bloco[1] == bloco[2] == bloco[3] and
                bloco[4] == bloco[5] == bloco[6] == bloco[7] and
                bloco[0] != bloco[4]):
                return True
        return False

    def _padrao_4x1(self):
        """Verifica um padrão de 4 resultados iguais seguidos por 1 diferente (ex: C-C-C-C-V)."""
        for i in range(len(self.historico) - 4):
            bloco = self.historico[i:i+5]
            if (bloco[0] == bloco[1] == bloco[2] == bloco[3] and
                bloco[4] != bloco[0]):
                return True
        return False

    # --- Funções Auxiliares e Sugestão ---

    def calcular_frequencias(self):
        """
        Calcula a porcentagem de ocorrência de 'C', 'V' e 'E' no histórico.
        """
        contador = collections.Counter(self.historico)
        total = len(self.historico)
        if total == 0:
            return {'C': 0, 'V': 0, 'E': 0}
        result = {k: round((v / total) * 100) for k, v in contador.items()}
        # Garante que todos os tipos de resultado apareçam, mesmo com 0%
        for tipo in ['C', 'V', 'E']:
            if tipo not in result:
                result[tipo] = 0
        return result

    def sugestao_inteligente(self):
        """
        Analisa os padrões e sugere um resultado com base na identificação
        de padrões e nas frequências dos resultados.
        """
        analise = self.analisar_todos()
        padroes_identificados = [nome for nome, ok in analise.items() if ok]

        if padroes_identificados:
            frequencias = self.calcular_frequencias()
            opcoes = ["V", "C", "E"] # Ordem de preferência para sugestão (pode ser ajustada)

            # Escolhe a opção com a menor frequência para sugerir uma "quebra" ou "menos comum"
            entrada_sugerida = None
            min_freq = float('inf')

            # Encontra a opção com a menor frequência
            for op in opcoes:
                if frequencias.get(op, 0) < min_freq:
                    min_freq = frequencias.get(op, 0)
                    entrada_sugerida = op

            # Se todas as opções tiverem a mesma frequência, ou se o histórico for muito pequeno, randomiza
            if not entrada_sugerida or len(set(frequencias.values())) == 1:
                 entrada_sugerida = random.choice(opcoes)

            mapeamento_legivel = {"C": "Casa", "V": "Visitante", "E": "Empate"}
            entrada_legivel = mapeamento_legivel[entrada_sugerida]

            # A confiança é uma estimativa; ajustada para refletir a presença de padrões.
            # Quanto mais padrões identificados, maior a confiança.
            confianca = min(90, int((len(padroes_identificados) / len(self.padroes_ativos)) * 100) + 20)

            return {
                "sugerir": True,
                "entrada": entrada_legivel,
                "entrada_codigo": entrada_sugerida,
                "motivos": padroes_identificados,
                "confianca": confianca,
                "frequencias": frequencias,
                "ultimos_resultados": self.historico[-3:] # Mostra os 3 últimos para contexto
            }
        else:
            return {
                "sugerir": False,
                "entrada": None,
                "entrada_codigo": None,
                "motivos": ["Nenhum padrão confiável identificado"],
                "confianca": 0,
                "frequencias": self.calcular_frequencias(),
                "ultimos_resultados": self.historico[-3:]
            }

# --- Bloco de Execução Principal ---
# Este bloco só é executado quando o script é rodado diretamente.
if __name__ == "__main__":
    # Exemplo de histórico de resultados:
    # 'C' para Casa, 'V' para Visitante, 'E' para Empate
    historico_exemplo = ['C', 'V', 'E', 'C', 'C', 'C', 'V', 'E', 'V', 'C',
                         'V', 'V', 'E', 'C', 'V', 'V', 'C', 'C', 'C', 'V',
                         'E', 'C', 'C', 'C', 'V', 'V', 'C']

    # Cria uma instância da classe AnalisePadroes com o histórico
    app_analise = AnalisePadroes(historico_exemplo)

    print("--- Padrões Detectados ---")
    padroes_encontrados = app_analise.analisar_todos()
    for nome, encontrado in padroes_encontrados.items():
        print(f"- {nome}: {'Sim' if encontrado else 'Não'}")

    print("\n--- Sugestão Inteligente ---")
    sugestao = app_analise.sugestao_inteligente()
    if sugestao['sugerir']:
        print(f"Sugestão: {sugestao['entrada']}")
        print(f"Confiança: {sugestao['confianca']}%")
        print(f"Motivos: {', '.join(sugestao['motivos'])}")
        print(f"Últimos 3 resultados: {', '.join(sugestao['ultimos_resultados'])}")
    else:
        print(f"Sem sugestão: {sugestao['motivos'][0]}")
    
    print("\n--- Frequências dos Resultados ---")
    frequencias = app_analise.calcular_frequencias()
    mapeamento_freq_legivel = {"C": "Casa", "V": "Visitante", "E": "Empate"}
    for tipo, freq in frequencias.items():
        print(f"{mapeamento_freq_legivel[tipo]}: {freq}%")

    print(f"\nTotal de jogos no histórico analisado: {len(app_analise.historico)}")
