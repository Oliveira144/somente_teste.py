# Football Studio Pro Analyzer com Contagem Hi-Lo e IA de Sugestão

def valor_carta(carta, as_vale_14=True):
    carta = carta.upper()
    if carta == 'A':
        return 14 if as_vale_14 else 1
    elif carta == 'J':
        return 11
    elif carta == 'Q':
        return 12
    elif carta == 'K':
        return 13
    else:
        try:
            return int(carta)
        except ValueError:
            return None

def conferir_resultado(carta_home, carta_away, as_vale_14=True):
    v_home = valor_carta(carta_home, as_vale_14)
    v_away = valor_carta(carta_away, as_vale_14)

    if v_home is None or v_away is None:
        return "ERRO"

    if v_home > v_away:
        return "HOME"
    elif v_home < v_away:
        return "AWAY"
    else:
        return "DRAW"

def contagem_hilo(carta):
    v = valor_carta(carta, as_vale_14=False)
    if v is None:
        return 0
    if 2 <= v <= 6:
        return +1
    elif 7 <= v <= 9:
        return 0
    elif v == 1 or v >= 10:  # A, 10, J, Q, K
        return -1
    return 0

def sugestao_de_entrada(historico, contador_hilo):
    if len(historico) < 3:
        return "Aguardando mais rodadas..."

    ultimos = historico[-3:]

    # Sugestão por padrão
    if all(r == "HOME" for r in ultimos):
        padrao = "Streak de HOME"
        entrada = "HOME"
    elif all(r == "AWAY" for r in ultimos):
        padrao = "Streak de AWAY"
        entrada = "AWAY"
    elif ultimos[-3:] == ["HOME", "AWAY", "HOME"]:
        padrao = "Alternância detectada"
        entrada = "AWAY"
    elif ultimos[-1] == "DRAW":
        padrao = "Último foi DRAW"
        entrada = "⚠️ Evitar entrada"
    else:
        padrao = "Tendência recente"
        entrada = ultimos[-1]

    # Ajuste pela contagem Hi-Lo
    if contador_hilo >= 4:
        carta_tendencia = "Muitas cartas baixas saíram → Alta chance de cartas ALTAS"
    elif contador_hilo <= -4:
        carta_tendencia = "Muitas cartas altas saíram → Tendência de cartas BAIXAS (DRAW mais provável)"
    else:
        carta_tendencia = "Contagem neutra – padrão prevalece"

    # Montar resposta
    resposta = f"📈 Padrão: {padrao}\n" \
               f"🎯 Sugestão de entrada: {entrada}\n" \
               f"🧠 Análise Hi-Lo: {carta_tendencia} (Contador: {contador_hilo:+d})"
    return resposta

# === Execução principal ===
if __name__ == "__main__":
    print("⚽ Football Studio Pro Analyzer v1.0 ⚽")
    modo_as = input("Ás vale 14 ou 1? (digite 14 ou 1): ").strip() == "14"

    historico_resultados = []
    contador_hilo = 0

    while True:
        print("\n📥 Nova rodada")
        home = input("Carta HOME (ex: A, 10, 7, J): ").strip()
        away = input("Carta AWAY (ex: K, 2, Q): ").strip()

        resultado = conferir_resultado(home, away, as_vale_14=modo_as)

        if resultado == "ERRO":
            print("❌ Erro: carta inválida. Tente novamente.")
            continue

        historico_resultados.append(resultado)
        contador_hilo += contagem_hilo(home)
        contador_hilo += contagem_hilo(away)

        print(f"\n✅ Resultado: {resultado}")
        print(f"📊 Contador Hi-Lo: {contador_hilo:+d}")

        sugestao = sugestao_de_entrada(historico_resultados, contador_hilo)
        print("\n🔎 Análise e Sugestão:\n" + sugestao)

        continuar = input("\n▶️ Conferir outra rodada? (s/n): ").strip().lower()
        if continuar != 's':
            break
