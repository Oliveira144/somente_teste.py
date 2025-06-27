import streamlit as st
from statistics import mean
import random

st.set_page_config(page_title="Football Studio Pro", layout="centered")

st.markdown(
    """
    <style>
        .result-bubble {
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            font-weight: bold;
            font-size: 16px;
            margin: 2px;
        }
    </style>
    """, unsafe_allow_html=True
)

# Inicializa sessões
if 'history' not in st.session_state:
    st.session_state.history = []
if 'streak' not in st.session_state:
    st.session_state.streak = {'type': None, 'count': 0}
if 'suggestion' not in st.session_state:
    st.session_state.suggestion = None


def analyze_patterns(results):
    if len(results) < 3:
        return None

    recent = results[-10:]
    last3 = results[-3:]
    last5 = results[-5:]
    last7 = results[-7:]

    surfDetected = False
    currentStreak = 1
    for i in range(len(recent) - 2, -1, -1):
        if recent[i] == recent[-1] and recent[i] != 'Empate':
            currentStreak += 1
        else:
            break
    if currentStreak >= 3:
        surfDetected = True

    zigzagCount = 0
    for i in range(1, len(last5)):
        if last5[i] != last5[i - 1] and last5[i] != 'Empate' and last5[i - 1] != 'Empate':
            zigzagCount += 1
    zigzagDetected = zigzagCount >= 3

    duplasRepetidas = False
    if len(recent) >= 6:
        duplaCount = 0
        for i in range(0, len(recent) - 1, 2):
            if recent[i] == recent[i + 1] and recent[i] != 'Empate':
                duplaCount += 1
        duplasRepetidas = duplaCount >= 2

    empatePositions = [i for i, r in enumerate(results) if r == 'Empate']
    empateRecorrente = False
    if len(empatePositions) >= 2:
        lastEmpateGap = len(results) - 1 - empatePositions[-1]
        if 15 <= lastEmpateGap <= 35:
            empateRecorrente = True

    padrao_escada = False
    if len(recent) >= 6:
        escalones = []
        count = 1
        current = recent[0]
        for i in range(1, len(recent)):
            if recent[i] == current and recent[i] != 'Empate':
                count += 1
            else:
                if current != 'Empate':
                    escalones.append(count)
                current = recent[i]
                count = 1
        if current != 'Empate':
            escalones.append(count)
        for i in range(len(escalones) - 2):
            if escalones[i + 1] == escalones[i] + 1 and escalones[i + 2] == escalones[i] + 2:
                padrao_escada = True
                break

    espelhamento = False
    if len(last5) >= 4:
        for i in range(len(last5) - 3):
            seg = last5[i:i + 4]
            if seg[0] == seg[3] and seg[1] == seg[2] and seg[0] != seg[1] and seg[0] != 'Empate' and seg[1] != 'Empate':
                espelhamento = True
                break

    alternanciaEmpate = False
    if len(last5) >= 3:
        for i in range(len(last5) - 2):
            if last5[i] != 'Empate' and last5[i + 1] == 'Empate' and last5[i + 2] != 'Empate' and last5[i] != last5[i + 2]:
                alternanciaEmpate = True
                break

    padrao_onda = False
    if len(recent) >= 6:
        grupos = []
        count = 1
        current = recent[0]
        for i in range(1, len(recent)):
            if recent[i] == current and recent[i] != 'Empate':
                count += 1
            else:
                if current != 'Empate':
                    grupos.append(count)
                current = recent[i]
                count = 1
        if current != 'Empate':
            grupos.append(count)
        for i in range(len(grupos) - 3):
            if grupos[i:i + 4] == [1, 2, 1, 2]:
                padrao_onda = True
                break

    padrao_3x1 = False
    if len(recent) >= 4:
        for i in range(len(recent) - 3):
            seg = recent[i:i + 4]
            if seg[0] == seg[1] == seg[2] and seg[2] != seg[3] and seg[0] != 'Empate' and seg[3] != 'Empate':
                padrao_3x1 = True
                break

    padrao_3x3 = False
    if len(recent) >= 6:
        for i in range(len(recent) - 5):
            seg = recent[i:i + 6]
            if seg[0] == seg[1] == seg[2] and seg[3] == seg[4] == seg[5] and seg[0] != seg[3] and seg[0] != 'Empate' and seg[3] != 'Empate':
                padrao_3x3 = True
                break

    empatesPontosFixes = False
    if len(empatePositions) >= 2:
        gaps = [empatePositions[i] - empatePositions[i - 1] for i in range(1, len(empatePositions))]
        avgGap = mean(gaps)
        if 9 <= avgGap <= 10:
            empatesPontosFixes = True

    quebrarSurf = surfDetected and currentStreak >= 4
    quebrarZigzag = zigzagDetected and all(r != 'Empate' for r in last3)
    quebrarDuplas = duplasRepetidas

    casaCount = recent.count('Casa')
    visitanteCount = recent.count('Visitante')
    empateCount = recent.count('Empate')

    suggestedEntry = None
    conf = 0
    mainPattern = ''

    if quebrarSurf:
        currentColor = recent[-1]
        suggestedEntry = 'Visitante' if currentColor == 'Casa' else 'Casa'
        conf = 88 + min(currentStreak * 2, 10)
        mainPattern = 'Quebra de Surf'
    elif empateRecorrente:
        suggestedEntry = 'Empate'
        conf = 82
        mainPattern = 'Empate Recorrente'
    elif padrao_3x1:
        suggestedEntry = 'Visitante' if recent[-1] == 'Casa' else 'Casa'
        conf = 80
        mainPattern = 'Padrão 3x1'
    elif espelhamento:
        penultimo = recent[-2]
        suggestedEntry = penultimo if penultimo != 'Empate' else 'Casa'
        conf = 78
        mainPattern = 'Espelhamento'
    elif zigzagDetected:
        lastResult = recent[-1]
        if lastResult != 'Empate':
            suggestedEntry = 'Visitante' if lastResult == 'Casa' else 'Casa'
            conf = 75
            mainPattern = 'Zig-Zag'
    elif alternanciaEmpate:
        suggestedEntry = 'Empate'
        conf = 72
        mainPattern = 'Alternância c/ Empate'
    elif surfDetected:
        suggestedEntry = recent[-1]
        conf = 65 + currentStreak * 3
        mainPattern = 'Surf Continuado'
    elif duplasRepetidas:
        suggestedEntry = recent[-1]
        conf = 68
        mainPattern = 'Duplas Repetidas'
    elif padrao_escada:
        suggestedEntry = 'Visitante' if recent[-1] == 'Casa' else 'Casa'
        conf = 70
        mainPattern = 'Padrão Escada'
    else:
        if casaCount > visitanteCount + 2:
            suggestedEntry = 'Visitante'
            conf = 60
            mainPattern = 'Análise Estatística'
        elif visitanteCount > casaCount + 2:
            suggestedEntry = 'Casa'
            conf = 60
            mainPattern = 'Análise Estatística'
        elif empateCount == 0 and len(recent) >= 8:
            suggestedEntry = 'Empate'
            conf = 65
            mainPattern = 'Falta de Empate'
        else:
            suggestedEntry = random.choice(['Casa', 'Visitante'])
            conf = 50
            mainPattern = 'Análise Básica'

    return {
        'entry': suggestedEntry,
        'confidence': min(conf, 95),
        'mainPattern': mainPattern,
        'patterns': {
            'surf': surfDetected,
            'surfStreak': currentStreak,
            'zigzag': zigzagDetected,
            'duplasRepetidas': duplasRepetidas,
            'empateRecorrente': empateRecorrente,
            'padrao_escada': padrao_escada,
            'espelhamento': espelhamento,
            'alternanciaEmpate': alternanciaEmpate,
            'padrao_onda': padrao_onda,
            'padrao_3x1': padrao_3x1,
            'padrao_3x3': padrao_3x3,
            'empatesPontosFixes': empatesPontosFixes,
            'quebrarSurf': quebrarSurf,
            'quebrarZigzag': quebrarZigzag,
            'quebrarDuplas': quebrarDuplas
        }
    }
    Football Studio Pro em Streamlit (parte visual)

import streamlit as st

Cabeçalho

st.markdown(""" <h1 style='text-align: center; color: #facc15;'>⚽ Football Studio Pro</h1> <p style='text-align: center; color: #aaa;'>Análise Inteligente de Padrões - Evolution Gaming</p> """, unsafe_allow_html=True)

Inicialização de variáveis de estado

if 'history' not in st.session_state: st.session_state.history = [] if 'suggestion' not in st.session_state: st.session_state.suggestion = None if 'streak' not in st.session_state: st.session_state.streak = {'type': None, 'count': 0}

Placeholder para a função analyze_patterns

Você deve implementar ou importar a função analyze_patterns completa aqui

def analyze_patterns(results): return None  # Substitua com a lógica real de análise de padrões

Botões de entrada

col1, col2, col3 = st.columns(3) with col1: if st.button("🏠 CASA"): st.session_state.history.append("Casa") with col2: if st.button("🤝 EMPATE"): st.session_state.history.append("Empate") with col3: if st.button("✈️ VISITANTE"): st.session_state.history.append("Visitante")

Analisar e atualizar sugestão

analysis = analyze_patterns(st.session_state.history) if analysis: st.session_state.suggestion = analysis if len(st.session_state.history) >= 1: last = st.session_state.history[-1] if st.session_state.streak['type'] == last: st.session_state.streak['count'] += 1 else: st.session_state.streak = {'type': last, 'count': 1}

Exibir sugestão

if st.session_state.suggestion: s = st.session_state.suggestion st.subheader(f"Padrão Principal: {s['mainPattern']}") st.markdown(f"### Próxima Entrada: {s['entry']} ({s['confidence']}% confiança)")

Histórico visual

st.markdown("### Histórico") row = "" for i, r in enumerate(reversed(st.session_state.history)): cor = '#ef4444' if r == 'Casa' else ('#3b82f6' if r == 'Visitante' else '#737373') letra = 'C' if r == 'Casa' else ('V' if r == 'Visitante' else 'E') row += f"<div style='width: 40px; height: 40px; background:{cor}; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; margin:2px; font-weight:bold;'>{letra}</div>" st.markdown(row, unsafe_allow_html=True)

Estatísticas

if st.session_state.history: total = len(st.session_state.history) casa = st.session_state.history.count("Casa") empate = st.session_state.history.count("Empate") visitante = st.session_state.history.count("Visitante") st.markdown(f""" ### Estatísticas - Casa: {casa} ({(casa/total)*100:.1f}%) - Empate: {empate} ({(empate/total)*100:.1f}%) - Visitante: {visitante} ({(visitante/total)*100:.1f}%) """)

Streak

if st.session_state.streak['type']: st.markdown(f"### Streak Atual: {st.session_state.streak['count']}x {st.session_state.streak['type']}")

Limpar histórico

if st.button("Limpar Histórico"): st.session_state.history = [] st.session_state.streak = {'type': None, 'count': 0} st.session_state.suggestion = None

Aviso legal

st.markdown("""

<div style='text-align: center; color: #aaa; font-size: small;'>
    <p>⚠️ Este aplicativo é apenas para fins educacionais e de entretenimento.</p>
    <p>Apostas envolvem riscos. Jogue com responsabilidade.</p>
</div>
""", unsafe_allow_html=True)
