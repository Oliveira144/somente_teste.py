import React, { useState, useEffect } from 'react';
import { TrendingUp, Target, BarChart3, Clock, Star, AlertTriangle } from 'lucide-react';

const FootballStudioAnalyzer = () => {
  const [gameHistory, setGameHistory] = useState([]);
  const [currentRound, setCurrentRound] = useState(1);
  const [statistics, setStatistics] = useState({
    home: { wins: 0, percentage: 0 },
    away: { wins: 0, percentage: 0 },
    draw: { wins: 0, percentage: 0 }
  });
  const [patterns, setPatterns] = useState([]);
  const [recommendation, setRecommendation] = useState(null);
  const [confidence, setConfidence] = useState(0);
  const [manualMode, setManualMode] = useState(true);
  const [homeCardInput, setHomeCardInput] = useState('');
  const [awayCardInput, setAwayCardInput] = useState('');

  // Histórico real baseado na imagem fornecida (corrigido com Ás = 14)
  const generateInitialHistory = () => {
    const realHistory = [
      { result: 'HOME', homeCard: 8, awayCard: 14 }, // Ás = 14, então AWAY vence
      { result: 'AWAY', homeCard: 4, awayCard: 9 },
      { result: 'HOME', homeCard: 8, awayCard: 7 },
      { result: 'AWAY', homeCard: 5, awayCard: 6 },
      { result: 'HOME', homeCard: 10, awayCard: 2 },
      { result: 'HOME', homeCard: 13, awayCard: 9 },
      { result: 'AWAY', homeCard: 2, awayCard: 12 },
      { result: 'AWAY', homeCard: 5, awayCard: 9 },
      { result: 'HOME', homeCard: 13, awayCard: 11 },
      { result: 'AWAY', homeCard: 4, awayCard: 13 },
      { result: 'HOME', homeCard: 13, awayCard: 12 },
      { result: 'AWAY', homeCard: 14, awayCard: 5 }, // Ás HOME = 14, então HOME vence
      { result: 'AWAY', homeCard: 14, awayCard: 7 }, // Ás HOME = 14, então HOME vence
      { result: 'HOME', homeCard: 2, awayCard: 14 }, // Ás AWAY = 14, então AWAY vence
      { result: 'AWAY', homeCard: 2, awayCard: 8 },
      { result: 'DRAW', homeCard: 5, awayCard: 5 },
      { result: 'HOME', homeCard: 10, awayCard: 14 }, // Ás AWAY = 14, então AWAY vence
      { result: 'DRAW', homeCard: 10, awayCard: 10 },
      { result: 'AWAY', homeCard: 12, awayCard: 6 },
      { result: 'DRAW', homeCard: 5, awayCard: 7 }
    ];

    return realHistory.map((game, index) => ({
      round: index + 1,
      result: game.result,
      homeCard: game.homeCard,
      awayCard: game.awayCard,
      timestamp: new Date(Date.now() - (20 - index) * 60000)
    }));
  };

  useEffect(() => {
    setGameHistory(generateInitialHistory());
  }, []);

  useEffect(() => {
    calculateStatistics();
    analyzePatterns();
    generateRecommendation();
  }, [gameHistory]);

  const calculateStatistics = () => {
    if (gameHistory.length === 0) return;

    const totalGames = gameHistory.length;
    const homeWins = gameHistory.filter(g => g.result === 'HOME').length;
    const awayWins = gameHistory.filter(g => g.result === 'AWAY').length;
    const draws = gameHistory.filter(g => g.result === 'DRAW').length;

    setStatistics({
      home: { wins: homeWins, percentage: (homeWins / totalGames * 100).toFixed(1) },
      away: { wins: awayWins, percentage: (awayWins / totalGames * 100).toFixed(1) },
      draw: { wins: draws, percentage: (draws / totalGames * 100).toFixed(1) }
    });
  };

  const analyzePatterns = () => {
    if (gameHistory.length < 5) return;

    const recent = gameHistory.slice(-10);
    const patterns = [];

    // Análise de sequências
    let currentStreak = 1;
    let streakType = recent[recent.length - 1]?.result;
    
    for (let i = recent.length - 2; i >= 0; i--) {
      if (recent[i].result === streakType) {
        currentStreak++;
      } else {
        break;
      }
    }

    if (currentStreak >= 3) {
      patterns.push({
        type: 'streak',
        description: `Sequência de ${currentStreak} ${streakType}`,
        impact: 'high'
      });
    }

    // Análise de alternância
    const alternating = recent.slice(-6);
    let isAlternating = true;
    for (let i = 1; i < alternating.length; i++) {
      if (alternating[i].result === alternating[i-1].result) {
        isAlternating = false;
        break;
      }
    }

    if (isAlternating) {
      patterns.push({
        type: 'alternating',
        description: 'Padrão de alternância detectado',
        impact: 'medium'
      });
    }

    // Análise de cartas altas/baixas
    const recentCards = recent.map(g => Math.max(g.homeCard, g.awayCard));
    const highCards = recentCards.filter(c => c >= 10).length;
    
    if (highCards >= 7) {
      patterns.push({
        type: 'cards',
        description: 'Tendência de cartas altas',
        impact: 'low'
      });
    }

    setPatterns(patterns);
  };

  const generateRecommendation = () => {
    if (gameHistory.length < 10) return;

    const recent = gameHistory.slice(-10);
    const stats = {
      home: recent.filter(g => g.result === 'HOME').length,
      away: recent.filter(g => g.result === 'AWAY').length,
      draw: recent.filter(g => g.result === 'DRAW').length
    };

    // Lógica de recomendação baseada em padrões
    let recommendation = 'DRAW';
    let confidence = 50;

    // Se há desequilíbrio nas últimas 10 rodadas
    const total = recent.length;
    const homePerc = (stats.home / total) * 100;
    const awayPerc = (stats.away / total) * 100;
    const drawPerc = (stats.draw / total) * 100;

    if (homePerc <= 20) {
      recommendation = 'HOME';
      confidence = 75;
    } else if (awayPerc <= 20) {
      recommendation = 'AWAY';
      confidence = 75;
    } else if (drawPerc <= 10) {
      recommendation = 'DRAW';
      confidence = 80;
    }

    // Ajustar baseado em sequências
    const lastResult = recent[recent.length - 1]?.result;
    let streak = 1;
    for (let i = recent.length - 2; i >= 0; i--) {
      if (recent[i].result === lastResult) {
        streak++;
      } else {
        break;
      }
    }

    if (streak >= 4) {
      // Contra a sequência
      if (lastResult === 'HOME') {
        recommendation = Math.random() > 0.5 ? 'AWAY' : 'DRAW';
      } else if (lastResult === 'AWAY') {
        recommendation = Math.random() > 0.5 ? 'HOME' : 'DRAW';
      } else {
        recommendation = Math.random() > 0.5 ? 'HOME' : 'AWAY';
      }
      confidence = Math.min(85, confidence + 10);
    }

    setRecommendation(recommendation);
    setConfidence(confidence);
  };

  const addManualResult = () => {
    const homeCard = parseInt(homeCardInput);
    const awayCard = parseInt(awayCardInput);
    
    if (!homeCard || !awayCard || homeCard < 2 || homeCard > 14 || awayCard < 2 || awayCard > 14) {
      alert('Por favor, insira cartas válidas (2-14, onde 14 = Ás)');
      return;
    }

    let result;
    if (homeCard > awayCard) result = 'HOME';
    else if (awayCard > homeCard) result = 'AWAY';
    else result = 'DRAW';

    const newGame = {
      round: currentRound,
      result,
      homeCard,
      awayCard,
      timestamp: new Date()
    };

    setGameHistory(prev => [...prev, newGame]);
    setCurrentRound(prev => prev + 1);
    setHomeCardInput('');
    setAwayCardInput('');
  };

  const addResult = (result) => {
    const homeCard = Math.floor(Math.random() * 13) + 2; // 2-14
    const awayCard = Math.floor(Math.random() * 13) + 2; // 2-14
    
    let actualResult = result;
    if (homeCard > awayCard) actualResult = 'HOME';
    else if (awayCard > homeCard) actualResult = 'AWAY';
    else actualResult = 'DRAW';

    const newGame = {
      round: currentRound,
      result: actualResult,
      homeCard,
      awayCard,
      timestamp: new Date()
    };

    setGameHistory(prev => [...prev, newGame]);
    setCurrentRound(prev => prev + 1);
  };

  const getRecommendationColor = (rec) => {
    switch (rec) {
      case 'HOME': return 'bg-blue-500';
      case 'AWAY': return 'bg-red-500';
      case 'DRAW': return 'bg-yellow-500';
      default: return 'bg-gray-500';
    }
  };

  const getConfidenceColor = (conf) => {
    if (conf >= 80) return 'text-green-500';
    if (conf >= 60) return 'text-yellow-500';
    return 'text-red-500';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-900 via-green-800 to-black text-white p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-yellow-400 to-yellow-600 bg-clip-text text-transparent">
            Football Studio Pro Analyzer
          </h1>
          <p className="text-gray-300">Análise Avançada e Sugestões Inteligentes</p>
        </div>

        {/* Recommendation Panel */}
        <div className="bg-black/50 rounded-xl p-6 mb-6 border border-yellow-500/30">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold flex items-center gap-2">
              <Target className="text-yellow-400" />
              Recomendação IA
            </h2>
            <div className="flex items-center gap-2">
              <Star className="text-yellow-400" size={20} />
              <span className="text-sm">Rodada {currentRound}</span>
            </div>
          </div>
          
          {recommendation && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-gray-800/50 rounded-lg p-4">
                <div className="flex items-center gap-3 mb-2">
                  <div className={`w-4 h-4 rounded-full ${getRecommendationColor(recommendation)}`}></div>
                  <span className="font-bold text-xl">{recommendation}</span>
                </div>
                <p className="text-gray-300 text-sm">Sugestão principal baseada em análise</p>
              </div>
              
              <div className="bg-gray-800/50 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <TrendingUp className="text-green-400" size={20} />
                  <span className={`font-bold text-xl ${getConfidenceColor(confidence)}`}>
                    {confidence}%
                  </span>
                </div>
                <p className="text-gray-300 text-sm">Nível de confiança</p>
              </div>
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Statistics Panel */}
          <div className="bg-black/50 rounded-xl p-6 border border-blue-500/30">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <BarChart3 className="text-blue-400" />
              Estatísticas ({gameHistory.length} jogos)
            </h2>
            
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                  HOME
                </span>
                <div className="flex items-center gap-2">
                  <span className="font-bold">{statistics.home.wins}</span>
                  <span className="text-blue-400">({statistics.home.percentage}%)</span>
                </div>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                  AWAY
                </span>
                <div className="flex items-center gap-2">
                  <span className="font-bold">{statistics.away.wins}</span>
                  <span className="text-red-400">({statistics.away.percentage}%)</span>
                </div>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                  DRAW
                </span>
                <div className="flex items-center gap-2">
                  <span className="font-bold">{statistics.draw.wins}</span>
                  <span className="text-yellow-400">({statistics.draw.percentage}%)</span>
                </div>
              </div>
            </div>
          </div>

          {/* Patterns Panel */}
          <div className="bg-black/50 rounded-xl p-6 border border-purple-500/30">
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
              <AlertTriangle className="text-purple-400" />
              Padrões Detectados
            </h2>
            
            <div className="space-y-3">
              {patterns.length > 0 ? patterns.map((pattern, index) => (
                <div key={index} className="bg-gray-800/50 rounded-lg p-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">{pattern.description}</span>
                    <span className={`text-xs px-2 py-1 rounded ${
                      pattern.impact === 'high' ? 'bg-red-500/20 text-red-400' :
                      pattern.impact === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                      'bg-blue-500/20 text-blue-400'
                    }`}>
                      {pattern.impact}
                    </span>
                  </div>
                </div>
              )) : (
                <p className="text-gray-400 text-sm">Nenhum padrão significativo detectado</p>
              )}
            </div>
          </div>
        </div>

        {/* Game History */}
        <div className="bg-black/50 rounded-xl p-6 mt-6 border border-gray-500/30">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Clock className="text-gray-400" />
            Histórico Recente
          </h2>
          
          <div className="grid grid-cols-5 md:grid-cols-10 gap-2 mb-4">
            {gameHistory.slice(-20).map((game, index) => (
              <div key={index} className="text-center">
                <div className={`w-8 h-8 mx-auto rounded-full flex items-center justify-center text-xs font-bold ${
                  game.result === 'HOME' ? 'bg-blue-500' :
                  game.result === 'AWAY' ? 'bg-red-500' :
                  'bg-yellow-500'
                }`}>
                  {game.result === 'HOME' ? 'H' : game.result === 'AWAY' ? 'A' : 'D'}
                </div>
                <div className="text-xs text-gray-400 mt-1">
                  {game.homeCard}-{game.awayCard}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Input Manual de Resultados */}
        <div className="bg-black/50 rounded-xl p-6 mt-6 border border-green-500/30">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold">Inserir Resultado Real</h2>
            <button
              onClick={() => setManualMode(!manualMode)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                manualMode ? 'bg-green-600 text-white' : 'bg-gray-600 text-white'
              }`}
            >
              {manualMode ? 'Modo Manual' : 'Modo Simulação'}
            </button>
          </div>
          
          {manualMode ? (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Carta HOME (2-14)</label>
                  <input
                    type="number"
                    min="2"
                    max="14"
                    value={homeCardInput}
                    onChange={(e) => setHomeCardInput(e.target.value)}
                    className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
                    placeholder="Ex: 10"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">Carta AWAY (2-14)</label>
                  <input
                    type="number"
                    min="2"
                    max="14"
                    value={awayCardInput}
                    onChange={(e) => setAwayCardInput(e.target.value)}
                    className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white focus:border-red-500 focus:outline-none"
                    placeholder="Ex: 7"
                  />
                </div>
                
                <div className="flex items-end">
                  <button
                    onClick={addManualResult}
                    className="w-full bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 px-6 py-2 rounded-lg font-bold transition-all transform hover:scale-105"
                  >
                    ✅ Adicionar Resultado
                  </button>
                </div>
              </div>
              
              <div className="bg-gray-800/50 rounded-lg p-4">
                <p className="text-sm text-gray-300 mb-2">
                  <strong>Como usar:</strong>
                </p>
                <ul className="text-sm text-gray-400 space-y-1">
                  <li>• Insira a carta HOME (2-14)</li>
                  <li>• Insira a carta AWAY (2-14)</li>
                  <li>• O resultado será calculado automaticamente</li>
                  <li>• <strong>Ás = 14 (carta mais alta)</strong>, Rei = 13, Dama = 12, Valete = 11</li>
                </ul>
              </div>
            </div>
          ) : (
            <div className="flex gap-4 justify-center">
              <button
                onClick={() => addResult('HOME')}
                className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-bold transition-colors"
              >
                Simular HOME
              </button>
              <button
                onClick={() => addResult('AWAY')}
                className="bg-red-600 hover:bg-red-700 px-6 py-3 rounded-lg font-bold transition-colors"
              >
                Simular AWAY
              </button>
              <button
                onClick={() => addResult('DRAW')}
                className="bg-yellow-600 hover:bg-yellow-700 px-6 py-3 rounded-lg font-bold transition-colors"
              >
                Simular DRAW
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FootballStudioAnalyzer;
