import random
import time
from datetime import datetime

class FootballStudioAnalyzer:
    """
    Analisador de jogos de Football Studio.
    Esta classe encapsula a lógica para calcular estatísticas,
    detectar padrões e gerar recomendações com base no histórico de jogos.
    """
    def __init__(self):
        # --- Estado da Análise ---
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

    def _get_result(self, home_card, away_card):
        """Função utilitária para determinar o resultado com base nas cartas."""
        if home_card > away_card:
            return 'HOME'
        if away_card > home_card:
            return 'AWAY'
        return 'DRAW'

    def generate_initial_history(self):
        """
        Gera um histórico inicial de jogos consistente, calculando
        o resultado com base nas cartas.
        Ás = 14, Rei = 13, Dama = 12, Valete = 11.
        """
        raw_history = [
            {'home_card': 8, 'away_card': 14},   # (8, A) -> AWAY
            {'home_card': 4, 'away_card': 9},    # (4, 9) -> AWAY
            {'home_card': 8, 'away_card': 7},    # (8, 7) -> HOME
            {'home_card': 5, 'away_card': 6},    # (5, 6) -> AWAY
            {'home_card': 10, 'away_card': 2},   # (10, 2) -> HOME
            {'home_card': 13, 'away_card': 9},   # (K, 9) -> HOME
            {'home_card': 2, 'away_card': 12},   # (2, Q) -> AWAY
            {'home_card': 5, 'away_card': 9},    # (5, 9) -> AWAY
            {'home_card': 13, 'away_card': 11},  # (K, J) -> HOME
            {'home_card': 4, 'away_card': 13},   # (4, K) -> AWAY
            {'home_card': 13, 'away_card': 12},  # (K, Q) -> HOME
            {'home_card': 14, 'away_card': 5},   # (A, 5) -> HOME
            {'home_card': 14, 'away_card': 7},   # (A, 7) -> HOME
            {'home_card': 2, 'away_card': 14},   # (2, A) -> AWAY
            {'home_card': 2, 'away_card': 8},    # (2, 8) -> AWAY
            {'home_card': 5, 'away_card': 5},    # (5, 5) -> DRAW
            {'home_card': 10, 'away_card': 14},  # (10, A) -> AWAY
            {'home_card': 10, 'away_card': 10},  # (10, 10) -> DRAW
            {'home_card': 12, 'away_card': 6},   # (Q, 6) -> HOME
            {'home_card': 5, 'away_card': 7},    # (5, 7) -> AWAY
        ]

        history_with_details = []
        for i, game in enumerate(raw_history):
            history_with_details.append({
                'round': i + 1,
                'home_card': game['home_card'],
                'away_card': game['away_card'],
                'result': self._get_result(game['home_card'], game['away_card']),
                'timestamp': datetime.now()
            })
        return history_with_details

    def initialize(self):
        """Inicializa o analisador com o histórico de jogos e faz a primeira análise."""
        self.game_history = self.generate_initial_history()
        self.current_round = len(self.game_history) + 1
        self.update_analysis()

    def update_analysis(self):
        """
        Recalcula todas as análises (estatísticas, padrões e recomendação)
        com base no histórico de jogos atual.
        """
        self._calculate_statistics()
        self._analyze_patterns()
        self._generate_recommendation()

    def _calculate_statistics(self):
        """Calcula as estatísticas de vitórias para HOME, AWAY e DRAW."""
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

    def _analyze_patterns(self):
        """Analisa o histórico recente em busca de padrões."""
        self.patterns = []
        if len(self.game_history) < 5:
            return

        recent = self.game_history[-10:]

        # Padrão de Sequência (Streak)
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
                    'impact': 'high' if current_streak >= 4 else 'medium'
                })

        # Padrão de Alternância
        alternating = recent[-6:]
        is_alternating = all(alternating[i]['result'] != alternating[i-1]['result'] for i in range(1, len(alternating)))
        if len(alternating) >= 2 and is_alternating:
            self.patterns.append({
                'type': 'alternating',
                'description': 'Padrão de alternância detectado',
                'impact': 'medium'
            })

        # Padrão de Cartas Altas/Baixas
        high_cards_count = sum(1 for g in recent if max(g['home_card'], g['away_card']) >= 10)
        if high_cards_count >= 7:
            self.patterns.append({
                'type': 'cards',
                'description': 'Tendência de cartas altas',
                'impact': 'low'
            })

    def _generate_recommendation(self):
        """Gera uma recomendação de aposta com base nos padrões e estatísticas."""
        self.recommendation = None
        self.confidence = 0
        if len(self.game_history) < 10:
            return

        recent = self.game_history[-10:]
        recent_stats = {
            'home': sum(1 for g in recent if g['result'] == 'HOME'),
            'away': sum(1 for g in recent if g['result'] == 'AWAY'),
            'draw': sum(1 for g in recent if g['result'] == 'DRAW')
        }

        # 1. Lógica baseada na frequência recente (sugerir o menos frequente)
        sorted_by_freq = sorted(recent_stats.items(), key=lambda item: item[1])
        least_frequent_bet = sorted_by_freq[0][0].upper()
        
        # Define uma confiança inicial com base na diferença de frequência
        least_freq_count = sorted_by_freq[0][1]
        most_freq_count = sorted_by_freq[-1][1]
        confidence_base = 50 + (most_freq_count - least_freq_count) * 5

        # 2. Ajuste com base nos padrões
        high_impact_pattern = next((p for p in self.patterns if p['impact'] == 'high'), None)
        if high_impact_pattern and 'Sequência' in high_impact_pattern['description']:
            # Se houver uma sequência forte, recomenda-se quebrar a sequência
            last_result = recent[-1]['result']
            if last_result.upper() == 'HOME':
                self.recommendation = 'AWAY'
            elif last_result.upper() == 'AWAY':
                self.recommendation = 'HOME'
            else: # Se a sequência for de empates
                self.recommendation = 'HOME' if random.random() > 0.5 else 'AWAY'
            self.confidence = 90
            return # A lógica da sequência é prioritária

        # 3. Se não houver sequência forte, usa a recomendação de frequência
        self.recommendation = least_frequent_bet
        self.confidence = min(100, max(50, confidence_base)) # Limita a confiança entre 50 e 100

    def add_manual_result(self, home_card, away_card):
        """Adiciona um resultado manual fornecendo as cartas."""
        try:
            home_card = int(home_card)
            away_card = int(away_card)
        except ValueError:
            print("Erro: As cartas devem ser números inteiros.")
            return

        if not (2 <= home_card <= 14 and 2 <= away_card <= 14):
            print("Erro: Insira cartas válidas (2-14, onde 14 = Ás).")
            return

        result = self._get_result(home_card, away_card)

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
        print(f"✅ Resultado adicionado: Rodada {new_game['round']}, Resultado: {new_game['result']} ({home_card}-{away_card})")

    def add_simulated_result(self):
        """Adiciona um resultado simulado com cartas aleatórias."""
        home_card = random.randint(2, 14)
        away_card = random.randint(2, 14)
        
        result = self._get_result(home_card, away_card)

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
        print(f"🎲 Resultado simulado adicionado: Rodada {new_game['round']}, Resultado: {new_game['result']} ({home_card}-{away_card})")
        
    def display_status(self):
        """Imprime o status atual do analisador no console."""
        print("\n" + "="*40)
        print("### Football Studio Analyzer Status ###")
        print("="*40)
        print(f"Total de Jogos Analisados: {len(self.game_history)}")
        print(f"Próxima Rodada: {self.current_round}")
        
        print("\n--- Estatísticas ---")
        for key, stats in self.statistics.items():
            print(f"  - {key.upper()}: {stats['wins']} vitórias ({stats['percentage']}%)")
        
        print("\n--- Padrões Detectados ---")
        if self.patterns:
            for pattern in self.patterns:
                print(f"  - {pattern['description']} (Impacto: {pattern['impact'].upper()})")
        else:
            print("  Nenhum padrão significativo detectado.")

        print("\n--- Recomendação de Aposta ---")
        if self.recommendation:
            print(f"  Recomendação: {self.recommendation}")
            print(f"  Confiança: {self.confidence}%")
        else:
            print("  Analisando dados... Jogue mais para gerar uma recomendação.")
        print("="*40 + "\n")

# --- Exemplo de Uso ---
if __name__ == "__main__":
    analyzer = FootballStudioAnalyzer()
    analyzer.initialize()

    print("Bem-vindo ao Analisador de Football Studio!\n")
    
    # Exibe o status inicial
    analyzer.display_status()

    # Demonstração do modo manual
    print("--- DEMONSTRAÇÃO DO MODO MANUAL ---")
    while True:
        home_input = input("Insira a carta HOME (2-14) ou 's' para simular ou 'q' para sair: ")
        if home_input.lower() == 'q':
            break
        if home_input.lower() == 's':
            print("\n--- MODO SIMULAÇÃO ATIVADO ---")
            break

        away_input = input("Insira a carta AWAY (2-14): ")
        
        analyzer.add_manual_result(home_input, away_input)
        analyzer.display_status()

    # Demonstração do modo de simulação
    print("\n--- DEMONSTRAÇÃO DO MODO DE SIMULAÇÃO ---")
    print("Adicionando 5 resultados aleatórios...")
    for i in range(5):
        analyzer.add_simulated_result()
        analyzer.display_status()
        time.sleep(1) # Aguarda 1 segundo para simular o tempo real

    print("Demonstração concluída. Obrigado por usar o analisador!")

