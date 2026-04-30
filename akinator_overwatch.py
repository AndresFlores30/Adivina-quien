import json
import os

ARCHIVO_DB = "personajes_overwatch.json"

# Mapeo de atributos internos a texto amigable
ATRIBUTOS_LEGIBLES = {
    "rol_tanque": "rol tanque",
    "usa_mecha": "usa mecha", 
    "es_coreana": "es coreana",
    "usa_arma_de_fuego": "usa arma de fuego",
    "puede_volar": "puede volar",
    "es_heroina": "es heroína",
    "tecnologia_avanzada": "tecnología avanzada",
    "combate_cuerpo_a_cuerpo": "combate cuerpo a cuerpo",
    "ataque_distancia": "ataque a distancia",
    "es_de_junkertown": "es de Junkertown",
    "gran_tamano": "gran tamaño",
    "usa_mascara": "usa máscara",
    "alta_movilidad": "alta movilidad",
    "cura_aliados": "cura aliados",
    "protege_aliados": "protege aliados",
    "es_talon": "es de Talon",
    "es_overwatch": "es de Overwatch",
    "es_omnico": "es ómnico",
    "es_animal": "es animal",
    "usa_escudo": "usa escudo",
    "usa_espada": "usa espada",
    "usa_martillo": "usa martillo",
    "usa_arco": "usa arco",
    "usa_sniper": "usa sniper",
    "usa_explosivos": "usa explosivos",
    "cientifico": "científico",
    "personaje_lore": "personaje del lore",
    "personaje_extra": "personaje extra",
    "usa_hielo": "usa hielo",
    "usa_musica": "usa música",
    "usa_orbes": "usa orbes",
    "hackea": "hackea",
    "usa_torreta": "usa torreta",
    "es_cyborg": "es cyborg",
    "categoria_combate_frontal": "combate frontal",
    "categoria_eliminacion": "eliminación",
    "categoria_soporte": "soporte",
    "puede_mantener_vivo_equipo": "puede mantener vivo al equipo",
    "posible_villano": "posible villano",
    "posible_heroe": "posible héroe",
    "ser_artificial": "ser artificial",
    "dificil_de_atrapar": "difícil de atrapar",
    "ataque_cercano": "ataque cercano",
    "mente_tecnica": "mente técnica",
    "sanador": "sanador",
    "tanque_defensivo": "tanque defensivo",
    "dps_movil": "DPS móvil",
    "rol_dano": "rol daño",
    "rol_apoyo": "rol apoyo",
    "usa_gancho": "usa gancho",
    "controla_gravedad": "controla gravedad",
    "usa_rayo": "usa rayo",
    "puede_saltar": "puede saltar",
    "usa_canon": "usa cañón",
    "usa_barreras": "usa barreras",
    "tiene_companero": "tiene compañero",
    "estilo_vaquero": "estilo vaquero",
    "modo_torreta": "modo torreta",
    "usa_revolver": "usa revolver",
    "puede_copiar": "puede copiar",
    "es_japones": "es japonés",
    "usa_dragones": "usa dragones",
    "usa_granadas": "usa granadas",
    "caotico": "caótico",
    "controla_zona": "controla zona",
    "usa_cohetes": "usa cohetes",
    "es_egipcia": "es egipcia",
    "usa_escopetas": "usa escopetas",
    "puede_teletransportarse": "puede teletransportarse",
    "usa_railgun": "usa railgun",
    "usa_visor": "usa visor",
    "veterano": "veterano",
    "puede_volverse_invisible": "puede volverse invisible",
    "usa_luz": "usa luz",
    "crea_portal": "crea portal",
    "es_ingeniero": "es ingeniero",
    "puede_retroceder_tiempo": "puede retroceder tiempo",
    "usa_pistolas": "usa pistolas",
    "excava": "excava",
    "usa_taladro": "usa taladro",
    "explorador": "explorador",
    "es_villana": "es villana",
    "es_villano": "es villano",
    "es_lider": "es líder",
    "usa_ametralladoras": "usa ametralladoras",
    "usa_ametralladora": "usa ametralladora",
    "forma_nemesis": "forma nemesis",
    "es_aleman": "es alemán",
    "es_rusa": "es rusa",
    "usa_escopeta": "usa escopeta",
    "usa_lanza": "usa lanza",
    "usa_hacha": "usa hacha",
    "usa_guante": "usa guante",
    "es_japonesa": "es japonesa",
    "usa_kunai": "usa kunai",
    "usa_espiritu": "usa espíritu",
    "usa_naturaleza": "usa naturaleza",
    "aumenta_velocidad": "aumenta velocidad",
    "revive_aliados": "revive aliados",
    "drena_vida": "drena vida",
    "monje": "monje",
    "espacial": "espacial",
    "usa_sol": "usa sol",
    "usa_maza": "usa maza",
    "ex_talon": "ex Talon",
    "ia": "IA",
    "ayuda_equipo": "ayuda al equipo",
    "pacifista": "pacifista",
    "lider_espiritual": "líder espiritual",
    "usa_traje_elegante": "usa traje elegante",
    "creadora": "creadora",
    "relacionada_orisa": "relacionada con Orisa",
    "relacionada_tracer": "relacionada con Tracer",
    "civil": "civil",
    "no_combatiente": "no combatiente",
    "relacionado_widowmaker": "relacionado con Widowmaker",
    "victima": "víctima",
    "cruzado": "cruzado",
    "mentor_reinhardt": "mentor de Reinhardt",
    "relacionado_winston": "relacionado con Winston",
    "lunar": "lunar",
    "mentor": "mentor",
    "blackwatch": "Blackwatch",
    "null_sector": "Null Sector",
    "usa_energia": "usa energía",
}

base_inicial = {
    # TANQUES
    "D.Va": {"rol_tanque", "usa_mecha", "es_coreana", "usa_arma_de_fuego", "puede_volar", "es_heroina", "tecnologia_avanzada"},
    "Doomfist": {"rol_tanque", "usa_guante", "es_talon", "combate_cuerpo_a_cuerpo", "es_villano", "alta_movilidad"},
    "Junker Queen": {"rol_tanque", "usa_hacha", "usa_escopeta", "es_de_junkertown", "combate_cuerpo_a_cuerpo", "es_lider"},
    "Mauga": {"rol_tanque", "usa_ametralladoras", "es_talon", "usa_arma_de_fuego", "es_villano", "gran_tamano"},
    "Orisa": {"rol_tanque", "es_omnico", "usa_lanza", "protege_aliados", "tecnologia_avanzada"},
    "Ramattra": {"rol_tanque", "es_omnico", "es_lider", "forma_nemesis", "combate_cuerpo_a_cuerpo", "es_villano"},
    "Reinhardt": {"rol_tanque", "usa_martillo", "usa_escudo", "es_overwatch", "combate_cuerpo_a_cuerpo", "es_aleman"},
    "Roadhog": {"rol_tanque", "usa_gancho", "usa_escopeta", "es_de_junkertown", "gran_tamano", "usa_mascara"},
    "Sigma": {"rol_tanque", "controla_gravedad", "es_talon", "cientifico", "tecnologia_avanzada"},
    "Winston": {"rol_tanque", "es_animal", "cientifico", "usa_rayo", "puede_saltar", "es_overwatch"},
    "Wrecking Ball": {"rol_tanque", "es_animal", "usa_mecha", "alta_movilidad", "es_de_junkertown"},
    "Zarya": {"rol_tanque", "usa_canon", "es_rusa", "usa_barreras", "protege_aliados", "usa_arma_de_fuego"},

    # DAÑO
    "Ashe": {"rol_dano", "usa_rifle", "usa_arma_de_fuego", "tiene_companero", "es_lider", "estilo_vaquero"},
    "Bastion": {"rol_dano", "es_omnico", "usa_ametralladora", "modo_torreta", "tecnologia_avanzada"},
    "Cassidy": {"rol_dano", "usa_revolver", "usa_arma_de_fuego", "estilo_vaquero", "es_overwatch"},
    "Echo": {"rol_dano", "es_omnico", "puede_volar", "tecnologia_avanzada", "puede_copiar"},
    "Genji": {"rol_dano", "usa_espada", "es_cyborg", "es_japones", "alta_movilidad", "combate_cuerpo_a_cuerpo"},
    "Hanzo": {"rol_dano", "usa_arco", "es_japones", "usa_dragones", "ataque_distancia"},
    "Junkrat": {"rol_dano", "usa_explosivos", "es_de_junkertown", "usa_granadas", "caotico"},
    "Mei": {"rol_dano", "usa_hielo", "cientifico", "controla_zona", "es_heroina"},
    "Pharah": {"rol_dano", "puede_volar", "usa_cohetes", "usa_arma_de_fuego", "es_egipcia"},
    "Reaper": {"rol_dano", "usa_escopetas", "es_talon", "puede_teletransportarse", "es_villano", "usa_mascara"},
    "Sojourn": {"rol_dano", "usa_railgun", "es_cyborg", "es_overwatch", "usa_arma_de_fuego", "alta_movilidad"},
    "Soldier: 76": {"rol_dano", "usa_rifle", "usa_arma_de_fuego", "es_overwatch", "usa_visor", "veterano"},
    "Sombra": {"rol_dano", "hackea", "es_talon", "puede_volverse_invisible", "usa_arma_de_fuego"},
    "Symmetra": {"rol_dano", "usa_luz", "usa_torretas", "crea_portal", "tecnologia_avanzada"},
    "Torbjorn": {"rol_dano", "usa_torreta", "es_ingeniero", "usa_martillo", "tecnologia_avanzada"},
    "Tracer": {"rol_dano", "alta_movilidad", "puede_retroceder_tiempo", "usa_pistolas", "es_overwatch"},
    "Venture": {"rol_dano", "excava", "usa_taladro", "explorador", "alta_movilidad"},
    "Widowmaker": {"rol_dano", "usa_sniper", "es_talon", "ataque_distancia", "es_villana"},
    "Sierra": {"rol_dano", "usa_arma_de_fuego", "alta_movilidad", "tecnologia_avanzada", "personaje_extra"},
    "Freja": {"rol_dano", "usa_arco", "alta_movilidad", "ataque_distancia", "personaje_extra"},
    "Emre": {"rol_dano", "es_cyborg", "es_overwatch", "usa_arma_de_fuego", "personaje_extra"},
    "Vendetta": {"rol_dano", "usa_espada", "combate_cuerpo_a_cuerpo", "es_talon", "personaje_extra"},

    # APOYO
    "Ana": {"rol_apoyo", "usa_sniper", "cura_aliados", "es_egipcia", "ataque_distancia", "es_overwatch"},
    "Baptiste": {"rol_apoyo", "cura_aliados", "usa_arma_de_fuego", "protege_aliados", "ex_talon"},
    "Brigitte": {"rol_apoyo", "usa_escudo", "usa_maza", "cura_aliados", "combate_cuerpo_a_cuerpo", "protege_aliados"},
    "Illari": {"rol_apoyo", "usa_sol", "cura_aliados", "usa_torreta", "ataque_distancia"},
    "Juno": {"rol_apoyo", "cura_aliados", "alta_movilidad", "espacial", "tecnologia_avanzada"},
    "Kiriko": {"rol_apoyo", "cura_aliados", "es_japonesa", "usa_kunai", "alta_movilidad", "usa_espiritu"},
    "Lifeweaver": {"rol_apoyo", "cura_aliados", "usa_naturaleza", "protege_aliados", "tecnologia_avanzada"},
    "Lucio": {"rol_apoyo", "cura_aliados", "usa_musica", "alta_movilidad", "aumenta_velocidad"},
    "Mercy": {"rol_apoyo", "cura_aliados", "puede_volar", "revive_aliados", "protege_aliados"},
    "Moira": {"rol_apoyo", "cura_aliados", "es_talon", "cientifico", "drena_vida"},
    "Zenyatta": {"rol_apoyo", "es_omnico", "cura_aliados", "usa_orbes", "monje"},
    "Jetpack Cat": {"rol_apoyo", "es_animal", "puede_volar", "cura_aliados", "personaje_extra"},
    "Mizuki": {"rol_apoyo", "cura_aliados", "alta_movilidad", "personaje_extra", "tecnologia_avanzada"},
    "Anran": {"rol_apoyo", "cura_aliados", "protege_aliados", "personaje_extra", "usa_energia"},

    # LORE / EXTRAS
    "Athena": {"ia", "es_overwatch", "tecnologia_avanzada", "personaje_lore", "ayuda_equipo"},
    "Mondatta": {"es_omnico", "monje", "personaje_lore", "pacifista", "lider_espiritual"},
    "Maximilien": {"es_omnico", "es_talon", "personaje_lore", "villano", "usa_traje_elegante"},
    "Efi Oladele": {"cientifico", "creadora", "personaje_lore", "tecnologia_avanzada", "relacionada_orisa"},
    "Emily": {"personaje_lore", "relacionada_tracer", "civil", "no_combatiente"},
    "Gerard Lacroix": {"personaje_lore", "relacionado_widowmaker", "es_overwatch", "victima"},
    "Balderich": {"personaje_lore", "usa_martillo", "usa_escudo", "cruzado", "mentor_reinhardt"},
    "Antonio Bartalotti": {"personaje_lore", "es_talon", "villano", "usa_traje_elegante"},
    "Katya Volskaya": {"personaje_lore", "es_rusa", "lider", "tecnologia_avanzada", "civil"},
    "Dr. Harold Winston": {"personaje_lore", "cientifico", "relacionado_winston", "lunar", "mentor"},
    "Tekhartha Zenyatta joven": {"es_omnico", "monje", "personaje_extra", "cura_aliados", "usa_orbes"},
    "Blackwatch Genji": {"rol_dano", "usa_espada", "es_cyborg", "blackwatch", "alta_movilidad"},
    "Blackwatch Cassidy": {"rol_dano", "usa_revolver", "usa_arma_de_fuego", "blackwatch", "estilo_vaquero"},
    "Commander Morrison": {"rol_dano", "usa_rifle", "es_overwatch", "veterano", "personaje_extra"},
    "Talon Baptiste": {"rol_apoyo", "cura_aliados", "ex_talon", "usa_arma_de_fuego", "personaje_extra"},
    "Null Sector Omnic": {"es_omnico", "villano", "null_sector", "personaje_extra", "tecnologia_avanzada"}
}

def guardar_base(personajes):
    with open(ARCHIVO_DB, "w", encoding="utf-8") as archivo:
        json.dump(
            {nombre: list(atributos) for nombre, atributos in personajes.items()},
            archivo,
            indent=4,
            ensure_ascii=False
        )

def cargar_base():
    if os.path.exists(ARCHIVO_DB):
        with open(ARCHIVO_DB, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            return {nombre: set(atributos) for nombre, atributos in datos.items()}
    else:
        guardar_base(base_inicial)
        return base_inicial.copy()

personajes = cargar_base()

preguntas = [
    ("¿Tu personaje es un héroe tanque?", "rol_tanque"),
    ("¿Tu personaje es un héroe de daño?", "rol_dano"),
    ("¿Tu personaje es un héroe de apoyo?", "rol_apoyo"),
    ("¿Tu personaje cura aliados?", "cura_aliados"),
    ("¿Tu personaje usa armas de fuego?", "usa_arma_de_fuego"),
    ("¿Tu personaje usa escudo?", "usa_escudo"),
    ("¿Tu personaje puede volar?", "puede_volar"),
    ("¿Tu personaje pertenece o estuvo relacionado con Talon?", "es_talon"),
    ("¿Tu personaje pertenece o estuvo relacionado con Overwatch?", "es_overwatch"),
    ("¿Tu personaje es ómnico o robot?", "es_omnico"),
    ("¿Tu personaje es un animal?", "es_animal"),
    ("¿Tu personaje usa espada?", "usa_espada"),
    ("¿Tu personaje usa martillo?", "usa_martillo"),
    ("¿Tu personaje usa arco?", "usa_arco"),
    ("¿Tu personaje usa sniper?", "usa_sniper"),
    ("¿Tu personaje usa explosivos?", "usa_explosivos"),
    ("¿Tu personaje tiene alta movilidad?", "alta_movilidad"),
    ("¿Tu personaje es científico o está relacionado con ciencia?", "cientifico"),
    ("¿Tu personaje usa tecnología avanzada?", "tecnologia_avanzada"),
    ("¿Tu personaje pelea cuerpo a cuerpo?", "combate_cuerpo_a_cuerpo"),
    ("¿Tu personaje es de Junkertown?", "es_de_junkertown"),
    ("¿Tu personaje es japonés o japonesa?", "es_japones"),
    ("¿Tu personaje usa hielo?", "usa_hielo"),
    ("¿Tu personaje usa música?", "usa_musica"),
    ("¿Tu personaje usa orbes?", "usa_orbes"),
    ("¿Tu personaje puede hackear?", "hackea"),
    ("¿Tu personaje usa torreta?", "usa_torreta"),
    ("¿Tu personaje usa mecha?", "usa_mecha"),
    ("¿Tu personaje es cyborg?", "es_cyborg"),
    ("¿Tu personaje usa máscara?", "usa_mascara"),
    ("¿Tu personaje es del lore y no necesariamente jugable?", "personaje_lore"),
    ("¿Tu personaje es una variante o personaje extra?", "personaje_extra"),
]

reglas = [
    {"si": {"rol_tanque"}, "entonces": "categoria_combate_frontal"},
    {"si": {"rol_dano"}, "entonces": "categoria_eliminacion"},
    {"si": {"rol_apoyo"}, "entonces": "categoria_soporte"},
    {"si": {"cura_aliados"}, "entonces": "puede_mantener_vivo_equipo"},
    {"si": {"usa_escudo"}, "entonces": "protege_aliados"},
    {"si": {"es_talon"}, "entonces": "posible_villano"},
    {"si": {"es_overwatch"}, "entonces": "posible_heroe"},
    {"si": {"es_omnico"}, "entonces": "ser_artificial"},
    {"si": {"usa_arma_de_fuego"}, "entonces": "ataque_distancia"},
    {"si": {"alta_movilidad"}, "entonces": "dificil_de_atrapar"},
    {"si": {"combate_cuerpo_a_cuerpo"}, "entonces": "ataque_cercano"},
    {"si": {"cientifico", "tecnologia_avanzada"}, "entonces": "mente_tecnica"},
    {"si": {"rol_apoyo", "cura_aliados"}, "entonces": "sanador"},
    {"si": {"rol_tanque", "usa_escudo"}, "entonces": "tanque_defensivo"},
    {"si": {"rol_dano", "alta_movilidad"}, "entonces": "dps_movil"},
]

def responder_si_no(pregunta):
    while True:
        respuesta = input(pregunta + " (s/n): ").lower().strip()

        if respuesta in ["s", "si", "sí"]:
            return True
        elif respuesta in ["n", "no"]:
            return False
        else:
            print("Respuesta inválida. Escribe solamente 's' o 'n'.")

def encadenamiento_hacia_delante(hechos):
    cambio = True

    while cambio:
        cambio = False

        for regla in reglas:
            condiciones = regla["si"]
            conclusion = regla["entonces"]

            if condiciones.issubset(hechos) and conclusion not in hechos:
                hechos.add(conclusion)
                cambio = True

    return hechos

def filtrar_personajes(hechos_positivos, hechos_negativos):
    candidatos = []

    for nombre, atributos in personajes.items():
        cumple_positivos = hechos_positivos.issubset(atributos)
        no_tiene_negativos = len(hechos_negativos.intersection(atributos)) == 0

        if cumple_positivos and no_tiene_negativos:
            candidatos.append(nombre)

    return candidatos

def mejor_pregunta(candidatos, preguntas_restantes):
    mejor = None
    mejor_diferencia = 9999

    for pregunta, hecho in preguntas_restantes:
        respuestas_si = 0
        respuestas_no = 0

        for candidato in candidatos:
            if hecho in personajes[candidato]:
                respuestas_si += 1
            else:
                respuestas_no += 1

        if respuestas_si == 0 or respuestas_no == 0:
            continue

        diferencia = abs(respuestas_si - respuestas_no)

        if diferencia < mejor_diferencia:
            mejor_diferencia = diferencia
            mejor = (pregunta, hecho)

    return mejor

def aprender_nuevo_personaje(hechos_positivos):
    print("\nNo pude adivinar correctamente.")
    print("Ayúdame a aprender para mejorar mi base de conocimiento.")

    nombre = input("\n¿Cuál era el personaje correcto?: ").strip()

    if nombre == "":
        print("No se agregó ningún personaje porque el nombre quedó vacío.")
        return

    print("\nAhora escribe características del personaje separadas por coma.")
    print("Puedes usar espacios en lugar de guiones bajos.")
    print("Ejemplo:")
    print("rol daño, usa arma de fuego, alta movilidad, es de Overwatch")

    atributos_input = input("\nCaracterísticas: ").strip()

    # Convertir espacios a guiones bajos para consistencia interna
    nuevos_atributos = set()
    for atributo in atributos_input.split(","):
        atributo = atributo.strip().lower()
        if atributo:
            # Reemplazar espacios por guiones bajos
            atributo_interno = atributo.replace(" ", "_")
            nuevos_atributos.add(atributo_interno)

    atributos_finales = hechos_positivos.union(nuevos_atributos)

    personajes[nombre] = atributos_finales
    guardar_base(personajes)

    print(f"\n✅ Personaje '{nombre}' agregado correctamente.")
    print("La próxima vez podré usarlo para adivinar.")

def jugar():
    print("\n🎮 AKINATOR OVERWATCH")
    print("Piensa en un personaje de Overwatch.")
    print("Responde con 's' para sí o 'n' para no.\n")

    hechos_positivos = set()
    hechos_negativos = set()
    preguntas_restantes = preguntas.copy()
    candidatos = list(personajes.keys())
    
    while len(candidatos) > 1 and preguntas_restantes:
        seleccion = mejor_pregunta(candidatos, preguntas_restantes)

        if seleccion is None:
            break

        pregunta_original, hecho = seleccion
        
        # Mostrar la pregunta con texto legible
        texto_legible = ATRIBUTOS_LEGIBLES.get(hecho, pregunta_original)
        if texto_legible != pregunta_original:
            pregunta_mostrar = f"¿Tu personaje {texto_legible}?"
        else:
            pregunta_mostrar = pregunta_original
            
        respuesta = responder_si_no(pregunta_mostrar)

        if respuesta:
            hechos_positivos.add(hecho)
        else:
            hechos_negativos.add(hecho)

        # Eliminar la pregunta del conjunto de disponibles
        preguntas_a_eliminar = []
        for p, h in preguntas_restantes:
            if h == hecho:
                preguntas_a_eliminar.append((p, h))
        
        for pregunta_eliminar in preguntas_a_eliminar:
            preguntas_restantes.remove(pregunta_eliminar)

        candidatos = filtrar_personajes(hechos_positivos, hechos_negativos)

    # Si queda exactamente un candidato
    if len(candidatos) == 1:
        personaje = candidatos[0]
        print(f"\n✅ ¡Tu personaje es: {personaje}!")
        
    # Si quedan varios candidatos
    elif len(candidatos) > 1:
        print(f"\n🤔 No pude determinar exactamente tu personaje.")
        print(f"Creo que podría ser uno de estos: {', '.join(candidatos[:3])}")
        aprender_nuevo_personaje(hechos_positivos)

    # Si no hay candidatos
    else:
        print(f"\n😕 No encontré ningún personaje con esas características.")
        aprender_nuevo_personaje(hechos_positivos)

def menu():
    while True:
        print("\n==================================================")
        print("AKINATOR OVERWATCH")
        print("==================================================")
        print("1. Jugar")
        print("2. Salir")

        opcion = input("\nElige una opción: ").strip()

        if opcion == "1":
            jugar()
        elif opcion == "2":
            print("\nGracias por jugar. ¡Hasta pronto!")
            break
        else:
            print("\nOpción inválida. Elige 1 o 2.")

if __name__ == "__main__":
    menu()