class AnalisePadroes:
    def __init__(self, historico):
        self.historico = list(reversed(historico[:54]))
        
        self.padroes_ativos = {
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
            "Padrão Fibonacci": self._padrao_fibonacci,
            "Sequência Dourada": self._sequencia_dourada,
            "Padrão Triangular": self._padrao_triangular,
            "Ciclo de Empates": self._ciclo_empates,
            "Padrão Martingale": self._padrao_martingale,
            "Sequência de Fibonacci Invertida": self._fibonacci_invertida,
            "Padrão Dragon Tiger": self._padrao_dragon_tiger,
            "Sequência de Paroli": self._sequencia_paroli,
            "Padrão de Ondas Longas": self._ondas_longas,
            "Ciclo de Dominância": self._ciclo_dominancia
        }

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
            "Ciclo de Dominância": 0.8
        }

    def analisar_todos(self):
        resultados = {}
        for nome, func in self.padroes_ativos.items():
            try:
                resultados[nome] = func()
            except:
                resultados[nome] = False
        return resultados

    def _sequencia_simples(self):
        for i in range(len(self.historico) - 2):
            if self.historico[i] == self.historico[i + 1] == self.historico[i + 2]:
                return True
        return False

    def _zig_zag(self):
        if len(self.historico) < 6:
            return False
        count = 0
        for i in range(len(self.historico) - 1):
            if self.historico[i] != self.historico[i + 1]:
                count += 1
            else:
                if count >= 5:
                    return True
                count = 0
        return count >= 5

    def _quebra_de_surf(self):
        for i in range(len(self.historico) - 3):
            if (
                self.historico[i] == self.historico[i + 1] == self.historico[i + 2]
                and self.historico[i + 2] != self.historico[i + 3]
            ):
                return True
        return False

    def _quebra_de_zig_zag(self):
        if len(self.historico) < 4:
            return False
        for i in range(len(self.historico) - 3):
            if (
                self.historico[i] != self.historico[i + 1]
                and self.historico[i + 1] != self.historico[i + 2]
                and self.historico[i + 2] == self.historico[i + 3]
            ):
                return True
        return False

    def _duplas_repetidas(self):
        if len(self.historico) < 4:
            return False
        for i in range(len(self.historico) - 3):
            if (
                self.historico[i] == self.historico[i + 1]
                and self.historico[i + 2] == self.historico[i + 3]
                and self.historico[i] != self.historico[i + 2]
            ):
                return True
        return False
    def _empate_recorrente(self):
        empates_indices = [i for i, r in enumerate(self.historico) if r == 'E']
        if len(empates_indices) < 3:
            return False
        
        intervalos = [
            empates_indices[i+1] - empates_indices[i]
            for i in range(len(empates_indices) - 1)
        ]
        
        if len(intervalos) >= 2:
            media = sum(intervalos) / len(intervalos)
            consistentes = [x for x in intervalos if abs(x - media) <= 2]
            return len(consistentes) / len(intervalos) >= 0.75
        return False

    def _padrao_escada(self):
        if len(self.historico) < 6:
            return False
        for i in range(len(self.historico) - 5):
            if (
                self.historico[i] != self.historico[i+1]
                and self.historico[i+1] == self.historico[i+2]
                and self.historico[i+2] != self.historico[i+3]
                and self.historico[i+3] == self.historico[i+4] == self.historico[i+5]
            ):
                return True
        return False

    def _espelho(self):
        if len(self.historico) < 4:
            return False
        for tamanho in range(4, min(len(self.historico) + 1, 13)):
            if tamanho % 2 == 0:
                metade = tamanho // 2
                for start in range(len(self.historico) - tamanho + 1):
                    a = self.historico[start:start + metade]
                    b = self.historico[start + metade:start + tamanho]
                    if a == b[::-1]:
                        return True
        return False

    def _alternancia_empate_meio(self):
        if len(self.historico) < 3:
            return False
        for i in range(len(self.historico) - 2):
            if (
                self.historico[i] != 'E'
                and self.historico[i+1] == 'E'
                and self.historico[i+2] != 'E'
                and self.historico[i] != self.historico[i+2]
            ):
                return True
        return False

    def _padrao_onda(self):
        if len(self.historico) < 6:
            return False
        for i in range(len(self.historico) - 5):
            if (
                self.historico[i] == self.historico[i+2] == self.historico[i+4]
                and self.historico[i+1] == self.historico[i+3] == self.historico[i+5]
                and self.historico[i] != self.historico[i+1]
            ):
                return True
        return False

    def _padrao_fibonacci(self):
        if len(self.historico) < 8:
            return False
        fib_seq = [1, 1, 2, 3, 5]
        rep = []
        count = 1
        for i in range(1, len(self.historico)):
            if self.historico[i] == self.historico[i-1]:
                count += 1
            else:
                rep.append(count)
                count = 1
        rep.append(count)
        for i in range(len(rep) - len(fib_seq) + 1):
            if rep[i:i+len(fib_seq)] == fib_seq:
                return True
        return False

    def _sequencia_dourada(self):
        if len(self.historico) < 8:
            return False
        for i in range(len(self.historico) - 7):
            if (
                self.historico[i] == self.historico[i+1] == self.historico[i+2]
                and self.historico[i+3:i+8].count(self.historico[i+3]) == 5
                and self.historico[i] != self.historico[i+3]
            ):
                return True
        return False
    def _padrao_triangular(self):
        if len(self.historico) < 9:
            return False
        for i in range(len(self.historico) - 8):
            seg = self.historico[i:i+9]
            if (seg[0] == seg[8] and seg[1] == seg[7] and seg[0] != seg[1]
                and seg[2:7].count(seg[2]) == 5 and seg[2] != seg[1]):
                return True
        return False

    def _ciclo_empates(self):
        empates = [i for i, x in enumerate(self.historico) if x == 'E']
        if len(empates) < 3:
            return False
        for ciclo in range(3, 10):
            if all(
                ciclo - 2 <= empates[i+1] - empates[i] <= ciclo + 2
                for i in range(len(empates) - 1)
            ):
                return True
        return False

    def _padrao_martingale(self):
        if len(self.historico) < 7:
            return False
        for i in range(len(self.historico) - 6):
            seg = self.historico[i:i+7]
            if (seg[0] != seg[1]
                and seg[1] == seg[2]
                and seg[3] == seg[4] == seg[5] == seg[6]
                and seg[1] != seg[3]):
                return True
        return False

    def _fibonacci_invertida(self):
        if len(self.historico) < 8:
            return False
        seg = self.historico[-8:]
        return (
            seg[0:4].count(seg[0]) == 4
            and seg[4] != seg[0]
            and seg[5:7].count(seg[5]) == 2
            and seg[7] == seg[4]
        )

    def _padrao_dragon_tiger(self):
        if len(self.historico) < 6:
            return False
        seg = self.historico[-6:]
        return (
            seg[0] != seg[1] != seg[2] and seg[0] != seg[2]
            and seg[3] == 'E'
            and seg[4] == seg[5] != 'E'
        )

    def _sequencia_paroli(self):
        if len(self.historico) < 7:
            return False
        seg = self.historico[-7:]
        return (
            seg[0] != seg[1]
            and seg[1] == seg[2]
            and seg[3:7].count(seg[3]) == 4
            and seg[0] == seg[3]
        )

    def _ondas_longas(self):
        count = 1
        for i in range(1, len(self.historico)):
            if self.historico[i] == self.historico[i - 1]:
                count += 1
                if count >= 5:
                    return True
            else:
                count = 1
        return False

    def _ciclo_dominancia(self):
        if len(self.historico) < 10:
            return False
        janela = self.historico[:10]
        c = collections.Counter(janela)
        return any(freq >= 7 for freq in c.values())
    def sugestao_inteligente(self):
        if len(self.historico) < 9:
            return {
                "sugerir": False,
                "entrada": None,
                "entrada_codigo": None,
                "motivos": ["Histórico insuficiente (mínimo 9 jogos para sugestão)"],
                "confianca": 0,
                "frequencias": self.calcular_frequencias(),
                "ultimos_resultados": self.historico[:5]
            }

        analise = self.analisar_todos()
        padroes_identificados = [nome for nome, ok in analise.items() if ok]

        if not padroes_identificados:
            return {
                "sugerir": False,
                "entrada": None,
                "entrada_codigo": None,
                "motivos": ["Nenhum padrão identificado"],
                "confianca": 0,
                "frequencias": self.calcular_frequencias(),
                "ultimos_resultados": self.historico[:5]
            }

        confianca_total = sum(self.pesos_padroes.get(p, 0.5) for p in padroes_identificados)
        peso_total = len(padroes_identificados)
        confianca_media = (confianca_total / peso_total) * 100 if peso_total else 0

        confianca_final = min(99, int(confianca_media + min(20, peso_total * 2)))

        frequencias = self.calcular_frequencias()
        opcoes = ["C", "V", "E"]

        if any("quebra" in p.lower() for p in padroes_identificados):
            ultimo = self.historico[0]
            entrada = random.choice([o for o in ["C", "V"] if o != ultimo])
        elif any(p for p in padroes_identificados if "sequência" in p.lower() or "dominância" in p.lower() or "onda" in p.lower()):
            entrada = self.historico[0]
        elif any("empate" in p.lower() for p in padroes_identificados):
            entrada = "E"
        else:
            entrada = min(opcoes, key=lambda x: frequencias.get(x, 0))

        nomes = {"C": "Casa", "V": "Visitante", "E": "Empate"}
        return {
            "sugerir": True,
            "entrada": nomes[entrada],
            "entrada_codigo": entrada,
            "motivos": padroes_identificados,
            "confianca": confianca_final,
            "frequencias": frequencias,
            "ultimos_resultados": self.historico[:5],
            "analise_detalhada": self._gerar_analise_detalhada(padroes_identificados)
        }

    def _gerar_analise_detalhada(self, padroes):
        categorias = {
            "Repetição e Sequência": ["Sequência", "Ondas", "Surf", "Dourada", "Momentum", "Paroli"],
            "Quebra e Reversão": ["Quebra", "Breakout"],
            "Ciclos e Ritmo": ["Ciclo", "Empate Recorrente", "Zonas", "Pressão", "Respiração"],
            "Formações Visuais": ["Escada", "Espelho", "Triangular", "Labouchere", "Dragon Tiger"],
            "Padrões Numéricos": ["Fibonacci"]
        }
        analise = {}
        for categoria, chaves in categorias.items():
            grupo = [p for p in padroes if any(k.lower() in p.lower() for k in chaves)]
            if grupo:
                analise[categoria] = grupo
        return analise

    def calcular_frequencias(self):
        total = len(self.historico)
        cont = collections.Counter(self.historico)
        return {k: round(cont.get(k, 0) / total * 100, 1) for k in ['C', 'V', 'E']}
# --- SIDEBAR ---
with st.sidebar:
    st.subheader("📊 Estatísticas")
    est = st.session_state.estatisticas
    if est['total_jogos'] > 0:
        acertos = est['acertos']
        erros = est['erros']
        taxa = (acertos / (acertos + erros)) * 100 if (acertos + erros) else 0
        st.metric("Jogos", est['total_jogos'])
        st.metric("Acertos", acertos)
        st.metric("Erros", erros)
        st.metric("Taxa de Acerto", f"{taxa:.1f}%")
    else:
        st.info("Nenhum jogo registrado.")

# --- BOTÕES DE ENTRADA ---
st.header("🎯 Inserir Resultado")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🔴 Casa"):
        adicionar_resultado("C")
        st.rerun()
with col2:
    if st.button("🟡 Empate"):
        adicionar_resultado("E")
        st.rerun()
with col3:
    if st.button("🔵 Visitante"):
        adicionar_resultado("V")
        st.rerun()
with col4:
    if st.button("↩️ Desfazer"):
        desfazer_ultimo()
        st.rerun()
with col5:
    if st.button("🗑️ Limpar"):
        limpar_historico()
        st.rerun()

# --- HISTÓRICO VISUAL ---
st.subheader("📈 Histórico")
if not st.session_state.historico:
    st.info("Nenhum resultado ainda. Insira resultados acima!")
else:
    html = ''.join(get_resultado_html(r) for r in st.session_state.historico)
    components.html(f"<div class='roadmap-grid-container'>{html}</div>", height=300, scrolling=False)

# --- ANÁLISE E SUGESTÃO ---
st.subheader("🧠 Sugestão Inteligente")

if len(st.session_state.historico) >= 9:
    analise = AnalisePadroes(st.session_state.historico)
    resultado = analise.sugestao_inteligente()
    st.session_state.ultima_sugestao = resultado

    if resultado["sugerir"]:
        st.success(f"🎯 Sugestão: **{resultado['entrada']}** com confiança de {resultado['confianca']}%")
        st.markdown(f"**Motivos Identificados:** {', '.join(resultado['motivos'])}")
        st.markdown(f"**Últimos 5 resultados:** {' - '.join(resultado['ultimos_resultados'])}")
        st.markdown("**Frequência histórica:**")
        st.write(resultado["frequencias"])
        
        if "analise_detalhada" in resultado:
            with st.expander("🔍 Ver análise detalhada"):
                for categoria, lista in resultado["analise_detalhada"].items():
                    st.markdown(f"**{categoria}:** {', '.join(lista)}")
    else:
        st.warning(f"🤖 Sem sugestão agora: {resultado['motivos'][0]}")
else:
    st.info("⏳ Insira pelo menos 9 resultados para ativar a análise.")
