import collections
import random

class AnalisePadroes:
    def __init__(self, historico):
        # Limita o histórico aos últimos 27 resultados, conforme o JS
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
        resultados = {}
        for nome, func in self.padroes_ativos.items():
            resultados[nome] = func()
        return resultados

    def _sequencia_simples(self):
        for i in range(len(self.historico) - 2):
            if self.historico[i] == self.historico[i+1] and self.historico[i+1] == self.historico[i+2]:
                return True
        return False

    def _zig_zag(self):
        if len(self.historico) < 4: # Mínimo para ver um zig-zag aparente (A, B, A, B)
            return False
        for i in range(len(self.historico) - 1):
            if self.historico[i] == self.historico[i+1]:
                return False
        return True

    def _quebra_de_surf(self):
        for i in range(len(self.historico) - 3):
            if (self.historico[i] == self.historico[i+1] and
                self.historico[i+1] == self.historico[i+2] and
                self.historico[i+2] != self.historico[i+3]):
                return True
        return False

    def _quebra_de_zig_zag(self):
        if len(self.historico) < 5:
            return False
        for i in range(len(self.historico) - 4):
            if (self.historico[i] != self.historico[i+1] and
                self.historico[i+1] != self.historico[i+2] and
                self.historico[i+2] == self.historico[i+3]): # O terceiro é igual ao quarto, quebrando o zig-zag
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
        empates = [i for i, r in enumerate(self.historico) if r == 'E']
        if len(empates) < 2:
            return False
        for i in range(len(empates) - 1):
            if 2 <= (empates[i+1] - empates[i]) <= 4: # Empates a cada 2, 3 ou 4 jogos
                return True
        return False

    def _padrao_escada(self):
        if len(self.historico) < 6:
            return False
        for i in range(len(self.historico) - 5):
            if (self.historico[i] != self.historico[i+1] and # AB
                self.historico[i+1] == self.historico[i+2] and # BCC
                self.historico[i+3] == self.historico[i+4] and # DEEE (mas C != E)
                self.historico[i+4] == self.historico[i+5] and
                self.historico[i+1] != self.historico[i+3]): # BC diferente de DE
                return True
        return False

    def _espelho(self):
        if len(self.historico) < 2:
            return False
        metade = len(self.historico) // 2
        primeira_metade = self.historico[:metade]
        segunda_metade_reversa = self.historico[len(self.historico) - metade:][::-1]
        return primeira_metade == segunda_metade_reversa

    def _alternancia_empate_meio(self):
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
        if len(self.historico) < 4:
            return False
        for i in range(len(self.historico) - 3):
            if (self.historico[i] == self.historico[i+2] and # A_A
                self.historico[i+1] == self.historico[i+3] and # _B_B
                self.historico[i] != self.historico[i+1]): # A != B
                return True
        return False

    def _padroes_ultimos_jogos(self):
        # Este padrão é um pouco mais genérico no JS.
        # Aqui, vamos verificar se há uma maioria esmagadora de um resultado nos últimos 5 jogos.
        if len(self.historico) < 5:
            return False
        ultimos5 = self.historico[-5:]
        contador = collections.Counter(ultimos5)
        for resultado, count in contador.items():
            if count / len(ultimos5) >= 0.6: # Mais de 60% do mesmo resultado nos últimos 5
                return True
        return False

    def _padrao_3x1(self):
        for i in range(len(self.historico) - 3):
            bloco = self.historico[i:i+4]
            if bloco[0] == bloco[1] == bloco[2] and bloco[3] != bloco[0]:
                return True
        return False

    def _padrao_3x3(self):
        for i in range(len(self.historico) - 5):
            bloco = self.historico[i:i+6]
            if (bloco[0] == bloco[1] == bloco[2] and
                bloco[3] == bloco[4] == bloco[5] and
                bloco[0] != bloco[3]):
                return True
        return False

    def _padrao_4x4(self):
        for i in range(len(self.historico) - 7):
            bloco = self.historico[i:i+8]
            if (bloco[0] == bloco[1] == bloco[2] == bloco[3] and
                bloco[4] == bloco[5] == bloco[6] == bloco[7] and
                bloco[0] != bloco[4]):
                return True
        return False

    def _padrao_4x1(self):
        for i in range(len(self.historico) - 4):
            bloco = self.historico[i:i+5]
            if (bloco[0] == bloco[1] == bloco[2] == bloco[3] and
                bloco[4] != bloco[0]):
                return True
        return False

    def calcular_frequencias(self):
        contador = collections.Counter(self.historico)
        total = len(self.historico)
        if total == 0:
            return {'C': 0, 'V': 0, 'E': 0}
        result = {k: round(v / total * 100) for k, v in contador.items()}
        # Garante que todos os tipos de resultado apareçam, mesmo com 0%
        for tipo in ['C', 'V', 'E']:
            if tipo not in result:
                result[tipo] = 0
        return result

    def sugestao_inteligente(self):
        analise = self.analisar_todos()
        padroes_identificados = [nome for nome, ok in analise.items() if ok]

        if padroes_identificados:
            frequencias = self.calcular_frequencias()
            opcoes = ["V", "C", "E"] # Ordem de preferência: Visitante, Casa, Empate
            
            # Escolhe a opção com a menor frequência para sugerir uma quebra de padrão ou algo menos comum
            entrada_sugerida = None
            min_freq = float('inf')
            
            # Encontra a opção com a menor frequência entre as válidas
            for op in opcoes:
                if frequencias.get(op, 0) < min_freq:
                    min_freq = frequencias.get(op, 0)
                    entrada_sugerida = op
            
            # Se todas tiverem a mesma frequência ou se o histórico for pequeno, randomiza
            if not entrada_sugerida or len(set(frequencias.values())) == 1:
                 entrada_sugerida = random.choice(opcoes)

            mapeamento = {"C": "Casa", "V": "Visitante", "E": "Empate"}
            entrada_legivel = mapeamento[entrada_sugerida]
            
            # A lógica de confiança é uma estimativa; ajustei para refletir a presença de padrões
            confianca = min(90, int((len(padroes_identificados) / len(self.padroes_ativos)) * 100) + 20)
            
            return {
                "sugerir": True,
                "entrada": entrada_legivel,
                "entrada_codigo": entrada_sugerida,
                "motivos": padroes_identificados,
                "confianca": confianca,
                "frequencias": frequencias,
                "ultimos_resultados": self.historico[-3:]
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

if __name__ == "__main__":
    # Exemplo de uso:
    historico_exemplo = ['C', 'V', 'E', 'C', 'C', 'C', 'V', 'E', 'V', 'C', 'V', 'V', 'E', 'C', 'V', 'V', 'C', 'C', 'C', 'V', 'E', 'C', 'C', 'C']
    
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
    else:
        print(f"Sem sugestão: {sugestao['motivos'][0]}")
    
    print("\n--- Frequências ---")
    frequencias = app_analise.calcular_frequencias()
    for tipo, freq in frequencias.items():
        mapeamento_freq_legivel = {"C": "Casa", "V": "Visitante", "E": "Empate"}
        print(f"{mapeamento_freq_legivel[tipo]}: {freq}%")

    print(f"\nTotal de jogos no histórico: {len(app_analise.historico)}")
