from controller import ControladorTraduccion

controlador = ControladorTraduccion()

while True:
    print("\n1. Cargar palabra")
    print("2. Traducir")
    print("3. Salir")
    opcion = input("Elige: ")

    if opcion == "1":
        esp = input("Escribe la palabra en español: ")
        ing = input("Escribe su traducción en inglés: ")
        controlador.cargar_palabra(esp, ing)
    elif opcion == "2":
        palabra = input("Escribe la palabra a traducir: ")
        print(f"{palabra} : {controlador.traducir(palabra)}")
    elif opcion == "3":
        break
    else:
        print("Opción no válida. Intenta de nuevo.")