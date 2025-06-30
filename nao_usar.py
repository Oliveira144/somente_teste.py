import json
import os
from collections import deque
import math # Importar o módulo math para funções como sin

class FootballStudioAnalyzer:
    def __init__(self, history_file='football_studio_history.json', weights_file='neural_weights.json'):
        self.history_file = history_file
        self.weights_file = weights_file
        self.history = self._load_history()
        self.stats = self._calculate_stats()
        self.hot_streak = {'type': None, 'count': 0}
        self.neural_weights = self._load_weights()
        self.ai_prediction = None
        self.game_phase = 'AQUECIMENTO'

        # Cores (apenas para referência, não usadas na lógica Python de console)
        self.colors = {
            'home': '#DC2626', 'away': '#2563EB', 'tie': '#F59E0B',
            'bg': '#0F172A', 'card': '#1E293B', 'success': '#10B981',
            'danger': '#EF4444', 'warning': '#F59E0B', 'g1': '#8B5CF6'
        }

    def _load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Erro ao carregar histórico. Criando um novo.")
                return []
        return []

    def _save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f)

    def _load_weights(self):
        if os.path.exists(self.weights_file):
            try:
                with open(self.weights_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Erro ao carregar pesos. Usando padrão.")
                pass # Fallback to default weights below
        
        # Default weights
        return {
            'sequence': 0.35,
            'alternation': 0.25,
            'fibonacci': 0.20,
            'gravitation': 0.30,
            'quantum': 0.40,
            'momentum': 0.45,
            'chaos': 0.15,
            'marketMaker': 0.30,
            'timeWave': 0.35,
            'neuralNetwork': 0.50,
            'hotStreakBreak': 0.60
        }

    def _save_weights(self):
        with open(self.weights_file, 'w') as f:
            json.dump(self.neural_weights, f)

    def _calculate_stats(self):
        stats = {'home': 0, 'away': 0, 'tie': 0}
        for res in self.history:
            stats[res] += 1
        return stats

    def add_result(self, result):
        if result not in ['home', 'away', 'tie']:
            print("Resultado inválido. Use 'home', 'away' ou 'tie'.")
            return

        self.history.insert(0, result) # Adiciona no início (mais recente)
        self._update_hot_streak(result)
        self.stats[result] += 1
        self._save_history()
        self.perform_deep_analysis()

    def undo_last(self):
        if self.history:
            last_result = self.history.pop(0)
            self.stats[last_result] -= 1
            self._update_hot_streak(self.history[0] if self.history else None)
            self._save_history()
            self.perform_deep_analysis()
        else:
            print("Histórico vazio, nada para desfazer.")

    def clear_history(self):
        self.history = []
        self.stats = {'home': 0, 'away': 0, 'tie': 0}
        self.hot_streak = {'type': None, 'count': 0}
        self.ai_prediction = None
        self.game_phase = 'ANÁLISE'
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
        print("Histórico limpo.")

    def _update_hot_streak(self, current_result):
        if len(self.history) >= 2 and self.history[0] == self.history[1]:
            if self.hot_streak['type'] == self.history[0]:
                self.hot_streak['count'] += 1
            else:
                self.hot_streak = {'type': self.history[0], 'count': 2}
        else:
            self.hot_streak = {'type': None, 'count': 0}

    def _get_result_text(self, result):
        mapping = {'home': 'CASA', 'away': 'FORA', 'tie': 'EMPATE'}
        return mapping.get(result, 'N/A')

    # --- Algoritmos de Análise ---

    def analyze_sequences(self):
        if not self.history:
            return {'current': 0, 'type': None}
        current = 1
        for i in range(1, len(self.history)):
            if self.history[i] == self.history[0]:
                current += 1
            else:
                break
        return {'current': current, 'type': self.history[0]}

    def analyze_alternation(self):
        if len(self.history) < 2:
            return {'strength': 'baixa'}
        alternations = 0
        limit = min(len(self.history), 10)
        for i in range(1, limit):
            if self.history[i] != self.history[i-1]:
                alternations += 1
        ratio = alternations / (limit - 1) if limit > 1 else 0
        if ratio > 0.7:
            return {'strength': 'alta'}
        elif ratio > 0.4:
            return {'strength': 'média'}
        else:
            return {'strength': 'baixa'}

    def analyze_fibonacci(self):
        counts = {'home': 0, 'away': 0, 'tie': 0}
        relevant_history = self.history[:min(len(self.history), 13)]
        for r in relevant_history:
            counts[r] += 1
        
        sorted_counts = sorted([c for c in counts.values() if c > 0], reverse=True)
        fibonacci_detected = 'nao detectado'
        if len(sorted_counts) >= 2 and sorted_counts[1] > 0:
            ratio = sorted_counts[0] / sorted_counts[1]
            if (1.5 < ratio < 1.7) or (0.6 < ratio < 0.65): # Aproximação de Phi ou 1/Phi
                fibonacci_detected = 'detectado'
        return {'strength': fibonacci_detected}

    def analyze_gravitation(self):
        relevant_history = self.history[:min(len(self.history), 20)]
        counts = {'home': 0, 'away': 0, 'tie': 0}
        for r in relevant_history:
            counts[r] += 1

        if not relevant_history:
            return {'pull': None, 'strength': 0}

        least_frequent = min(counts, key=counts.get)
        # Strength: difference between average and actual count, scaled
        strength = min(100, (len(relevant_history) / 3 - counts[least_frequent]) * 10)
        return {'pull': least_frequent, 'strength': strength}

    def analyze_quantum_state(self):
        relevant_history = self.history[:min(len(self.history), 15)]
        home_score = 0
        away_score = 0
        tie_score = 0

        for i, result in enumerate(relevant_history):
            weight = 1 - (i / len(relevant_history)) if len(relevant_history) > 0 else 0
            if result == 'home':
                home_score += weight
            elif result == 'away':
                away_score += weight
            else:
                tie_score += weight

        total_score = home_score + away_score + tie_score
        if total_score == 0:
            return {'coherence': 'baixa', 'nextCollapse': None}

        home_prob = home_score / total_score
        away_prob = away_score / total_score
        tie_prob = tie_score / total_score

        coherence = 'alta' if max(home_prob, away_prob, tie_prob) > 0.55 else 'baixa'

        next_collapse = 'tie'
        if home_prob > away_prob and home_prob > tie_prob:
            next_collapse = 'home'
        elif away_prob > home_prob and away_prob > tie_prob:
            next_collapse = 'away'

        return {'state': [home_prob, away_prob, tie_prob], 'coherence': coherence, 'nextCollapse': next_collapse}

    def analyze_momentum(self):
        relevant_history = self.history[:min(len(self.history), 10)]
        momentum_score = 0

        for i, result in enumerate(relevant_history):
            weight = (len(relevant_history) - i) / len(relevant_history) if len(relevant_history) > 0 else 0
            if result == 'home':
                momentum_score += weight
            elif result == 'away':
                momentum_score -= weight
        
        direction = 'neutral'
        strength = 'fraca'

        if momentum_score > 1.5:
            direction = 'home'
            strength = 'forte'
        elif momentum_score > 0.5:
            direction = 'home'
            strength = 'média'
        elif momentum_score < -1.5:
            direction = 'away'
            strength = 'forte'
        elif momentum_score < -0.5:
            direction = 'away'
            strength = 'média'

        return {'direction': direction, 'strength': strength, 'value': momentum_score}

    def analyze_chaos_theory(self):
        relevant_history = self.history[:min(len(self.history), 20)]
        butterfly_effect = False
        attractor_strength = 0

        if len(relevant_history) >= 7:
            last_seven = relevant_history[:7]
            # Simple "butterfly" logic: a tie in the middle, followed by strong trends
            if last_seven[3] == 'tie':
                pre_tie_trend_home = sum(1 for r in last_seven[4:7] if r == 'home') >= 2
                pre_tie_trend_away = sum(1 for r in last_seven[4:7] if r == 'away') >= 2
                post_tie_trend_home = sum(1 for r in last_seven[:3] if r == 'home') >= 2
                post_tie_trend_away = sum(1 for r in last_seven[:3] if r == 'away') >= 2
                if (pre_tie_trend_home and post_tie_trend_away) or \
                   (pre_tie_trend_away and post_tie_trend_home):
                    butterfly_effect = True

        for result in relevant_history:
            if result == 'home':
                attractor_strength += 1
            elif result == 'away':
                attractor_strength -= 1
        
        prediction = 'tie'
        if attractor_strength > 0: # If more home, chaos theory might predict away to balance
            prediction = 'away'
        elif attractor_strength < 0: # If more away, predict home
            prediction = 'home'

        return {
            'butterfly': butterfly_effect,
            'attractor': 'forte' if abs(attractor_strength) > 5 else 'fraco',
            'prediction': prediction
        }

    def run_neural_network(self):
        relevant_history = self.history[:min(len(self.history), 30)]
        if len(relevant_history) < 5:
            return {'prediction': 'tie', 'confidence': 0, 'outputs': [0, 0, 0], 'activations': 0}

        home_score = 0
        away_score = 0
        tie_score = 0

        for i, result in enumerate(relevant_history):
            recency_weight = (len(relevant_history) - i) / len(relevant_history)
            
            # Simple trend check for first 5
            trend_weight = 1
            if i < 5:
                recent_five = relevant_history[:5]
                if all(r == result for r in recent_five):
                    trend_weight = 2 # Boost for very strong recent trends
            
            # Alternation check
            alternation_weight = 1
            if i > 0 and relevant_history[i] != relevant_history[i-1]:
                alternation_weight = 1.5

            if result == 'home':
                home_score += (recency_weight * trend_weight * alternation_weight)
            elif result == 'away':
                away_score += (recency_weight * trend_weight * alternation_weight)
            else: # tie
                tie_score += (recency_weight * trend_weight * alternation_weight * 0.7) # Empate ligeiramente menor peso

        # Analysis of "gaps" or imbalances across the full history
        total_count = len(self.history)
        if total_count > 0:
            home_freq = self.stats['home'] / total_count
            away_freq = self.stats['away'] / total_count
            tie_freq = self.stats['tie'] / total_count

            target_freq = 1 / 3
            home_score += (target_freq - home_freq) * 5
            away_score += (target_freq - away_freq) * 5
            tie_score += (target_freq - tie_freq) * 5 * 0.5
        
        sum_scores = home_score + away_score + tie_score
        if sum_scores == 0: # Avoid division by zero
            return {'prediction': 'tie', 'confidence': 0, 'outputs': [0, 0, 0], 'activations': 0}

        outputs = [home_score / sum_scores, away_score / sum_scores, tie_score / sum_scores]

        max_output = max(outputs)
        max_index = outputs.index(max_output)
        
        prediction_map = {0: 'home', 1: 'away', 2: 'tie'}
        prediction = prediction_map[max_index]
        confidence = max_output * 100

        return {'prediction': prediction, 'confidence': confidence, 'outputs': outputs, 'activations': len(relevant_history)}

    def analyze_market_maker(self):
        recent_results = self.history[:min(len(self.history), 6)]
        home_freq = recent_results.count('home')
        away_freq = recent_results.count('away')
        tie_freq = recent_results.count('tie')

        total = len(recent_results)
        if total == 0:
            return {'direction': 'tie', 'deficit': 0, 'confidence': 0}

        expected_each = total / 3

        home_deficit = expected_each - home_freq
        away_deficit = expected_each - away_freq
        tie_deficit = expected_each - tie_freq

        market_direction = 'tie'
        max_deficit = 0

        if home_deficit > max_deficit:
            max_deficit = home_deficit
            market_direction = 'home'
        if away_deficit > max_deficit:
            max_deficit = away_deficit
            market_direction = 'away'
        if tie_deficit > max_deficit: # Tie gets priority if deficit is equal
            max_deficit = tie_deficit
            market_direction = 'tie'

        return {
            'direction': market_direction,
            'deficit': max_deficit,
            'confidence': min(100, max_deficit * 30)
        }

    def analyze_time_wave(self):
        relevant_history = self.history[:min(len(self.history), 25)]
        if len(relevant_history) < 5:
            return {'amplitude': 0, 'phase': 0, 'nextWave': 'tie', 'strength': 'baixa'}

        wave_sum = 0
        amplitude_sum = 0
        period_dominance = {'home': 0, 'away': 0, 'tie': 0}

        for i, result in enumerate(relevant_history):
            result_value = 0
            if result == 'home':
                result_value = 1
            elif result == 'away':
                result_value = -1

            # Adaptive sinusoidal wave weight
            wave_weight = math.sin((i * math.pi) / (len(relevant_history) / 2 + 1e-9)) + 1
            
            wave_sum += result_value * wave_weight
            amplitude_sum += abs(result_value * wave_weight)

            # Analyze periodicity in short periods (last 5)
            if i < 5:
                period_dominance[result] += 1

        amplitude = amplitude_sum / len(relevant_history)
        phase = wave_sum

        next_wave = 'tie'
        if phase > 2:
            next_wave = 'away'
        elif phase < -2:
            next_wave = 'home'
        elif phase > 0.5:
            next_wave = 'away'
        elif phase < -0.5:
            next_wave = 'home'

        # Override based on strong periodicity in last 5
        if period_dominance['home'] >= 4:
            next_wave = 'away'
        if period_dominance['away'] >= 4:
            next_wave = 'home'

        return {
            'amplitude': amplitude,
            'phase': phase,
            'nextWave': next_wave,
            'strength': 'alta' if amplitude > 0.8 else 'média'
        }

    def perform_deep_analysis(self):
        if len(self.history) < 5:
            self.ai_prediction = None
            self.game_phase = 'AQUECIMENTO'
            return

        analysis = {
            'sequences': self.analyze_sequences(),
            'alternation': self.analyze_alternation(),
            'fibonacci': self.analyze_fibonacci(),
            'gravitation': self.analyze_gravitation(),
            'quantum': self.analyze_quantum_state(),
            'momentum': self.analyze_momentum(),
            'chaos': self.analyze_chaos_theory(),
            'neuralNetwork': self.run_neural_network(),
            'marketMaker': self.analyze_market_maker(),
            'timeWave': self.analyze_time_wave()
        }

        self.ai_prediction = self.generate_g1_prediction(analysis)
        self.determine_game_phase(analysis)

    def generate_g1_prediction(self, analysis):
        predictions = []
        debug_reasons = []

        # Collect predictions with dynamic weights
        # CORREÇÃO APLICADA AQUI: Adicionado ':' no final da linha 'if analysis['neuralNetwork']['confidence'] > 50'
        if analysis['neuralNetwork']['confidence'] > 50:
            predictions.append({
                'source': 'Neural Network',
                'prediction': analysis['neuralNetwork']['prediction'],
                'weight': self.neural_weights['neuralNetwork'] * (analysis['neuralNetwork']['confidence'] / 100),
                'confidence': analysis['neuralNetwork']['confidence']
            })
            debug_reasons.append(f"NN ({analysis['neuralNetwork']['confidence']:.0f}%) -> {analysis['neuralNetwork']['prediction']}")

        if analysis['momentum']['strength'] == 'forte':
            predictions.append({
                'source': 'Momentum',
                'prediction': analysis['momentum']['direction'],
                'weight': self.neural_weights['momentum'],
                'confidence': 75
            })
            debug_reasons.append(f"Momentum (Forte) -> {analysis['momentum']['direction']}")
        elif analysis['momentum']['strength'] == 'média':
            predictions.append({
                'source': 'Momentum',
                'prediction': analysis['momentum']['direction'],
                'weight': self.neural_weights['momentum'] * 0.7,
                'confidence': 60
            })
            debug_reasons.append(f"Momentum (Média) -> {analysis['momentum']['direction']}")

        if analysis['quantum']['coherence'] == 'alta' and analysis['quantum']['nextCollapse']:
            predictions.append({
                'source': 'Quantum State',
                'prediction': analysis['quantum']['nextCollapse'],
                'weight': self.neural_weights['quantum'],
                'confidence': 70
            })
            debug_reasons.append(f"Quantum (Alta) -> {analysis['quantum']['nextCollapse']}")

        if analysis['marketMaker']['confidence'] > 60:
            predictions.append({
                'source': 'Market Maker',
                'prediction': analysis['marketMaker']['direction'],
                'weight': self.neural_weights['marketMaker'] * (analysis['marketMaker']['confidence'] / 100),
                'confidence': analysis['marketMaker']['confidence']
            })
            debug_reasons.append(f"Market Maker ({analysis['marketMaker']['confidence']:.0f}%) -> {analysis['marketMaker']['direction']}")

        if analysis['timeWave']['strength'] == 'alta':
            predictions.append({
                'source': 'Time Wave',
                'prediction': analysis['timeWave']['nextWave'],
                'weight': self.neural_weights['timeWave'],
                'confidence': 65
            })
            debug_reasons.append(f"Time Wave (Alta) -> {analysis['timeWave']['nextWave']}")
        elif analysis['timeWave']['strength'] == 'média':
            predictions.append({
                'source': 'Time Wave',
                'prediction': analysis['timeWave']['nextWave'],
                'weight': self.neural_weights['timeWave'] * 0.7,
                'confidence': 50
            })
            debug_reasons.append(f"Time Wave (Média) -> {analysis['timeWave']['nextWave']}")
        
        # Strong sequence pattern
        if analysis['sequences']['current'] >= 3:
            predictions.append({
                'source': 'Sequência',
                'prediction': analysis['sequences']['type'],
                'weight': self.neural_weights['sequence'] * (analysis['sequences']['current'] / 5),
                'confidence': 50 + (analysis['sequences']['current'] * 5)
            })
            debug_reasons.append(f"Sequência ({analysis['sequences']['current']}x) -> {analysis['sequences']['type']}")

        # Gravitation
        if analysis['gravitation']['strength'] > 50:
            predictions.append({
                'source': 'Gravitação',
                'prediction': analysis['gravitation']['pull'],
                'weight': self.neural_weights['gravitation'] * (analysis['gravitation']['strength'] / 100),
                'confidence': analysis['gravitation']['strength']
            })
            debug_reasons.append(f"Gravitação ({analysis['gravitation']['strength']:.0f}%) -> {analysis['gravitation']['pull']}")

        # Hot streak override
        override_message = None
        if self.hot_streak['count'] >= 3:
            opposite = {'home': 'away', 'away': 'home', 'tie': 'tie'}.get(self.hot_streak['type'], 'tie')
            
            streak_weight = self.neural_weights['hotStreakBreak'] + (self.hot_streak['count'] - 3) * 0.1
            streak_confidence = min(99, 80 + (self.hot_streak['count'] * 5))

            predictions.append({
                'source': 'Hot Streak Break',
                'prediction': opposite,
                'weight': streak_weight,
                'confidence': streak_confidence
            })
            override_message = f"QUEBRA DE SEQUÊNCIA ({self.hot_streak['count']}x {self._get_result_text(self.hot_streak['type'])}) - Aposte no {self._get_result_text(opposite)}"
            debug_reasons.append(f"HOT STREAK BREAK ({self.hot_streak['count']}x) -> {opposite}")

        # Final consolidation
        votes = {'home': 0, 'away': 0, 'tie': 0}
        total_weight = 0

        for pred in predictions:
            votes[pred['prediction']] += pred['weight']
            total_weight += pred['weight']

        if total_weight == 0:
            return {'prediction': 'tie', 'confidence': 0, 'grade': 'C', 'sources': 0, 'reasoning': [], 'override': None}

        winner = max(votes, key=votes.get)
        final_confidence = (votes[winner] / total_weight) * 100

        # Adjust confidence based on number of sources and vote dispersion
        if len(predictions) < 3:
            final_confidence *= 0.7
        # Check for close votes (e.g., if difference between top two is less than 10% of total weight)
        sorted_votes = sorted(votes.values(), reverse=True)
        if len(sorted_votes) >= 2 and total_weight > 0 and (sorted_votes[0] - sorted_votes[1]) < (total_weight * 0.1):
            final_confidence *= 0.8
        
        final_confidence = min(99.9, max(0, final_confidence))

        grade = 'C'
        if final_confidence >= 85 and len(predictions) >= 4:
            grade = 'G1'
        elif final_confidence >= 75 and len(predictions) >= 3:
            grade = 'A+'
        elif final_confidence >= 65:
            grade = 'A'
        elif final_confidence >= 50:
            grade = 'B'

        return {
            'prediction': winner,
            'confidence': final_confidence,
            'grade': grade,
            'sources': len(predictions),
            'reasoning': debug_reasons,
            'override': override_message
        }

    def determine_game_phase(self, analysis):
        if len(self.history) < 5:
            self.game_phase = 'AQUECIMENTO'
        elif self.hot_streak['count'] >= 4:
            self.game_phase = 'RUPTURA IMINENTE'
        elif analysis['momentum']['strength'] == 'forte':
            self.game_phase = 'MOMENTUM DE ALTA'
        elif analysis['quantum']['coherence'] == 'alta':
            self.game_phase = 'COMPLEXO QUÂNTICO'
        elif analysis['marketMaker']['confidence'] > 70:
            self.game_phase = 'EQUILÍBRIO MERCADO'
        else:
            self.game_phase = 'ANÁLISE PROFUNDA'

    def set_weight(self, algorithm_name, value):
        if algorithm_name in self.neural_weights and 0 <= value <= 1:
            self.neural_weights[algorithm_name] = value
            self._save_weights()
            print(f"Peso de '{algorithm_name}' ajustado para {value:.2f}. Reanalisando...")
            self.perform_deep_analysis()
        else:
            print(f"Algoritmo '{algorithm_name}' não encontrado ou valor ({value}) inválido (0-1).")

    def reset_weights(self):
        if os.path.exists(self.weights_file):
            os.remove(self.weights_file)
        self.neural_weights = self._load_weights() # Reloads default
        print("Pesos redefinidos para o padrão. Reanalisando...")
        self.perform_deep_analysis()

    def display_status(self):
        print("\n" + "="*50)
        print(f"⚽ FOOTBALL STUDIO AI STATUS")
        print("="*50)
        print(f"Fase do Jogo: {self.game_phase}")
        if self.hot_streak['count'] > 0:
            print(f"🔥 Streak: {self.hot_streak['count']}x {self._get_result_text(self.hot_streak['type'])}")
        print(f"\nHistórico Total: {len(self.history)} resultados")
        print(f"Estatísticas: Casa={self.stats['home']}, Fora={self.stats['away']}, Empate={self.stats['tie']}")
        
        print("\n--- Predição IA ---")
        if self.ai_prediction and self.ai_prediction['confidence'] > 0:
            pred = self.ai_prediction
            print(f"Sugestão G1: {self._get_result_text(pred['prediction'])}")
            print(f"Grau: {pred['grade']} | Confiança: {pred['confidence']:.1f}%")
            print(f"Baseado em {pred['sources']} algoritmos.")
            if pred['override']:
                print(f"⚡ OVERRIDE: {pred['override']}")
            print("Fundamentação:")
            for reason in pred['reasoning']:
                print(f"  - {reason}")
        else:
            print("Aguardando mais dados para uma análise confiável (mín. 5 resultados).")

        print("\n--- Histórico Recente (Top 10) ---")
        if self.history:
            recent_display = [self._get_result_text(r) for r in self.history[:10]]
            print(" -> ".join(recent_display))
        else:
            print("Nenhum resultado ainda.")
        print("="*50)

# --- Exemplo de Uso (no console) ---
if __name__ == "__main__":
    analyzer = FootballStudioAnalyzer()
    
    while True:
        analyzer.display_status()
        print("\nComandos:")
        print("  1. Adicionar resultado (home, away, tie)")
        print("  2. Desfazer último resultado")
        print("  3. Limpar todo o histórico")
        print("  4. Ajustar peso de algoritmo (nome_algoritmo valor_0_a_1)")
        print("  5. Redefinir pesos padrão")
        print("  6. Sair")
        
        command = input("Escolha uma opção: ").strip().lower()

        if command == '1':
            result = input("Digite o resultado (home, away, tie): ").strip().lower()
            analyzer.add_result(result)
        elif command == '2':
            analyzer.undo_last()
        elif command == '3':
            analyzer.clear_history()
        elif command == '4':
            parts = input("Digite o nome do algoritmo e o novo peso (ex: neuralnetwork 0.7): ").strip().split()
            if len(parts) == 2:
                algo_name = parts[0]
                try:
                    weight_value = float(parts[1])
                    analyzer.set_weight(algo_name, weight_value)
                except ValueError:
                    print("Valor do peso inválido. Deve ser um número entre 0 e 1.")
            else:
                print("Formato inválido. Use 'nome_algoritmo valor_0_a_1'.")
        elif command == '5':
            analyzer.reset_weights()
        elif command == '6':
            print("Saindo do analisador.")
            break
        else:
            print("Comando inválido. Tente novamente.")
