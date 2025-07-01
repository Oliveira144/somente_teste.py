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
        
        # Adiciona sequências atuais
        stats['current_streak'] = self.get_current_streak()
        
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
            'total_cards': total_cards,
            'high_cards': high_cards,
            'low_cards': low_cards
        }

    def find_betting_opportunities(self):
        ev = self.calculate_ev()
        if not ev:
            return []
        
        opportunities = []
        card_analysis = self.card_distribution_analysis()
        stats = self.calculate_statistics()
        
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

    def get_current_streak(self):
        if not self.game_history:
            return {'type': None, 'length': 0}
        
        streak_type = self.game_history[-1]['result']
        streak_length = 1
        
        # Percorre o histórico de trás para frente
        for i in range(len(self.game_history)-2, -1, -1):
            if self.game_history[i]['result'] == streak_type:
                streak_length += 1
            else:
                break
                
        return {'type': streak_type, 'length': streak_length}
    
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

# Função para converter valor da carta para nome
def card_name(value):
    if value == 11:
        return 'J'
    elif value == 12:
        return 'Q'
    elif value == 13:
        return 'K'
    elif value == 14:
        return 'A'
    else:
        return str(value)

# Função para criar um círculo visual de jogo
def game_circle(game):
    home = card_name(game['home_card'])
    away = card_name(game['away_card'])
    result = game['result']
    
    # Cores de fundo baseadas no resultado
    if result == 'home':
        bg_color = '#EF4444'  # vermelho
        border_color = '#B91C1C'
    elif result == 'away':
        bg_color = '#3B82F6'  # azul
        border_color = '#1D4ED8'
    else:
        bg_color = '#EAB308'  # amarelo
        border_color = '#CA8A04'
    
    # Tamanho do círculo
    size = "50px"
    font_size = "1em"
    
    circle_html = f"""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 3px;
    ">
        <div style="
            background-color: {bg_color};
            border: 2px solid {border_color};
            border-radius: 50%;
            width: {size};
            height: {size};
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            text-align: center;
        ">
            {home}x{away}
        </div>
        <div style="font-size: 0.7em; margin-top: 3px; color: #777; font-weight: bold;">
            R{game['round']}
        </div>
    </div>
    """
    return circle_html

# Função para exibir jogos em linhas
def display_games_in_lines(games, games_per_line=9):
    if not games:
        return
    
    # Dividir os jogos em linhas
    lines = [games[i:i+games_per_line] for i in range(0, len(games), games_per_line)]
    
    for line in lines:
        # Criar uma linha com várias colunas
        cols = st.columns(games_per_line)
        for idx, game in enumerate(line):
            with cols[idx]:
                circle_html = game_circle(game)
                st.markdown(circle_html, unsafe_allow_html=True)

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
                st.success(f"Resultado registrado: HOME {card_name(home_card)} x {card_name(away_card)} AWAY → {result.upper()}")
            except ValueError as e:
                st.error(str(e))
        
        st.divider()
        if st.button("Simular Próximo Jogo"):
            result = analyzer.simulate_game()
            if result:
                st.success(f"Jogo simulado: HOME {card_name(result['home_card'])} x {card_name(result['away_card'])} AWAY → {result['result'].upper()}")
    
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
    
    # Sequência atual
    if stats:
        streak = stats.get('current_streak', {})
        if streak and streak['type']:
            streak_type = streak['type'].upper()
            streak_length = streak['length']
            
            streak_color = "#EF4444" if streak_type == 'HOME' else "#3B82F6" if streak_type == 'AWAY' else "#EAB308"
            streak_text = f"<div style='background-color:#1E1E1E; padding:10px; border-radius:5px;'>" \
                          f"<h3 style='color:{streak_color};'>Sequência Atual: {streak_type} ({streak_length} rodadas)</h3>" \
                          f"</div>"
            st.markdown(streak_text, unsafe_allow_html=True)
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Estatísticas", "💡 Recomendações", "🃏 Distribuição de Cartas", "📜 Histórico Completo"])
    
    with tab1:
        st.subheader("Análise Estatística")
        
        if stats:
            # Gráfico de pizza
            if plotly_available:
                try:
                    fig = px.pie(
                        names=['HOME', 'AWAY', 'DRAW'],
                        values=[
                            stats['home_win_percentage'], 
                            stats['away_win_percentage'], 
                            stats['draw_percentage']
                        ],
                        color_discrete_sequence=['#EF4444', '#3B82F6', '#EAB308'],
                        title="Distribuição de Resultados"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Erro ao criar gráfico: {str(e)}")
                    pie_data = {
                        'HOME': stats['home_win_percentage'],
                        'AWAY': stats['away_win_percentage'],
                        'DRAW': stats['draw_percentage']
                    }
                    create_fallback_chart(pie_data, "Distribuição de Resultados", 'pie')
            else:
                pie_data = {
                    'HOME': stats['home_win_percentage'],
                    'AWAY': stats['away_win_percentage'],
                    'DRAW': stats['draw_percentage']
                }
                create_fallback_chart(pie_data, "Distribuição de Resultados", 'pie')
            
            # Valor Esperado (EV)
            ev = analyzer.calculate_ev()
            if ev:
                st.subheader("Valor Esperado (EV)")
                col1, col2, col3 = st.columns(3)
                col1.metric("EV HOME", f"{ev['home']:.4f}", 
                            delta_color="inverse" if ev['home'] < 0 else "normal")
                col2.metric("EV AWAY", f"{ev['away']:.4f}", 
                            delta_color="inverse" if ev['away'] < 0 else "normal")
                col3.metric("EV DRAW", f"{ev['draw']:.4f}", 
                            delta_color="inverse" if ev['draw'] < 0 else "normal")
                
                st.info("""
                **Interpretação do Valor Esperado (EV):**
                - **EV > 0**: Aposta favorável a longo prazo
                - **EV = 0**: Aposta neutra
                - **EV < 0**: Aposta desfavorável
                """)
        else:
            st.warning("Adicione jogos para ver as estatísticas")
    
    with tab2:
        st.subheader("Oportunidades de Aposta")
        
        opportunities = analyzer.find_betting_opportunities()
        recommendation = analyzer.get_betting_recommendation()
        
        if opportunities:
            st.success("🎯 Oportunidades de Valor Encontradas!")
            
            for opp in opportunities:
                with st.expander(f"Aposta em {opp['bet'].upper()} (EV: {opp['ev']:.4f})"):
                    st.write(opp['reason'])
                    st.progress(min(1.0, opp['ev'] + 0.2), text=f"Potencial: {opp['ev']:.4f}")
            
            st.divider()
            st.subheader("Recomendação Principal")
            
            if recommendation['recommendation'] != 'no_bet':
                confidence = recommendation['confidence']
                color = "green" if confidence > 75 else "orange" if confidence > 60 else "red"
                
                st.markdown(f"""
                <div style="border-left: 5px solid {color}; padding: 10px; background-color: #1E1E1E; border-radius: 5px;">
                    <h3 style="color: white;">Aposta recomendada: <span style="color: {color};">{recommendation['recommendation'].upper()}</span></h3>
                    <p><strong>Confiança:</strong> <span style="color: {color};">{confidence:.1f}%</span></p>
                    <p><strong>Motivo:</strong> {recommendation['reason']}</p>
                    <p><strong>Valor Esperado:</strong> {recommendation['ev']:.4f}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(recommendation['message'])
        else:
            st.warning("Nenhuma oportunidade de valor encontrada no momento.")
            st.info("""
            **Por que não há oportunidades?**
            - As probabilidades atuais não oferecem valor esperado positivo
            - Distribuição de cartas não é favorável
            - Dados insuficientes para análise confiável
            """)
        
        # Histórico compacto abaixo da recomendação
        st.divider()
        st.subheader("Histórico de Jogos (da esquerda para direita: mais recente -> mais antigo)")
        
        if analyzer.game_history:
            # Exibir apenas os últimos 30 jogos
            recent_games = analyzer.game_history[-30:]
            
            # Usar função de exibição em linhas
            display_games_in_lines(recent_games, games_per_line=9)
        else:
            st.info("Nenhum jogo registrado. Adicione jogos para ver o histórico.")
    
    with tab3:
        st.subheader("Distribuição de Cartas")
        
        if card_analysis['total_cards'] > 0:
            # Métricas
            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Cartas", card_analysis['total_cards'])
            col2.metric("Cartas Altas (10+)", card_analysis['high_cards'], f"{card_analysis['high_card_ratio']*100:.1f}%")
            col3.metric("Cartas Baixas (2-9)", card_analysis['low_cards'], f"{card_analysis['low_card_ratio']*100:.1f}%")
            
            # Preparar dados para gráfico
            card_data = []
            for value, count in analyzer.card_count.items():
                card_data.append({
                    'Carta': card_name(value),
                    'Quantidade': count,
                    'Tipo': 'Alta' if value >= 10 else 'Baixa'
                })
            
            # Usar Plotly se disponível, caso contrário usar gráfico nativo
            if plotly_available:
                try:
                    fig = px.bar(
                        card_data,
                        x='Carta',
                        y='Quantidade',
                        color='Tipo',
                        color_discrete_map={'Alta': '#EF4444', 'Baixa': '#3B82F6'},
                        title="Distribuição de Cartas Restantes"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Erro ao criar gráfico: {str(e)}")
                    # Criar gráfico nativo
                    chart_data = {item['Carta']: item['Quantidade'] for item in card_data}
                    st.bar_chart(chart_data)
            else:
                # Criar gráfico nativo
                chart_data = {item['Carta']: item['Quantidade'] for item in card_data}
                st.bar_chart(chart_data)
        else:
            st.warning("Nenhuma carta restante. Reinicie a análise.")
    
    with tab4:
        st.subheader("Histórico Completo de Jogos")
        
        if analyzer.game_history:
            # Usar função de exibição em linhas para todos os jogos
            display_games_in_lines(analyzer.game_history, games_per_line=9)
            
            # Tabela detalhada
            st.subheader("Detalhes por Rodada")
            display_data = []
            for game in analyzer.game_history:
                display_data.append({
                    'Rodada': game['round'],
                    'HOME': card_name(game['home_card']),
                    'AWAY': card_name(game['away_card']),
                    'Resultado': game['result'].upper(),
                    'Diferença': game['card_difference']
                })
            
            st.dataframe(
                display_data,
                column_config={
                    "Resultado": st.column_config.TextColumn(
                        "Resultado",
                        help="Resultado do jogo",
                        width="medium"
                    ),
                    "Diferença": st.column_config.ProgressColumn(
                        "Diferença",
                        help="Diferença entre cartas",
                        format="%d",
                        min_value=0,
                        max_value=12,
                    )
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("Nenhum jogo registrado. Adicione jogos para ver o histórico.")

if __name__ == "__main__":
    main()
