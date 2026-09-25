temperatura = 31.0
modo_ausente = False

if modo_ausente:
    print("Modo auente: climatización apagada")
else:
    if temperatura > 28:
        print("Encender aire acondicionado")
    else:
        print("Temperatura comfortable")