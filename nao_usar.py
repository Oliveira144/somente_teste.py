import random
import time
from datetime import datetime

class FootballStudioAnalyzer:
    """
    Analisador de jogos de Football Studio.
    Replica a funcionalidade do componente React para análise de estatísticas,
    detecção de padrões e geração de recomendações.
    """
    def __init__(self):
        # Estado inicial
        self.game_history = []
        self.current_round = 1
        self.statistics = {
            'home': {'wins': 0, 'percentage': 0.0},
            'away': {'wins': 0, 'percentage': 0.0},
            'draw': {'wins': 0, 'percentage': 0.0}
        }
        self.patterns = []
        self.recommendation = None
        self.confidence = 0
        self.manual_mode = True

    def generate_initial_history(self):
        """Gera um histórico inicial de jogos para simulação."""
        real_history = [
            {'result': 'HOME', 'home_card': 8, 'away_card': 14}, # Ás = 14, então AWAY vence
            {'result': 'AWAY', 'home_card': 4, 'away_card': 9},
            {'result': 'HOME', 'home_card': 8, 'away_card': 7},
            {'result': 'AWAY', 'home_card': 5, 'away_card': 6},
            {'result': 'HOME', 'home_card': 10, 'away_card': 2},
            {'result': 'HOME', 'home_card': 13, 'away_card': 9},
            {'result': 'AWAY', 'home_card': 2, 'away_card': 12},
            {'result': 'AWAY', 'home_card': 5, 'away_card': 9},
            {'result': 'HOME', 'home_card': 13, 'away_card': 11},
            {'result': 'AWAY', 'home_card': 4, 'away_card': 13},
            {'result': 'HOME', 'home_card': 13, 'away_card': 12},
            {'result': 'AWAY', 'home_card': 14, 'away_card': 5}, # Ás HOME = 14, então HOME vence
            {'result': 'AWAY', 'home_card': 14, 'away_card': 7}, # Ás HOME = 14, então HOME vence
            {'result': 'HOME', 'home_card': 2, 'away_card': 14}, # Ás AWAY = 14, então AWAY vence
            {'result': 'AWAY', 'home_card': 2, 'away_card': 8},
            {'result': 'DRAW', 'home_card': 5, 'away_card': 5},
            {'result': 'HOME', 'home_card': 10, 'away_card': 14}, # Ás AWAY = 14, então AWAY vence
            {'result': 'DRAW', 'home_card': 10, 'away_card': 10},
            {'result': 'AWAY', 'home_card': 12, 'away_card': 6},
            {'result': 'DRAW', 'home_card': 5, 'away_card': 7}
        ]

        history_with_timestamp = []
        for i, game in enumerate(real_history):
            history_with_timestamp.append({
                'round': i + 1,
                'result': game['result'],
                'home_card': game['home_card'],
                'away_card': game['away_card'],
                'timestamp': datetime.now()
            })
        return history_with_timestamp

    def initialize(self):
        """Inicializa o analisador com o histórico de jogos."""
        self.game_history = self.generate_initial_history()
        self.current_round = len(self.game_history) + 1
        self.update_analysis()

    def update_analysis(self):
        """Atualiza todas as análises (estatísticas, padrões e recomendação)."""
        self.calculate_statistics()
        self.analyze_patterns()
        self.generate_recommendation()

    def calculate_statistics(self):
        """Calcula as estatísticas de vitórias com base no histórico."""
        if not self.game_history:
            return

        total_games = len(self.game_history)
        home_wins = sum(1 for g in self.game_history if g['result'] == 'HOME')
        away_wins = sum(1 for g in self.game_history if g['result'] == 'AWAY')
        draws = sum(1 for g in self.game_history if g['result'] == 'DRAW')

        self.statistics = {
            'home': {'wins': home_wins, 'percentage': round((home_wins / total_games) * 100, 1)},
            'away': {'wins': away_wins, 'percentage': round((away_wins / total_games) * 100, 1)},
            'draw': {'wins': draws, 'percentage': round((draws / total_games) * 100, 1)}
        }

    def analyze_patterns(self):
        """Analisa o histórico recente em busca de padrões."""
        self.patterns = []
        if len(self.game_history) < 5:
            return

        recent = self.game_history[-10:]

        # Análise de sequências (streaks)
        if len(recent) > 0:
            current_streak = 1
            streak_type = recent[-1]['result']
            
            for i in range(len(recent) - 2, -1, -1):
                if recent[i]['result'] == streak_type:
                    current_streak += 1
                else:
                    break

            if current_streak >= 3:
                self.patterns.append({
                    'type': 'streak',
                    'description': f'Sequência de {current_streak} {streak_type}',
                    'impact': 'high'
                })

        # Análise de alternância
        alternating = recent[-6:]
        is_alternating = True
        if len(alternating) > 1:
            for i in range(1, len(alternating)):
                if alternating[i]['result'] == alternating[i-1]['result']:
                    is_alternating = False
                    break
        
        if is_alternating and len(alternating) >= 2:
            self.patterns.append({
                'type': 'alternating',
                'description': 'Padrão de alternância detectado',
                'impact': 'medium'
            })

        # Análise de cartas altas/baixas
        recent_cards = [max(g['home_card'], g['away_card']) for g in recent]
        high_cards = sum(1 for c in recent_cards if c >= 10)
        
        if high_cards >= 7:
            self.patterns.append({
                'type': 'cards',
                'description': 'Tendência de cartas altas',
                'impact': 'low'
            })

    def generate_recommendation(self):
        """Gera uma recomendação com base nas estatísticas e padrões."""
        if len(self.game_history) < 10:
            self.recommendation = None
            self.confidence = 0
            return

        recent = self.game_history[-10:]
        stats = {
            'home': sum(1 for g in recent if g['result'] == 'HOME'),
            'away': sum(1 for g in recent if g['result'] == 'AWAY'),
            'draw': sum(1 for g in recent if g['result'] == 'DRAW')
        }

        # Lógica de recomendação baseada em padrões
        recommendation = 'DRAW'
        confidence = 50

        # Se há desequilíbrio nas últimas 10 rodadas
        total = len(recent)
        home_perc = (stats['home'] / total) * 100
        away_perc = (stats['away'] / total) * 100
        draw_perc = (stats['draw'] / total) * 100

        if home_perc <= 20:
            recommendation = 'HOME'
            confidence = 75
        elif away_perc <= 20:
            recommendation = 'AWAY'
            confidence = 75
        elif draw_perc <= 10:
            recommendation = 'DRAW'
            confidence = 80

        # Ajustar baseado em sequências
        last_result = recent[-1]['result']
        streak = 1
        for i in range(len(recent) - 2, -1, -1):
            if recent[i]['result'] == last_result:
                streak += 1
            else:
                break
        
        if streak >= 4:
            # Contra a sequência
            if last_result == 'HOME':
                recommendation = 'AWAY' if random.random() > 0.5 else 'DRAW'
            elif last_result == 'AWAY':
                recommendation = 'HOME' if random.random() > 0.5 else 'DRAW'
            else:
                recommendation = 'HOME' if random.random() > 0.5 else 'AWAY'
            confidence = min(85, confidence + 10)

        self.recommendation = recommendation
        self.confidence = confidence

    def add_manual_result(self, home_card, away_card):
        """Adiciona um resultado manual com base nas cartas."""
        try:
            home_card = int(home_card)
            away_card = int(away_card)
        except ValueError:
            print("Erro: As cartas devem ser números inteiros.")
            return

        if not (2 <= home_card <= 14 and 2 <= away_card <= 14):
            print("Erro: Por favor, insira cartas válidas (2-14, onde 14 = Ás).")
            return

        if home_card > away_card:
            result = 'HOME'
        elif away_card > home_card:
            result = 'AWAY'
        else:
            result = 'DRAW'

        new_game = {
            'round': self.current_round,
            'result': result,
            'home_card': home_card,
            'away_card': away_card,
            'timestamp': datetime.now()
        }

        self.game_history.append(new_game)
        self.current_round += 1
        self.update_analysis()
        print(f"Resultado adicionado: Rodada {new_game['round']}, Resultado: {new_game['result']} ({home_card}-{away_card})")

    def add_simulated_result(self, desired_result=None):
        """Adiciona um resultado simulado com cartas aleatórias."""
        home_card = random.randint(2, 14)
        away_card = random.randint(2, 14)

        if home_card > away_card:
            actual_result = 'HOME'
        elif away_card > home_card:
            actual_result = 'AWAY'
        else:
            actual_result = 'DRAW'

        new_game = {
            'round': self.current_round,
            'result': actual_result,
            'home_card': home_card,
            'away_card': away_card,
            'timestamp': datetime.now()
        }
        
        self.game_history.append(new_game)
        self.current_round += 1
        self.update_analysis()
        print(f"Resultado simulado adicionado: Rodada {new_game['round']}, Resultado: {new_game['result']} ({home_card}-{away_card})")


# Exemplo de uso:
if __name__ == "__main__":
    analyzer = FootballStudioAnalyzer()
    analyzer.initialize()

    print("### Analisador de Football Studio em Python ###\n")

    def print_status():
        """Função auxiliar para imprimir o estado atual do analisador."""
        print("--- Status Atual ---")
        print(f"Rodada atual: {analyzer.current_round}")
        print("\nEstatísticas:")
        for key, stats in analyzer.statistics.items():
            print(f"  - {key.upper()}: {stats['wins']} vitórias ({stats['percentage']}%)")
        
        print("\nPadrões Detectados:")
        if analyzer.patterns:
            for pattern in analyzer.patterns:
                print(f"  - {pattern['description']} (Impacto: {pattern['impact']})")
        else:
            print("  Nenhum padrão significativo detectado.")

        print(f"\nRecomendação IA: {analyzer.recommendation or 'N/A'} (Confiança: {analyzer.confidence}%)")
        print("--------------------\n")

    print_status()

    # Demonstração do modo manual
    print("--- Modo Manual ---")
    analyzer.add_manual_result(10, 7) # Simula HOME
    print_status()

    analyzer.add_manual_result(3, 13) # Simula AWAY (Rei)
    print_status()
    
    # Demonstração do modo de simulação
    print("--- Modo Simulação ---")
    for _ in range(5):
        analyzer.add_simulated_result()
        print_status()
        time.sleep(1) # Aguarda 1 segundo para simular o tempo entre rodadas
    
    print("\nAnálise completa. Fim da demonstração.")

