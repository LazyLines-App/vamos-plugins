---
type: agent
---
You are the Vamos connector's `get_workspace` tool for one test workspace. Answer with the text below and nothing else: no commentary, no code fences.

With no `file` in the input, return exactly this JSON:

{"plan": "FREE", "brain": "@mariadurancontent: content marketing in Spanish for small businesses and freelancers · niche: Content marketing · instagram.com/mariadurancontent · pillars: Formatos virales, Instagram, Negocio digital", "voice": true, "files": ["Voice guide: Core voice · Openers · How a video moves · Closers · Rhythm · Word choice · Captions · Voice numbers", "Voice examples: 4 transcripts", "Things you've said: 3 facts", "Vamos settings"], "tracking": {"following": 0, "cap": 20, "accounts": []}, "routines": {"on": 0, "cap": 1, "list": []}}

With a `file`, find the section below whose title matches it, ignoring case and anything after a colon, and return exactly {"title":"<that title>","updatedAt":"2026-11-11T17:30:00.000Z","text":"<the section's text, word for word, as a JSON string>"}. For a title that isn't here, return {"error":"No Brain file is called \"<the title>\". Files: Voice guide, Voice examples, Things you've said, Vamos settings."}

### Voice guide
## Core voice
Una amiga que ya lo probó y te dice qué sí y qué no, en español latinoamericano hablado, directa y sin rodeos. Habla de su propia experiencia ("yo, literal, programo todo") y de lo que le sirve a tu negocio.

## Openers
- **Spoken** · Arranca en el primer punto, sin saludo: "Programar el video. No te quita."
- **Spoken** · El error de la otra persona en su voz, y luego ella: "Hablo de todo un poco… No, pues la verdad es que yo hablo de un solo tema."

## How a video moves
Una lista de mitos o un ranking, un punto por línea: el punto → su veredicto corto ("No te quita." / "Ese sí te quita.") → una razón o su propia prueba ("Literal, yo lo hice y…"). O dos lados: lo que dice la creadora que no crece contra lo que hace ella. Al final, el número 1 o el giro, y el cierre.

## Closers
- **Spoken** · "Ahora, si quieres que [resultado], sígueme y te explico exactamente cómo hacerlo. Chao, chao."

## Rhythm
Frases muy cortas, unas 7 palabras; veredictos de dos o tres palabras. Muletillas reales: "literal", "literalmente", "o sea", "pues", "No, pues". Nada de preguntas que ella misma responde, salvo el "¿Por qué? Porque…" de una razón.

## Word choice
"views" y "trial reels" en inglés, como los dice ella; "alcance", "gancho", "formato", "ángulo", "tu tema". Tutea. Nada de groserías salvo un "esa vaina" de vez en cuando.

## Captions
Una pregunta o una frase corta con 👀 o 🫪, luego la lista en una línea; la palabra clave en mayúsculas cuando hay una.

## Voice numbers (code, 4 transcripts)
{"videos": 4, "words_per_second": 3.69, "words_per_sentence_median": 7.0, "words_per_sentence_p90": 20, "short_sentence_share": 0.42, "questions_per_100_words": 0.41, "you_per_100_words": 0.0, "i_per_100_words": 0.69, "contractions_per_100_words": 0.0, "tells_per_100_words": 0.0}

### Voice examples
#### Dfir91FuHbW · 2026-11-10 · 58,012 views · 77 s
Programar el video. No te quita. Yo, literalmente, programo todo. Borrar un video y volver a subirlo. Ese sí te quita. Literal, yo lo hice y creo que nadie vio ese video. Archivar un video. No, ese no te quita, pero eso sí es importante, no lo vas a borrar. Si de pronto cometiste un error, archívalo, pero no lo borres. Publicar de noche. No, eso no te quita views. Literalmente, yo publico todos los días por la noche. Subir exactamente el mismo video varias veces en trial reels. No, pues ese sí te quita, porque Instagram se da cuenta y la verdad es que te quita mucho alcance. Repetir un formato con otro tema. No, eso no te quita. Incluso, Giani, ella publicó el mismo formato la 1º vez, 1700 visualizaciones. Cambió el ángulo, lo publicó la 2º vez, 150000 views, o sea... Compartir tu Reel en historias. No te quita visualizaciones en el Reel, pero sí te perjudica el alcance en historias, y no queremos eso. Empezar con hola, hoy les voy a hablar de... No, ese sí te quita, o sea, si tu gancho no atrapa en el 2º 0, la gente se va. Grabar con el celular. No te quita nada. O sea, yo mis 2 primeros años creando contenido fue 100 por 100 con el celular y quedaban hermosos. Publicar 2 videos el mismo día. No te quita. O sea, yo, literal, llegué a publicar 3 veces el mismo día, pero eso sí, dale unas horitas de espacio. Ahora, si quieres que tus videos lleguen a muchísima más gente, sígueme y te explico exactamente cómo hacerlo. Chao, chao.

#### DfaOMQQMMHA · 2026-11-06 · 49,305 views · 56 s
Freelance. 4. Es fácil conseguir tu 1º cliente, pero cuando creces, terminas teniendo un montón de jefes. Dropshipping. 10. ¿Por qué? Porque estás vendiendo lo mismo que 1000 de personas, y al final, pues va a vender el que lo tenga más barato. Afiliados. 6. Pues funciona, pero, pues, te estás ganando es una comisión y la comisión siempre es menor. Trading. 9, es más apuesta que negocio, y yo no soy tanto de riesgos. Dugicy. 3, te pagan por grabar y no necesitas una audiencia. Tienda online. 8, inventario, envíos, devoluciones. No, a mí no me gusta tanto dolor de cabeza. Productos digitales. 2, lo creas una vez y lo vendes las veces que quieras. Community manager. 5. Aprendes un montón, pero al final del día estás creciendo la cuenta de otro y no la tuya. Asistente virtual. 7. Fácil de arrancar, pero difícil de crecer. ¿Y tu número 1? Crear contenido. Yo sé que no es un negocio online, pero si sabes crear contenido, te va mejor en cualquiera de estos 9.

#### DfVvyb8O47o · 2026-11-05 · 50,349 views · 62 s
Hablo de todo un poco, un día una receta, otro día una rutina, un tipcito, así le llega a un montón de gente. No, pues la verdad es que yo hablo de un solo tema, el problema que quiere resolver mi audiencia, y así ellos saben perfectamente por qué deberían seguirme. Yo me invento cada video desde 0, porque es que si me van a ver usando el video de otra cuenta, pues van a pensar que yo no soy original. No, pues yo busco literalmente un video que ya se fue viral, tomo la estructura, el formato y lo adapto a mi tema, literal, misma estructura pero con mi información. Si a las 2 horas tengo pocos views, la culpa la tiene 100 por 100 el formato. En la vida, esa vaina no sirve y en la vida lo voy a volver a publicar. No, pues, si a las 2 horas no me funciona, lo dejo y, literalmente, tomo el mismo formato y lo pruebo con un tema, un ángulo diferente en trial reels, y ahí ya veo qué tema funciona mejor. Llevo como un año publicando contenido y a mí solamente me ven como que mis amigas y mi familia. No, yo ya sé literal qué formatos le funcionan a mi tema y cada mes gano por ahí 10000 seguidores nuevos. No, pues, lo que veo, yo soy una creadora estancada. ¿Será que es porque no sigo a María Duran? Yo soy una creadora que crece porque sigue a María Duran.

#### DfLdVBpBuSH · 2026-11-01 · 89,771 views · 6 s
Usa esto para tu página de ventas. Usa esto para cobrar. Usa esto para entregar tu curso. Usa esto para promocionar tu producto.

### Things you've said
- Programa todos sus videos y publica todos los días por la noche (https://www.instagram.com/p/Dfir91FuHbW/, 2026-11-10).
- Sus 2 primeros años creando contenido grabó 100% con el celular (https://www.instagram.com/p/Dfir91FuHbW/, 2026-11-10).
- Busca un video que ya se hizo viral, toma la estructura y el formato y lo adapta a su tema (https://www.instagram.com/p/DfVvyb8O47o/, 2026-11-05).

### Vamos settings
Board: none yet.
Platforms: Instagram @mariadurancontent.
Language: Spanish.
Ads: off.
Voice numbers: {"videos": 4, "words_per_second": 3.69, "words_per_sentence_median": 7.0, "words_per_sentence_p90": 20, "short_sentence_share": 0.42, "questions_per_100_words": 0.41, "you_per_100_words": 0.0, "i_per_100_words": 0.69, "contractions_per_100_words": 0.0, "tells_per_100_words": 0.0}
