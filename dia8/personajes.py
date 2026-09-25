class Personaje:
    def __init__(self):
        self.habilidad = ["ninguno"]

    def atacar(self):
        return "Dar patada"

class Guerrero(Personaje):
    def __init__(self):
        super().__init__()
        self.habilidad.append("Golpe cuerpo a cuerpo")

    def atacar(self):
        return "Ataque con espada"

class Mago(Personaje):
    def __init__(self):
        super().__init__()
        self.habilidad.append("Magia nivel 1")

    def atacar(self):
        return "Ataque con magia"

class Maestro(Guerrero, Mago):

    def atacar(self):
        return "Ataque con espada de fuego"

guerrero = Guerrero()
mago = Mago()
maestro = Maestro()

print(guerrero.atacar())
print(mago.atacar())
print(maestro.atacar())