
importar streamlit como st
importar aleatório
de coleções importar contador

classe AnalisePadroes:
    def __init__(self, histórico):
        self.historico = histórico

    def detectar_surf(self):
        sequência = 1
        cor = self.historico[-1] if self.historico else Nenhum
        para i no intervalo(len(self.historico) - 2, -1, -1):
            se self.historico[i] == cor e cor != 'Empate':
                sequência += 1
            outro:
                quebrar
        retornar {"ativo": streak >= 3, "streak": streak, "cor": cor}

    def detectar_zigzag(self):
        últimos = self.historico[-5:]
        contagem = 0
        para i no intervalo(1, len(últimos)):
            if ultimos[i] != ultimos[i-1] e ultimos[i] != 'Empate' e ultimos[i-1] != 'Empate':
                contagem += 1
        retornar {"ativo": contagem >= 3}

    def detectar_empate_recorrente(self):
        posicoes = [i para i, r em enumerate(self.historico) se r == 'Empate']
        se len(posições) >= 2:
            ultima = posicoes[-1]
            distancia = len(self.histórico) - 1 - ultima
            return {"ativo": 15 <= distancia <= 35}
        retornar {"ativo": Falso}

    def detectar_espelho(self):
        seq = self.historico[-4:]
        return {"ativo": seq == ['Casa', 'Visitante', 'Visitante', 'Casa']}

    def detectar_4x4(self):
        se len(self.historico) < 8:
            retornar {"ativo": Falso}
        bloco1 = self.histórico[-8:-4]
        bloco2 = self.historico[-4:]
        retornar {"ativo": len(conjunto(bloco1)) == 1 e len(conjunto(bloco2)) == 1 e bloco1[0] != bloco2[0]}

    def detectar_custom_2x1x2x1x1x1x3(self):
        se len(self.historico) < 11:
            retornar {"ativo": Falso}
        seq = self.historico[-11:]
        contagem = [2,1,2,1,1,1,3]
        eu = 0
        partes = []
        enquanto i < len(seq):
            atual = seq[i]
            j = i
            enquanto j < len(seq) e seq[j] == atual:
                j += 1
            partes.append(j - i)
            i = j
        return {"ativo": partes[-7:] == contagem}

    def detectar_3x1(self):
        se len(self.historico) < 4:
            retornar {"ativo": Falso}
        seq = self.historico[-4:]
        retornar {"ativo": seq.count(seq[0]) == 3 e seq[3] != seq[0]}

    def detectar_3x3(self):
        se len(self.historico) < 6:
            retornar {"ativo": Falso}
        seq = self.historico[-6:]
        retornar {"ativo": seq[:3] == seq[3:] e len(set(seq[:3])) == 1}

    def detectar_duplas(self):
        se len(self.historico) < 6:
            retornar {"ativo": Falso}
        pares = [self.historico[i:i+2] para i no intervalo(0, len(self.historico)-1, 2)]
        return {"ativo": all(len(set(par)) == 1 para par em pares[-3:])}

    def detectar_escada(self):
        se len(self.historico) < 6:
            retornar {"ativo": Falso}
        seq = self.historico[-12:]
        blocos = []
        eu = 0
        enquanto i < len(seq):
            j = i
            enquanto j < len(seq) e seq[j] == seq[i]:
                j += 1
            blocos.append((seq[i], j - i))
            i = j
        blocos = blocos[-3:]
        = [b[1] para b em blocos]
        return {"ativo": tamanhos == sorted(tamanhos) and len(set(b[0] for b in blocos)) > 1}

    def gerar_sugestao(self):
        surf = self.detectar_surf()
        se surf["ativo"] e surf["streak"] >= 4:
            sugerido = "Visitante" if surf["cor"] == "Casa" else "Casa"
            return sugerido, "Quebra de Surf", 90

        if self.detectar_4x4()["ativo"]:
            cor = self.historico[-1]
            sugerido = "Casa" if cor == "Visitante" else "Visitante"
            return sugerido, "Padrão 4x4", 85

        if self.detectar_custom_2x1x2x1x1x1x3()["ativo"]:
            return "Casa", "Padrão 2x1x2x1x1x1x3", 88

        if self.detectar_espelho()["ativo"]:
            retornar "Casa", "Espelho", 80

        if self.detectar_zigzag()["ativo"]:
            ultima = self.historico[-1]
            sugerido = "Visitante" if ultima == "Casa" else "Casa"
            return sugerido, "Zig-Zag", 78

        if self.detectar_empate_recorrente()["ativo"]:
            return "Empate", "Empate Recorrente", 75

        if self.detectar_escada()["ativo"]:
            retornar "Casa", "Escada", 70

        if self.detectar_3x3()["ativo"]:
            retornar "Visitante", "3x3", 70

        if self.detectar_3x1()["ativo"]:
            retornar "Casa", "3x1", 70

        if self.detectar_duplas()["ativo"]:
            retornar "Visitante", "Duplas", 65

        últimos = self.historico[-15:]
        contagem = Counter(últimos)
        if contagem["Casa"] >= 9 e contagem["Casa"] > contagem["Visitante"] + 2:
            retornar "Visitante", "Frequência", 65
        elif contagem["Visitante"] >= 9 e contagem["Visitante"] > contagem["Casa"] + 2:
            return "Casa", "Frequência", 65
        elif contagem["Empate"] >= 3:
            return "Empate", "Frequência", 60

        return random.choice(["Casa", "Visitante"]), "Aleatória", 50


# Interface Streamlit
se 'history' não estiver em st.session_state:
    st.session_state.history = []
se 'log_entradas' não estiver em st.session_state:
    st.session_state.log_entradas = []
se 'streak' não estiver em st.session_state:
    st.session_state.streak = {"tipo": Nenhum, "contagem": 0}
se 'sugestao' não estiver em st.session_state:
    st.session_state.sugestao = Nenhum

st.title("âš½ Football Studio Analyzer - Todos os PadrÃµes")

col1, col2, col3 = st.columns(3)
com col1:
    se st.button("ðŸ Casa"):
        resultado = "Casa"
        st.session_state.history.append(resultado)
com col2:
    se st.button("ðŸ¤ Empate"):
        resultado = "Empatar"
        st.session_state.history.append(resultado)
com col3:
    se st.button("âœˆï¸ Visitante"):
        resultado = "Visitante"
        st.session_state.history.append(resultado)

se len(st.session_state.history) > 0:
    analisar = AnalisePadroes(st.session_state.history)
    sugestão, padrão, confiança = analise.gerar_sugestao()

    se st.session_state.sugestao:
        entrada_anterior = st.session_state.sugestao['sugestao']
        resultado_real = st.session_state.history[-1]
        acertou = entrada_anterior == resultado_real
        st.session_state.log_entradas.append({
            "entrada": entrada_anterior,
            "real": resultado_real,
            "acertou": acertou,
            "padrão": st.session_state.sugestao['padrão']
        })

    st.session_state.sugestao = {
        "sugestão": sugestão,
        "padrão": padrão,
        "confiança": confiança
    }

    se st.session_state.streak['type'] == resultado:
        st.session_state.streak['contagem'] += 1
    outro:
        st.session_state.streak = {'tipo': resultado, 'contagem': 1}

se st.session_state.sugestao:
    st.subheader("ðŸŽ¯ Sugestão de Entrada")
    st.markdown(f"**Entrada:** `{st.session_state.sugestao['sugestao']}`")
    st.markdown(f"**Padrão Detectado:** `{st.session_state.sugestao['padrao']}`")
    st.markdown(f"**Confiança:** `{st.session_state.sugestao['confianca']}%`")

st.subheader("ðŸ“Š Histórico de Resultados")
para r em reversed(st.session_state.history):
    cor = "#dc2626" se r == "Casa" senão "#3b82f6" se r == "Visitante" senão "#6b7280"
    st.markdown(f"<div style='display:inline-block;largura:20px;altura:20px;raio da borda:50%;margem:2px;fundo:{cor}'></div>", unsafe_allow_html=True)

st.subheader("ðŸ“ˆ Estatísticas")
total = len(st.session_state.history)
se total:
    casa = st.session_state.history.count("Casa")
    empate = st.session_state.history.count("Empate")
    visitante = st.session_state.history.count("Visitante")
    st.write(f"Casa: {casa} ({(casa/total)*100:.1f}%) | Empate: {empate} ({(empate/total)*100:.1f}%) | Visitante: {visitante} ({(visitante/total)*100:.1f}%)")

st.subheader("âœ… Conferência de Entradas")
acertos = sum(1 for l in st.session_state.log_entradas if l["acertou"])
total_logs = len(st.session_state.log_entradas)
se total_logs:
    st.write(f"Acertos: {acertos} / {total_logs} ({(acertos/total_logs)*100:.1f}%)")
    with st.expander("ðŸ“‹ Ver Histórico de Entradas"):
        para i, faça login enumerate(reversed(st.session_state.log_entradas[-15:])):
            st.write(f"{i+1}. Entrada: `{log['entrada']}` | Resultado: `{log['real']}` â†' {'âœ…' if log['acertou'] else 'â Œ'} via `{log['padrao']}`")
