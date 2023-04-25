// Índices
// IS727272 - Crdero Hernández, Marco Ricardo

// Creación de índices
// Range
CREATE RANGE INDEX tipo_posicion_idx IF NOT EXISTS
FOR (j:Jugador)
ON (j.estatura, j.peso, j.numero);

// Text
CREATE TEXT INDEX municipalidad_idx IF NOT EXISTS
FOR ()-[r:CASA_DE]-()
ON (r.municipalidad);

// Full-text
CREATE FULLTEXT INDEX player_name_idx IF NOT EXISTS
FOR (n:Jugador|Equipo|Conferencia|Estado)
ON EACH [n.nombre];

// Demostración en búsquedas
// tipo_posicion_idx
PROFILE
MATCH (j:Jugador)
WHERE j.estatura > 1.8
AND j.peso < 110
AND j.numero IN range(1, 15)
RETURN j;

//municipalidad_idx
PROFILE
MATCH (s:Estado)-[r:CASA_DE]->(e:Equipo)
WHERE r.municipalidad =~ '[F|f].*'
OR r.municipalidad ENDS WITH 'y'
RETURN s, r, e; // No usa el índice

PROFILE
MATCH (s:Estado)-[r:CASA_DE]->(e:Equipo)
WHERE r.municipalidad STARTS WITH 'B'
OR r.municipalidad ENDS WITH 'y'
RETURN s, r, e; // Sí usa el índice

// player_name_idx
CALL db.index.fulltext.queryNodes("player_name_idx", "kelce") YIELD node, score
RETURN node.nombre, score;
