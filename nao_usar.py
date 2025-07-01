import streamlit as st
import random
import numpy as np
from collections import defaultdict

# Verifica e instala o Plotly se necessário
try:
    import plotly.express as px
    plotly_available = True
except ImportError:
    plotly_available = False
    st.warning("Plotly não está instalado. Usando gráficos nativos do Streamlit.")

# Configuração da página
st.set_page_config(
    page_title="Football Studio Analyzer Pro",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Classe principal
class FootballStudioAnalyzer:
    def __init__(self, decks=1):
        self.game_history = []
        self.current_round = 1
        self.card_values = list(range(2, 15))  # 2-10, J=11, Q=12, K=13, A=14
        self.probabilities = {
            'home': 44.47,  # Probabilidade teórica de vitória do Home
            'away': 44.47,  # Probabilidade teórica de vitória do Away
            'draw': 11.06   # Probabilidade teórica de empate
        }
        self.house_edge = {
            'home': 3.73,   # Vantagem da casa para Home
            'away': 3.73,   # Vantagem da casa para Away
            'draw': 10.36   # Vantagem da casa para Draw
        }
        
        # Inicializa o contador de cartas com múltiplos baralhos
        self.decks = decks
        self.card_count = {value: 4 * self.decks for value in self.card_values}
        
    def add_result(self, home_card, away_card):
        if home_card not in self.card_values or away_card not in self.card_values:
            raise ValueError("Valores de carta inválidos. Use valores entre 2 e 14.")
        
        # Atualiza contagem de cartas
        self.card_count[home_card] -= 1
        self.card_count[away_card] -= 1
        
        # Determina o resultado
        if home_card > away_card:
            result = 'home'
        elif away_card > home_card:
            result = 'away'
        else:
            result = 'draw'
        
        self.game_history.append({
            'round': self.current_round,
            'home_card': home_card,
            'away_card': away_card,
            'result': result,
            'card_difference': abs(home_card - away_card)
        })
        
        self.current_round += 1
        return result

    def calculate_statistics(self):
        if not self.game_history:
            return None
        
        stats = {
            'home_wins': 0,
            'away_wins': 0,
            'draws': 0,
            'total_games': len(self.game_history)
        }
        
        for game in self.game_history:
            if game['result'] == 'home':
                stats['home_wins'] += 1
            elif game['result'] == 'away':
                stats['away_wins'] += 1
            else:
                stats['draws'] += 1
        
        stats['home_win_percentage'] = (stats['home_wins'] / stats['total_games']) * 100
        stats['away_win_percentage'] = (stats['away_wins'] / stats['total_games']) * 100
        stats['draw_percentage'] = (stats['draws'] / stats['total_games']) * 100
        
        return stats

    def calculate_ev(self):
        stats = self.calculate_statistics()
        if not stats:
            return None
        
        # Usa probabilidades observadas se houver dados suficientes
        if stats['total_games'] >= 20:
            p_home = stats['home_win_percentage'] / 100
            p_away = stats['away_win_percentage'] / 100
            p_draw = stats['draw_percentage'] / 100
        else:
            p_home = self.probabilities['home'] / 100
            p_away = self.probabilities['away'] / 100
            p_draw = self.probabilities['draw'] / 100
        
        # Cálculo do EV considerando a regra do empate (perde metade)
        ev_home = (p_home * 1) + (p_away * -1) + (p_draw * -0.5)
        ev_away = (p_away * 1) + (p_home * -1) + (p_draw * -0.5)
        ev_draw = (p_draw * 11) + ((p_home + p_away) * -1)
        
        return {
            'home': ev_home,
            'away': ev_away,
            'draw': ev_draw
        }

    def card_distribution_analysis(self):
        high_cards = sum(count for value, count in self.card_count.items() if value >= 10)
        low_cards = sum(count for value, count in self.card_count.items() if value < 10)
        total_cards = sum(self.card_count.values())
        
        return {
            'high_card_ratio': high_cards / total_cards if total_cards > 0 else 0,
            'low_card_ratio': low_cards / total_cards if total_cards > 0 else 0,
            'total_cards': total_cards
        }

    def find_betting_opportunities(self):
        ev = self.calculate_ev()
        if not ev:
            return []
        
        opportunities = []
        card_analysis = self.card_distribution_analysis()
        
        # Critério para sugestão de aposta em Home/Away
        if ev['home'] > 0.05 or ev['away'] > 0.05:
            # Prefere apostas quando há mais cartas altas restantes
            if card_analysis['high_card_ratio'] > 0.35:
                if ev['home'] > ev['away']:
                    opportunities.append({
                        'bet': 'home',
                        'ev': ev['home'],
                        'reason': f"EV positivo ({ev['home']:.4f}) e alta probabilidade de cartas altas"
                    })
                else:
                    opportunities.append({
                        'bet': 'away',
                        'ev': ev['away'],
                        'reason': f"EV positivo ({ev['away']:.4f}) e alta probabilidade de cartas altas"
                    })
        
        # Critério para sugestão de aposta em Draw
        if ev['draw'] > 0.2:
            # Prefere apostas quando há muitas cartas de valor similar
            recent_close_games = sum(1 for g in self.game_history[-10:] if g['card_difference'] <= 2)
            
            if recent_close_games >= 4 or card_analysis['high_card_ratio'] < 0.25:
                opportunities.append({
                    'bet': 'draw',
                    'ev': ev['draw'],
                    'reason': f"EV alto para empate ({ev['draw']:.4f})"
                })
        
        return opportunities

    def simulate_game(self):
        # Cria lista de cartas disponíveis
        available_cards = []
        for card, count in self.card_count.items():
            if count > 0:
                available_cards.extend([card] * count)
        
        if len(available_cards) < 2:
            st.warning("Não há cartas suficientes para simular uma rodada")
            return None
        
        home_card = random.choice(available_cards)
        # Remove uma instância da carta escolhida
        self.card_count[home_card] -= 1
        
        # Atualiza lista de cartas disponíveis
        available_cards = []
        for card, count in self.card_count.items():
            if count > 0:
                available_cards.extend([card] * count)
        
        if not available_cards:
            st.warning("Não há cartas suficientes para simular uma rodada")
            return None
        
        away_card = random.choice(available_cards)
        self.card_count[away_card] -= 1
        
        result = self.add_result(home_card, away_card)
        return {
            'home_card': home_card,
            'away_card': away_card,
            'result': result
        }

    def get_betting_recommendation(self):
        opportunities = self.find_betting_opportunities()
        
        if not opportunities:
            return {
                'recommendation': 'no_bet',
                'message': "Nenhuma oportunidade de valor encontrada",
                'confidence': 0
            }
        
        # Ordena oportunidades pelo maior EV
        best_opportunity = max(opportunities, key=lambda x: x['ev'])
        
        # Calcula confiança baseada no EV e quantidade de dados
        stats = self.calculate_statistics()
        confidence = min(95, 50 + (best_opportunity['ev'] * 100) + (min(100, stats['total_games']) * 0.3))
        
        return {
            'recommendation': best_opportunity['bet'],
            'reason': best_opportunity['reason'],
            'ev': best_opportunity['ev'],
            'confidence': confidence
        }

    def reset_game(self):
        self.game_history = []
        self.current_round = 1
        self.card_count = {value: 4 * self.decks for value in self.card_values}

# Função para criar gráficos alternativos
def create_fallback_chart(data, title, chart_type='bar'):
    if chart_type == 'pie':
        chart_data = {
            'labels': list(data.keys()),
            'values': list(data.values())
        }
        st.write(f"**{title}**")
        st.dataframe(chart_data)
        st.bar_chart(chart_data['values'])
    else:
        st.bar_chart(data)

# Inicialização do aplicativo
def main():
    # Inicializa ou recupera a instância do analisador
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = FootballStudioAnalyzer(decks=1)
    
    analyzer = st.session_state.analyzer
    
    # Layout da barra lateral
    with st.sidebar:
        st.title("⚽ Configurações")
        decks = st.slider("Número de baralhos", 1, 8, 1, help="Quantos baralhos estão sendo usados na mesa?")
        initial_games = st.number_input("Jogos iniciais para simular", 0, 100, 30, step=5)
        
        if st.button("Iniciar/Reiniciar Análise"):
            analyzer = FootballStudioAnalyzer(decks=decks)
            st.session_state.analyzer = analyzer
            
            # Simula jogos iniciais
            for _ in range(initial_games):
                analyzer.simulate_game()
            st.success(f"{initial_games} jogos simulados! Análise iniciada.")
        
        st.divider()
        st.subheader("Adicionar Jogo Manual")
        
        col1, col2 = st.columns(2)
        with col1:
            home_card = st.number_input("Carta HOME", 2, 14, 10)
        with col2:
            away_card = st.number_input("Carta AWAY", 2, 14, 7)
        
        if st.button("Adicionar Resultado"):
            try:
                result = analyzer.add_result(home_card, away_card)
                st.success(f"Resultado registrado: HOME {home_card} x {away_card} AWAY → {result.upper()}")
            except ValueError as e:
                st.error(str(e))
        
        st.divider()
        if st.button("Simular Próximo Jogo"):
            result = analyzer.simulate_game()
            if result:
                st.success(f"Jogo simulado: HOME {result['home_card']} x {result['away_card']} AWAY → {result['result'].upper()}")
    
    # Layout principal
    st.title("⚽ Football Studio Analyzer Pro")
    st.caption("Análise estatística avançada com recomendações de apostas baseadas em valor esperado positivo")
    
    # Seção de métricas principais
    stats = analyzer.calculate_statistics()
    card_analysis = analyzer.card_distribution_analysis()
    
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total de Jogos", stats['total_games'])
        col2.metric("Vitórias HOME", f"{stats['home_win_percentage']:.2f}%", delta=f"{stats['home_wins']} vitórias")
        col3.metric("Vitórias AWAY", f"{stats['away_win_percentage']:.2f}%", delta=f"{stats['away_wins']} vitórias")
        col4.metric("Empates", f"{stats['draw_percentage']:.2f}%", delta=f"{stats['draws']} empates")
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Estatísticas", "💡 Recomendações", "🃏 Distribuição de Cartas", "📜 Histórico"])
    
    with tab1:
        st.subheader("Análise Estatística")
        
        if stats:
            # Gráfico de pizza
            if plotly_available:
                fig = px.pie(
                    name
