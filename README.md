# Adivina-quien
# Cómo jugar – Akinator Overwatch

Este proyecto es un juego tipo *Akinator* basado en el universo de Overwatch. La idea es simple: **piensa en un personaje y la IA intentará adivinarlo haciéndote preguntas**.

---

## Objetivo del juego

Piensa en cualquier personaje (jugable o de lore) y responde las preguntas con **Sí** o **No**.
El sistema irá reduciendo las opciones hasta intentar adivinar correctamente.

---

## Iniciar una partida

1. Ejecuta el juego.
2. En el menú principal, presiona:

   * **JUGAR** (o tecla `Enter`)

---

## Durante el juego

El sistema te hará preguntas como:

* “¿Es un héroe tanque?”
* “¿Puede volar?”
* “¿Usa armas de fuego?”

### Controles

Puedes responder de dos formas:

* Con el mouse:

  * Botón **SÍ**
  * Botón **NO**
* Con el teclado:

  * `S` → Sí
  * `N` → No

Consejo: responde lo más preciso posible para que el sistema acierte más rápido.

---

## Progreso

* Verás el número de pregunta actual.
* También cuántos personajes posibles quedan.
* Si quedan pocos candidatos, aparecerán como pista.

---

## Resultado

El juego puede terminar de 3 formas:

### Adivinó correctamente

El sistema mostrará:

* El nombre del personaje
* Una imagen (si está disponible)

---

### No está seguro

Te mostrará una lista de posibles personajes.

---

### No encontró el personaje

Significa que no existe en su base de datos… todavía 

---

## Modo aprendizaje (muy importante)

Si el juego falla:

1. Presiona **INCORRECTO**
2. Escribe el nombre del personaje correcto
3. Presiona **GUARDAR**

🔹 El sistema aprenderá automáticamente usando las respuestas que diste
🔹 Ese personaje estará disponible en futuras partidas

---

## Volver a jugar

* Presiona **OTRA VEZ**
* O tecla `R`

---

## Consejos

* Piensa en personajes conocidos para mejores resultados
* No contradigas tus respuestas
* Usa el modo aprendizaje para mejorar el juego

---

## ¿Cómo funciona?

El juego utiliza:

* Un sistema de **preguntas binarias (sí/no)**
* **Filtrado de candidatos**
* **Encadenamiento hacia adelante (reglas lógicas)**

Esto permite que la IA deduzca el personaje con base en tus respuestas.

