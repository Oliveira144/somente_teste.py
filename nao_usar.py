import streamlit as st
import collections
import random

class AnalisePadroes:
    def __init__(self, historico):
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
            try:
                resultados[nome] = func()
            except Exception as e:
                # É bom logar erros aqui para depuração
                # st.error(f"Erro ao analisar o padrão '{nome}': {e}") # Pode ser muito verboso
                resultados[nome] = False
        return resultados

    # --- Métodos de Verificação de Padrões (Mantenha todos os métodos aqui) ---
    def _sequencia_simples(self):
        for i in range(len(self.historico) - 2):
            if self.historico[i] == self.historico[i+1] and \
               self.historico[i+1] == self.historico[i+2]:
                return True
        return False

    def _zig_zag(self):
        if len(self.historico) < 4:
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
        if len(empates_indices) < 2:
            return False
        for i in range(len(empates_indices) - 1):
            diferenca = empates_indices[i+1] - empates_indices[i]
            if 2 <= diferenca <= 4:
                return True
        return False

    def _padrao_escada(self):
        if len(self.historico) < 6:
            return False
        for i in range(len(self.historico) - 5):
            if (self.historico[i] != self.historico[i+1] and
                self.historico[i+1] == self.historico[i+2] and
                self.historico[i+3] == self.historico[i+4] and
                self.historico[i+4] == self.historico[i+5] and
                self.historico[i+1] != self.historico[i+3]):
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
                self.historico[i] != self.historico[i+2]):
                return True
        return False

    def _padrao_onda(self):
        if len(self.historico) < 4:
            return False
        for i in range(len(self.historico) - 3):
            if (self.historico[i] == self.historico[i+2] and
                self.historico[i+1] == self.historico[i+3] and
                self.historico[i] != self.historico[i+1]):
                return True
        return False

    def _padroes_ultimos_jogos(self):
        if len(self.historico) < 5:
            return False
        ultimos5 = self.historico[-5:]
        contador = collections.Counter(ultimos5)
        for resultado, count in contador.items():
            if count / len(ultimos5) >= 0.6:
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
        for tipo in ['C', 'V', 'E']:
            if tipo not in result:
                result[tipo] = 0
        return result

    def sugestao_inteligente(self):
        analise = self.analisar_todos()
        padroes_identificados = [nome for nome, ok in analise.items() if ok]

        if padroes_identificados:
            frequencias = self.calcular_frequencias()
            opcoes = ["V", "C", "E"]
            entrada_sugerida = None
            min_freq = float('inf')

            for op in opcoes:
                if frequencias.get(op, 0) < min_freq:
                    min_freq = frequencias.get(op, 0)
                    entrada_sugerida = op

            if not entrada_sugerida or len(set(frequencias.values())) == 1:
                 entrada_sugerida = random.choice(opcoes)

            mapeamento = {"C": "Casa", "V": "Visitante", "E": "Empate"}
            entrada_legivel = mapeamento[entrada_sugerida]

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

# --- Início da Aplicação Streamlit ---
st.set_page_config(layout="wide")

st.title("⚽ Análise de Padrões de Resultados de Jogos")
st.markdown("---")

# Exemplo de histórico inicial para o campo de texto
historico_exemplo_inicial = ['C', 'V', 'E', 'C', 'C', 'C', 'V', 'E', 'V', 'C',
                             'V', 'V', 'E', 'C', 'V', 'V', 'C', 'C', 'C', 'V',
                             'E', 'C', 'C', 'C', 'V', 'V', 'C']

st.sidebar.header("Configurações de Entrada")
historico_input = st.sidebar.text_area(
    "Insira o histórico de resultados (separado por vírgulas, ex: C,V,E,C):",
    value=",".join(historico_exemplo_inicial),
    height=150 # Aumenta a altura do campo de texto
)

# Botão para submeter o histórico
# Ao clicar no botão, o script é re-executado.
if st.sidebar.button("Analisar Histórico"):
    historico_processado = [r.strip().upper() for r in historico_input.split(',') if r.strip()]

    if not historico_processado:
        st.warning("Por favor, insira um histórico de resultados para análise.")
    else:
        st.write("---") # Separador visual

        app_analise = AnalisePadroes(historico_processado)

        st.header("🔍 Padrões Detectados")
        padroes_encontrados = app_analise.analisar_todos()
        
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Padrões Encontrados:")
            encontrados_lista = [nome for nome, encontrado in padroes_encontrados.items() if encontrado]
            if encontrados_lista:
                for padrao in encontrados_lista:
                    st.success(f"✔️ {padrao}")
            else:
                st.info("Nenhum padrão específico detectado no momento.")
        
        with col2:
            st.subheader("Padrões Não Encontrados:")
            nao_encontrados_lista = [nome for nome, encontrado in padroes_encontrados.items() if not encontrado]
            if nao_encontrados_lista:
                for padrao in nao_encontrados_lista:
                    st.markdown(f"<span style='color: grey;'>✖️ {padrao}</span>", unsafe_allow_html=True)
            else:
                st.info("Todos os padrões foram encontrados!")


        st.markdown("---")
        st.header("💡 Sugestão Inteligente para o Próximo Jogo")
        sugestao = app_analise.sugestao_inteligente()

        if sugestao['sugerir']:
            st.write(f"Considerando os padrões e frequências:")
            st.success(f"**Sugestão:** Próximo resultado provável: **{sugestao['entrada']}**")
            st.metric(label="Confiança da Sugestão", value=f"{sugestao['confianca']}%")
            st.info(f"**Motivos:** {', '.join(sugestao['motivos'])}")
            st.markdown(f"Últimos 3 resultados: `{', '.join(sugestao['ultimos_resultados'])}`")
        else:
            st.warning(f"**Sem sugestão:** {sugestao['motivos'][0]}")
        
        st.markdown("---")
        st.header("📊 Frequência dos Resultados no Histórico")
        frequencias = app_analise.calcular_frequencias()
        
        mapeamento_freq_legivel = {"C": "Casa", "V": "Visitante", "E": "Empate"}
        freq_data = {
            "Resultado": [mapeamento_freq_legivel[t] for t in ['C', 'V', 'E']],
            "Porcentagem": [frequencias.get(t, 0) for t in ['C', 'V', 'E']]
        }
        
        st.bar_chart(freq_data, x="Resultado", y="Porcentagem")
        st.write(f"Total de jogos no histórico analisado: **{len(app_analise.historico)}**")
else:
    st.info("Insira o histórico de resultados na barra lateral e clique em 'Analisar Histórico' para começar.")
