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
        except:
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
    elif v == 1 or v >= 10:
        return -1
    return 0

def sugestao_de_entrada(historico, contador):
    if len(historico) < 3:
        return "Aguardando mais rodadas..."
    ultimos = historico[-3:]
    if all(r == "HOME" for r in ultimos):
        padrao = "Streak de HOME"
        entrada = "HOME"
    elif all(r == "AWAY" for r in ultimos):
        padrao = "Streak de AWAY"
        entrada = "AWAY"
    elif ultimos == ["HOME", "AWAY", "HOME"]:
        padrao = "Alternância detectada"
        entrada = "AWAY"
    elif ultimos[-1] == "DRAW":
        padrao = "Último foi DRAW"
        entrada = "Evite entrada"
    else:
        padrao = "Tendência"
        entrada = ultimos[-1]

    if contador >= 4:
        tendencia = "Muitas cartas baixas saíram → Tendência de ALTAS"
    elif contador <= -4:
        tendencia = "Muitas cartas altas saíram → Tendência de BAIXAS"
    else:
        tendencia = "Contagem neutra"

    return f"Padrão: {padrao}\nSugestão: {entrada}\nHi-Lo: {tendencia} (Contador: {contador:+d})"

# Execução principal
if __name__ == "__main__":
    print("⚽ Football Studio Analyzer ⚽")
    as_vale_14 = input("Ás vale 14? (s/n): ").strip().lower() == "s"
    historico = []
    contador = 0

    while True:
        print("\nNova rodada:")
        home = input("Carta HOME: ").strip()
        away = input("Carta AWAY: ").strip()
        resultado = conferir_resultado(home, away, as_vale_14)
        if resultado == "ERRO":
            print("❌ Cartas inválidas!")
            continue
        historico.append(resultado)
        contador += contagem_hilo(home)
        contador += contagem_hilo(away)
        print(f"✅ Resultado: {resultado}")
        print(f"📊 Contador Hi-Lo: {contador:+d}")
        print(sugestao_de_entrada(historico, contador))

        cont = input("Continuar? (s/n): ").strip().lower()
        if cont != 's':
            break
