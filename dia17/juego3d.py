import random
import math
import wave
import struct
import os
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import (
    AmbientLight,
    DirectionalLight,
    Vec4,
    Vec3,
    CardMaker,
    CollisionNode,
    CollisionBox,
    CollisionTraverser,
    CollisionHandlerQueue,
    BitMask32,
    TextNode,
    Material,
    PNMImage,
    Texture,
    TextureStage,
)


class TrafficRider3D(ShowBase):
    def __init__(self):
        super().__init__()

        self.disableMouse()
        self.win.setClearColor(Vec4(0.08, 0.08, 0.12, 1.0))

        # 1. ESTADO DEL JUEGO
        self.game_over = False
        self.puntuacion = 0.0
        self.velocidad_base = 25.0
        self.velocidad_actual = self.velocidad_base
        self.carriles = [-3.0, 0.0, 3.0]
        
        self.haciendo_wheelie = False
        self.mensaje_temporal_tiempo = 0.0

        # 2. GENERAR Y CARGAR SONIDOS PROCEDURALES
        self.sonidos = {}
        self.generar_archivos_audio_temporales()
        self.cargar_efectos_sonido()

        # 3. SISTEMA DE COLISIONES
        self.cTrav = CollisionTraverser()
        self.handler_queue = CollisionHandlerQueue()

        # 4. TEXTURA DE CARRETERA PROCEDURAL
        self.textura_carretera = self.crear_textura_carretera()

        # 5. CONSTRUCCIÓN DE LA ESCENA Y ELEMENTOS
        self.crear_carretera()
        self.crear_jugador()
        self.configurar_luces()

        self.obstaculos = []
        self.obstaculos_adelantados = set()
        self.tiempo_siguiente_obstaculo = 0.0

        # 6. CÁMARA
        self.distancia_cam = 7.0
        self.angulo_h = 0.0
        self.angulo_v = 15.0
        self.arrastrando_raton = False
        self.ultima_pos_raton = (0, 0)

        # 7. INTERFAZ EN PANTALLA (HUD)
        self.hud_texto = OnscreenText(
            text="Distancia: 0 m",
            pos=(-1.2, 0.85),
            scale=0.07,
            fg=(1, 1, 1, 1),
            align=TextNode.ALeft,
            mayChange=True,
        )

        self.hud_aviso = OnscreenText(
            text="",
            pos=(0, 0.4),
            scale=0.08,
            fg=(1, 0.8, 0.2, 1),
            align=TextNode.ACenter,
            mayChange=True,
        )

        self.hud_gameover = OnscreenText(
            text="",
            pos=(0, 0),
            scale=0.12,
            fg=(1, 0.2, 0.2, 1),
            align=TextNode.ACenter,
            mayChange=True,
        )

        # 8. EVENTOS DE ENTRADA
        self.teclas = {"izquierda": False, "derecha": False, "acelerar": False, "frenar": False, "wheelie": False}

        self.accept("a", self.set_tecla, ["izquierda", True])
        self.accept("a-up", self.set_tecla, ["izquierda", False])
        self.accept("d", self.set_tecla, ["derecha", True])
        self.accept("d-up", self.set_tecla, ["derecha", False])
        self.accept("w", self.set_tecla, ["acelerar", True])
        self.accept("w-up", self.set_tecla, ["acelerar", False])
        self.accept("s", self.set_tecla, ["frenar", True])
        self.accept("s-up", self.set_tecla, ["frenar", False])
        self.accept("space", self.set_tecla, ["wheelie", True])
        self.accept("space-up", self.set_tecla, ["wheelie", False])

        self.accept("arrow_left", self.set_tecla, ["izquierda", True])
        self.accept("arrow_left-up", self.set_tecla, ["izquierda", False])
        self.accept("arrow_right", self.set_tecla, ["derecha", True])
        self.accept("arrow_right-up", self.set_tecla, ["derecha", False])
        self.accept("arrow_up", self.set_tecla, ["acelerar", True])
        self.accept("arrow_up-up", self.set_tecla, ["acelerar", False])
        self.accept("arrow_down", self.set_tecla, ["frenar", True])
        self.accept("arrow_down-up", self.set_tecla, ["frenar", False])

        self.accept("r", self.reiniciar_juego)

        self.accept("mouse3", self.iniciar_arrastre)
        self.accept("mouse3-up", self.detener_arrastre)

        self.taskMgr.add(self.bucle_principal, "BuclePrincipal")

    def set_tecla(self, accion, estado):
        self.teclas[accion] = estado

    def generar_archivos_audio_temporales(self):
        """Crea archivos WAV básicos en la carpeta local si no existen."""
        sample_rate = 22050

        # 1. Sonido de motor (Zumbido grave constante)
        if not os.path.exists("motor.wav"):
            with wave.open("motor.wav", "w") as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(sample_rate)
                duracion = 1.0
                frames = int(sample_rate * duracion)
                datos = []
                for i in range(frames):
                    t = i / sample_rate
                    val = int(10000 * math.sin(2 * math.pi * 110 * t) + 5000 * math.sin(2 * math.pi * 220 * t))
                    datos.append(struct.pack('<h', val))
                f.writeframes(b''.join(datos))

        # 2. Sonido de choque (Ruido blanco seco)
        if not os.path.exists("crash.wav"):
            with wave.open("crash.wav", "w") as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(sample_rate)
                duracion = 0.5
                frames = int(sample_rate * duracion)
                datos = []
                for i in range(frames):
                    atenuacion = 1.0 - (i / frames)
                    val = int(random.randint(-15000, 15000) * atenuacion)
                    datos.append(struct.pack('<h', val))
                f.writeframes(b''.join(datos))

        # 3. Sonido de bonus (Tono agudo ascendente)
        if not os.path.exists("bonus.wav"):
            with wave.open("bonus.wav", "w") as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(sample_rate)
                duracion = 0.3
                frames = int(sample_rate * duracion)
                datos = []
                for i in range(frames):
                    t = i / sample_rate
                    freq = 400 + (i * 2)
                    val = int(8000 * math.sin(2 * math.pi * freq * t))
                    datos.append(struct.pack('<h', val))
                f.writeframes(b''.join(datos))

    def cargar_efectos_sonido(self):
        archivos_audio = {
            "motor": "motor.wav",
            "crash": "crash.wav",
            "bonus": "bonus.wav"
        }
        for nombre, archivo in archivos_audio.items():
            try:
                sonido = self.loader.loadSfx(archivo)
                if sonido:
                    self.sonidos[nombre] = sonido
            except Exception:
                self.sonidos[nombre] = None

        if self.sonidos.get("motor"):
            self.sonidos["motor"].setLoop(True)
            self.sonidos["motor"].play()

    def reproducir_sonido(self, nombre):
        if self.sonidos.get(nombre):
            self.sonidos[nombre].play()

    def detener_sonido(self, nombre):
        if self.sonidos.get(nombre):
            self.sonidos[nombre].stop()

    def crear_textura_carretera(self):
        pnm = PNMImage(256, 256)
        for y in range(256):
            for x in range(256):
                ruido = random.uniform(-0.02, 0.02)
                val = 0.16 + ruido
                pnm.setXel(x, y, (val, val, val + 0.01))

        for y in range(256):
            es_linea = (y // 16) % 2 == 0
            if es_linea:
                for w in range(-2, 3):
                    if 0 <= 85 + w < 256:
                        pnm.setXel(85 + w, y, (0.9, 0.9, 0.95))
                    if 0 <= 170 + w < 256:
                        pnm.setXel(170 + w, y, (0.9, 0.9, 0.95))

        tex = Texture("asfalto_textura")
        tex.load(pnm)
        tex.setWrapU(Texture.WMRepeat)
        tex.setWrapV(Texture.WMRepeat)
        return tex

    def aplicar_material(self, nodo, color_rgb, brillo=0.3):
        nodo.setColor(Vec4(color_rgb[0], color_rgb[1], color_rgb[2], 1.0))
        mat = Material()
        mat.setAmbient(Vec4(color_rgb[0] * 0.3, color_rgb[1] * 0.3, color_rgb[2] * 0.3, 1.0))
        mat.setDiffuse(Vec4(color_rgb[0], color_rgb[1], color_rgb[2], 1.0))
        mat.setSpecular(Vec4(brillo, brillo, brillo, 1.0))
        mat.setShininess(32.0)
        nodo.setMaterial(mat, 1)

    def crear_carretera(self):
        self.tramos_carretera = []
        cm = CardMaker("carretera")
        cm.setFrame(-6.5, 6.5, 0, 100)

        for i in range(2):
            tramo = self.render.attachNewNode(cm.generate())
            tramo.setP(-90)
            tramo.setY(i * 100)
            tramo.setTexture(self.textura_carretera)
            tramo.setTexScale(TextureStage.getDefault(), 1.0, 4.0)
            self.tramos_carretera.append(tramo)

    def crear_jugador(self):
        self.jugador = self.render.attachNewNode("Jugador")
        self.jugador.setPos(0, 5, 0.35)

        chasis = self.loader.loadModel("models/box")
        chasis.reparentTo(self.jugador)
        chasis.setScale(0.32, 1.2, 0.3)
        chasis.setPos(-0.16, -0.6, 0.1)
        self.aplicar_material(chasis, (0.95, 0.1, 0.1), brillo=0.6)

        tanque = self.loader.loadModel("models/box")
        tanque.reparentTo(self.jugador)
        tanque.setScale(0.35, 0.7, 0.28)
        tanque.setPos(-0.175, -0.4, 0.25)
        self.aplicar_material(tanque, (0.85, 0.05, 0.05), brillo=0.6)

        parabrisas = self.loader.loadModel("models/box")
        parabrisas.reparentTo(self.jugador)
        parabrisas.setScale(0.26, 0.25, 0.3)
        parabrisas.setPos(-0.13, -0.15, 0.42)
        self.aplicar_material(parabrisas, (0.1, 0.6, 0.85), brillo=0.9)

        asiento = self.loader.loadModel("models/box")
        asiento.reparentTo(self.jugador)
        asiento.setScale(0.28, 0.5, 0.18)
        asiento.setPos(-0.14, -0.9, 0.28)
        self.aplicar_material(asiento, (0.15, 0.15, 0.15), brillo=0.1)

        escape = self.loader.loadModel("models/box")
        escape.reparentTo(self.jugador)
        escape.setScale(0.08, 0.8, 0.08)
        escape.setPos(0.22, -0.7, 0.0)
        self.aplicar_material(escape, (0.8, 0.8, 0.85), brillo=0.8)

        manillar = self.loader.loadModel("models/box")
        manillar.reparentTo(self.jugador)
        manillar.setScale(0.7, 0.08, 0.08)
        manillar.setPos(-0.35, -0.1, 0.52)
        self.aplicar_material(manillar, (0.2, 0.2, 0.2), brillo=0.3)

        faro = self.loader.loadModel("models/box")
        faro.reparentTo(self.jugador)
        faro.setScale(0.22, 0.08, 0.18)
        faro.setPos(-0.11, 0.2, 0.35)
        self.aplicar_material(faro, (1.0, 1.0, 0.9), brillo=1.0)

        for posY in [0.4, -1.2]:
            rueda = self.loader.loadModel("models/box")
            rueda.reparentTo(self.jugador)
            rueda.setScale(0.14, 0.45, 0.38)
            rueda.setPos(-0.07, posY, -0.05)
            self.aplicar_material(rueda, (0.08, 0.08, 0.08), brillo=0.1)
            
            llanta = self.loader.loadModel("models/box")
            llanta.reparentTo(rueda)
            llanta.setScale(0.5, 0.6, 0.5)
            llanta.setPos(0, 0, 0)
            self.aplicar_material(llanta, (0.75, 0.75, 0.75), brillo=0.7)

        c_box = CollisionBox(Vec3(-0.1, -0.4, 0.25), 0.25, 0.75, 0.35)
        c_node = CollisionNode("colision_jugador")
        c_node.addSolid(c_box)
        c_node.setFromCollideMask(BitMask32.bit(1))
        c_node.setIntoCollideMask(BitMask32.allOff())

        self.col_jugador_np = self.jugador.attachNewNode(c_node)
        self.cTrav.addCollider(self.col_jugador_np, self.handler_queue)

    def generar_obstaculo(self):
        carril_x = random.choice(self.carriles)
        obs = self.render.attachNewNode("Obstaculo")
        obs.setPos(carril_x, 90, 0.5)

        colores_coche = [
            (0.1, 0.35, 0.85),
            (0.85, 0.85, 0.1),
            (0.15, 0.7, 0.3),
            (0.85, 0.35, 0.1),
            (0.75, 0.75, 0.75)
        ]
        color_elegido = random.choice(colores_coche)

        carroceria = self.loader.loadModel("models/box")
        carroceria.reparentTo(obs)
        carroceria.setScale(0.9, 2.2, 0.65)
        carroceria.setPos(-0.45, -1.1, 0.1)
        self.aplicar_material(carroceria, color_elegido, brillo=0.5)

        cabina = self.loader.loadModel("models/box")
        cabina.reparentTo(obs)
        cabina.setScale(0.75, 1.2, 0.5)
        cabina.setPos(-0.375, -0.6, 0.75)
        self.aplicar_material(cabina, (color_elegido[0]*0.7, color_elegido[1]*0.7, color_elegido[2]*0.7), brillo=0.4)

        for posY in [-0.2, -1.2]:
            luna = self.loader.loadModel("models/box")
            luna.reparentTo(obs)
            luna.setScale(0.7, 0.08, 0.42)
            luna.setPos(-0.35, posY, 0.8)
            self.aplicar_material(luna, (0.1, 0.1, 0.15), brillo=0.8)

        for posX in [-0.35, 0.35]:
            luz = self.loader.loadModel("models/box")
            luz.reparentTo(obs)
            luz.setScale(0.15, 0.05, 0.1)
            luz.setPos(posX, -2.15, 0.3)
            self.aplicar_material(luz, (0.9, 0.1, 0.1), brillo=0.9)

        c_box = CollisionBox(Vec3(-0.45, -1.1, 0.45), 0.45, 1.1, 0.5)
        c_node = CollisionNode("colision_obstaculo")
        c_node.addSolid(c_box)
        c_node.setFromCollideMask(BitMask32.allOff())
        c_node.setIntoCollideMask(BitMask32.bit(1))

        obs.attachNewNode(c_node)
        self.obstaculos.append(obs)

    def configurar_luces(self):
        alight = AmbientLight("alight")
        alight.setColor(Vec4(0.5, 0.5, 0.55, 1))
        self.render.setLight(self.render.attachNewNode(alight))

        dlight = DirectionalLight("dlight")
        dlight.setColor(Vec4(0.95, 0.95, 0.9, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(-45, -55, 0)
        self.render.setLight(dlnp)

    def iniciar_arrastre(self):
        if self.mouseWatcherNode.hasMouse():
            self.arrastrando_raton = True
            m_pos = self.mouseWatcherNode.getMouse()
            self.ultima_pos_raton = (m_pos.getX(), m_pos.getY())

    def detener_arrastre(self):
        self.arrastrando_raton = False

    def actualizar_camara(self):
        if self.arrastrando_raton and self.mouseWatcherNode.hasMouse():
            m_pos = self.mouseWatcherNode.getMouse()
            dx = m_pos.getX() - self.ultima_pos_raton[0]
            dy = m_pos.getY() - self.ultima_pos_raton[1]

            self.angulo_h -= dx * 80.0
            self.angulo_v = max(5.0, min(50.0, self.angulo_v + dy * 80.0))
            self.ultima_pos_raton = (m_pos.getX(), m_pos.getY())

        pos_j = self.jugador.getPos()
        rad_h = math.radians(self.angulo_h)
        rad_v = math.radians(self.angulo_v)

        cam_x = pos_j.getX() + self.distancia_cam * math.sin(rad_h) * math.cos(rad_v)
        cam_y = pos_j.getY() - self.distancia_cam * math.cos(rad_h) * math.cos(rad_v)
        cam_z = pos_j.getZ() + self.distancia_cam * math.sin(rad_v) + 1.0

        self.camera.setPos(cam_x, cam_y, cam_z)
        self.camera.lookAt(pos_j + Vec3(0, 2.5, 0.6))

    def bucle_principal(self, tarea):
        dt = globalClock.getDt()

        if self.game_over:
            return Task.cont

        self.haciendo_wheelie = self.teclas["wheelie"]

        velocidad_objetivo = self.velocidad_base
        if self.haciendo_wheelie:
            velocidad_objetivo = 15.0

        if self.teclas["acelerar"]:
            self.velocidad_actual = min(60.0, self.velocidad_actual + 22.0 * dt)
        elif self.teclas["frenar"]:
            self.velocidad_actual = max(10.0, self.velocidad_actual - 35.0 * dt)
        else:
            if self.velocidad_actual < velocidad_objetivo:
                self.velocidad_actual = min(velocidad_objetivo, self.velocidad_actual + 12.0 * dt)
            elif self.velocidad_actual > velocidad_objetivo:
                self.velocidad_actual = max(velocidad_objetivo, self.velocidad_actual - 12.0 * dt)

        pos_x = self.jugador.getX()
        vel_lateral = (6.0 if self.haciendo_wheelie else 10.0) * dt
        if self.teclas["izquierda"]:
            pos_x = max(-4.2, pos_x - vel_lateral)
        if self.teclas["derecha"]:
            pos_x = min(4.2, pos_x + vel_lateral)
        self.jugador.setX(pos_x)

        inclinacion_roll = 0.0
        if self.teclas["izquierda"]:
            inclinacion_roll = 18.0
        elif self.teclas["derecha"]:
            inclinacion_roll = -18.0
        self.jugador.setR(inclinacion_roll)

        inclinacion_pitch = 16.0 if self.haciendo_wheelie else 0.0
        self.jugador.setP(inclinacion_pitch)

        multiplicador = 2.5 if self.haciendo_wheelie else 1.0
        desplazamiento = self.velocidad_actual * dt
        self.puntuacion += desplazamiento * multiplicador

        wheelie_txt = " | ¡STOPPIE x2.5!" if self.haciendo_wheelie else ""
        self.hud_texto.setText(f"Distancia: {int(self.puntuacion)} m  |  Velocidad: {int(self.velocidad_actual * 3.2)} km/h{wheelie_txt}")

        if self.mensaje_temporal_tiempo > 0:
            self.mensaje_temporal_tiempo -= dt
            if self.mensaje_temporal_tiempo <= 0:
                self.hud_aviso.setText("")

        for tramo in self.tramos_carretera:
            tramo.setY(tramo.getY() - desplazamiento)
            if tramo.getY() <= -100:
                tramo.setY(tramo.getY() + 200)

        self.tiempo_siguiente_obstaculo -= dt
        if self.tiempo_siguiente_obstaculo <= 0:
            self.generar_obstaculo()
            self.tiempo_siguiente_obstaculo = random.uniform(0.7, 1.5)

        for obs in self.obstaculos[:]:
            obs.setY(obs.getY() - desplazamiento)
            
            if obs not in self.obstaculos_adelantados and obs.getY() < self.jugador.getY():
                self.obstaculos_adelantados.add(obs)
                distancia_lateral = abs(self.jugador.getX() - obs.getX())
                if distancia_lateral < 1.8:
                    self.puntuacion += 250
                    self.hud_aviso.setText("¡Adelantamiento apurado! +250m")
                    self.mensaje_temporal_tiempo = 1.2
                    self.reproducir_sonido("bonus")

            if obs.getY() < -10:
                if obs in self.obstaculos_adelantados:
                    self.obstaculos_adelantados.remove(obs)
                self.obstaculos.remove(obs)
                obs.removeNode()

        self.cTrav.traverse(self.render)
        if self.handler_queue.getNumEntries() > 0:
            self.game_over = True
            self.hud_gameover.setText("¡CRASH!\nPresiona 'R' para reiniciar")
            self.hud_aviso.setText("")
            self.reproducir_sonido("crash")
            self.detener_sonido("motor")

        self.actualizar_camara()

        return Task.cont

    def reiniciar_juego(self):
        if not self.game_over:
            return

        for obs in self.obstaculos:
            obs.removeNode()
        self.obstaculos.clear()
        self.obstaculos_adelantados.clear()

        self.jugador.setPos(0, 5, 0.35)
        self.jugador.setR(0)
        self.jugador.setP(0)
        self.puntuacion = 0.0
        self.velocidad_actual = self.velocidad_base
        self.game_over = False
        self.hud_gameover.setText("")
        
        if self.sonidos.get("motor"):
            self.sonidos["motor"].play()


if __name__ == "__main__":
    app = TrafficRider3D()
    app.run()