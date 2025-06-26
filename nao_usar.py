import streamlit as st
import random
from streamlit.components.v1 import html

# Inicialização de sessão
if 'history' not in st.session_state:
    st.session_state.history = []
if 'suggestion' not in st.session_state:
    st.session_state.suggestion = None
if 'confidence' not in st.session_state:
    st.session_state.confidence = 0
if 'streak' not in st.session_state:
    st.session_state.streak = {'type': None, 'count': 0}


def analyze_patterns(results):
    if len(results) < 3:
        return None

    recent = results[-10:]
    last5 = results[-5:]

    # Surf de Cor
    surf_detected = False
    current_streak = 1
    for i in range(len(recent) - 2, -1, -1):
        if recent[i] == recent[-1] and recent[i] != 'Empate':
            current_streak += 1
        else:
            break
    if current_streak >= 3:
        surf_detected = True

    # Zig-Zag
    zigzag_count = 0
    for i in range(1, len(last5)):
        if last5[i] != last5[i - 1] and last5[i] != 'Empate' and last5[i - 1] != 'Empate':
            zigzag_count += 1
    zigzag_detected = zigzag_count >= 3

    # Empate recorrente
    empate_positions = [i for i, r in enumerate(results) if r == 'Empate']
    empate_recorrente = False
    if len(empate_positions) >= 2:
        last_gap = len(results) - 1 - empate_positions[-1]
        if 15 <= last_gap <= 35:
            empate_recorrente = True

    # Quebras
    quebrar_surf = surf_detected and current_streak >= 4
    quebrar_zigzag = zigzag_detected

    # Sugestão
    suggested_entry = None
    conf = 0

    if quebrar_surf:
        suggested_entry = 'Visitante' if recent[-1] == 'Casa' else 'Casa'
        conf = 85 + min(current_streak * 2, 15)
    elif zigzag_detected:
        if recent[-1] != 'Empate':
            suggested_entry = 'Visitante' if recent[-1] == 'Casa' else 'Casa'
            conf = 75
    elif empate_recorrente:
        suggested_entry = 'Empate'
        conf = 70
    elif surf_detected:
        suggested_entry = recent[-1]
        conf = 65 + current_streak * 3
    else:
        casa_count = recent.count('Casa')
        visitante_count = recent.count('Visitante')
        if casa_count > visitante_count + 2:
            suggested_entry = 'Visitante'
            conf = 60
        elif visitante_count > casa_count + 2:
            suggested_entry = 'Casa'
            conf = 60
        else:
            suggested_entry = random.choice(['Casa', 'Visitante'])
            conf = 50

    return {
        'entry': suggested_entry,
        'confidence': min(conf, 98),
        'patterns': {
            'surf': surf_detected,
            'surfStreak': current_streak,
            'zigzag': zigzag_detected,
            'empateRecorrente': empate_recorrente,
            'quebrarSurf': quebrar_surf,
            'quebrarZigzag': quebrar_zigzag
        }
    }


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


def clear_history():
    st.session_state.history = []
    st.session_state.suggestion = None
    st.session_state.confidence = 0
    st.session_state.streak = {'type': None, 'count': 0}


# Título
st.title("⚽ Football Studio Pro")
st.caption("Análise Inteligente de Padrões - Evolution Gaming")

# Botões de entrada
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Casa"):
        add_result("Casa")
with col2:
    if st.button("🤝 Empate"):
        add_result("Empate")
with col3:
    if st.button("✈️ Visitante"):
        add_result("Visitante")

# Sugestão
if st.session_state.suggestion:
    entry = st.session_state.suggestion['entry']
    conf = st.session_state.confidence
    patterns = st.session_state.suggestion['patterns']

    st.markdown("### 🎯 Próxima Entrada Sugerida")
    st.markdown(f"**Entrada:** `{entry}`")
    st.markdown(f"**Confiança:** `{conf}%`")

    st.markdown("#### 📊 Padrões Detectados")
    if patterns['surf']:
        st.success(f"⚡ Surf de Cor ({patterns['surfStreak']}x)")
    if patterns['quebrarSurf']:
        st.warning("⚠️ Quebra de Surf detectada")
    if patterns['zigzag']:
        st.info("📈 Zig-Zag detectado")
    if patterns['empateRecorrente']:
        st.info("🎯 Empate Recorrente possível")

# Histórico visual em bolinhas
st.divider()
st.markdown(f"### Últimos Resultados ({len(st.session_state.history)})")
if st.button("🧹 Limpar Histórico"):
    clear_history()

if st.session_state.history:
    colors = {
        "Casa": "#dc2626",        # Vermelho
        "Empate": "#4b5563",      # Cinza
        "Visitante": "#2563eb"    # Azul
    }

    html_content = "<div style='display: flex; flex-wrap: wrap; gap: 8px;'>"
    for result in reversed(st.session_state.history):
        letra = 'C' if result == 'Casa' else 'V' if result == 'Visitante' else 'E'
        cor = colors[result]
        html_content += f"""
            <div style="
                width: 36px;
                height: 36px;
                border-radius: 50%;
                background-color: {cor};
                color: white;
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 14px;
            ">
                {letra}
            </div>
        """
    html_content += "</div>"

    html(html_content, height=120)

    # Estatísticas
    total = len(st.session_state.history)
    casa = st.session_state.history.count("Casa")
    empate = st.session_state.history.count("Empate")
    visitante = st.session_state.history.count("Visitante")

    st.markdown("#### Estatísticas")
    col1, col2, col3 = st.columns(3)
    col1.metric("Casa", f"{casa}", f"{(casa / total * 100):.1f}%")
    col2.metric("Empate", f"{empate}", f"{(empate / total * 100):.1f}%")
    col3.metric("Visitante", f"{visitante}", f"{(visitante / total * 100):.1f}%")

# Streak atual
if st.session_state.streak['type']:
    tipo = st.session_state.streak['type']
    count = st.session_state.streak['count']
    aviso = "⚠️ Possível quebra" if count >= 3 and tipo != 'Empate' else ""
    st.markdown(f"### 🔁 Streak Atual: {count}x {tipo} {aviso}")

# Rodapé
st.info("⚠️ Este aplicativo é apenas para fins educacionais e de entretenimento. Apostas envolvem riscos. Jogue com responsabilidade.")
