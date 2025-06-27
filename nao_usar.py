import streamlit as st 
import random from statistics
import mean
Classe analisadora
class FootballStudioAnalyzer: def init(self): self.history = [] self.suggestion = None self.confidence = 0 self.streak = {'type': None, 'count': 0}
def add_result(self, result):
    self.history.append(result)
    self.update_streak()
    analysis = self.analyze_patterns(self.history)
    if analysis:
        self.suggestion = analysis
        self.confidence = analysis['confidence']

def clear_history(self):
    self.history = []
    self.suggestion = None
    self.confidence = 0
    self.streak = {'type': None, 'count': 0}

def update_streak(self):
    if self.history:
        last_result = self.history[-1]
        if self.streak['type'] == last_result:
            self.streak['count'] += 1
        else:
            self.streak = {'type': last_result, 'count': 1}

def analyze_patterns(self, results):
    if len(results) < 3:
        return None

    recent = results[-10:]
    last3 = results[-3:]
    last5 = results[-5:]

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
            if grupos[i:i+4] == [1, 2, 1, 2]:
                padrao_onda = True
                break

    padrao_3x1 = False
    if len(recent) >= 4:
        for i in range(len(recent) - 3):
            seg = recent[i:i+4]
            if seg[0] == seg[1] == seg[2] and seg[3] != seg[0] and seg[0] != 'Empate' and seg[3] != 'Empate':
                padrao_3x1 = True
                break

    padrao_3x3 = False
    if len(recent) >= 6:
        for i in range(len(recent) - 5):
            seg = recent[i:i+6]
            if seg[0] == seg[1] == seg[2] and seg[3] == seg[4] == seg[5] and seg[0] != seg[3] and seg[0] != 'Empate' and seg[3] != 'Empate':
                padrao_3x3 = True
                break

    empatesPontosFixes = False
    if len(empatePositions) >= 2:
        gaps = [empatePositions[i] - empatePositions[i - 1] for i in range(1, len(empatePositions))]
        if gaps:
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
        last = recent[-1]
        suggestedEntry = 'Visitante' if last == 'Casa' else 'Casa'
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

--- Interface Streamlit ---

analyzer = FootballStudioAnalyzer()

st.set_page_config(page_title="Football Studio Pro", layout="centered") st.title("⚽ Football Studio Pro") st.markdown("Análise Inteligente de Padrões - Evolution Gaming")

col1, col2, col3 = st.columns(3) with col1: if st.button("🏠 CASA"): analyzer.add_result("Casa") with col2: if st.button("🤝 EMPATE"): analyzer.add_result("Empate") with col3: if st.button("✈️ VISITANTE"): analyzer.add_result("Visitante")

st.markdown("---")

if analyzer.suggestion: st.subheader(f"🎯 Próxima Entrada: {analyzer.suggestion['entry']}") st.markdown(f"Padrão Detectado: {analyzer.suggestion['mainPattern']}") st.markdown(f"Confiabilidade: {analyzer.suggestion['confidence']}%") st.markdown("Padrões Ativos:") for k, v in analyzer.suggestion['patterns'].items(): if v: st.markdown(f"- {k} ({v if not isinstance(v, bool) else ''})")

st.markdown("---")

if analyzer.history: st.subheader(f"📜 Histórico ({len(analyzer.history)})") cols = st.columns(len(analyzer.history)) for i, res in enumerate(reversed(analyzer.history)): color = 'red' if res == 'Casa' else 'blue' if res == 'Visitante' else 'gray' cols[i].markdown(f"<div style='background-color:{color}; color:white; padding:10px; border-radius:50%; text-align:center;'>{res[0]}</div>", unsafe_allow_html=True)

st.markdown("---")
casa = analyzer.history.count('Casa')
visitante = analyzer.history.count('Visitante')
empate = analyzer.history.count('Empate')
total = len(analyzer.history)
st.markdown(f"🏠 Casa: {casa} ({casa / total:.1%})")
st.markdown(f"✈️ Visitante: {visitante} ({visitante / total:.1%})")
st.markdown(f"🤝 Empate: {empate} ({empate / total:.1%})")

if analyzer.streak['type']: st.markdown("---") tipo = analyzer.streak['type'] count = analyzer.streak['count'] alerta = " ⚠️ Possível quebra" if count >= 3 and tipo != 'Empate' else "" st.info(f"🔥 Streak Atual: {count}x {tipo}{alerta}")

if st.button("🧹 Limpar Histórico"): analyzer.clear_history() st.experimental_rerun()

st.markdown("---") st.caption("⚠️ Este aplicativo é apenas para fins educacionais e de entretenimento. Apostas envolvem riscos. Jogue com responsabilidade.")

