// IS727272 - Ejercicio 2

// 0. Diseña el grafo que permita entender el uso de la plataforma Stackoverflow (nodos, relaciones y propiedades).
//      DEFINICIÓN DE NODOS
CREATE (u:Usuario);
CREATE (p:Pregunta);
CREATE (r:Respuesta);
CREATE (c:Comentario);
CREATE (e:Etiqueta);

//      Nodos ejemplo
CREATE (u:Usuario {
    nombre:'Marco Cordero',
    nickname:'MarCordero727272',
    fechaRegistro:date('2022-07-12'),
    ultimoIngreso:datetime("2023-05-03T21:21:00.000+0100"),
    reputacion:-1
});

CREATE (u:Usuario {
    nombre:'Profe Malévolo',
    nickname:'AVLLPD',
    fechaRegistro:date('2022-07-12'),
    ultimoIngreso:datetime("2023-05-03T21:21:00.000+0100"),
    reputacion:-1
});

CREATE (p:Pregunta {
    id: 13,
    titulo: '¿Cómo dar de baja arquitectura después de la semana 12?',
    contenido: 'Solo quiero graduarme...',
    fechaPublicacion:datetime("2023-04-20T03:00:00.000+0100"),
    calificacion: -1000,
    resuelta:false,
    idioma:'ESP-MX'
});

CREATE (r:Respuesta {
    id: 1301,
    contenido: 'Jajaja date de baja pero de esta universidad. No hay escapatoria',
    fechaPublicacion:datetime("2023-04-23T16:00:00.000+0100"),
    calificacion: 8051
});

CREATE (r:Comentario {
    id: 130101,
    contenido: 'Siempre es lo mismo en stack overflow...',
    fechaPublicacion:datetime("2023-04-23T16:03:00.000+0100"),
    calificacion: -2
});

CREATE (e:Etiqueta {
    nombre: 'Plegaria'
});

CREATE (e:Etiqueta {
    nombre: 'Magia'
});

CREATE (e:Etiqueta {
    nombre: 'Ocultismo'
});

//      Relaciones ejemplo
MATCH (u:Usuario {nickname:'MarCordero727272'}), (p:Pregunta {id: 13})
MERGE (u)-[:REALIZA]->(p);

MATCH (u:Usuario {nickname:'AVLLPD'}), (r:Respuesta {id: 1301})
MERGE (u)-[:CONTESTA_CON]->(r);

MATCH (r:Respuesta {id: 1301}), (p:Pregunta {id: 13})
MERGE (r)-[:ATIENDE_A]->(p);

MATCH (u:Usuario {nickname:'MarCordero727272'}), (c:Comentario {id: 130101})
MERGE (u)-[:POSTEA]->(c);

MATCH (c:Comentario {id: 130101}), (r:Respuesta {id: 1301})
MERGE (c)-[:RETROALIMENTA_A]->(r);

MATCH (e:Etiqueta {nombre: 'Plegaria'}), (p:Pregunta {id: 13})
MERGE (e)-[:CATEGORIZA_A]->(p);

MATCH (e:Etiqueta {nombre: 'Magia'}), (p:Pregunta {id: 13})
MERGE (e)-[:CATEGORIZA_A]->(p);

MATCH (e:Etiqueta {nombre: 'Ocultismo'}), (p:Pregunta {id: 13})
MERGE (e)-[:CATEGORIZA_A]->(p);

// 1. Representa el modelo en forma de diagrama.
CALL db.schema.visualization;

// Genera 2 índices FULLTEXT con Cypher donde tengan más sentido,
// describe el por qué tomaste la decisión de cada índice generado.

// 1. Índice para títulos de preguntas
//      Este índice es útil para buscar preguntas que pudieran
//      resultar útiles para el usuario o para evitar duplicidad,
//      esto recomendándole preguntas que pudieran ya haber resuelto
//      la pregunta que se estaría a punto de publicar
CREATE FULLTEXT INDEX pregunta_titulo_idx IF NOT EXISTS
FOR (n:Pregunta)
ON EACH [n.titulo];

// 2. Índice para contenido de preguntas, respuestas y comentarios
//      Se genera este índice porque los motores de búsqueda
//      de contenido usualmente buscan entre estos campos
//      para determinar resultados más exactos entre grandes
//      bases que contienen textos similares
CREATE FULLTEXT INDEX contenido_idx IF NOT EXISTS
FOR (n:Pregunta|Respuesta|Comentario)
ON EACH [n.contenido];
