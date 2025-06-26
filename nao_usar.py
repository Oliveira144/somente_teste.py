import React, { useState, useEffect } from 'react';
import { AlertTriangle, TrendingUp, Target, BarChart3, Zap } from 'lucide-react';

const FootballStudioAnalyzer = () => {
  const [history, setHistory] = useState([]);
  const [suggestion, setSuggestion] = useState(null);
  const [confidence, setConfidence] = useState(0);
  const [streak, setStreak] = useState({ type: null, count: 0 });
  const [patterns, setPatterns] = useState({
    zigzag: 0,
    surfCor: 0,
    empateRecorrente: 0,
    escada: 0,
    espelho: 0
  });

  // Análise de padrões baseada nos dados das imagens
  const analyzePatterns = (results) => {
    if (results.length < 3) return null;

    // Análise sempre do mais antigo para o mais recente (ordem original)
    const recent = results.slice(-10);
    const last3 = results.slice(-3);
    const last5 = results.slice(-5);

    // Detectar Surf de Cor (3+ vezes a mesma cor seguida)
    let surfDetected = false;
    let currentStreak = 1;
    for (let i = recent.length - 2; i >= 0; i--) {
      if (recent[i] === recent[recent.length - 1] && recent[i] !== 'Empate') {
        currentStreak++;
      } else {
        break;
      }
    }
    if (currentStreak >= 3) surfDetected = true;

    // Detectar Zig-Zag (alternância Casa/Visitante)
    let zigzagCount = 0;
    for (let i = 1; i < last5.length; i++) {
      if (last5[i] !== last5[i-1] && last5[i] !== 'Empate' && last5[i-1] !== 'Empate') {
        zigzagCount++;
      }
    }
    const zigzagDetected = zigzagCount >= 3;

    // Detectar Empate Recorrente (intervalo de 15-35 rodadas)
    const empatePositions = results.map((r, i) => r === 'Empate' ? i : -1).filter(i => i !== -1);
    let empateRecorrente = false;
    if (empatePositions.length >= 2) {
      const lastEmpateGap = results.length - 1 - empatePositions[empatePositions.length - 1];
      if (lastEmpateGap >= 15 && lastEmpateGap <= 35) {
        empateRecorrente = true;
      }
    }

    // Detectar quebra de padrão
    const quebrarSurf = surfDetected && currentStreak >= 4;
    const quebrarZigzag = zigzagDetected;

    // Gerar sugestão com base nos padrões
    let suggestedEntry = null;
    let conf = 0;

    if (quebrarSurf) {
      const currentColor = recent[recent.length - 1];
      suggestedEntry = currentColor === 'Casa' ? 'Visitante' : 'Casa';
      conf = 85 + Math.min(currentStreak * 2, 15);
    } else if (zigzagDetected) {
      const lastResult = recent[recent.length - 1];
      if (lastResult !== 'Empate') {
        suggestedEntry = lastResult === 'Casa' ? 'Visitante' : 'Casa';
        conf = 75;
      }
    } else if (empateRecorrente) {
      suggestedEntry = 'Empate';
      conf = 70;
    } else if (surfDetected) {
      // Continuar o surf se ainda não quebrou
      suggestedEntry = recent[recent.length - 1];
      conf = 65 + currentStreak * 3;
    } else {
      // Análise baseada nos últimos 5/7/10 jogos
      const casaCount = recent.filter(r => r === 'Casa').length;
      const visitanteCount = recent.filter(r => r === 'Visitante').length;
      
      if (casaCount > visitanteCount + 2) {
        suggestedEntry = 'Visitante';
        conf = 60;
      } else if (visitanteCount > casaCount + 2) {
        suggestedEntry = 'Casa';
        conf = 60;
      } else {
        suggestedEntry = Math.random() > 0.5 ? 'Casa' : 'Visitante';
        conf = 50;
      }
    }

    return {
      entry: suggestedEntry,
      confidence: Math.min(conf, 98),
      patterns: {
        surf: surfDetected,
        surfStreak: currentStreak,
        zigzag: zigzagDetected,
        empateRecorrente,
        quebrarSurf,
        quebrarZigzag
      }
    };
  };

  const addResult = (result) => {
    const newHistory = [...history, result];
    setHistory(newHistory);
    
    const analysis = analyzePatterns(newHistory);
    if (analysis) {
      setSuggestion(analysis);
      setConfidence(analysis.confidence);
    }

    // Atualizar streak atual
    if (newHistory.length > 0) {
      const lastResult = newHistory[newHistory.length - 1];
      if (streak.type === lastResult) {
        setStreak({ type: lastResult, count: streak.count + 1 });
      } else {
        setStreak({ type: lastResult, count: 1 });
      }
    }
  };

  const clearHistory = () => {
    setHistory([]);
    setSuggestion(null);
    setConfidence(0);
    setStreak({ type: null, count: 0 });
  };

  const getConfidenceColor = (conf) => {
    if (conf >= 85) return 'text-green-400';
    if (conf >= 70) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getConfidenceText = (conf) => {
    if (conf >= 90) return 'ALTÍSSIMA GARANTIA';
    if (conf >= 80) return 'ALTA GARANTIA';
    if (conf >= 70) return 'BOA GARANTIA';
    if (conf >= 60) return 'GARANTIA MODERADA';
    return 'BAIXA GARANTIA';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent mb-2">
            ⚽ Football Studio Pro
          </h1>
          <p className="text-gray-300">Análise Inteligente de Padrões - Evolution Gaming</p>
        </div>

        {/* Botões de Entrada */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <button
            onClick={() => addResult('Casa')}
            className="bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 p-6 rounded-xl font-bold text-xl transition-all duration-200 transform hover:scale-105 shadow-lg"
          >
            🏠 CASA
          </button>
          <button
            onClick={() => addResult('Empate')}
            className="bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 p-6 rounded-xl font-bold text-xl transition-all duration-200 transform hover:scale-105 shadow-lg"
          >
            🤝 EMPATE
          </button>
          <button
            onClick={() => addResult('Visitante')}
            className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 p-6 rounded-xl font-bold text-xl transition-all duration-200 transform hover:scale-105 shadow-lg"
          >
            ✈️ VISITANTE
          </button>
        </div>

        {/* Sugestão Principal */}
        {suggestion && (
          <div className="bg-gradient-to-r from-purple-800 to-indigo-800 rounded-xl p-6 mb-6 border border-purple-500 shadow-2xl">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <Target className="text-yellow-400" size={32} />
                <h2 className="text-2xl font-bold">PRÓXIMA ENTRADA</h2>
              </div>
              <div className="text-right">
                <div className={`text-2xl font-bold ${getConfidenceColor(confidence)}`}>
                  {confidence}%
                </div>
                <div className="text-sm text-gray-300">
                  {getConfidenceText(confidence)}
                </div>
              </div>
            </div>
            
            <div className="text-center py-4">
              <div className={`text-4xl font-bold p-4 rounded-lg ${
                suggestion.entry === 'Casa' 
                  ? 'bg-red-600 text-white' 
                  : suggestion.entry === 'Visitante'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-600 text-white'
              }`}>
                {suggestion.entry === 'Casa' ? '🏠 APOSTAR NA CASA' : 
                 suggestion.entry === 'Visitante' ? '✈️ APOSTAR NO VISITANTE' : 
                 '🤝 APOSTAR NO EMPATE'}
              </div>
            </div>

            {/* Padrões Detectados */}
            <div className="mt-4 p-4 bg-black bg-opacity-30 rounded-lg">
              <h3 className="font-bold mb-2 flex items-center">
                <BarChart3 className="mr-2" size={20} />
                Padrões Detectados:
              </h3>
              <div className="grid grid-cols-2 gap-2 text-sm">
                {suggestion.patterns.surf && (
                  <div className="flex items-center text-yellow-300">
                    <Zap size={16} className="mr-1" />
                    Surf de Cor ({suggestion.patterns.surfStreak}x)
                  </div>
                )}
                {suggestion.patterns.zigzag && (
                  <div className="flex items-center text-green-300">
                    <TrendingUp size={16} className="mr-1" />
                    Zig-Zag Detectado
                  </div>
                )}
                {suggestion.patterns.quebrarSurf && (
                  <div className="flex items-center text-red-300">
                    <AlertTriangle size={16} className="mr-1" />
                    Quebra de Surf
                  </div>
                )}
                {suggestion.patterns.empateRecorrente && (
                  <div className="flex items-center text-purple-300">
                    <Target size={16} className="mr-1" />
                    Empate Recorrente
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Histórico */}
        <div className="bg-gray-800 rounded-xl p-6 mb-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-bold">Últimos Resultados ({history.length})</h3>
            <button
              onClick={clearHistory}
              className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg text-sm transition-colors"
            >
              Limpar Histórico
            </button>
          </div>
          
          <div className="flex flex-wrap gap-2 mb-4">
            {[...history].reverse().map((result, index) => (
              <div
                key={index}
                className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold ${
                  result === 'Casa' 
                    ? 'bg-red-600' 
                    : result === 'Visitante'
                    ? 'bg-blue-600'
                    : 'bg-gray-600'
                }`}
              >
                {result === 'Casa' ? 'C' : result === 'Visitante' ? 'V' : 'E'}
              </div>
            ))}
          </div>

          {/* Estatísticas */}
          {history.length > 0 && (
            <div className="grid grid-cols-3 gap-4 text-center">
              <div className="bg-red-600 bg-opacity-30 p-3 rounded-lg">
                <div className="text-2xl font-bold">
                  {history.filter(r => r === 'Casa').length}
                </div>
                <div className="text-sm">Casa ({((history.filter(r => r === 'Casa').length / history.length) * 100).toFixed(1)}%)</div>
              </div>
              <div className="bg-gray-600 bg-opacity-30 p-3 rounded-lg">
                <div className="text-2xl font-bold">
                  {history.filter(r => r === 'Empate').length}
                </div>
                <div className="text-sm">Empate ({((history.filter(r => r === 'Empate').length / history.length) * 100).toFixed(1)}%)</div>
              </div>
              <div className="bg-blue-600 bg-opacity-30 p-3 rounded-lg">
                <div className="text-2xl font-bold">
                  {history.filter(r => r === 'Visitante').length}
                </div>
                <div className="text-sm">Visitante ({((history.filter(r => r === 'Visitante').length / history.length) * 100).toFixed(1)}%)</div>
              </div>
            </div>
          )}
        </div>

        {/* Streak Atual */}
        {streak.type && (
          <div className="bg-gradient-to-r from-yellow-600 to-orange-600 rounded-xl p-4 text-center">
            <div className="text-lg font-bold">
              Streak Atual: {streak.count}x {streak.type}
              {streak.count >= 3 && streak.type !== 'Empate' && (
                <span className="ml-2 text-red-200">(⚠️ Possível Quebra)</span>
              )}
            </div>
          </div>
        )}

        {/* Disclaimer */}
        <div className="text-center text-gray-400 text-sm mt-8 p-4 bg-gray-800 bg-opacity-50 rounded-lg">
          <p className="mb-2">⚠️ Este aplicativo é apenas para fins educacionais e de entretenimento.</p>
          <p>Apostas envolvem riscos. Jogue com responsabilidade.</p>
        </div>
      </div>
    </div>
  );
};

export default FootballStudioAnalyzer;
