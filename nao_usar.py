import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

# --- Configuração da Página ---
st.set_page_config(page_title="Bac Bo Inteligente", layout="wide", initial_sidebar_state="expanded")
st.title("🎲 Analisador Inteligente de Padrões - Bac Bo Evolution (v3.0 - Correção de Lógica)")

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
    st.rerun()

# --- Exibir e Gerenciar Histórico ---
st.subheader("Histórico Atual")
if st.session_state.historico_dados:
    df_historico_exibicao = pd.DataFrame(st.session_state.historico_dados, columns=["Player", "Banker", "Resultado"])
    st.dataframe(df_historico_exibicao.tail(20), use_container_width=True)
    
    col_hist1, col_hist2 = st.columns(2)
    with col_hist1:
        if st.button("Remover Última Linha"):
            if st.session_state.historico_dados:
                st.session_session.historico_dados.pop()
                st.rerun()
    with col_hist2:
        if st.button("Limpar Histórico Completo"):
            st.session_state.historico_dados = []
            st.rerun()
else:
    st.info("Nenhum dado no histórico ainda. Adicione resultados acima ou cole na caixa de texto.")

# --- Entrada de Dados em Massa ---
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
    st.stop()

df = pd.DataFrame(st.session_state.historico_dados, columns=["Player", "Banker", "Resultado"])

# --- Algoritmos de Análise Avançados (Mantidos da v2.0) ---

def detectar_zigzag(resultado_series):
    zigzags = 0
    if len(resultado_series) < 3: return 0
    for i in range(2, len(resultado_series)):
        if (resultado_series.iloc[i-2] == resultado_series.iloc[i] and resultado_series.iloc[i-2] != resultado_series.iloc[i-1]):
            zigzags += 1
    return zigzags

def detectar_alternancia_curta(resultado_series, n_ultimos=5):
    if len(resultado_series) < n_ultimos: return 0

    alternancias = 0
    recentes = resultado_series.tail(n_ultimos).tolist()

    for i in range(len(recentes) - 1):
        if recentes[i] != recentes[i+1] and recentes[i+1] != 'T':
            alternancias += 1
    
    return alternancias / (n_ultimos - 1) >= 0.8 # Considera 80% ou mais de alternância

def detectar_streaks(df_analise):
    streaks = []
    if df_analise.empty: return streaks

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
    
    if current_streak_data['contagem'] >= 2:
        streaks.append(current_streak_data)
    return streaks

def freq_resultados(df_analise):
    total = len(df_analise)
    if total == 0: return {'P': 0, 'B': 0, 'T': 0}
    freq = df_analise["Resultado"].value_counts(normalize=True).reindex(['P', 'B', 'T'], fill_value=0) * 100
    return freq.to_dict()

def analisar_somas_proximas(df_analise, n_ultimos=7):
    somas_proximas_detectadas = []
    if len(df_analise) < 2: return somas_proximas_detectadas

    df_recentes = df_analise.tail(n_ultimos).reset_index(drop=True)

    for i in range(len(df_recentes) - 1):
        r_atual = df_recentes["Resultado"].iloc[i]
        r_prox = df_recentes["Resultado"].iloc[i+1]

        if r_atual == r_prox and r_atual != 'T':
            soma_atual = df_recentes["Player"].iloc[i] if r_atual == 'P' else df_recentes["Banker"].iloc[i]
            soma_prox = df_recentes["Player"].iloc[i+1] if r_prox == 'P' else df_recentes["Banker"].iloc[i+1]

            if abs(soma_atual - soma_prox) <= 1 or (soma_atual in [7,8,9] and soma_prox in [7,8,9]):
                somas_proximas_detectadas.append({
                    'lado': r_atual,
                    'soma_1': soma_atual,
                    'soma_2': soma_prox
                })
    return somas_proximas_detectadas

def analisar_near_misses_tie(df_analise, n_ultimos=10):
    near_misses = 0
    if len(df_analise) < n_ultimos: return 0
    
    recentes = df_analise.tail(n_ultimos)
    for index, row in recentes.iterrows():
        if row['Resultado'] != 'T':
            if abs(row['Player'] - row['Banker']) == 1:
                near_misses += 1
    return near_misses

def analisar_soma_vencedora_recorrente(df_analise, n_ultimos=15):
    if len(df_analise) < n_ultimos: return None, 0

    vencedoras = []
    for index, row in df_analise.tail(n_ultimos).iterrows():
        if row['Resultado'] == 'P':
            vencedoras.append(row['Player'])
        elif row['Resultado'] == 'B':
            vencedoras.append(row['Banker'])
    
    if not vencedoras: return None, 0

    contagem_somas = Counter(vencedoras)
    soma_mais_comum = None
    max_ocorrencias = 0

    for soma, count in contagem_somas.items():
        if count > max_ocorrencias:
            max_ocorrencias = count
            soma_mais_comum = soma
    
    if len(vencedoras) > 0:
        return soma_mais_comum, (max_ocorrencias / len(vencedoras)) * 100
    return None, 0

def analisar_distribuicao_somas(df_analise, n_ultimos=20):
    if len(df_analise) < n_ultimos:
        return {'P_Altas_Pct': 0, 'B_Altas_Pct': 0, 'P_Baixas_Pct': 0, 'B_Baixas_Pct': 0}

    df_recentes = df_analise.tail(n_ultimos)

    player_somas_altas = df_recentes[df_recentes['Resultado'] == 'P']['Player'].apply(lambda x: 1 if x >= 8 else 0).sum()
    player_somas_baixas = df_recentes[df_recentes['Resultado'] == 'P']['Player'].apply(lambda x: 1 if x <= 6 else 0).sum()
    total_player_wins = (df_recentes['Resultado'] == 'P').sum()

    banker_somas_altas = df_recentes[df_recentes['Resultado'] == 'B']['Banker'].apply(lambda x: 1 if x >= 8 else 0).sum()
    banker_somas_baixas = df_recentes[df_recentes['Resultado'] == 'B']['Banker'].apply(lambda x: 1 if x <= 6 else 0).sum()
    total_banker_wins = (df_recentes['Resultado'] == 'B').sum()

    return {
        'P_Altas_Pct': (player_somas_altas / total_player_wins * 100) if total_player_wins > 0 else 0,
        'B_Altas_Pct': (banker_somas_altas / total_banker_wins * 100) if total_banker_wins > 0 else 0,
        'P_Baixas_Pct': (player_somas_baixas / total_player_wins * 100) if total_player_wins > 0 else 0,
        'B_Baixas_Pct': (banker_somas_baixas / total_banker_wins * 100) if total_banker_wins > 0 else 0,
    }


def gerar_relatorio_sugestoes(df_completo):
    n_jogos_sugestao = 20 # Analisar os últimos 20 jogos para sugestões
    df_analise_sugestao = df_completo.tail(n_jogos_sugestao).copy()

    sugestoes_geradas = []
    logicas_ativas = {
        'tie_ciclo_forte': False,
        'tie_ciclo_medio': False,
        'player_vantagem_soma': False,
        'banker_vantagem_soma': False,
        'zigzag_soma_real': False, # ZigZag baseado em soma e ritmo
        'zigzag_fraco_apenas_cor': False, # ZigZag fraco = nada confiável
        'alternancia_curta_ativa': False,
        'streak_player_verdadeiro': False, # Streak verdadeiro (somas altas seguidas)
        'streak_banker_verdadeiro': False,
        'streak_player_normal': False,
        'streak_banker_normal': False,
        'somas_proximas_player': False,
        'somas_proximas_banker': False,
        'near_misses_tie_ativos': False,
        'soma_vencedora_player_recorrente': False,
        'soma_vencedora_banker_recorrente': False,
        'distribuicao_somas_player_alta': False,
        'distribuicao_somas_banker_alta': False,
    }

    if df_analise_sugestao.empty:
        return sugestoes_geradas, logicas_ativas

    # --- Lógicas de Análise ---

    # 1. Empates e Ciclo de TIE
    freq_t = freq_resultados(df_analise_sugestao).get('T', 0)
    ultimos_ties_idx = df_completo[df_completo["Resultado"] == "T"].index
    desde_ultimo_tie = len(df_completo)

    if not ultimos_ties_idx.empty:
        desde_ultimo_tie = len(df_completo) - ultimos_ties_idx[-1]

    if (6 <= desde_ultimo_tie <= 10): # "6+ jogadas sem empate", "entre 6 a 10 jogadas"
        sugestoes_geradas.append("🟢 **TIE (Ciclo Madura)**: Padrão estatístico (6-10 jogos sem TIE) sugere TIE próximo.")
        logicas_ativas['tie_ciclo_forte'] = True
    elif (11 <= desde_ultimo_tie <= 15) or (freq_t < 15 and desde_ultimo_tie > 8):
        sugestoes_geradas.append("🟢 **TIE (Ciclo Médio)**: Padrão cíclico (11-15 jogos ou baixa freq).")
        logicas_ativas['tie_ciclo_medio'] = True
    elif freq_t < 10 and desde_ultimo_tie > 15:
        sugestoes_geradas.append("🟢 **TIE (Ciclo Atrasado)**: Muito tempo sem TIE (>15 jogos) e frequência baixa. Aumenta a chance.")
        logicas_ativas['tie_ciclo_forte'] = True
    
    # Near Misses para TIE
    near_misses_count = analisar_near_misses_tie(df_analise_sugestao, n_ultimos=10)
    if near_misses_count >= 3:
        sugestoes_geradas.append(f"🟡 **TIE (Near Misses)**: {near_misses_count} 'quase empates' recentes. Aumenta a chance de um TIE real.")
        logicas_ativas['near_misses_tie_ativos'] = True

    # 2. Vantagem de Soma
    player_med = df_analise_sugestao["Player"].mean()
    banker_med = df_analise_sugestao["Banker"].mean()
    
    # "Aposte no lado que está com soma consistentemente maior."
    if player_med > banker_med + 1.5: # Diferença maior para ser "consistentemente maior"
        sugestoes_geradas.append(f"🔵 **PLAYER**: Soma média ({player_med:.1f}) consistentemente mais alta. Vantagem no lance de dados.")
        logicas_ativas['player_vantagem_soma'] = True
    elif banker_med > player_med + 1.5:
        sugestoes_geradas.append(f"🔴 **BANKER**: Soma média ({banker_med:.1f}) consistentemente mais alta. Vantagem no lance de dados.")
        logicas_ativas['banker_vantagem_soma'] = True
    
    # 3. ZigZag e Alternância Curta (Foco na soma para ZigZag "real")
    zigzag_count = detectar_zigzag(df_analise_sugestao["Resultado"])
    alternancia_curta_ativa = detectar_alternancia_curta(df_analise_sugestao["Resultado"], n_ultimos=5)
    
    # "Sequência alternando vitória com valores quase iguais -> ZigZag real."
    # Implementação simplificada: se zigzag_count > 0 e a soma média dos zigzags é similar.
    # Para um zigzag "real", precisamos de mais do que apenas a cor.
    is_zigzag_soma_real = False
    if zigzag_count >= 2 and len(df_analise_sugestao) >= 5:
        # Verifica se os zigzags ocorreram com somas "quase iguais" (média próxima)
        # Isso é uma heurística simplificada, o ideal seria analisar cada par de zigzag
        df_pb = df_analise_sugestao[(df_analise_sugestao['Resultado'] == 'P') | (df_analise_sugestao['Resultado'] == 'B')]
        if len(df_pb) >= 4:
            somas_p_zigzag = df_pb[df_pb['Resultado'] == 'P']['Player'].mean()
            somas_b_zigzag = df_pb[df_pb['Resultado'] == 'B']['Banker'].mean()
            if abs(somas_p_zigzag - somas_b_zigzag) <= 1.0: # Somente se as somas médias forem muito próximas
                is_zigzag_soma_real = True

    if is_zigzag_soma_real:
        ultimo_resultado = df_analise_sugestao["Resultado"].iloc[-1]
        sugestoes_geradas.append(f"🔁 **{('BANKER' if ultimo_resultado == 'P' else 'PLAYER')} (ZigZag Real por Soma)**: Padrão ZigZag ativo com somas próximas. Sugere alternância baseada em ritmo dos dados.")
        logicas_ativas['zigzag_soma_real'] = True
    elif alternancia_curta_ativa:
        sugestoes_geradas.append("🔄 **Alternância Curta Ativa (Sem Padrão Forte)**: O jogo está alternando P/B frequentemente, mas sem um padrão de soma ou ritmo claro.")
        logicas_ativas['alternancia_curta_ativa'] = True
    else:
        # "Zig-zag fraco — nada confiável, evite apostar apenas por cor."
        sugestoes_geradas.append("⚠️ **ZigZag Fraco / Sem Padrão de Alternância Clara**: Não há ZigZag real ou alternância consistente. Não se baseie apenas na cor.")
        logicas_ativas['zigzag_fraco_apenas_cor'] = True

    # 4. Streaks (Foco em "Streak Verdadeiro" com somas altas)
    streaks = detectar_streaks(df_analise_sugestao)
    if streaks:
        ultimo_streak = streaks[-1]
        lado_nome = ultimo_streak['lado']
        somas_altas_no_streak = [s for s in ultimo_streak['somas'] if s >= 8 and s <= 12] # "somas altas (8 a 12)"
        
        # "Sequências onde o mesmo lado tira somas altas seguidas -> Streak verdadeiro"
        if ultimo_streak['contagem'] >= 3:
            if len(somas_altas_no_streak) >= (ultimo_streak['contagem'] * 0.75): # Pelo menos 75% das somas foram altas
                sugestoes_geradas.append(f"🔥 **{lado_nome} (Streak VERDADEIRO c/ Somas Altas)**: {ultimo_streak['contagem']} consecutivos com somas consistentemente altas. Forte tendência de seguir o lado.")
                if lado_nome == 'P': logicas_ativas['streak_player_verdadeiro'] = True
                elif lado_nome == 'B': logicas_ativas['streak_banker_verdadeiro'] = True
            else:
                # "Player levemente superior em soma, mas sem streak claro."
                sugestoes_geradas.append(f"🔥 **{lado_nome} (Streak de {ultimo_streak['contagem']} )**: Tendência de seguir, mas as somas não foram predominantemente altas (não é um 'streak verdadeiro' pela soma).")
                if lado_nome == 'P': logicas_ativas['streak_player_normal'] = True
                elif lado_nome == 'B': logicas_ativas['streak_banker_normal'] = True
    
    # 5. Repetição de Somas Próximas
    somas_prox = analisar_somas_proximas(df_analise_sugestao, n_ultimos=7)
    if somas_prox:
        for sp in somas_prox:
            msg = f"✨ **Padrão de Somas Próximas em {sp['lado']}**: Duas vitórias consecutivas de {sp['lado']} com somas {sp['soma_1']} e {sp['soma_2']}. Sugere repetição do comportamento de somas."
            if msg not in sugestoes_geradas:
                sugestoes_geradas.append(msg)
                if sp['lado'] == 'P': logicas_ativas['somas_proximas_player'] = True
                elif sp['lado'] == 'B': logicas_ativas['somas_proximas_banker'] = True

    # 6. Soma Vencedora Recorrente
    soma_comum, pct_comum = analisar_soma_vencedora_recorrente(df_analise_sugestao, n_ultimos=15)
    if soma_comum is not None and pct_comum >= 40:
        player_vitorias_com_soma = df_analise_sugestao[(df_analise_sugestao['Resultado'] == 'P') & (df_analise_sugestao['Player'] == soma_comum)].shape[0]
        banker_vitorias_com_soma = df_analise_sugestao[(df_analise_sugestao['Resultado'] == 'B') & (df_analise_sugestao['Banker'] == soma_comum)].shape[0]

        if player_vitorias_com_soma > banker_vitorias_com_soma:
            sugestoes_geradas.append(f"📊 **PLAYER (Soma Recorrente)**: Soma {soma_comum} aparece frequentemente em vitórias de Player ({pct_comum:.1f}% das vitórias).")
            logicas_ativas['soma_vencedora_player_recorrente'] = True
        elif banker_vitorias_com_soma > player_vitorias_com_soma:
            sugestoes_geradas.append(f"📊 **BANKER (Soma Recorrente)**: Soma {soma_comum} aparece frequentemente em vitórias de Banker ({pct_comum:.1f}% das vitórias).")
            logicas_ativas['soma_vencedora_banker_recorrente'] = True

    # 7. Distribuição de Somas (Altas)
    dist_somas = analisar_distribuicao_somas(df_analise_sugestao, n_ultimos=20)
    # "Está surfando uma sequência de somas altas (8 a 12)."
    if dist_somas['P_Altas_Pct'] >= 60:
        sugestoes_geradas.append(f"📈 **PLAYER (Somas Altas)**: Player vencendo com somas altas em {dist_somas['P_Altas_Pct']:.1f}% das vezes (8 a 12).")
        logicas_ativas['distribuicao_somas_player_alta'] = True
    if dist_somas['B_Altas_Pct'] >= 60:
        sugestoes_geradas.append(f"📈 **BANKER (Somas Altas)**: Banker vencendo com somas altas em {dist_somas['B_Altas_Pct']:.1f}% das vezes (8 a 12).")
        logicas_ativas['distribuicao_somas_banker_alta'] = True
    
    # Removendo 'distribuicao_somas_player_baixa' e 'distribuicao_somas_banker_baixa'
    # pois o foco da estratégia é em somas altas.

    return sugestoes_geradas, logicas_ativas


def determinar_acao_recomendada_inteligente(logicas_ativas, sugestoes_detalhadas):
    # --- Pesos das Lógicas (Refinados e Alinhados com a Estratégia do Usuário) ---
    pesos = {
        'tie_ciclo_forte': 4.0, # Muito forte
        'tie_ciclo_medio': 2.0,
        'near_misses_tie_ativos': 1.5, # Reforça o TIE

        'streak_verdadeiro': 5.0, # O mais forte para P/B
        'streak_normal': 1.0,     # Pouco peso, sem somas altas claras

        'vantagem_soma': 2.5,     # Consistente
        'somas_proximas': 2.0,    # Repetição de comportamento físico
        'soma_vencedora_recorrente': 1.8,
        'distribuicao_somas_alta': 1.2, # Complementa a vantagem de soma
        
        'zigzag_soma_real': 1.5, # ZigZag baseado em soma
        'alternancia_curta_ativa': 0.5, # Indicador de volatilidade, não de aposta
    }

    # --- Pontuação por lado ---
    score = {'P': 0.0, 'B': 0.0, 'T': 0.0}
    justificativas_finais = []
    
    # Flag para indicar se há um padrão forte o suficiente para APOSTAR
    ha_padrao_aposta_direta = False

    # Avaliação do TIE
    if logicas_ativas['tie_ciclo_forte']:
        score['T'] += pesos['tie_ciclo_forte']
        justificativas_finais.append("Padrão de Empate (TIE) FORTEMENTE maduro/atrasado.")
        ha_padrao_aposta_direta = True
    elif logicas_ativas['tie_ciclo_medio']:
        score['T'] += pesos['tie_ciclo_medio']
        justificativas_finais.append("Padrão de Empate (TIE) em ciclo médio.")
    if logicas_ativas['near_misses_tie_ativos']:
        score['T'] += pesos['near_misses_tie_ativos']
        justificativas_finais.append("Vários 'quase empates' (Near Misses) recentes.")
        
    # Avaliação de Player
    if logicas_ativas['streak_player_verdadeiro']:
        score['P'] += pesos['streak_verdadeiro']
        justificativas_finais.append("Streak VERDADEIRO de PLAYER com somas altas.")
        ha_padrao_aposta_direta = True
    elif logicas_ativas['streak_player_normal']:
        score['P'] += pesos['streak_normal']
        justificativas_finais.append("Streak normal de PLAYER (somas não predominantemente altas).")

    if logicas_ativas['player_vantagem_soma']:
        score['P'] += pesos['vantagem_soma']
        justificativas_finais.append("PLAYER com vantagem consistente de soma.")
    if logicas_ativas['somas_proximas_player']:
        score['P'] += pesos['somas_proximas']
        justificativas_finais.append("Padrão de somas próximas em PLAYER.")
    if logicas_ativas['soma_vencedora_player_recorrente']:
        score['P'] += pesos['soma_vencedora_recorrente']
        justificativas_finais.append("Soma vencedora recorrente para PLAYER.")
    if logicas_ativas['distribuicao_somas_player_alta']:
        score['P'] += pesos['distribuicao_somas_alta']
        justificativas_finais.append("PLAYER vencendo com somas predominantemente altas (8 a 12).")
    
    # Avaliação de Banker
    if logicas_ativas['streak_banker_verdadeiro']:
        score['B'] += pesos['streak_verdadeiro']
        justificativas_finais.append("Streak VERDADEIRO de BANKER com somas altas.")
        ha_padrao_aposta_direta = True
    elif logicas_ativas['streak_banker_normal']:
        score['B'] += pesos['streak_normal']
        justificativas_finais.append("Streak normal de BANKER (somas não predominantemente altas).")

    if logicas_ativas['banker_vantagem_soma']:
        score['B'] += pesos['vantagem_soma']
        justificativas_finais.append("BANKER com vantagem consistente de soma.")
    if logicas_ativas['somas_proximas_banker']:
        score['B'] += pesos['somas_proximas']
        justificativas_finais.append("Padrão de somas próximas em BANKER.")
    if logicas_ativas['soma_vencedora_banker_recorrente']:
        score['B'] += pesos['soma_vencedora_recorrente']
        justificativas_finais.append("Soma vencedora recorrente para BANKER.")
    if logicas_ativas['distribuicao_somas_banker_alta']:
        score['B'] += pesos['distribuicao_somas_alta']
        justificativas_finais.append("BANKER vencendo com somas predominantemente altas (8 a 12).")

    # ZigZag Real por Soma (adiciona ao lado oposto do último resultado)
    if logicas_ativas['zigzag_soma_real']:
        ultimo_resultado = df.tail(1)["Resultado"].iloc[0]
        if ultimo_resultado == 'P':
            score['B'] += pesos['zigzag_soma_real']
            justificativas_finais.append("Padrão ZigZag REAL por soma ativo (sugere BANKER).")
        elif ultimo_resultado == 'B':
            score['P'] += pesos['zigzag_soma_real']
            justificativas_finais.append("Padrão ZigZag REAL por soma ativo (sugere PLAYER).")
    
    # Alternância Curta Ativa (indica volatilidade, não aposta direta)
    if logicas_ativas['alternancia_curta_ativa']:
        justificativas_finais.append("Jogo em fase de alternância rápida (sem streaks longos ou padrões definidos).")


    # --- REGRAS DE DECISÃO FINAL (PRIORIDADE CRÍTICA) ---
    
    # 1. Prioridade MÁXIMA para AGUARDAR se houver fraqueza no padrão ou conflito de soma
    # "Zig-zag fraco — nada confiável, evite apostar apenas por cor."
    # "Player levemente superior em soma, mas sem streak claro."
    # Se o zigzag é fraco E não tem nenhum streak verdadeiro, é aguardar.
    if logicas_ativas['zigzag_fraco_apenas_cor'] and \
       not (logicas_ativas['streak_player_verdadeiro'] or logicas_ativas['streak_banker_verdadeiro']):
        return "AGUARDAR", 20, "Cenário **instável/fraco**: ZigZag fraco detectado e sem Streaks Verdadeiros. Não se baseie apenas na cor. " + ", ".join(justificativas_finais), "warning"

    # Se há alguma vantagem de soma, mas o streak é normal (não "claro") ou não há streak
    if ((logicas_ativas['player_vantagem_soma'] and not logicas_ativas['streak_player_verdadeiro']) or
        (logicas_ativas['banker_vantagem_soma'] and not logicas_ativas['streak_banker_verdadeiro'])):
        # E se não há Tie forte
        if score['T'] < pesos['tie_ciclo_forte']:
             return "AGUARDAR", 40, "Cenário **incerto**: Vantagem de soma existe, mas sem um 'streak claro' ou padrão forte para aposta direta. " + ", ".join(justificativas_finais), "warning"

    # Conflito de Lógicas Fortes (P vs B)
    # Se ambos os lados têm pontuação alta, mas nenhum é claramente dominante (ex: ambos > 3.0)
    if score['P'] >= 2.5 and score['B'] >= 2.5: # Limiar ajustado para conflito
        # Se a diferença entre os scores P e B não é significativa
        if abs(score['P'] - score['B']) < 2.0: # Ex: Player 3.0, Banker 2.8 - muito próximos
            return "AGUARDAR", 50, "Cenário de **conflito**: Lógicas fortes apontam para Player E Banker. Aguarde clareza. " + ", ".join(justificativas_finais), "warning"

    # 2. Prioridade para APOSTAR NO TIE (Se forte o suficiente E sem conflito P/B significativo)
    if score['T'] >= pesos['tie_ciclo_forte'] * 1.0: # Requer pelo menos a força de um ciclo forte
        # E se P e B não estão com pontuação muito alta OU estão equilibrados
        if (score['P'] < 2.0 and score['B'] < 2.0) or (abs(score['P'] - score['B']) < 1.0):
            confianca = min(100, int(score['T'] * 18)) # Escala de confiança para TIE
            return "APOSTAR NO TIE", confianca, f"**ALTA CHANCE DE TIE** devido a forte convergência de padrões de empate ({score['T']:.1f} pontos). " + ", ".join(justificativas_finais), "success"
        else: # Tie forte, mas P ou B também estão fortes, pode ser conflito
            return "AGUARDAR", 60, "Cenário misto: TIE está forte, mas Player/Banker também apresentam força. Aguarde a confirmação de um padrão dominante. " + ", ".join(justificativas_finais), "warning"
    
    # 3. Prioridade para APOSTAR PLAYER/BANKER com Confirmação Forte
    # Requer um "Streak Verdadeiro" ou a combinação de "Vantagem de Soma" e "Somas Próximas"
    
    limiar_aposta_direta_P_B = 4.0 # Limiar alto para aposta direta

    if score['P'] >= limiar_aposta_direta_P_B and score['P'] > score['B'] * 1.8 and score['T'] < 1.5: # Player MUITO mais forte
        confianca = min(100, int(score['P'] * 15))
        return "APOSTAR NO PLAYER", confianca, f"**FORTE CONSENSO para PLAYER** ({score['P']:.1f} pontos): " + ", ".join(justificativas_finais), "success"
    
    elif score['B'] >= limiar_aposta_direta_P_B and score['B'] > score['P'] * 1.8 and score['T'] < 1.5: # Banker MUITO mais forte
        confianca = min(100, int(score['B'] * 15))
        return "APOSTAR NO BANKER", confianca, f"**FORTE CONSENSO para BANKER** ({score['B']:.1f} pontos): " + ", ".join(justificativas_finais), "success"
    
    # 4. Nenhum padrão forte o suficiente para aposta direta, então AGUARDAR
    # Se chegou aqui, não houve um sinal forte o suficiente para P, B ou T.
    if ha_padrao_aposta_direta: # Se alguma lógica de "aposta direta" foi ativada, mas não atingiu os limiares.
        confianca_aguardar = min(100, int(max(score.values()) * 10))
        return "AGUARDAR", confianca_aguardar, "Padrões identificados, mas sem força ou clareza suficiente para uma entrada segura imediata. Aguarde mais confirmações. " + ", ".join(justificativas_finais), "warning"
    
    # Caso padrão: não há padrões fortes
    return "AGUARDAR", 10, "Aguardando mais dados ou padrões claros para análise. Cenário muito neutro. " + ", ".join(justificativas_finais), "warning"


# --- Mostrar Análises e Sugestões ---
st.markdown("---")
st.header("📊 Análise Detalhada e Sugestões Inteligentes")

# Gera sugestões e o mapeamento das lógicas ativas
sugestoes_detalhadas_texto, logicas_ativas_map = gerar_relatorio_sugestoes(df)
acao, confianca, justificativa_acao, acao_tipo = determinar_acao_recomendada_inteligente(logicas_ativas_map, sugestoes_detalhadas_texto)

# Exibe a Ação Recomendada (com CSS personalizado)
st.markdown(f"""
<div class="stAlert alert-{acao_tipo}">
    Ação Recomendada: {acao}
    <br>
    Confiança: {confianca}%
    <br>
    <span style="font-size: 0.8em; font-weight: normal;">{justificativa_acao}</span>
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
    freq_df = pd.DataFrame(list(freq_resultados(df).items()), columns=['Resultado', 'Porcentagem'])
    fig_freq = px.bar(freq_df, x='Resultado', y='Porcentagem', 
                      title='Frequência de Resultados (Geral)',
                      color='Resultado',
                      color_discrete_map={'P': 'blue', 'B': 'red', 'T': 'green'},
                      template="plotly_dark")
    st.plotly_chart(fig_freq, use_container_width=True)

    n_ultimos_para_grafico = min(50, len(df))
    df_ultimos = df.tail(n_ultimos_para_grafico).reset_index(drop=True)
    df_ultimos['Indice'] = df_ultimos.index + 1

    fig_seq = px.line(df_ultimos, x='Indice', y='Resultado', 
                      title=f'Sequência dos Últimos {n_ultimos_para_grafico} Resultados',
                      color='Resultado',
                      color_discrete_map={'P': 'blue', 'B': 'red', 'T': 'green'},
                      line_shape='hv',
                      markers=True,
                      template="plotly_dark")
    fig_seq.update_layout(yaxis_title="Resultado (P/B/T)", showlegend=False)
    st.plotly_chart(fig_seq, use_container_width=True)

# Sugestões Detalhadas
st.subheader("✨ Detalhes das Lógicas Ativas")
if sugestoes_detalhadas_texto:
    for s in sugestoes_detalhadas_texto:
        if "ZigZag Fraco" in s or "Alternância Curta Ativa" in s or "sem um padrão de soma ou ritmo claro" in s:
            st.info(s)
        else:
            st.success(s)
else:
    st.warning("Nenhum padrão detectado no momento para detalhes.")

st.markdown("---")
st.info("Lembre-se: Este analisador é uma ferramenta de apoio. Jogos de azar envolvem risco e dependem da sorte.")
