import os

while True:
    print(f"1. Bloc \n2. Calculadora \n3. Multiplicación \n4. Dados \n5. Ordenamiento burbuja \n6. Salir")
    respuesta = input("Seleccione una opción: ")
    if respuesta == "1":
        os.system("notepad")
    elif respuesta == "2":
        os.system("calc")
    elif respuesta == "3":
        # Lógica para la multiplicación
        pass
    elif respuesta == "4":
        # Lógica para los dados
        pass
    elif respuesta == "5":
        # Lógica para el ordenamiento burbuja
        pass
    elif respuesta == "6":
        print("Saliendo...")
        break
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")