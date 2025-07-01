import random
import numpy as np
from collections import defaultdict

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
        self.risk_profile = 'balanced'
        
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
            print("Não há cartas suficientes para simular uma rodada")
            return None
        
        home_card = random.choice(available_cards)
        # Remove uma instância da carta escolhida
        self.card_count[home_card] -= 1
        available_cards = [card for card in available_cards if card != home_card]
        
        if not available_cards:
            print("Não há cartas suficientes para simular uma rodada")
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

    def generate_report(self):
        stats = self.calculate_statistics()
        ev = self.calculate_ev()
        card_analysis = self.card_distribution_analysis()
        opportunities = self.find_betting_opportunities()
        recommendation = self.get_betting_recommendation()
        
        report = "\n=== RELATÓRIO DE ANÁLISE DO FOOTBALL STUDIO ===\n"
        
        if stats:
            report += f"\n[ESTATÍSTICAS] Total de Jogos: {stats['total_games']}\n"
            report += f"Home Wins: {stats['home_win_percentage']:.2f}% | "
            report += f"Away Wins: {stats['away_win_percentage']:.2f}% | "
            report += f"Draws: {stats['draw_percentage']:.2f}%\n"
        
        if ev:
            report += f"\n[VALOR ESPERADO] Home: {ev['home']:.4f} | "
            report += f"Away: {ev['away']:.4f} | "
            report += f"Draw: {ev['draw']:.4f}\n"
        
        report += f"\n[ANÁLISE DE CARTAS] Cartas Restantes: {card_analysis['total_cards']}\n"
        report += f"Cartas Altas (10+): {card_analysis['high_card_ratio']*100:.1f}% | "
        report += f"Cartas Baixas: {card_analysis['low_card_ratio']*100:.1f}%\n"
        
        if opportunities:
            report += "\n[OPORTUNIDADES DE APOSTA]\n"
            for i, opp in enumerate(opportunities, 1):
                report += f"{i}. {opp['bet'].upper()}: {opp['reason']} (EV: {opp['ev']:.4f})\n"
        else:
            report += "\n[NENHUMA OPORTUNIDADE DE VALOR ENCONTRADA]\n"
        
        report += "\n[RECOMENDAÇÃO PRINCIPAL]\n"
        if recommendation['recommendation'] == 'no_bet':
            report += "Não apostar no momento\n"
            report += f"Motivo: {recommendation['message']}\n"
        else:
            report += f"Aposta em {recommendation['recommendation'].upper()}\n"
            report += f"Motivo: {recommendation['reason']}\n"
            report += f"Confiança: {recommendation['confidence']:.1f}%\n"
        
        report += "\n=== FIM DO RELATÓRIO ==="
        return report


# Função para executar uma demonstração completa
def run_full_demo():
    print("===== DEMONSTRAÇÃO DO ANALISADOR DE FOOTBALL STUDIO =====")
    decks = int(input("Quantos baralhos estão sendo usados? (1-8): ") or 1)
    analyzer = FootballStudioAnalyzer(decks=decks)
    
    # Simula jogos iniciais
    initial_games = int(input("Quantos jogos iniciais para simular? (20-100): ") or 30)
    print(f"\nSimulando {initial_games} jogos iniciais...")
    for _ in range(initial_games):
        analyzer.simulate_game()
    
    # Gera e mostra o relatório inicial
    print("\n" + analyzer.generate_report())
    
    # Menu interativo
    while True:
        print("\nOpções:")
        print("1. Adicionar resultado manual")
        print("2. Simular próximo jogo")
        print("3. Atualizar relatório")
        print("4. Reiniciar análise")
        print("5. Sair")
        
        choice = input("Escolha: ")
        
        if choice == '1':
            home = int(input("Carta do Home (2-14): "))
            away = int(input("Carta do Away (2-14): "))
            result = analyzer.add_result(home, away)
            print(f"Resultado registrado: {result.upper()}")
            
        elif choice == '2':
            result = analyzer.simulate_game()
            if result:
                print(f"Jogo simulado: Home {result['home_card']} x {result['away_card']} Away -> {result['result'].upper()}")
        
        elif choice == '3':
            print("\nAtualizando relatório...")
            print(analyzer.generate_report())
        
        elif choice == '4':
            decks = int(input("Quantos baralhos? (1-8): ") or 1)
            analyzer = FootballStudioAnalyzer(decks=decks)
            print("Análise reiniciada!")
        
        elif choice == '5':
            print("Saindo...")
            break
        
        else:
            print("Opção inválida!")

# Executar a demonstração completa
if __name__ == "__main__":
    run_full_demo()
