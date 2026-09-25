import random
import time
while True:
    # Los dados se lanzan en cada vuelta del ciclo
    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6)
    
    if dado1 == dado2:
        print(f"¡Doble! {dado1} - {dado2}")
        break  # Detiene el ciclo cuando son iguales
    else:
        print(f"{dado1} - {dado2}")
    time.sleep(2)  # Pausa de 1 segundo entre lanzamientos