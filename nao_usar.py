import streamlit as st
from collections import Counter

# Inicialização do estado
if 'history' not in st.session_state:
    st.session_state.history = []
if 'suggestion' not in st.session_state:
    st.session_state.suggestion = None
if 'confidence' not in st.session_state:
    st.session_state.confidence = 0
if 'streak' not in st.session_state:
    st.session_state.streak = {'type': None, 'count': 0}

# Função de análise dos padrões
def analyze_patterns(results):
    if len(results) < 3:
        return None

    recent = results[-10:]
    last3 = results[-3:]
    last5 = results[-5:]
    empate_positions = [i for i, r in enumerate(results) if r == 'Empate']

    # Padrão 1: Surf
    surf_detected = False
    current_streak = 1
    for i in range(len(recent) - 2, -1, -1):
        if recent[i] == recent[-1] and recent[i] != 'Empate':
            current_streak += 1
        else:
            break
    if current_streak >= 3:
        surf_detected = True

    # Padrão 2: Zig-Zag
    zigzag_count = sum(1 for i in range(1, len(last5))
                       if last5[i] != last5[i - 1] and last5[i] != 'Empate' and last5[i - 1] != 'Empate')
    zigzag_detected = zigzag_count >= 3

    # Padrão 3: Duplas repetidas
    duplas_repetidas = False
    if len(recent) >= 6:
        dupla_count = sum(1 for i in range(0, len(recent) - 1, 2)
                          if recent[i] == recent[i + 1] and recent[i] != 'Empate')
        duplas_repetidas = dupla_count >= 2

    # Padrão 4: Empate recorrente
    empate_recorrente = False
    if len(empate_positions) >= 2:
        last_gap = len(results) - 1 - empate_positions[-1]
        if 15 <= last_gap <= 35:
            empate_recorrente = True

    # Estatísticas
    casa_count = recent.count('Casa')
    visitante_count = recent.count('Visitante')
    empate_count = recent.count('Empate')

    # Regras de decisão
    suggested_entry = None
    confidence = 0
    main_pattern = 'Análise Básica'

    if surf_detected and current_streak >= 4:
        suggested_entry = 'Visitante' if recent[-1] == 'Casa' else 'Casa'
        confidence = 88 + min(current_streak * 2, 10)
        main_pattern = 'Quebra de Surf'
    elif empate_recorrente:
        suggested_entry = 'Empate'
        confidence = 82
        main_pattern = 'Empate Recorrente'
    elif zigzag_detected:
        suggested_entry = 'Visitante' if recent[-1] == 'Casa' else 'Casa'
        confidence = 75
        main_pattern = 'Zig-Zag'
    elif surf_detected:
        suggested_entry = recent[-1]
        confidence = 65 + current_streak * 3
        main_pattern = 'Surf Continuado'
    elif duplas_repetidas:
        suggested_entry = recent[-1]
        confidence = 68
        main_pattern = 'Duplas Repetidas'
    elif casa_count > visitante_count + 2:
        suggested_entry = 'Visitante'
        confidence = 60
        main_pattern = 'Análise Estatística'
    elif visitante_count > casa_count + 2:
        suggested_entry = 'Casa'
        confidence = 60
        main_pattern = 'Análise Estatística'
    elif empate_count == 0 and len(recent) >= 8:
        suggested_entry = 'Empate'
        confidence = 65
        main_pattern = 'Falta de Empate'
    else:
        suggested_entry = 'Casa' if st.session_state.history[-1:] == ['Visitante'] else 'Visitante'
        confidence = 50

    return {
        'entry': suggested_entry,
        'confidence': min(confidence, 95),
        'main_pattern': main_pattern,
        'patterns': {
            'surf': surf_detected,
            'zigzag': zigzag_detected,
            'duplas': duplas_repetidas,
            'empateRecorrente': empate_recorrente,
            'surfStreak': current_streak
        }
    }

# Função para adicionar resultado
def add_result(result):
    st.session_state.history.append(result)
    analysis = analyze_patterns(st.session_state.history)
    if analysis:
        st.session_state.suggestion = analysis
        st.session_state.confidence = analysis['confidence']
    last_result = st.session_state.history[-1]
    if st.session_state.streak['type'] == last_result:
        st.session_state.streak['count'] += 1
    else:
        st.session_state.streak = {'type': last_result, 'count': 1}

# Função para limpar
def clear_history():
    st.session_state.history = []
    st.session_state.suggestion = None
    st.session_state.confidence = 0
    st.session_state.streak = {'type': None, 'count': 0}

# ---------- INTERFACE STREAMLIT ---------- #

st.set_page_config(page_title="Football Studio Pro", layout="centered")

st.title("⚽ Football Studio Pro")
st.caption("Análise Inteligente de Padrões - Evolution Gaming")

# Botões de entrada
st.subheader("Registrar Resultado")
col1, col2, col3 = st.columns(3)
with col1:
    st.button("🏠 Casa", on_click=lambda: add_result('Casa'))
with col2:
    st.button("🤝 Empate", on_click=lambda: add_result('Empate'))
with col3:
    st.button("✈️ Visitante", on_click=lambda: add_result('Visitante'))

# Sugestão de entrada
if st.session_state.suggestion:
    st.subheader("📊 Sugestão de Entrada")
    entry = st.session_state.suggestion['entry']
    conf = st.session_state.suggestion['confidence']
    st.success(f"👉 **Aposte em:** {entry} \n\n🔍 Padrão detectado: `{st.session_state.suggestion['main_pattern']}` \n\n✅ Confiança: `{conf}%`")

# Histórico de resultados
st.subheader(f"🕒 Histórico ({len(st.session_state.history)})")
st.write(' '.join(st.session_state.history[-30:]))

# Estatísticas
if st.session_state.history:
    stats = Counter(st.session_state.history)
    total = len(st.session_state.history)
    st.subheader("📈 Estatísticas")
    st.markdown(f"""
- 🏠 Casa: {stats['Casa']} ({(stats['Casa'] / total * 100):.1f}%)
- 🤝 Empate: {stats['Empate']} ({(stats['Empate'] / total * 100):.1f}%)
- ✈️ Visitante: {stats['Visitante']} ({(stats['Visitante'] / total * 100):.1f}%)
    """)

# Streak atual
if st.session_state.streak['type']:
    tipo = st.session_state.streak['type']
    count = st.session_state.streak['count']
    alert = " ⚠️" if count >= 3 and tipo != 'Empate' else ""
    st.info(f"🔥 Streak atual: {count}x {tipo}{alert}")

# Botão para limpar histórico
st.button("🧹 Limpar Histórico", on_click=clear_history)

# Rodapé
st.markdown("---")
st.caption("⚠️ Este app é apenas para fins educacionais. Jogue com responsabilidade.")
