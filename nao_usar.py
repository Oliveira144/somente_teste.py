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
    # A lógica original pode ser mais sobre 'não igual ao anterior e não igual ao ante-anterior'
    # Vamos redefinir para um zigzag mais clássico (P,B,P ou B,P,B)
    zigzags = 0
    if len(resultado_series) < 3:
        return 0
    for i in range(2, len(resultado_series)):
        # Verifica se os três últimos não são iguais e se o primeiro e o terceiro são iguais (alternância)
        if (resultado_series[i-2] == resultado_series[i] and
            resultado_series[i-2] != resultado_series[i-1]):
            zigzags += 1
    return zigzags

def detectar_streaks(resultado_series):
    streaks = []
    if not resultado_series.empty:
        atual = resultado_series.iloc[0]
        cont = 1
        for i in range(1, len(resultado_series)):
            if resultado_series.iloc[i] == atual:
                cont += 1
            else:
                if cont >= 2: # Contabiliza streaks de 2 ou mais
                    streaks.append({'lado': atual, 'contagem': cont})
                atual = resultado_series.iloc[i]
                cont = 1
        if cont >= 2: # Adiciona o último streak, se houver
            streaks.append({'lado': atual, 'contagem': cont})
    return streaks

def freq_resultados(df_analise):
    total = len(df_analise)
    if total == 0:
        return {'P': 0, 'B': 0, 'T': 0}
    freq = df_analise["Resultado"].value_counts(normalize=True).reindex(['P', 'B', 'T'], fill_value=0) * 100
    return freq.to_dict()

def sugestao_de_entrada(df_completo):
    # Usaremos os últimos N resultados para a maioria das análises de sugestão
    n_jogos_sugestao = 20 # Parâmetro ajustável para a profundidade da análise
    df = df_completo.tail(n_jogos_sugestao).copy()

    entrada_segura = []

    if df.empty:
        return ["Nenhum dado recente para análise de sugestão."]

    # 1. Frequência de Empates e Ciclo
    freq_t = freq_resultados(df).get('T', 0)
    if freq_t < 10: # Se empates estão abaixo de 10% nos últimos N jogos
        # Verifica a última vez que um empate ocorreu
        ultimos_ties_idx = df_completo[df_completo["Resultado"] == "T"].index
        if not ultimos_ties_idx.empty:
            desde_ultimo_tie = len(df_completo) - ultimos_ties_idx[-1]
            if desde_ultimo_tie > 8 and freq_t < 15: # Se não teve empate por mais de 8 jogos e a frequência geral é baixa
                entrada_segura.append("🟢 **TIE (Empate)**: Ciclo pode estar maduro (não empata há muito tempo e frequência baixa).")
        else: # Nunca teve empate
             if len(df_completo) > 15: # Se o histórico já tem um tamanho razoável e nunca empatou
                 entrada_segura.append("🟢 **TIE (Empate)**: Ciclo pode estar maduro (nenhum empate no histórico).")


    # 2. Vantagem de Soma (últimos N jogos)
    player_med = df["Player"].mean()
    banker_med = df["Banker"].mean()
    if player_med > banker_med + 1: # Diferença de 1 ponto ou mais na média
        entrada_segura.append(f"🔵 **PLAYER**: Soma média ({player_med:.1f}) consistentemente mais alta. Vantagem no lance de dados.")
    elif banker_med > player_med + 1:
        entrada_segura.append(f"🔴 **BANKER**: Soma média ({banker_med:.1f}) consistentemente mais alta. Vantagem no lance de dados.")
    
    # 3. ZigZag Ativo
    zigzag_count = detectar_zigzag(df["Resultado"])
    if zigzag_count >= 2 and len(df) >= 5: # Pelo menos 2 zigzags nos últimos 5 jogos
        ultimo_resultado = df["Resultado"].iloc[-1]
        if ultimo_resultado == 'P':
            entrada_segura.append("🔁 **BANKER (Contra ZigZag)**: Padrão ZigZag (PBPB...) ativo. Último foi Player, Banker pode vir agora.")
        elif ultimo_resultado == 'B':
            entrada_segura.append("🔁 **PLAYER (Contra ZigZag)**: Padrão ZigZag (PBPB...) ativo. Último foi Banker, Player pode vir agora.")

    # 4. Streaks (últimos N jogos)
    streaks = detectar_streaks(df["Resultado"])
    if streaks:
        ultimo_streak = streaks[-1]
        if ultimo_streak['contagem'] >= 3: # Streak de 3 ou mais
            lado_nome = "Player" if ultimo_streak['lado'] == "P" else "Banker" if ultimo_streak['lado'] == "B" else "Tie"
            entrada_segura.append(f"🔥 **{lado_nome}**: Streak forte de {ultimo_streak['contagem']} consecutivos. Tendência de seguir o lado.")
        elif ultimo_streak['contagem'] == 2 and len(streaks) >= 2 and streaks[-2]['lado'] == ultimo_streak['lado']:
            # Padrão de 2 duplos (PPBB) - pode indicar alternância de duplos
            entrada_segura.append(f"⚠️ **{lado_nome}**: Padrão de 'duplos' ativo. {ultimo_streak['lado']}{ultimo_streak['lado']} pode indicar alternância.")

    # 5. Padrão de "Não Repetição"
    if len(df) >= 3:
        if df["Resultado"].iloc[-1] != df["Resultado"].iloc[-2] and df["Resultado"].iloc[-2] != df["Resultado"].iloc[-3]:
            # Padrão de não repetição (P, B, T ou P, B, P - mas não alternância exata)
            # Ex: P, B, T -> próximo pode ser P (seguindo o ciclo) ou B (quebrando)
            # Isso é mais uma observação do que uma sugestão forte sem contexto
            pass

    # 6. Analisar a SOMA dos Dados (tendências)
    # Aqui, a lógica é mais avançada e pode envolver Machine Learning ou estatística mais profunda.
    # Por enquanto, mantemos a análise de médias simples.
    # Futuramente: Análise de desvio padrão das somas, contagem de naturais (7 ou 11)

    return entrada_segura

# --- Mostrar Análises e Sugestões ---
st.markdown("---")
st.header("📊 Análise Detalhada e Sugestões Inteligentes")

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

# Sugestões
st.subheader("✨ Sugestões Inteligentes de Entrada")
sugestoes = sugestao_de_entrada(df)

if sugestoes:
    for s in sugestoes:
        st.success(s)
else:
    st.warning("Nenhuma entrada segura detectada neste momento. Continue adicionando dados ou aguarde novos padrões.")

st.markdown("---")
st.info("Lembre-se: Este analisador é uma ferramenta de apoio. Jogos de azar envolvem risco e dependem da sorte.")
