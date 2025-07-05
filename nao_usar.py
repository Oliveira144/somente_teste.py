import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
st.set_page_config(page_title="Bac Bo Inteligente", layout="wide", initial_sidebar_state="expanded")
st.title("🎲 Analisador Inteligente de Padrões - Bac Bo Evolution")

st.markdown("""
<style>
    .stApp {
        background-color: #262730;
        color: white;
    }
    .stTextInput>div>div>input {
        color: black;
    }
    .stTextArea>div>div>textarea {
        color: black;
    }
    /* Estilos para as caixas de Ação Recomendada */
    .stAlert {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        font-size: 1.2em;
        font-weight: bold;
        text-align: center;
    }
    .alert-success {
        background-color: #28a745; /* Verde */
        color: white;
    }
    .alert-danger {
        background-color: #dc3545; /* Vermelho */
        color: white;
    }
    .alert-warning {
        background-color: #ffc107; /* Amarelo */
        color: black;
    }
    .stSuccess {
        background-color: #28a745 !important;
        color: white !important;
    }
    .stWarning {
        background-color: #ffc107 !important;
        color: black !important;
    }
    .stError {
        background-color: #dc3545 !important;
        color: white !important;
    }
    /* Estilo para a tabela do histórico */
    .stDataFrame {
        color: black; /* Cor do texto dentro da tabela */
    }
    .stDataFrame thead th {
        background-color: #3e3f47; /* Cor de fundo do cabeçalho */
        color: white; /* Cor do texto do cabeçalho */
    }
    .stDataFrame tbody tr:nth-child(even) {
        background-color: #f0f2f6; /* Cor de fundo para linhas pares */
    }
    .stDataFrame tbody tr:nth-child(odd) {
        background-color: #ffffff; /* Cor de fundo para linhas ímpares */
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
Olá! Bem-vindo ao analisador de padrões Bac Bo.
Para começar, insira os resultados recentes no campo abaixo.
Cada linha deve seguir o formato: **SomaPlayer,SomaBanker,Resultado**
(Ex: `11,4,P` para Player, `7,11,B` para Banker, `6,6,T` para Tie).
""")

# --- Inicialização do Session State para Histórico ---
if 'historico_dados' not in st.session_state:
    st.session_state.historico_dados = []

# --- Entrada de Dados Individualmente (para facilitar a adição) ---
st.subheader("Adicionar Novo Resultado")
col1, col2, col3 = st.columns(3)
with col1:
    player_soma = st.number_input("Soma Player (2-12)", min_value=2, max_value=12, value=7, key="player_soma_input")
with col2:
    banker_soma = st.number_input("Soma Banker (2-12)", min_value=2, max_value=12, value=7, key="banker_soma_input")
with col3:
    resultado_op = st.selectbox("Resultado", ['P', 'B', 'T'], key="resultado_select")

if st.button("Adicionar Linha ao Histórico"):
    st.session_state.historico_dados.append((player_soma, banker_soma, resultado_op))
    st.rerun() # Atualiza a página para mostrar o novo histórico

# --- Exibir e Gerenciar Histórico ---
st.subheader("Histórico Atual")
if st.session_state.historico_dados:
    # Cria um DataFrame temporário para exibição
    df_historico_exibicao = pd.DataFrame(st.session_state.historico_dados, columns=["Player", "Banker", "Resultado"])
    st.dataframe(df_historico_exibicao.tail(20), use_container_width=True) # Mostra os últimos 20
    
    col_hist1, col_hist2 = st.columns(2)
    with col_hist1:
        if st.button("Remover Última Linha"):
            if st.session_state.historico_dados:
                st.session_state.historico_dados.pop()
                st.rerun()
    with col_hist2:
        if st.button("Limpar Histórico Completo"):
            st.session_state.historico_dados = []
            st.rerun()
else:
    st.info("Nenhum dado no histórico ainda. Adicione resultados acima ou cole na caixa de texto.")

# --- Entrada de Dados em Massa (compatibilidade com a versão anterior) ---
st.subheader("Adicionar Histórico em Massa (Cole aqui)")
historico_input_mass = st.text_area("Cole múltiplas linhas (Player,Banker,Resultado por linha)", height=150,
    value="")

if st.button("Processar Histórico em Massa"):
    linhas = historico_input_mass.strip().split("\n")
    novos_dados = []
    erros = []
    for linha in linhas:
        try:
            p_str, b_str, r = linha.strip().split(',')
            p = int(p_str)
            b = int(b_str)
            r = r.upper()

            # Validação mais rigorosa para dados em massa
            if not (2 <= p <= 12 and 2 <= b <= 12):
                erros.append(f"Valores de soma inválidos na linha: {linha} (Soma deve ser entre 2 e 12).")
                continue
            if r not in ['P', 'B', 'T']:
                erros.append(f"Resultado inválido na linha: {linha} (Resultado deve ser 'P', 'B' ou 'T').")
                continue
            novos_dados.append((p, b, r))
        except ValueError:
            erros.append(f"Formato incorreto na linha: {linha} (Esperado: Player,Banker,Resultado).")
        except Exception as e:
            erros.append(f"Erro desconhecido na linha: {linha} - {e}")
    
    if erros:
        for erro in erros:
            st.error(erro)
    else:
        st.session_state.historico_dados.extend(novos_dados)
        st.success(f"{len(novos_dados)} linhas adicionadas com sucesso ao histórico!")
        st.rerun()

# --- Processar e Analisar Dados ---
if not st.session_state.historico_dados:
    st.warning("Adicione dados para iniciar a análise!")
    st.stop() # Interrompe a execução se não houver dados

df = pd.DataFrame(st.session_state.historico_dados, columns=["Player", "Banker", "Resultado"])

# --- Algoritmos de Análise ---

def detectar_zigzag(resultado_series):
    # Um zigzag ocorre quando há uma alternância: A, B, A (ou B, A, B)
    zigzags = 0
    if len(resultado_series) < 3:
        return 0
    for i in range(2, len(resultado_series)):
        if (resultado_series.iloc[i-2] == resultado_series.iloc[i] and
            resultado_series.iloc[i-2] != resultado_series.iloc[i-1]):
            zigzags += 1
    return zigzags

def detectar_streaks(df_analise):
    streaks = []
    if df_analise.empty:
        return streaks

    current_streak_data = {
        'lado': df_analise["Resultado"].iloc[0],
        'contagem': 1,
        'somas': [df_analise["Player"].iloc[0] if df_analise["Resultado"].iloc[0] == 'P' else df_analise["Banker"].iloc[0]]
    }

    for i in range(1, len(df_analise)):
        if df_analise["Resultado"].iloc[i] == current_streak_data['lado']:
            current_streak_data['contagem'] += 1
            current_streak_data['somas'].append(df_analise["Player"].iloc[i] if current_streak_data['lado'] == 'P' else df_analise["Banker"].iloc[i])
        else:
            if current_streak_data['contagem'] >= 2:
                streaks.append(current_streak_data)
            current_streak_data = {
                'lado': df_analise["Resultado"].iloc[i],
                'contagem': 1,
                'somas': [df_analise["Player"].iloc[i] if df_analise["Resultado"].iloc[i] == 'P' else df_analise["Banker"].iloc[i]]
            }
    
    if current_streak_data['contagem'] >= 2: # Add the last streak
        streaks.append(current_streak_data)
    return streaks

def freq_resultados(df_analise):
    total = len(df_analise)
    if total == 0:
        return {'P': 0, 'B': 0, 'T': 0}
    freq = df_analise["Resultado"].value_counts(normalize=True).reindex(['P', 'B', 'T'], fill_value=0) * 100
    return freq.to_dict()

def analisar_somas_proximas(df_analise, n_ultimos=7):
    somas_proximas_detectadas = []
    if len(df_analise) < 2: # Precisa de pelo menos 2 resultados para comparar
        return somas_proximas_detectadas

    # Considera os últimos resultados
    df_recentes = df_analise.tail(n_ultimos).reset_index(drop=True)

    for i in range(len(df_recentes) - 1):
        r_atual = df_recentes["Resultado"].iloc[i]
        r_prox = df_recentes["Resultado"].iloc[i+1]

        if r_atual == r_prox and r_atual != 'T': # Se o mesmo lado venceu (e não foi Tie)
            soma_atual = df_recentes["Player"].iloc[i] if r_atual == 'P' else df_recentes["Banker"].iloc[i]
            soma_prox = df_recentes["Player"].iloc[i+1] if r_prox == 'P' else df_recentes["Banker"].iloc[i+1]

            # Verifica se as somas estão próximas (ex: diferença <= 1 ou ambas 7/8)
            if abs(soma_atual - soma_prox) <= 1 or (soma_atual in [7,8] and soma_prox in [7,8]):
                somas_proximas_detectadas.append({
                    'lado': r_atual,
                    'soma_1': soma_atual,
                    'soma_2': soma_prox
                })
    return somas_proximas_detectadas

def sugestao_de_entrada(df_completo):
    n_jogos_sugestao = 20
    df_analise_sugestao = df_completo.tail(n_jogos_sugestao).copy()

    sugestoes_geradas = []
    
    # Dicionário para contar o consenso de cada lado
    consenso_lado = {'P': 0, 'B': 0, 'T': 0}

    if df_analise_sugestao.empty:
        return sugestoes_geradas, consenso_lado

    # 1. Frequência de Empates e Ciclo
    freq_t = freq_resultados(df_analise_sugestao).get('T', 0)
    
    ultimos_ties_idx = df_completo[df_completo["Resultado"] == "T"].index
    desde_ultimo_tie = len(df_completo)

    if not ultimos_ties_idx.empty:
        desde_ultimo_tie = len(df_completo) - ultimos_ties_idx[-1]

    if (5 <= desde_ultimo_tie <= 12) or (freq_t < 15 and desde_ultimo_tie > 8):
        sugestoes_geradas.append("🟢 **TIE (Empate)**: Padrão estatístico (lacuna de 5-12 jogos) sugere TIE próximo.")
        consenso_lado['T'] += 1
    elif freq_t < 10 and desde_ultimo_tie > 15:
        sugestoes_geradas.append("🟢 **TIE (Empate)**: Alta chance, pois não empata há muito tempo (>15 jogos) e frequência baixa.")
        consenso_lado['T'] += 1
    
    # 2. Vantagem de Soma (últimos N jogos)
    player_med = df_analise_sugestao["Player"].mean()
    banker_med = df_analise_sugestao["Banker"].mean()
    if player_med > banker_med + 1:
        sugestoes_geradas.append(f"🔵 **PLAYER**: Soma média ({player_med:.1f}) consistentemente mais alta. Vantagem no lance de dados.")
        consenso_lado['P'] += 1
    elif banker_med > player_med + 1:
        sugestoes_geradas.append(f"🔴 **BANKER**: Soma média ({banker_med:.1f}) consistentemente mais alta. Vantagem no lance de dados.")
        consenso_lado['B'] += 1
    
    # 3. ZigZag Ativo
    zigzag_count = detectar_zigzag(df_analise_sugestao["Resultado"])
    if zigzag_count >= 2 and len(df_analise_sugestao) >= 5:
        ultimo_resultado = df_analise_sugestao["Resultado"].iloc[-1]
        if ultimo_resultado == 'P':
            sugestoes_geradas.append("🔁 **BANKER (Contra ZigZag)**: Padrão ZigZag (PBPB...) ativo. Último foi Player, Banker pode vir agora.")
            consenso_lado['B'] += 0.5 # Menor peso, pois a imagem diz "fraco"
        elif ultimo_resultado == 'B':
            sugestoes_geradas.append("🔁 **PLAYER (Contra ZigZag)**: Padrão ZigZag (PBPB...) ativo. Último foi Banker, Player pode vir agora.")
            consenso_lado['P'] += 0.5 # Menor peso
    else:
        sugestoes_geradas.append("⚠️ **ZigZag Fraco**: Não há um padrão ZigZag claro ou consistente. Evite apostar baseado apenas na alternância de cores.")


    # 4. Streaks (últimos N jogos) - APRIMORADO para considerar somas altas
    streaks = detectar_streaks(df_analise_sugestao)
    if streaks:
        ultimo_streak = streaks[-1]
        lado_nome = "Player" if ultimo_streak['lado'] == "P" else "Banker" if ultimo_streak['lado'] == "B" else "Tie"
        
        somas_altas_no_streak = [s for s in ultimo_streak['somas'] if s >= 8]
        
        if ultimo_streak['contagem'] >= 3:
            if len(somas_altas_no_streak) >= (ultimo_streak['contagem'] * 0.75): # Pelo menos 75% das somas são altas
                sugestoes_geradas.append(f"🔥 **{lado_nome} (Streak Forte com Somas Altas)**: {ultimo_streak['contagem']} consecutivos com somas consistentemente altas ({somas_altas_no_streak}). Tendência de seguir o lado.")
                consenso_lado[ultimo_streak['lado']] += 1.5 # Maior peso para streak forte com somas altas
            else:
                sugestoes_geradas.append(f"🔥 **{lado_nome} (Streak de {ultimo_streak['contagem']} )**: Tendência de seguir o lado, mas as somas não foram predominantemente altas.")
                consenso_lado[ultimo_streak['lado']] += 1
        
        elif ultimo_streak['contagem'] == 2 and len(streaks) >= 2 and streaks[-2]['lado'] == ultimo_streak['lado']:
            sugestoes_geradas.append(f"⚠️ **{lado_nome}**: Padrão de 'duplos' ativo. {ultimo_streak['lado']}{ultimo_streak['lado']} pode indicar alternância.")
            consenso_lado[ultimo_streak['lado']] += 0.25 # Peso menor para padrão de duplos


    # 5. Repetição de Somas Próximas (NOVO)
    somas_prox = analisar_somas_proximas(df_analise_sugestao, n_ultimos=7)
    if somas_prox:
        for sp in somas_prox:
            # Para evitar duplicidade de sugestão se houver múltiplos padrões próximos
            if f"✨ **Padrão de Somas Próximas em {sp['lado']}**" not in sugestoes_geradas:
                sugestoes_geradas.append(f"✨ **Padrão de Somas Próximas em {sp['lado']}**: Duas vitórias consecutivas de {sp['lado']} com somas {sp['soma_1']} e {sp['soma_2']}. Sugere repetição do comportamento de somas.")
                consenso_lado[sp['lado']] += 0.75 # Peso médio

    return sugestoes_geradas, consenso_lado

# NOVA FUNÇÃO: Determinar a Ação Recomendada
def determinar_acao_recomendada(consenso_lado):
    # Parâmetros de decisão
    min_consenso_para_apostar = 1.5 # Mínimo de "pontos" de consenso para recomendar uma aposta
    confianca_base_por_ponto = 25 # Porcentagem de confiança por ponto de consenso

    lados_com_consenso = {lado: score for lado, score in consenso_lado.items() if score >= min_consenso_para_apostar}

    if not lados_com_consenso:
        return "AGUARDAR", 0, "Nenhuma lógica forte o suficiente ou consenso claro.", "warning"

    # Encontra o lado com o maior consenso
    lado_recomendado = max(lados_com_consenso, key=lados_com_consenso.get)
    maior_consenso = lados_com_consenso[lado_recomendado]

    # Verifica se há lados com consenso forte que se contradizem
    # Ex: Player tem 2 pontos e Banker tem 2 pontos -> Aguardar
    conflito = False
    for lado, score in lados_com_consenso.items():
        if lado != lado_recomendado and score >= min_consenso_para_apostar:
            conflito = True
            break
    
    if conflito:
        return "AGUARDAR", 0, "Lógicas conflitantes fortes para lados diferentes.", "warning"

    # Calcula a confiança
    confianca = min(100, int(maior_consenso * confianca_base_por_ponto))

    # Mensagem final
    lado_nome_completo = ""
    if lado_recomendado == 'P': lado_nome_completo = "PLAYER"
    elif lado_recomendado == 'B': lado_nome_completo = "BANKER"
    elif lado_recomendado == 'T': lado_nome_completo = "TIE"

    return f"APOSTAR NO {lado_nome_completo}", confianca, f"Consenso de {maior_consenso:.1f} ponto(s) de algoritmos para {lado_nome_completo}.", "success"

# --- Mostrar Análises e Sugestões ---
st.markdown("---")
st.header("📊 Análise Detalhada e Sugestões Inteligentes")

# Gera sugestões e o consenso
sugestoes, consenso_contagem = sugestao_de_entrada(df)
acao, confianca, justificativa, acao_tipo = determinar_acao_recomendada(consenso_contagem)

# Exibe a Ação Recomendada (com CSS personalizado)
st.markdown(f"""
<div class="stAlert alert-{acao_tipo}">
    Ação Recomendada: {acao}
    <br>
    Confiança: {confianca}%
    <br>
    <span style="font-size: 0.8em; font-weight: normal;">{justificativa}</span>
</div>
""", unsafe_allow_html=True)


# Visão Geral
st.subheader("Visão Geral do Histórico")
col_overview1, col_overview2 = st.columns(2)
with col_overview1:
    st.metric("Total de Jogos Analisados", len(df))
with col_overview2:
    freq = freq_resultados(df)
    st.metric(f"Frequência Player", f"{freq['P']:.1f}%")
    st.metric(f"Frequência Banker", f"{freq['B']:.1f}%")
    st.metric(f"Frequência Tie", f"{freq['T']:.1f}%")

# Gráficos
st.subheader("Visualização dos Resultados")
if len(df) >= 1:
    # Gráfico de Frequência
    freq_df = pd.DataFrame(list(freq_resultados(df).items()), columns=['Resultado', 'Porcentagem'])
    fig_freq = px.bar(freq_df, x='Resultado', y='Porcentagem', 
                      title='Frequência de Resultados (Geral)',
                      color='Resultado',
                      color_discrete_map={'P': 'blue', 'B': 'red', 'T': 'green'},
                      template="plotly_dark")
    st.plotly_chart(fig_freq, use_container_width=True)

    # Gráfico de Sequência (últimos N resultados)
    n_ultimos_para_grafico = min(50, len(df)) # Mostra até os últimos 50 resultados
    df_ultimos = df.tail(n_ultimos_para_grafico).reset_index(drop=True)
    df_ultimos['Indice'] = df_ultimos.index + 1 # Para ter um eixo X sequencial

    fig_seq = px.line(df_ultimos, x='Indice', y='Resultado', 
                      title=f'Sequência dos Últimos {n_ultimos_para_grafico} Resultados',
                      color='Resultado',
                      color_discrete_map={'P': 'blue', 'B': 'red', 'T': 'green'},
                      line_shape='hv', # Linhas horizontais e verticais para clareza
                      markers=True,
                      template="plotly_dark")
    fig_seq.update_layout(yaxis_title="Resultado (P/B/T)", showlegend=False)
    st.plotly_chart(fig_seq, use_container_width=True)

# Sugestões Detalhadas
st.subheader("✨ Sugestões Inteligentes de Entrada (Detalhes)")
if sugestoes:
    for s in sugestoes:
        # Verifica se é a mensagem de zigzag fraco para usar st.warning
        if "ZigZag Fraco" in s:
            st.warning(s)
        else:
            st.success(s)
else:
    st.warning("Nenhuma entrada segura detectada neste momento. Continue adicionando dados ou aguarde novos padrões.")

st.markdown("---")
st.info("Lembre-se: Este analisador é uma ferramenta de apoio. Jogos de azar envolvem risco e dependem da sorte.")
