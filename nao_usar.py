# app.py
import streamlit as st
import random
from collections import Counter

# --- Funções Auxiliares para Análise de Padrões ---

def analyze_patterns_python(results):
    if len(results) < 3:
        return None

    # Fatias do histórico para análise
    recent = results[-15:]
    last3 = results[-3:]
    last4 = results[-4:]
    last5 = results[-5:]
    last6 = results[-6:]
    last7 = results[-7:]
    last10 = results[-10:]
    last_result = results[-1] if results else None

    # --- Padrões Existentes ---

    # Detectar Surf de Cor (3+ vezes a mesma cor seguida)
    surf_detected = False
    current_surf_streak = 0
    if recent and last_result != 'Empate':
        current_surf_streak = 1
        for i in range(len(recent) - 2, -1, -1):
            if recent[i] == last_result:
                current_surf_streak += 1
            else:
                break
        if current_surf_streak >= 3:
            surf_detected = True

    # Detectar Zig-Zag (alternância Casa/Visitante)
    zigzag_count = 0
    if len(last5) >= 2:
        for i in range(1, len(last5)):
            if last5[i] != last5[i-1] and last5[i] != 'Empate' and last5[i-1] != 'Empate':
                zigzag_count += 1
    zigzag_detected = zigzag_count >= 3

    # Detectar Empate Recorrente (intervalo de 15-35 rodadas)
    empate_positions = [i for i, r in enumerate(results) if r == 'Empate']
    empate_recorrente = False
    if len(empate_positions) >= 2:
        last_empate_gap = len(results) - 1 - empate_positions[-1]
        if 15 <= last_empate_gap <= 35:
            empate_recorrente = True

    # Dominância de um Lado no Curto Prazo (últimos 7 jogos)
    dominancia_curto_prazo = None
    casa_count_7 = last7.count('Casa')
    visitante_count_7 = last7.count('Visitante')
    if casa_count_7 >= 5 and casa_count_7 > visitante_count_7 + 2:
        dominancia_curto_prazo = 'Casa'
    elif visitante_count_7 >= 5 and visitante_count_7 > casa_count_7 + 2:
        dominancia_curto_prazo = 'Visitante'

    # Padrão de Reversão (Após Duas do Mesmo Lado)
    reversao_duas = None
    if len(results) >= 2 and last_result != 'Empate':
        penultimo = results[-2]
        if penultimo == last_result:
            reversao_duas = 'Visitante' if last_result == 'Casa' else 'Casa'

    # Sequência 2-1-2 (Ex: C-C-V-C-C ou V-V-C-V-V)
    padrao_212 = None
    if len(last5) == 5 and \
       last5[0] == last5[1] and \
       last5[3] == last5[4] and \
       last5[0] == last5[3] and \
       last5[2] != last5[0] and last5[2] != 'Empate':
        padrao_212 = last5[0]

    # Sequência 2-2-1 (Ex: C-C-V-V-C ou V-V-C-C-V)
    padrao_221 = None
    if len(last5) == 5 and \
       last5[0] == last5[1] and \
       last5[2] == last5[3] and \
       last5[4] != last5[0] and last5[4] != last5[2] and last5[0] != last5[2] and last5[4] != 'Empate':
        padrao_221 = last5[4]

    # Alternância de Empates (Ex: ...C-E-V-E-C-E...)
    alternancia_empate = False
    if len(last6) == 6:
        count_alternating_empate = 0
        for i in range(3):
            if last6[i * 2] != 'Empate' and last6[i * 2 + 1] == 'Empate':
                count_alternating_empate += 1
        if count_alternating_empate >= 2:
            alternancia_empate = True

    # --- Novos Padrões Solicitados ---

    # 1. Padrão 3x3 (ex: C-C-C-V-V-V)
    padrao_3x3 = None
    if len(last6) == 6 and \
       last6[0] == last6[1] and last6[1] == last6[2] and \
       last6[3] == last6[4] and last6[4] == last6[5] and \
       last6[0] != last6[3] and \
       last6[0] != 'Empate' and last6[3] != 'Empate':
        padrao_3x3 = last6[0]

    # 2. Padrão 3x1x1x2x3 (ex: C-C-C-V-C-V-V-C-C-C)
    padrao_31123 = None
    if len(last10) == 10:
        p = last10
        if p[0] == p[1] == p[2] and \
           p[3] != p[2] and p[3] != 'Empate' and \
           p[4] == p[2] and p[4] != 'Empate' and \
           p[5] != p[4] and p[5] == p[6] and p[5] != 'Empate' and \
           p[7] == p[8] == p[9] and p[7] == p[4] and p[7] != 'Empate':
            padrao_31123 = p[0]

    # 3. 4x4 Surf (Variação mais forte do surf)
    surf_4x4 = surf_detected and current_surf_streak >= 4 and last_result != 'Empate'


    # Quebra de Padrão (Baseado nos originais)
    quebrar_surf = surf_detected and current_surf_streak >= 4
    quebrar_zigzag = zigzag_detected and zigzag_count >= 4

    # --- Geração da Sugestão com Prioridade ---
    suggested_entry = None
    conf = 0

    # Ordem de prioridade (do mais forte/confiável para o menos):
    if padrao_31123: # Padrão 3x1x1x2x3 - altíssima prioridade
        suggested_entry = padrao_31123
        conf = 97
    elif surf_4x4: # 4x4 Surf - muito forte
        suggested_entry = 'Visitante' if last_result == 'Casa' else 'Casa' # Sugere a quebra
        conf = 95
    elif quebrar_surf: # Quebra de Surf (genérica, mais de 4x)
        suggested_entry = 'Visitante' if last_result == 'Casa' else 'Casa'
        conf = 90 + min(current_surf_streak * 2, 8)
    elif zigzag_detected and quebrar_zigzag and last_result != 'Empate':
        suggested_entry = 'Visitante' if last_result == 'Casa' else 'Casa'
        conf = 88
    elif padrao_3x3: # Padrão 3x3
        suggested_entry = 'Visitante' if padrao_3x3 == 'Casa' else 'Casa' # Sugere o oposto
        conf = 87
    elif reversao_duas: # Padrão de Reversão
        suggested_entry = reversao_duas
        conf = 85
    elif empate_recorrente:
        suggested_entry = 'Empate'
        conf = 80
    elif padrao_212: # Sequência 2-1-2
        suggested_entry = padrao_212
        conf = 78
    elif padrao_221: # Sequência 2-2-1
        suggested_entry = padrao_221
        conf = 76
    elif dominancia_curto_prazo: # Dominância de Curto Prazo
        suggested_entry = 'Visitante' if dominancia_curto_prazo == 'Casa' else 'Casa'
        conf = 72
    elif alternancia_empate and last_result != 'Empate': # Alternância de Empates
        suggested_entry = 'Empate'
        conf = 70
    elif surf_detected: # Continuar o surf (3x)
        suggested_entry = last_result
        conf = 68 + current_surf_streak * 2
    elif zigzag_detected and last_result != 'Empate': # Continuar o zig-zag
        suggested_entry = 'Visitante' if last_result == 'Casa' else 'Casa'
        conf = 65
    else:
        # Análise baseada nos últimos 10 jogos como fallback
        casa_count_10 = last10.count('Casa')
        visitante_count_10 = last10.count('Visitante')

        if casa_count_10 > visitante_count_10 + 2:
            suggested_entry = 'Visitante'
            conf = 55
        elif visitante_count_10 > casa_count_10 + 2:
            suggested_entry = 'Casa'
            conf = 55
        else:
            suggested_entry = random.choice(['Casa', 'Visitante'])
            conf = 50

    return {
        "entry": suggested_entry,
        "confidence": min(conf, 99),
        "patterns": {
            "surf": surf_detected,
            "surf_streak": current_surf_streak,
            "zigzag": zigzag_detected,
            "empate_recorrente": empate_recorrente,
            "quebrar_surf": quebrar_surf,
            "quebrar_zigzag": quebrar_zigzag,
            "dominancia_curto_prazo": dominancia_curto_prazo,
            "reversao_duas": reversao_duas,
            "padrao_212": padrao_212,
            "padrao_221": padrao_221,
            "alternancia_empate": alternancia_empate,
            "padrao_3x3": padrao_3x3,
            "padrao_31123": padrao_31123,
            "surf_4x4": surf_4x4,
        }
    }

# --- Funções de Ajuda para o Streamlit ---

def get_confidence_color(conf):
    if conf >= 85:
        return "green"
    if conf >= 70:
        return "orange"
    return "red"

def get_confidence_text(conf):
    if conf >= 90: return 'ALTÍSSIMA GARANTIA'
    if conf >= 80: return 'ALTA GARANTIA'
    if conf >= 70: return 'BOA GARANTIA'
    if conf >= 60: return 'GARANTIA MODERADA'
    return 'BAIXA GARANTIA'

# --- Inicialização do Estado da Sessão Streamlit ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'suggestion' not in st.session_state:
    st.session_state.suggestion = None
if 'confidence' not in st.session_state:
    st.session_state.confidence = 0
if 'streak' not in st.session_state:
    st.session_state.streak = {'type': None, 'count': 0}
if 'hits' not in st.session_state: # Novo: Contagem de acertos
    st.session_state.hits = 0
if 'misses' not in st.session_state: # Novo: Contagem de erros
    st.session_state.misses = 0
if 'last_suggestion' not in st.session_state: # Novo: Salva a última sugestão para comparação
    st.session_state.last_suggestion = None
if 'awaiting_feedback' not in st.session_state: # Novo: Flag para saber se espera feedback
    st.session_state.awaiting_feedback = False


# --- Funções de Ação ---

def add_result_to_history(result):
    # Antes de adicionar o novo resultado, se havia uma sugestão pendente,
    # significa que o usuário não deu feedback, então consideramos um erro/acerto automático.
    if st.session_state.awaiting_feedback and st.session_state.last_suggestion:
        if st.session_state.last_suggestion['entry'] == result:
            st.session_state.hits += 1
            st.toast("Acerto automático! (Sugestão anterior correspondia)", icon="✅")
        else:
            st.session_state.misses += 1
            st.toast("Erro automático! (Sugestão anterior não correspondia)", icon="❌")

    st.session_state.history.append(result)
    analysis = analyze_patterns_python(st.session_state.history)
    
    if analysis:
        st.session_state.suggestion = analysis
        st.session_state.confidence = analysis['confidence']
        st.session_state.last_suggestion = analysis # Guarda a sugestão atual para feedback futuro
        st.session_state.awaiting_feedback = True # Indica que estamos esperando feedback
    else:
        st.session_state.suggestion = None
        st.session_state.confidence = 0
        st.session_state.last_suggestion = None
        st.session_state.awaiting_feedback = False

    # Atualizar streak atual
    if st.session_state.history:
        last_result = st.session_state.history[-1]
        if st.session_state.streak['type'] == last_result:
            st.session_state.streak['count'] += 1
        else:
            st.session_state.streak = {'type': last_result, 'count': 1}

def register_feedback(feedback_type):
    # Esta função será chamada pelos botões de feedback "Acerto" ou "Erro"
    if st.session_state.awaiting_feedback and st.session_state.last_suggestion:
        if feedback_type == 'hit':
            st.session_state.hits += 1
            st.toast("ACERTO registrado!", icon="🎯")
        else: # feedback_type == 'miss'
            st.session_state.misses += 1
            st.toast("ERRO registrado!", icon="❌")
        st.session_state.awaiting_feedback = False # Já recebeu o feedback
    # Não limpamos st.session_state.last_suggestion aqui, ela é sobrescrita
    # na próxima chamada de add_result_to_history.

def clear_history_and_stats():
    st.session_state.history = []
    st.session_state.suggestion = None
    st.session_state.confidence = 0
    st.session_state.streak = {'type': None, 'count': 0}
    st.session_state.hits = 0
    st.session_state.misses = 0
    st.session_state.last_suggestion = None
    st.session_state.awaiting_feedback = False
    # Streamlit redesenha automaticamente quando o st.session_state é alterado.


# --- Layout da Aplicação Streamlit ---

# Estilos CSS Injetados
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom right, #1a202c, #4a0e4e, #1a202c);
    color: white;
}
.header-title {
    font-size: 3em;
    font-weight: bold;
    text-align: center;
    background: -webkit-linear-gradient(left, #facc15, #f97316);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5em;
}
.header-subtitle {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 2em;
}
/* Estilo para os botões de entrada específicos */
button[data-testid*="btn_casa"] {
    background-image: linear-gradient(to right, #dc2626, #b91c1c); /* Vermelho para Casa */
    color: white;
    width: 100%;
    padding: 1.5em;
    font-size: 1.25em;
    font-weight: bold;
    border-radius: 0.75em;
    transition: all 0.2s ease-in-out;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
button[data-testid*="btn_empate"] {
    background-image: linear-gradient(to right, #d97706, #b45309); /* Amarelo para Empate */
    color: white;
    width: 100%;
    padding: 1.5em;
    font-size: 1.25em;
    font-weight: bold;
    border-radius: 0.75em;
    transition: all 0.2s ease-in-out;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
button[data-testid*="btn_visitante"] {
    background-image: linear-gradient(to right, #2563eb, #1d4ed8); /* Azul para Visitante */
    color: white;
    width: 100%;
    padding: 1.5em;
    font-size: 1.25em;
    font-weight: bold;
    border-radius: 0.75em;
    transition: all 0.2s ease-in-out;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Estilo para o hover, aplicado a todos os botões que queremos interativo */
.stButton>button:hover {
    transform: scale(1.05);
    filter: brightness(1.1);
}

.suggestion-box {
    background: linear-gradient(to right, #6b21a8, #4f46e5);
    border-radius: 0.75em;
    padding: 1.5em;
    margin-bottom: 1.5em;
    border: 1px solid #a78bfa;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}
.pattern-detection-box {
    background-color: rgba(0, 0, 0, 0.3);
    border-radius: 0.5em;
    padding: 1em;
    margin-top: 1em;
}
.history-line-container {
    display: flex;
    flex-wrap: wrap; /* Permite que os itens quebrem para a próxima linha */
    gap: 0.2em; /* Espaço entre as bolhas */
    margin-bottom: 0.5em; /* Espaço entre as linhas de bolhas */
    justify-content: flex-start; /* Alinhar à esquerda */
    width: 100%; /* Ocupa a largura total para quebrar corretamente */
}
.history-item {
    width: 1.5em; /* Bolhas menores */
    height: 1.5em; /* Bolhas menores */
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 0.7em; /* Texto menor para bolhas menores */
    flex-shrink: 0; /* Não permite que as bolhas encolham */
}
/* Cores das Bolhas */
.red-bg-bubble { background-color: #dc2626; } /* Vermelho para Casa */
.blue-bg-bubble { background-color: #2563eb; } /* Azul para Visitante */
.yellow-bg-bubble { background-color: #d97706; } /* Amarelo para Empate */
.stat-box {
    background-color: rgba(75, 85, 99, 0.3);
    padding: 0.75em;
    border-radius: 0.5em;
    text-align: center;
}
.disclaimer-box {
    background-color: rgba(75, 85, 99, 0.5);
    padding: 1em;
    border-radius: 0.5em;
    text-align: center;
    color: #9ca3af;
    font-size: 0.875em;
    margin-top: 2em;
}
.performance-box {
    background-color: #1f2937;
    border-radius: 0.75em;
    padding: 1em;
    margin-top: 1.5em;
    text-align: center;
    border: 1px solid #a78bfa;
}
/* Estilo para os botões de feedback (Acerto/Erro) */
button[data-testid*="btn_acerto"] {
    background-image: linear-gradient(to right, #4CAF50, #2E8B57); /* Verde para Acerto */
    border: none;
    color: white;
    padding: 0.75em 1em;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 1em;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 8px;
    width: auto;
    min-width: 100px;
}
button[data-testid*="btn_erro"] {
    background-image: linear-gradient(to right, #f44336, #b71c1c); /* Vermelho para Erro */
    border: none;
    color: white;
    padding: 0.75em 1em;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 1em;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 8px;
    width: auto;
    min-width: 100px;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="header-title">⚽ Football Studio Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="header-subtitle">Análise Inteligente de Padrões - Evolution Gaming</p>', unsafe_allow_html=True)

# Botões de Entrada
col1, col2, col3 = st.columns(3)
with col1:
    st.button("🏠 CASA", on_click=add_result_to_history, args=('Casa',), key="btn_casa", help="Adicionar resultado Casa")
with col2:
    st.button("🤝 EMPATE", on_click=add_result_to_history, args=('Empate',), key="btn_empate", help="Adicionar resultado Empate")
with col3:
    st.button("✈️ VISITANTE", on_click=add_result_to_history, args=('Visitante',), key="btn_visitante", help="Adicionar resultado Visitante")

# Sugestão Principal
if st.session_state.suggestion:
    st.markdown('<div class="suggestion-box">', unsafe_allow_html=True)
    
    suggestion_col1, suggestion_col2 = st.columns([2, 1])
    with suggestion_col1:
        st.markdown(f'<h2 style="font-size: 1.5em; font-weight: bold; color: #fcd34d;">PRÓXIMA ENTRADA</h2>', unsafe_allow_html=True)
    with suggestion_col2:
        st.markdown(f'<div style="text-align: right; font-size: 1.5em; font-weight: bold; color: {get_confidence_color(st.session_state.confidence)};">{st.session_state.confidence}%</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align: right; font-size: 0.875em; color: #cbd5e1;">{get_confidence_text(st.session_state.confidence)}</div>', unsafe_allow_html=True)
    
    entry_color_class = ""
    entry_text = ""
    if st.session_state.suggestion['entry'] == 'Casa':
        entry_color_class = "red-600"
        entry_text = "🏠 APOSTAR NA CASA"
    elif st.session_state.suggestion['entry'] == 'Visitante':
        entry_color_class = "blue-600"
        entry_text = "✈️ APOSTAR NO VISITANTE"
    else:
        entry_color_class = "gray-600" # Mantenha o botão cinza, mas a bolha será amarela
        entry_text = "🤝 APOSTAR NO EMPATE"
        
    st.markdown(f'''
        <div style="text-align: center; padding: 1em; border-radius: 0.5em; background-color: var(--{entry_color_class}); font-size: 2.25em; font-weight: bold; color: white;">
            {entry_text}
        </div>
    ''', unsafe_allow_html=True)

    # Padrões Detectados
    st.markdown('<div class="pattern-detection-box">', unsafe_allow_html=True)
    st.markdown(f'<h3 style="font-weight: bold; margin-bottom: 0.5em; display: flex; align-items: center;"><span style="margin-right: 0.5em;">📊</span>Padrões Detectados:</h3>', unsafe_allow_html=True)
    
    patterns = st.session_state.suggestion['patterns']
    
    # Usar colunas para exibir os padrões em 2 colunas
    pattern_cols = st.columns(2)
    col_idx = 0

    def add_pattern_line(col_obj, icon_char, text, color):
        col_obj.markdown(f'<div style="display: flex; align-items: center; color: {color}; margin-bottom: 0.25em;"><span style="margin-right: 0.25em;">{icon_char}</span>{text}</div>', unsafe_allow_html=True)

    if patterns['surf']:
        add_pattern_line(pattern_cols[col_idx % 2], '⚡', f'Surf de Cor ({patterns["surf_streak"]}x)', '#fcd34d')
        col_idx += 1
    if patterns['zigzag']:
        add_pattern_line(pattern_cols[col_idx % 2], '📈', 'Zig-Zag Detectado', '#86efad')
        col_idx += 1
    if patterns['quebrar_surf']:
        add_pattern_line(pattern_cols[col_idx % 2], '⚠️', 'Quebra de Surf (Forte!)', '#f87171')
        col_idx += 1
    if patterns['quebrar_zigzag']:
        add_pattern_line(pattern_cols[col_idx % 2], '⚠️', 'Quebra de Zig-Zag (Forte!)', '#f87171')
        col_idx += 1
    if patterns['empate_recorrente']:
        add_pattern_line(pattern_cols[col_idx % 2], '🎯', 'Empate Recorrente', '#d8b4fe')
        col_idx += 1
    if patterns['dominancia_curto_prazo']:
        add_pattern_line(pattern_cols[col_idx % 2], '📊', f'Dominância de {patterns["dominancia_curto_prazo"]} (Curto Prazo)', '#fdba74')
        col_idx += 1
    if patterns['reversao_duas']:
        add_pattern_line(pattern_cols[col_idx % 2], '🔄', 'Padrão de Reversão (Após 2x Igual)', '#67e8f9')
        col_idx += 1
    if patterns['padrao_212']:
        add_pattern_line(pattern_cols[col_idx % 2], '🔁', f'Padrão 2-1-2 ({patterns["padrao_212"]})', '#bef264')
        col_idx += 1
    if patterns['padrao_221']:
        add_pattern_line(pattern_cols[col_idx % 2], '🔁', f'Padrão 2-2-1 ({patterns["padrao_221"]})', '#5eead4')
        col_idx += 1
    if patterns['alternancia_empate']:
        add_pattern_line(pattern_cols[col_idx % 2], '🎯', 'Alternância de Empates', '#f472b6')
        col_idx += 1
    if patterns['padrao_3x3']:
        add_pattern_line(pattern_cols[col_idx % 2], '⬡', f'Padrão 3x3 Detectado ({patterns["padrao_3x3"]} inicial)', '#a78bfa') # Hexagon character
        col_idx += 1
    if patterns['padrao_31123']:
        add_pattern_line(pattern_cols[col_idx % 2], '🔁', f'Padrão 3x1x1x2x3 Detectado ({patterns["padrao_31123"]} inicial)', '#f0abfc')
        col_idx += 1
    if patterns['surf_4x4']:
        add_pattern_line(pattern_cols[col_idx % 2], '⚡', 'SUPER SURF 4x4! (Quebra Iminente?)', '#ef4444')
        col_idx += 1

    st.markdown('</div>', unsafe_allow_html=True) # Fecha pattern-detection-box
    st.markdown('</div>', unsafe_allow_html=True) # Fecha suggestion-box

# --- Histórico ---
st.markdown('<div style="background-color: #1f2937; border-radius: 0.75em; padding: 1.5em; margin-bottom: 1.5em;">', unsafe_allow_html=True)
history_header_col1, history_header_col2 = st.columns([3, 1])
with history_header_col1:
    st.markdown(f'<h3 style="font-size: 1.25em; font-weight: bold;">Últimos Resultados ({len(st.session_state.history)})</h3>', unsafe_allow_html=True)
with history_header_col2:
    st.button("Limpar Histórico e Estatísticas", on_click=clear_history_and_stats, key="btn_clear_all", help="Limpar todos os resultados e estatísticas de desempenho")

# Exibição do histórico em linha de 9
history_html = []
current_line_items = []
for i, result in enumerate(reversed(st.session_state.history)):
    color_class = ""
    text_char = ""
    if result == 'Casa':
        color_class = "red-bg-bubble"
        text_char = "C"
    elif result == 'Visitante':
        color_class = "blue-bg-bubble"
        text_char = "V"
    else: # Empate
        color_class = "yellow-bg-bubble"
        text_char = "E"
    
    current_line_items.append(f'<div class="history-item {color_class}">{text_char}</div>')
    
    # Se alcançou 9 itens ou é o último item do histórico
    if (i + 1) % 9 == 0 or (i + 1) == len(st.session_state.history):
        history_html.append('<div class="history-line-container">' + "".join(current_line_items) + '</div>')
        current_line_items = [] # Reinicia para a próxima linha

# Exibir as linhas HTML no Streamlit
for line_html in history_html:
    st.markdown(line_html, unsafe_allow_html=True)

# --- Conferidor de Desempenho ---
st.markdown('<div class="performance-box">', unsafe_allow_html=True)
st.markdown(f'<h3 style="font-weight: bold; margin-bottom: 0.5em;">Desempenho Geral</h3>', unsafe_allow_html=True)

perf_col1, perf_col2, perf_col3 = st.columns(3)
total_bets = st.session_state.hits + st.session_state.misses
hit_rate = (st.session_state.hits / total_bets * 100) if total_bets > 0 else 0

with perf_col1:
    st.metric(label="Acertos ✅", value=st.session_state.hits)
with perf_col2:
    st.metric(label="Erros ❌", value=st.session_state.misses)
with perf_col3:
    st.metric(label="Taxa de Acerto", value=f"{hit_rate:.1f}%")

st.markdown('</div>', unsafe_allow_html=True)

# Botões de feedback (Acerto/Erro) - Aparecem somente após uma sugestão
if st.session_state.awaiting_feedback:
    st.markdown('<div style="text-align: center; margin-top: 1.5em;">', unsafe_allow_html=True)
    st.markdown('<h3 style="font-weight: bold; margin-bottom: 1em;">O resultado da última sugestão foi um:</h3>', unsafe_allow_html=True)
    feedback_col1, feedback_col2 = st.columns(2)
    with feedback_col1:
        st.button("✅ ACERTO", on_click=register_feedback, args=('hit',), key="btn_acerto_feedback", help="Clique se a última sugestão foi correta") # Alterei a key
    with feedback_col2:
        st.button("❌ ERRO", on_click=register_feedback, args=('miss',), key="btn_erro_feedback", help="Clique se a última sugestão foi incorreta") # Alterei a key
    st.markdown('</div>', unsafe_allow_html=True)


# Estatísticas de distribuição de resultados (movidas para depois do desempenho, se desejar)
if st.session_state.history:
    st.markdown('<div style="background-color: rgba(75, 85, 99, 0.3); border-radius: 0.75em; padding: 1.5em; margin-top: 1.5em;">', unsafe_allow_html=True)
    st.markdown(f'<h3 style="font-size: 1.25em; font-weight: bold;">Distribuição de Resultados</h3>', unsafe_allow_html=True)
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    total_results = len(st.session_state.history)
    casa_count = st.session_state.history.count('Casa')
    empate_count = st.session_state.history.count('Empate')
    visitante_count = st.session_state.history.count('Visitante')

    with stats_col1:
        st.markdown(f'<div class="stat-box">', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size: 1.5em; font-weight: bold;">{casa_count}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size: 0.875em;">Casa ({((casa_count / total_results) * 100):.1f}%)</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with stats_col2:
        st.markdown(f'<div class="stat-box">', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size: 1.5em; font-weight: bold;">{empate_count}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size: 0.875em;">Empate ({((empate_count / total_results) * 100):.1f}%)</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with stats_col3:
        st.markdown(f'<div class="stat-box">', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size: 1.5em; font-weight: bold;">{visitante_count}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size: 0.875em;">Visitante ({((visitante_count / total_results) * 100):.1f}%)</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Streak Atual (mantido no final para visualização)
if st.session_state.streak['type']:
    streak_message = f"Streak Atual: {st.session_state.streak['count']}x {st.session_state.streak['type']}"
    if st.session_state.streak['count'] >= 3 and st.session_state.streak['type'] != 'Empate':
        streak_message += ' <span style="color: #f87171;">(⚠️ Possível Quebra)</span>'
    st.markdown(f'''
        <div style="background: linear-gradient(to right, #fbbf24, #f97316); border-radius: 0.75em; padding: 1em; text-align: center; font-size: 1.125em; font-weight: bold; margin-top: 1.5em;">
            {streak_message}
        </div>
    ''', unsafe_allow_html=True)

# Disclaimer
st.markdown('''
<div class="disclaimer-box">
  <p style="margin-bottom: 0.5em;">⚠️ Este aplicativo é apenas para fins educacionais e de entretenimento.</p>
  <p>Apostas envolvem riscos. Jogue com responsabilidade.</p>
</div>
''', unsafe_allow_html=True)
