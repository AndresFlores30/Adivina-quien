import json
import os
import sys
import pygame
import pygame.freetype

# ──────────────────────────────────────────────
#  CONFIGURACIÓN GENERAL
# ──────────────────────────────────────────────
ARCHIVO_DB  = "personajes_overwatch.json"
ANCHO, ALTO = 900, 680
FPS         = 60

# Paleta visual
C_BG        = (8,  12,  24)
C_PANEL     = (14, 22,  45)
C_ACCENT    = (0, 200, 255)
C_ACCENT2   = (255, 100,  0)
C_TEXT      = (220, 235, 255)
C_DIMTEXT   = (120, 145, 180)
C_YES       = ( 30, 200,  80)
C_NO        = (220,  50,  50)
C_BTN_HOVER = (20,  40,  80)
C_BORDER    = (30,  60, 110)
C_GOLD      = (255, 210,  50)

# ──────────────────────────────────────────────
#  FUNCIÓN PARA MANEJAR IMÁGENES (NUEVO - LÍNEAS 42-83)
# ──────────────────────────────────────────────
def cargar_imagen_personaje(nombre_personaje):
    """Intenta cargar la imagen del personaje desde la carpeta 'imagenes'"""
    # Limpiar el nombre para usarlo como nombre de archivo
    nombre_archivo = nombre_personaje.replace(":", "").replace(".", "")
    nombre_archivo = nombre_archivo.replace(" ", "_")
    
    # Extensiones posibles
    extensiones = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    
    for ext in extensiones:
        ruta = os.path.join("imagenes", f"{nombre_archivo}{ext}")
        if os.path.exists(ruta):
            try:
                imagen = pygame.image.load(ruta)
                imagen = pygame.transform.scale(imagen, (200, 200))
                return imagen
            except:
                return None
    
    return crear_signo_pregunta()

def crear_signo_pregunta():
    """Crea una superficie con un signo de pregunta"""
    surf = pygame.Surface((200, 200), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))
    
    # Fondo gris oscuro
    pygame.draw.rect(surf, (50, 50, 50), (0, 0, 200, 200), border_radius=10)
    pygame.draw.rect(surf, C_ACCENT, (0, 0, 200, 200), 3, border_radius=10)
    
    # Signo de pregunta
    font = pygame.font.Font(None, 120)
    text = font.render("?", True, C_ACCENT)
    text_rect = text.get_rect(center=(100, 100))
    surf.blit(text, text_rect)
    
    return surf

# ──────────────────────────────────────────────
#  BASE DE CONOCIMIENTO – ATRIBUTOS ENRIQUECIDOS
# ──────────────────────────────────────────────
base_inicial = {
    # TANQUES
    "D.Va":          {"rol_tanque","usa_mecha","es_coreana","usa_arma_de_fuego","puede_volar","es_heroina","tecnologia_avanzada","alta_movilidad","protege_aliados"},
    "Doomfist":      {"rol_tanque","usa_guante","es_talon","es_lider","combate_cuerpo_a_cuerpo","es_villano","alta_movilidad","gran_tamano","es_africano"},
    "Domina":        {"rol_tanque","usa_luz","es_talon","usa_escudo","es_villana","gran_tamano","tecnologia_avanzada"},
    "Hazard":        {"rol_tanque","usa_escopeta","combate_cuerpo_a_cuerpo","caotico","es_lider","gran_tamano","puede_saltar","tecnologia_avanzada","es_cyborg","alta_movilidad"},
    "Junker Queen":  {"rol_tanque","usa_hacha","usa_arma_de_fuego","caotico","usa_escopeta","es_de_junkertown","combate_cuerpo_a_cuerpo","es_lider","gran_tamano","drena_vida"},
    "Mauga":         {"rol_tanque","usa_ametralladoras","es_talon","caotico","usa_arma_de_fuego","es_villano","gran_tamano","es_de_isla"},
    "Orisa":         {"rol_tanque","es_omnico","es_overwatch","usa_lanza","protege_aliados","tecnologia_avanzada","es_africana","usa_energia"},
    "Ramattra":      {"rol_tanque","es_omnico","es_lider","usa_baston","gran_tamano","forma_nemesis","combate_cuerpo_a_cuerpo","es_villano","usa_energia","null_sector"},
    "Reinhardt":     {"rol_tanque","usa_martillo","usa_escudo","es_overwatch","combate_cuerpo_a_cuerpo","es_aleman","gran_tamano","veterano"},
    "Roadhog":       {"rol_tanque","usa_gancho","usa_escopeta","es_de_junkertown","gran_tamano","usa_mascara","usa_explosivos"},
    "Sigma":         {"rol_tanque","controla_gravedad","es_talon","cientifico","tecnologia_avanzada","usa_escudo"},
    "Winston":       {"rol_tanque","es_animal","cientifico","usa_rayo","puede_saltar","es_overwatch","tecnologia_avanzada"},
    "Wrecking Ball": {"rol_tanque","es_animal","usa_mecha","alta_movilidad","es_de_junkertown","tecnologia_avanzada","gran_tamano"},
    "Zarya":         {"rol_tanque","usa_canon","es_rusa","es_overwatch","usa_barreras","protege_aliados","usa_arma_de_fuego"},

    # DAÑO
    "Anran":          {"rol_dano","usa_arma_de_fuego","es_overwatch","alta_movilidad","es_china"},
    "Ashe":           {"rol_dano","usa_rifle","usa_arma_de_fuego","tiene_companero","es_lider","estilo_vaquero","es_americana"},
    "Bastion":        {"rol_dano","es_omnico","gran_tamano","es_overwatch","usa_ametralladora","modo_torreta","tecnologia_avanzada","usa_arma_de_fuego"},
    "Cassidy":        {"rol_dano","usa_revolver","usa_arma_de_fuego","estilo_vaquero","es_overwatch","usa_granadas","es_americano"},
    "Echo":           {"rol_dano","es_omnico","alta_movilidad","puede_volar","es_overwatch","tecnologia_avanzada","puede_copiar","usa_laser"},
    "Genji":          {"rol_dano","usa_espada","es_cyborg","es_overwatch","es_japones","alta_movilidad","combate_cuerpo_a_cuerpo","usa_kunai","blackwatch"},
    "Hanzo":          {"rol_dano","usa_arco","es_japones","usa_dragones","ataque_distancia","usa_explosivos"},
    "Junkrat":        {"rol_dano","usa_explosivos","es_de_junkertown","usa_granadas","caotico","alta_movilidad"},
    "Mei":            {"rol_dano","usa_hielo","cientifico","es_overwatch","controla_zona","es_heroina","es_china","usa_arma_de_fuego"},
    "Pharah":         {"rol_dano","puede_volar","usa_cohetes","alta_movilidad","es_overwatch","usa_arma_de_fuego","es_egipcia","usa_armadura"},
    "Reaper":         {"rol_dano","usa_escopetas","usa_arma_de_fuego","es_talon","alta_movilidad","puede_teletransportarse","es_villano","usa_mascara","blackwatch","es_americano"},
    "Sojourn":        {"rol_dano","usa_railgun","es_cyborg","es_overwatch","usa_arma_de_fuego","alta_movilidad","es_canadiense"},
    "Soldado: 76":    {"rol_dano","usa_rifle","usa_arma_de_fuego","es_overwatch","usa_visor","veterano","es_americano"},
    "Sombra":         {"rol_dano","hackea","es_talon","puede_volverse_invisible","usa_arma_de_fuego","alta_movilidad","es_mexicana"},
    "Symmetra":       {"rol_dano","usa_luz","usa_torreta","crea_portal","tecnologia_avanzada","es_india"},
    "Torbjorn":       {"rol_dano","usa_torreta","es_ingeniero","usa_martillo","tecnologia_avanzada","es_sueco","usa_arma_de_fuego"},
    "Tracer":         {"rol_dano","alta_movilidad","puede_retroceder_tiempo","usa_pistolas","es_overwatch","es_britanica"},
    "Venture":        {"rol_dano","excava","usa_taladro","explorador","alta_movilidad","combate_cuerpo_a_cuerpo"},
    "Widowmaker":     {"rol_dano","usa_sniper","es_talon","ataque_distancia","es_villana","es_francesa","usa_gancho"},
    "Freja":          {"rol_dano","usa_arco","es_talon","alta_movilidad","ataque_distancia","usa_explosivos"},
    "Emre":           {"rol_dano","es_cyborg","es_talon","usa_arma_de_fuego","usa_granadas","usa_rifle","es_villano"},
    "Vendetta":       {"rol_dano","usa_espada","es_talon","combate_cuerpo_a_cuerpo","es_villana"},
    "Sierra":         {"rol_dano","usa_arma_de_fuego","usa_granadas","explorador","usa_rifle","alta_movilidad"},
    

    # APOYO
    "Ana":           {"rol_apoyo","usa_sniper","cura_aliados","es_egipcia","ataque_distancia","es_overwatch","usa_mascara","veterano"},
    "Baptiste":      {"rol_apoyo","cura_aliados","usa_arma_de_fuego","protege_aliados","ex_talon","es_haitiano"},
    "Brigitte":      {"rol_apoyo","usa_escudo","usa_maza","es_overwatch","cura_aliados","combate_cuerpo_a_cuerpo","protege_aliados","es_sueca"},
    "Illari":        {"rol_apoyo","usa_sol","cura_aliados","usa_torreta","ataque_distancia","usa_arma_de_fuego","es_peruana"},
    "Juno":          {"rol_apoyo","cura_aliados","alta_movilidad","es_overwatch","espacial","tecnologia_avanzada","puede_volar"},
    "Jetpack cat":   {"rol_apoyo","cura_aliados","es_animal","usa_arma_de_fuego","alta_movilidad","es_overwatch","puede_volar","ataque_distancia"},
    "Kiriko":        {"rol_apoyo","cura_aliados","es_japonesa","usa_kunai","alta_movilidad","usa_espiritu"},
    "Lifeweaver":    {"rol_apoyo","cura_aliados","usa_naturaleza","protege_aliados","tecnologia_avanzada","es_tailandes"},
    "Lucio":         {"rol_apoyo","cura_aliados","es_overwatch","usa_musica","alta_movilidad","aumenta_velocidad","es_brasileno"},
    "Mercy":         {"rol_apoyo","cura_aliados","puede_volar","usa_baston","es_overwatch","revive_aliados","protege_aliados","usa_arma_de_fuego","es_suiza"},
    "Mizuki":        {"rol_apoyo","cura_aliados","es_japonesa","alta_movilidad","usa_espiritu"},
    "Moira":         {"rol_apoyo","cura_aliados","es_talon","cientifico","drena_vida","puede_teletransportarse","es_irlandesa"},
    "Wuyang":        {"rol_apoyo","cura_aliados","usa_baston","es_overwatch","es_china"},
    "Zenyatta":      {"rol_apoyo","es_omnico","cura_aliados","usa_orbes","monje","ataque_distancia"},

    # LORE
    "Athena":        {"ia","es_overwatch","tecnologia_avanzada","personaje_lore"},
    "Mondatta":      {"es_omnico","monje","personaje_lore"},
    "Maximilien":    {"es_omnico","es_talon","personaje_lore",},
    "Efi Oladele":   {"cientifico","es_overwatch","civil","personaje_lore","tecnologia_avanzada"},
    "Emily":         {"personaje_lore","civil","es_britanica"},
    "Gerard Lacroix": {"personaje_lore","civil","es_overwatch"},
    "Balderich":     {"personaje_lore","usa_martillo","usa_escudo"},
    "Antonio Bartalotti": {"personaje_lore","civil","es_talon","es_lider"},
    "Katya Volskaya": {"personaje_lore","es_rusa","civil","es_lider"},
    "Dr. Harold Winston": {"personaje_lore","es_overwatch","cientifico","civil"},
}

# ──────────────────────────────────────────────
#  PREGUNTAS Y REGLAS
# ──────────────────────────────────────────────
PREGUNTAS = [
    ("¿Es un héroe tanque?",                    "rol_tanque"),
    ("¿Es un héroe de daño (DPS)?",             "rol_dano"),
    ("¿Es un héroe de apoyo?",                  "rol_apoyo"),
    ("¿Es parte del lore?",                     "personaje_lore"),
    ("¿Cura aliados?",                          "cura_aliados"),
    ("¿Usa armas de fuego?",                    "usa_arma_de_fuego"),
    ("¿Usa escudo?",                            "usa_escudo"),
    ("¿Puede volar?",                           "puede_volar"),
    ("¿Pertenece o estuvo en Talon?",           "es_talon"),
    ("¿Pertenece o estuvo en Overwatch?",       "es_overwatch"),
    ("¿Es ómnico o robot?",                     "es_omnico"),
    ("¿Es un animal?",                          "es_animal"),
    ("¿Usa espada?",                            "usa_espada"),
    ("¿Usa martillo?",                          "usa_martillo"),
    ("¿Usa arco?",                              "usa_arco"),
    ("¿Usa baston?",                            "usa_baston"),
    ("¿Usa guante como arma principal?",        "usa_guante"),
    ("¿Usa hacha?",                             "usa_hacha"),
    ("¿Usa lanza?",                             "usa_lanza"),
    ("¿Usa cañón?",                             "usa_canon"),
    ("¿Usa ametralladora?",                     "usa_ametralladora"),
    ("¿Usa múltiples ametralladoras?",          "usa_ametralladoras"),
    ("¿Usa rifle?",                             "usa_rifle"),
    ("¿Usa revólver?",                          "usa_revolver"),
    ("¿Usa granadas?",                          "usa_granadas"),
    ("¿Usa visor táctico?",                     "usa_visor"),
    ("¿Usa railgun?",                           "usa_railgun"),
    ("¿Usa láser?",                             "usa_laser"),
    ("¿Usa kunai?",                             "usa_kunai"),
    ("¿Usa dragones o invoca criaturas?",       "usa_dragones"),
    ("¿Usa barreras?",                          "usa_barreras"),
    ("¿Usa energía como arma?",                 "usa_energia"),
    ("¿Usa sniper?",                            "usa_sniper"),
    ("¿Usa explosivos?",                        "usa_explosivos"),
    ("¿Tiene alta movilidad?",                  "alta_movilidad"),
    ("¿Es una asistente virtual?",              "ia"),
    ("¿Es una persona normal?",                 "civil"),
    ("¿Es científico o trabaja con ciencia?",   "cientifico"),
    ("¿Puede saltar grandes distancias?",       "puede_saltar"),
    ("¿Puede retroceder en el tiempo?",         "puede_retroceder_tiempo"),
    ("¿Tiene forma alternativa o transformación?", "forma_nemesis"),
    ("¿Explora o es aventurero?",               "explorador"),
    ("¿Usa tecnología avanzada?",               "tecnologia_avanzada"),
    ("¿Pelea cuerpo a cuerpo?",                 "combate_cuerpo_a_cuerpo"),
    ("¿Es de Junkertown?",                      "es_de_junkertown"),
    ("¿Es caótico o impredecible?",             "caotico"),
    ("¿Es líder de un grupo?",                  "es_lider"),
    ("¿Tiene compañero o mascota?",             "tiene_companero"),
    ("¿Usa armadura?",                          "usa_armadura"),
    ("¿Es japonés o japonesa?",                 "es_japones"),
    ("¿Usa hielo?",                             "usa_hielo"),
    ("¿Usa música?",                            "usa_musica"),
    ("¿Usa orbes?",                             "usa_orbes"),
    ("¿Puede hackear?",                         "hackea"),
    ("¿Usa torreta?",                           "usa_torreta"),
    ("¿Usa mecha?",                             "usa_mecha"),
    ("¿Es cyborg?",                             "es_cyborg"),
    ("¿Usa máscara?",                           "usa_mascara"),
    ("¿Protege aliados?",                       "protege_aliados"),
    ("¿Es grande o imponente físicamente?",     "gran_tamano"),
    ("¿Puede teletransportarse?",               "puede_teletransportarse"),
    ("¿Puede volverse invisible?",              "puede_volverse_invisible"),
    ("¿Crea portales o zonas de acceso?",       "crea_portal"),
    ("¿Usa cohetes?",                           "usa_cohetes"),
    ("¿Revive aliados?",                        "revive_aliados"),
    ("¿Drena vida de enemigos?",                "drena_vida"),
    ("¿Es de Egipto?",                          "es_egipcia"),
    ("¿Es ruso o rusa?",                        "es_rusa"),
    ("¿Es alemán?",                             "es_aleman"),
    ("¿Es de Irlanda?",                         "es_irlandesa"),
    ("¿Tiene estilo vaquero?",                  "estilo_vaquero"),
    ("¿Usa gancho?",                            "usa_gancho"),
    ("¿Controla gravedad?",                     "controla_gravedad"),
    ("¿Es veterano con mucha experiencia?",     "veterano"),
    ("¿Es ingeniero o mecánico?",               "es_ingeniero"),
    ("¿Excava o usa taladro?",                  "excava"),
    ("¿Puede copiar habilidades?",              "puede_copiar"),
    ("¿Usa el sol o luz solar?",                "usa_sol"),
    ("¿Es espacial o viajó al espacio?",        "espacial"),
    ("¿Es un monje o líder espiritual?",        "monje"),
    ("¿Aumenta la velocidad de aliados?",       "aumenta_velocidad"),
    ("¿Usa pistolas (no rifles)?",              "usa_pistolas"),
    ("¿Usa escopeta?",                          "usa_escopeta"),
    ("¿Es mexicano o mexicana?",                "es_mexicana"),
    ("¿Es brasileño?",                          "es_brasileno"),
    ("¿Es de china?",                           "es_china"),
    ("¿Es africano o africana?",                "es_africano"),
    ("¿Es de una isla?",                        "es_de_isla"),
    ("¿Es estadounidense?",                     "es_americano"),
    ("¿Es canadiense?",                         "es_canadiense"),
    ("¿Es francesa?",                           "es_francesa"),
    ("¿Es sueco o sueca?",                      "es_sueco"),
    ("¿Es suizo o suiza?",                      "es_suiza"),
    ("¿Es tailandés?",                          "es_tailandes"),
    ("¿Es peruano?",                            "es_peruana"),
    ("¿Es haitiano?",                           "es_haitiano"),
    ("¿Es indio o india?",                      "es_india"),
]

REGLAS = [
    {"si": {"rol_tanque"},              "entonces": "categoria_tanque"},
    {"si": {"rol_dano"},                "entonces": "categoria_dano"},
    {"si": {"rol_apoyo"},               "entonces": "categoria_apoyo"},
    {"si": {"cura_aliados"},            "entonces": "puede_mantener_vivo_equipo"},
    {"si": {"usa_escudo"},              "entonces": "protege_aliados"},
    {"si": {"es_talon"},                "entonces": "posible_villano"},
    {"si": {"es_overwatch"},            "entonces": "posible_heroe"},
    {"si": {"es_omnico"},               "entonces": "ser_artificial"},
    {"si": {"usa_arma_de_fuego"},       "entonces": "ataque_distancia"},
    {"si": {"alta_movilidad"},          "entonces": "dificil_de_atrapar"},
    {"si": {"combate_cuerpo_a_cuerpo"}, "entonces": "ataque_cercano"},
    {"si": {"cientifico","tecnologia_avanzada"}, "entonces": "mente_tecnica"},
    {"si": {"rol_apoyo","cura_aliados"}, "entonces": "sanador"},
    {"si": {"rol_tanque","usa_escudo"}, "entonces": "tanque_defensivo"},
    {"si": {"rol_dano","alta_movilidad"}, "entonces": "dps_movil"},
]

# ──────────────────────────────────────────────
#  PERSISTENCIA
# ──────────────────────────────────────────────
def guardar_base(personajes):
    with open(ARCHIVO_DB, "w", encoding="utf-8") as f:
        json.dump({n: list(a) for n, a in personajes.items()}, f, indent=4, ensure_ascii=False)

def cargar_base():
    if os.path.exists(ARCHIVO_DB):
        with open(ARCHIVO_DB, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return {n: set(a) for n, a in datos.items()}
    guardar_base(base_inicial)
    return {n: set(a) for n, a in base_inicial.items()}

# ──────────────────────────────────────────────
#  LÓGICA DEL JUEGO
# ──────────────────────────────────────────────
def encadenamiento(hechos):
    cambio = True
    while cambio:
        cambio = False
        for regla in REGLAS:
            c = regla["si"]; e = regla["entonces"]
            if c.issubset(hechos) and e not in hechos:
                hechos.add(e); cambio = True
    return hechos

def filtrar(personajes, pos, neg):
    return [n for n, a in personajes.items()
            if pos.issubset(a) and not neg.intersection(a)]

def mejor_pregunta(personajes, candidatos, restantes):
    mejor, mejor_diff = None, 9999
    for p, h in restantes:
        si  = sum(1 for c in candidatos if h in personajes[c])
        no_ = len(candidatos) - si
        if si == 0 or no_ == 0:
            continue
        d = abs(si - no_)
        if d < mejor_diff:
            mejor_diff = d; mejor = (p, h)
    return mejor

# ──────────────────────────────────────────────
#  INTERFAZ PYGAME
# ──────────────────────────────────────────────
class Button:
    def __init__(self, rect, text, color_normal, color_hover, text_color=C_TEXT, font=None):
        self.rect   = pygame.Rect(rect)
        self.text   = text
        self.cn     = color_normal
        self.ch     = color_hover
        self.tc     = text_color
        self.font   = font
        self.hovered= False

    def draw(self, surf):
        col = self.ch if self.hovered else self.cn
        pygame.draw.rect(surf, col, self.rect, border_radius=10)
        pygame.draw.rect(surf, C_ACCENT, self.rect, 2, border_radius=10)
        if self.font:
            txt = self.font.render(self.text, True, self.tc)
            surf.blit(txt, txt.get_rect(center=self.rect.center))

    def update(self, mx, my):
        self.hovered = self.rect.collidepoint(mx, my)

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and self.rect.collidepoint(event.pos))


class TextInput:
    """Campo de texto simple para ingresar nombre."""
    def __init__(self, rect, font, placeholder=""):
        self.rect   = pygame.Rect(rect)
        self.font   = font
        self.text   = ""
        self.active = True
        self.placeholder = placeholder

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key not in (pygame.K_RETURN, pygame.K_ESCAPE):
                if len(self.text) < 40:
                    self.text += event.unicode

    def draw(self, surf):
        pygame.draw.rect(surf, C_PANEL, self.rect, border_radius=8)
        pygame.draw.rect(surf, C_ACCENT, self.rect, 2, border_radius=8)
        display = self.text if self.text else self.placeholder
        color   = C_TEXT if self.text else C_DIMTEXT
        txt = self.font.render(display, True, color)
        surf.blit(txt, (self.rect.x + 12, self.rect.centery - txt.get_height()//2))


class AkinatorApp:
    MENU     = "menu"
    QUESTION = "question"
    RESULT   = "result"
    LEARN    = "learn"

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Akinator Overwatch")
        self.clock  = pygame.time.Clock()

        # Fonts
        pygame.freetype.init()
        self.f_title  = pygame.font.SysFont("Impact", 56)
        self.f_big    = pygame.font.SysFont("Segoe UI", 32, bold=True)
        self.f_med    = pygame.font.SysFont("Segoe UI", 24)
        self.f_small  = pygame.font.SysFont("Segoe UI", 18)
        self.f_input  = pygame.font.SysFont("Segoe UI", 22)

        self.personajes = cargar_base()
        self._init_state()
        self._build_menu()
        
        # NUEVO: Variable para almacenar la imagen del personaje (LÍNEA 487)
        self.imagen_personaje = None

    # ── Estado del juego ──────────────────────
    def _init_state(self):
        self.state       = self.MENU
        self.pos         = set()
        self.neg         = set()
        self.restantes   = list(PREGUNTAS)
        self.candidatos  = list(self.personajes.keys())
        self.pregunta_actual = None
        self.hecho_actual    = None
        self.resultado       = None
        self.resultado_tipo  = None   # "exacto" | "varios" | "nadie"
        self.learn_step  = 0          # 0=nombre, 1=confirmar
        self.learn_nombre = ""
        self.text_input  = None
        self.learn_attrs_seleccionados = set()
        self.msg_aprendido = ""
        self.num_pregunta  = 0
        self.particulas    = []

    # ── Botones ───────────────────────────────
    def _build_menu(self):
        cx = ANCHO // 2
        self.btn_jugar  = Button((cx-130, 320, 260, 60), "JUGAR", C_PANEL, C_BTN_HOVER, C_ACCENT, self.f_big)
        self.btn_salir  = Button((cx-130, 400, 260, 60), "SALIR", C_PANEL, C_BTN_HOVER, C_NO,    self.f_big)

    def _build_question_btns(self):
        cx = ANCHO // 2
        self.btn_si  = Button((cx-220, 470, 200, 65), "✓  SÍ",  (20,80,30), (30,140,50),  C_YES, self.f_big)
        self.btn_no  = Button((cx+20,  470, 200, 65), "✗  NO",  (80,20,20), (140,30,30),  C_NO,  self.f_big)
        self.btn_menu_q = Button((20, 20, 110, 38), "← Menú", C_PANEL, C_BTN_HOVER, C_DIMTEXT, self.f_small)

    def _build_result_btns(self):
        cx = ANCHO // 2
        self.btn_otra    = Button((cx-200, 560, 185, 55), "OTRA VEZ",  C_PANEL, C_BTN_HOVER, C_ACCENT,  self.f_med)
        self.btn_incorr  = Button((cx+20,  560, 185, 55), "INCORRECTO", C_PANEL, C_BTN_HOVER, C_ACCENT2, self.f_med)

    def _build_learn_btns(self):
        cx = ANCHO // 2
        self.btn_confirm = Button((cx-100, 570, 200, 52), "GUARDAR", C_PANEL, C_BTN_HOVER, C_YES, self.f_med)
        self.btn_cancel  = Button((cx-100, 630, 200, 40), "CANCELAR", C_PANEL, C_BTN_HOVER, C_NO,  self.f_small)

    # ── Transiciones de estado ─────────────────
    def start_game(self):
        self._init_state()
        self.candidatos = list(self.personajes.keys())
        self.restantes  = list(PREGUNTAS)
        self._next_question()
        self._build_question_btns()

    def _next_question(self):
        self.candidatos = filtrar(self.personajes, self.pos, self.neg)
        if len(self.candidatos) == 1:
            self._set_result(self.candidatos[0], "exacto"); return
        if len(self.candidatos) == 0:
            self._set_result(None, "nadie"); return
        sel = mejor_pregunta(self.personajes, self.candidatos, self.restantes)
        if sel is None:
            top = self.candidatos[:3]
            self._set_result(top, "varios"); return
        self.pregunta_actual, self.hecho_actual = sel
        self.restantes.remove(sel)
        self.num_pregunta += 1
        self.state = self.QUESTION

    # NUEVO: Método _set_result modificado para cargar la imagen (LÍNEAS 566-579)
    def _set_result(self, res, tipo):
        self.resultado      = res
        self.resultado_tipo = tipo
        self.state = self.RESULT
        self._build_result_btns()
        
        if tipo == "exacto":
            self._spawn_particles()
            # Cargar la imagen del personaje
            self.imagen_personaje = cargar_imagen_personaje(res)
        else:
            self.imagen_personaje = None

    def answer(self, yes: bool):
        if yes:
            self.pos.add(self.hecho_actual)
        else:
            self.neg.add(self.hecho_actual)
        self._next_question()

    def go_learn(self):
        self.state = self.LEARN
        self.learn_step  = 0
        self.learn_nombre = ""
        self.text_input   = TextInput((ANCHO//2 - 250, 280, 500, 48), self.f_input, "Escribe el nombre del personaje…")
        self._build_learn_btns()

    def save_learned(self):
        nombre = self.text_input.text.strip()
        if not nombre:
            self.msg_aprendido = "⚠ Escribe un nombre válido."; return
        nuevos = self.pos.copy()
        self.personajes[nombre] = nuevos
        guardar_base(self.personajes)
        self.msg_aprendido = f"✅ '{nombre}' aprendido. ¡Gracias!"
        self.learn_step = 1   # Mostrar confirmación breve

    # ── Partículas ────────────────────────────
    def _spawn_particles(self):
        import random
        self.particulas = []
        for _ in range(60):
            self.particulas.append({
                "x": random.randint(0, ANCHO), "y": random.randint(ALTO//2-100, ALTO//2+100),
                "vx": random.uniform(-3, 3), "vy": random.uniform(-5, -1),
                "life": random.randint(40, 80),
                "color": random.choice([C_GOLD, C_ACCENT, C_YES, (255,255,255)])
            })

    def _update_particles(self):
        for p in self.particulas:
            p["x"] += p["vx"]; p["y"] += p["vy"]
            p["vy"] += 0.12; p["life"] -= 1
        self.particulas = [p for p in self.particulas if p["life"] > 0]

    # ── Dibujado ──────────────────────────────
    def _draw_bg(self):
        self.screen.fill(C_BG)
        # Grid sutil
        for x in range(0, ANCHO, 60):
            pygame.draw.line(self.screen, (15,25,50), (x,0), (x,ALTO))
        for y in range(0, ALTO, 60):
            pygame.draw.line(self.screen, (15,25,50), (0,y), (ANCHO,y))
        # Borde decorativo
        pygame.draw.rect(self.screen, C_BORDER, (0,0,ANCHO,ALTO), 3)

    def _draw_header(self, subtitle=""):
        title = self.f_title.render("AKINATOR OVERWATCH", True, C_ACCENT)
        self.screen.blit(title, title.get_rect(centerx=ANCHO//2, y=28))
        if subtitle:
            sub = self.f_small.render(subtitle, True, C_DIMTEXT)
            self.screen.blit(sub, sub.get_rect(centerx=ANCHO//2, y=94))
        pygame.draw.line(self.screen, C_ACCENT, (60, 118), (ANCHO-60, 118), 2)

    def _draw_text_wrapped(self, text, font, color, x, y, max_w):
        words = text.split()
        lines, line = [], ""
        for w in words:
            test = line + (" " if line else "") + w
            if font.size(test)[0] <= max_w:
                line = test
            else:
                if line: lines.append(line)
                line = w
        if line: lines.append(line)
        for i, l in enumerate(lines):
            surf = font.render(l, True, color)
            self.screen.blit(surf, (x, y + i * (font.get_height() + 6)))
        return y + len(lines) * (font.get_height() + 6)

    def draw_menu(self):
        self._draw_bg()
        self._draw_header("Piensa en un personaje de Overwatch y lo adivinaré")
        # Logo decorativo
        pygame.draw.circle(self.screen, C_PANEL, (ANCHO//2, 230), 72)
        pygame.draw.circle(self.screen, C_ACCENT, (ANCHO//2, 230), 72, 3)
        icon = self.f_title.render("OW", True, C_ACCENT)
        self.screen.blit(icon, icon.get_rect(center=(ANCHO//2, 230)))

        self.btn_jugar.draw(self.screen)
        self.btn_salir.draw(self.screen)

        credits = self.f_small.render("Powered por IA con encadenamiento hacia adelante", True, C_DIMTEXT)
        self.screen.blit(credits, credits.get_rect(centerx=ANCHO//2, y=ALTO-34))

    def draw_question(self):
        self._draw_bg()
        self._draw_header(f"Pregunta {self.num_pregunta}  •  {len(self.candidatos)} personaje(s) posible(s)")

        # Panel central
        panel = pygame.Rect(60, 135, ANCHO-120, 310)
        pygame.draw.rect(self.screen, C_PANEL, panel, border_radius=16)
        pygame.draw.rect(self.screen, C_BORDER, panel, 2, border_radius=16)

        q = self.pregunta_actual or "…"
        self._draw_text_wrapped(q, self.f_big, C_TEXT, panel.x+30, panel.y+30, panel.width-60)

        # Pista: candidatos visibles
        if len(self.candidatos) <= 6:
            hint_y = panel.y + 160
            hint = self.f_small.render("Posibles: " + ", ".join(self.candidatos[:6]), True, C_DIMTEXT)
            self.screen.blit(hint, (panel.x+20, hint_y))

        # Barra de progreso
        total = len(PREGUNTAS)
        used  = total - len(self.restantes)
        bar_w = ANCHO - 120
        pygame.draw.rect(self.screen, C_BORDER, (60, 458, bar_w, 8), border_radius=4)
        fill = int(bar_w * (used / total))
        pygame.draw.rect(self.screen, C_ACCENT, (60, 458, fill, 8), border_radius=4)

        self.btn_si.draw(self.screen)
        self.btn_no.draw(self.screen)
        self.btn_menu_q.draw(self.screen)

        tip = self.f_small.render("Pulsa  S = Sí  •  N = No", True, C_DIMTEXT)
        self.screen.blit(tip, tip.get_rect(centerx=ANCHO//2, y=550))

    # NUEVO: Método draw_result completamente modificado (LÍNEAS 725-813)
    def draw_result(self):
        self._draw_bg()
        self._update_particles()
        for p in self.particulas:
            a = max(0, min(255, int(255 * p["life"] / 80)))
            s = pygame.Surface((8,8), pygame.SRCALPHA)
            s.fill((*p["color"], a))
            self.screen.blit(s, (int(p["x"]), int(p["y"])))

        if self.resultado_tipo == "exacto":
            self._draw_header("¡Lo adiviné!")
            panel = pygame.Rect(80, 140, ANCHO-160, 380)
            pygame.draw.rect(self.screen, C_PANEL, panel, border_radius=18)
            pygame.draw.rect(self.screen, C_GOLD,  panel, 3, border_radius=18)

            # Mostrar imagen del personaje si existe
            if self.imagen_personaje:
                # Posición de la imagen (lado izquierdo del panel)
                img_x = panel.x + 30
                img_y = panel.y + 50
                self.screen.blit(self.imagen_personaje, (img_x, img_y))
                
                # Ajustar posición del texto para que no se superponga
                txt_x = img_x + 220
                txt_y = img_y + 40
                
                txt = self.f_big.render("Tu personaje es…", True, C_DIMTEXT)
                self.screen.blit(txt, txt.get_rect(x=txt_x, y=txt_y))
                
                big = self.f_title.render(str(self.resultado), True, C_GOLD)
                big_rect = big.get_rect(x=txt_x, y=txt_y + 50)
                # Asegurar que el texto no se salga de la pantalla
                if big_rect.right > ANCHO - 30:
                    big = self.f_med.render(str(self.resultado), True, C_GOLD)
                    big_rect = big.get_rect(x=txt_x, y=txt_y + 50)
                self.screen.blit(big, big_rect)
            else:
                txt = self.f_big.render("Tu personaje es…", True, C_DIMTEXT)
                self.screen.blit(txt, txt.get_rect(centerx=ANCHO//2, y=180))
                big = self.f_title.render(str(self.resultado), True, C_GOLD)
                self.screen.blit(big, big.get_rect(centerx=ANCHO//2, y=250))

            q_txt = self.f_small.render(f"Resuelto en {self.num_pregunta} preguntas", True, C_DIMTEXT)
            self.screen.blit(q_txt, q_txt.get_rect(centerx=ANCHO//2, y=360))

        elif self.resultado_tipo == "varios":
            self._draw_header("No estoy seguro…")
            panel = pygame.Rect(80, 140, ANCHO-160, 380)
            pygame.draw.rect(self.screen, C_PANEL, panel, border_radius=18)
            pygame.draw.rect(self.screen, C_ACCENT2, panel, 2, border_radius=18)
            txt = self.f_big.render("¿Es uno de estos?", True, C_TEXT)
            self.screen.blit(txt, txt.get_rect(centerx=ANCHO//2, y=180))
            for i, nombre in enumerate(self.resultado[:5]):
                n_txt = self.f_med.render(f"• {nombre}", True, C_ACCENT)
                self.screen.blit(n_txt, n_txt.get_rect(centerx=ANCHO//2, y=250+i*42))
        else:
            self._draw_header("No encontré ningún personaje")
            panel = pygame.Rect(80, 140, ANCHO-160, 360)
            pygame.draw.rect(self.screen, C_PANEL, panel, border_radius=18)
            pygame.draw.rect(self.screen, C_NO,    panel, 2, border_radius=18)
            txt = self.f_big.render("¡Enséñame este personaje!", True, C_TEXT)
            self.screen.blit(txt, txt.get_rect(centerx=ANCHO//2, y=210))
            sub = self.f_med.render("Presiona 'Incorrecto / Aprender' para añadirlo.", True, C_DIMTEXT)
            self.screen.blit(sub, sub.get_rect(centerx=ANCHO//2, y=280))

        self.btn_otra.draw(self.screen)
        self.btn_incorr.draw(self.screen)

    def draw_learn(self):
        self._draw_bg()
        self._draw_header("Aprendizaje — ¿Quién era el personaje?")
        if self.learn_step == 1:
            ok = self.f_big.render(self.msg_aprendido, True, C_YES)
            self.screen.blit(ok, ok.get_rect(centerx=ANCHO//2, y=300))
            back = self.f_med.render("Pulsa cualquier tecla o haz clic para volver al menú.", True, C_DIMTEXT)
            self.screen.blit(back, back.get_rect(centerx=ANCHO//2, y=370))
            return

        panel = pygame.Rect(60, 135, ANCHO-120, 400)
        pygame.draw.rect(self.screen, C_PANEL, panel, border_radius=14)
        pygame.draw.rect(self.screen, C_ACCENT2, panel, 2, border_radius=14)

        inst = self.f_med.render("Escribe el nombre del personaje correcto:", True, C_DIMTEXT)
        self.screen.blit(inst, inst.get_rect(centerx=ANCHO//2, y=160))

        self.text_input.draw(self.screen)

        info = self.f_small.render(
            "Las características que respondiste 'Sí' se guardarán automáticamente.",
            True, C_DIMTEXT)
        self.screen.blit(info, info.get_rect(centerx=ANCHO//2, y=360))

        if self.msg_aprendido:
            err = self.f_small.render(self.msg_aprendido, True, C_ACCENT2)
            self.screen.blit(err, err.get_rect(centerx=ANCHO//2, y=430))

        self.btn_confirm.draw(self.screen)
        self.btn_cancel.draw(self.screen)

    # ── Bucle principal ───────────────────────
    def run(self):
        while True:
            mx, my = pygame.mouse.get_pos()
            events = pygame.event.get()

            for ev in events:
                if ev.type == pygame.QUIT:
                    guardar_base(self.personajes)
                    pygame.quit(); sys.exit()

                # ── Menú
                if self.state == self.MENU:
                    self.btn_jugar.update(mx, my)
                    self.btn_salir.update(mx, my)
                    if self.btn_jugar.clicked(ev): self.start_game()
                    if self.btn_salir.clicked(ev):
                        guardar_base(self.personajes)
                        pygame.quit(); sys.exit()
                    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                        self.start_game()

                # ── Pregunta
                elif self.state == self.QUESTION:
                    self.btn_si.update(mx, my)
                    self.btn_no.update(mx, my)
                    self.btn_menu_q.update(mx, my)
                    if self.btn_si.clicked(ev)     : self.answer(True)
                    if self.btn_no.clicked(ev)     : self.answer(False)
                    if self.btn_menu_q.clicked(ev) : self.state = self.MENU; self._build_menu()
                    if ev.type == pygame.KEYDOWN:
                        if ev.key in (pygame.K_s, pygame.K_y): self.answer(True)
                        if ev.key == pygame.K_n             : self.answer(False)

                # ── Resultado
                elif self.state == self.RESULT:
                    self.btn_otra.update(mx, my)
                    self.btn_incorr.update(mx, my)
                    if self.btn_otra.clicked(ev)  : self.start_game()
                    if self.btn_incorr.clicked(ev): self.go_learn()
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_r: self.start_game()
                        if ev.key == pygame.K_i: self.go_learn()

                # ── Aprendizaje
                elif self.state == self.LEARN:
                    if self.learn_step == 1:
                        if (ev.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN)):
                            self.state = self.MENU; self._build_menu()
                    else:
                        self.btn_confirm.update(mx, my)
                        self.btn_cancel.update(mx, my)
                        self.text_input.handle(ev)
                        if self.btn_confirm.clicked(ev): self.save_learned()
                        if self.btn_cancel.clicked(ev) :
                            self.state = self.MENU; self._build_menu()
                        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                            self.save_learned()

            # ── Dibujo
            if   self.state == self.MENU    : self.draw_menu()
            elif self.state == self.QUESTION: self.draw_question()
            elif self.state == self.RESULT  : self.draw_result()
            elif self.state == self.LEARN   : self.draw_learn()

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    AkinatorApp().run()