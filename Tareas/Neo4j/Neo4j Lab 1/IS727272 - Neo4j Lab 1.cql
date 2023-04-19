// Asegurar inexistencia de datos
MATCH (n)
DETACH DELETE n;

DROP CONSTRAINT nombreJugador IF EXISTS;
DROP CONSTRAINT posID IF EXISTS;
DROP CONSTRAINT equipoID IF EXISTS;
DROP CONSTRAINT nombreConferencia IF EXISTS;
DROP CONSTRAINT estadoINIT IF EXISTS;

// Definición inicial de nodos
CREATE (j:Jugador);
CREATE (p:Posicion);
CREATE (e:Equipo);
CREATE (c:Conferencia);
CREATE (s:Estado);

// Reestricciones
CREATE CONSTRAINT nombreJugador IF NOT EXISTS
FOR (j:Jugador)
REQUIRE j.nombre IS UNIQUE;

CREATE CONSTRAINT posID IF NOT EXISTS
FOR (p:Posicion)
REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT equipoID IF NOT EXISTS
FOR (e:Equipo)
REQUIRE e.id IS UNIQUE;

CREATE CONSTRAINT nombreConferencia IF NOT EXISTS
FOR (c:Conferencia)
REQUIRE c.nombre IS UNIQUE;

CREATE CONSTRAINT estadoINIT IF NOT EXISTS
FOR (s:Estado)
REQUIRE s.id IS UNIQUE;

// Creación de nodos
CREATE (j:Jugador {
    nombre: 'Josh Allen', nacimiento: date('1996-05-21'),
    estatura: 1.96, peso: 108, numero: 17
});
CREATE (j:Jugador {
    nombre: 'Stefon Diggs', nacimiento: date('1993-11-29'),
    estatura: 1.83, peso: 88, numero: 14
});
CREATE (j:Jugador {
    nombre: 'John Unitas', nacimiento: date('1933-05-07'),
    estatura: 1.85, peso: 88, numero: -1
});
CREATE (j:Jugador {
    nombre: 'Raheem Mostert', nacimiento: date('1992-04-09'),
    estatura: 1.78, peso: 89, numero: 31
});
CREATE (j:Jugador {
    nombre: 'Antonio Brown', nacimiento: date('1988-07-10'),
    estatura: 1.78, peso: 84, numero: -1
});
CREATE (j:Jugador {
    nombre: 'Patrick Mahomes', nacimiento: date('1995-09-17'),
    estatura: 1.88, peso: 102, numero: 15
});
CREATE (j:Jugador {
    nombre: 'Travis Kelce', nacimiento: date('1989-10-05'),
    estatura: 1.96, peso: 113, numero: 87
});
CREATE (j:Jugador {
    nombre: 'Jason Kelce', nacimiento: date('1987-11-05'),
    estatura: 1.91, peso: 128, numero: 62
});
CREATE (j:Jugador {
    nombre: 'Justin Tucker', nacimiento: date('1989-11-21'),
    estatura: 1.85, peso: 82, numero: 9
});
CREATE (j:Jugador {
    nombre: 'AJ Dillon', nacimiento: date('1998-05-02'),
    estatura: 1.83, peso: 112, numero: 28
});

CREATE (p:Posicion {id: 'QB', nombre: 'Mariscal de campo', tipo: 'Backs'});
CREATE (p:Posicion {id: 'TE', nombre: 'Ala cerrada', tipo: 'Backs'});
CREATE (p:Posicion {id: 'WR', nombre: 'Receptor abierto', tipo: 'Backs'});
CREATE (p:Posicion {id: 'RB', nombre: 'Corredor', tipo: 'Backs'});
CREATE (p:Posicion {id: 'LB', nombre: 'Apoyador', tipo: 'Línea defensiva'});
CREATE (p:Posicion {id: 'CB', nombre: 'Esquinero', tipo: 'Línea defensiva'});
CREATE (p:Posicion {id: 'S', nombre: 'Profundo', tipo: 'Línea defensiva'});
CREATE (p:Posicion {id: 'K', nombre: 'Pateador', tipo: 'Especial'});
CREATE (p:Posicion {id: 'P', nombre: 'Despeje', tipo: 'Especial'});
CREATE (p:Posicion {id: 'C', nombre: 'Centro', tipo: 'Línea ofensiva'});
CREATE (p:Posicion {id: 'OG', nombre: 'Guardia ofensivo', tipo: 'Línea ofensiva'});

CREATE (e:Equipo {id: 'BUF', nombre: 'Bills', campeonatos: 0}); // Duele
CREATE (e:Equipo {id: 'IND', nombre: 'Colts', campeonatos: 2});
CREATE (e:Equipo {id: 'MIA', nombre: 'Dolphins', campeonatos: 2});
CREATE (e:Equipo {id: 'TB', nombre: 'Buccaneers', campeonatos: 2});
CREATE (e:Equipo {id: 'PIT', nombre: 'Steelers', campeonatos: 6});
CREATE (e:Equipo {id: 'KC', nombre: 'Chiefs', campeonatos: 3});
CREATE (e:Equipo {id: 'PHI', nombre: 'Eagles', campeonatos: 1});
CREATE (e:Equipo {id: 'BLT', nombre: 'Ravens', campeonatos: 2});
CREATE (e:Equipo {id: 'CIN', nombre: 'Bengals', campeonatos: 0});
CREATE (e:Equipo {id: 'CHI', nombre: 'Bears', campeonatos: 1});
CREATE (e:Equipo {id: 'GB', nombre: 'Packers', campeonatos: 4});
CREATE (e:Equipo {id: 'MIN', nombre: 'Vikings', campeonatos: 0});
CREATE (e:Equipo {id: 'LAC', nombre: 'Chargers', campeonatos: 0});
CREATE (e:Equipo {id: 'SF', nombre: '49ers', campeonatos: 0});
CREATE (e:Equipo {id: 'CLV', nombre: 'Browns', campeonatos: 0});
CREATE (e:Equipo {id: 'LV', nombre: 'Raiders', campeonatos: 3});
CREATE (e:Equipo {id: 'NE', nombre: 'Patriots', campeonatos: 6});
CREATE (e:Equipo {id: 'DEN', nombre: 'Broncos', campeonatos: 3});
CREATE (e:Equipo {id: 'SEA', nombre: 'Seahawks', campeonatos: 1});

CREATE (c:Conferencia {nombre: 'AFC'});
CREATE (c:Conferencia {nombre: 'NFC'});

CREATE (s:Estado {id: 'NY', nombre: 'Nueva York'});
CREATE (s:Estado {id: 'IN', nombre: 'Indianápolis'});
CREATE (s:Estado {id: 'FL', nombre: 'Florida'});
CREATE (s:Estado {id: 'PA', nombre: 'Pensilvania'});
CREATE (s:Estado {id: 'KS', nombre: 'Kansas'});
CREATE (s:Estado {id: 'MD', nombre: 'Maryland'});
CREATE (s:Estado {id: 'OH', nombre: 'Ohio'});
CREATE (s:Estado {id: 'IL', nombre: 'Illinois'});
CREATE (s:Estado {id: 'MN', nombre: 'Minesota'});
CREATE (s:Estado {id: 'MO', nombre: 'Misuri'});
CREATE (s:Estado {id: 'CA', nombre: 'California'});
CREATE (s:Estado {id: 'NV', nombre: 'Nevada'});
CREATE (s:Estado {id: 'CO', nombre: 'Colorado'});
CREATE (s:Estado {id: 'WA', nombre: 'Washington'});
CREATE (s:Estado {id: 'WI', nombre: 'Wisconsin'});
CREATE (s:Estado {id: 'MA', nombre: 'Massachusetts'});

// Creación de relaciones
MATCH (j:Jugador {nombre: 'Josh Allen'}), (p:Posicion {id: 'QB'})
MERGE (j)-[r:JUEGA_DE]->(p);
MATCH (j:Jugador {nombre: 'Stefon Diggs'}), (p:Posicion {id: 'WR'})
MERGE (j)-[r:JUEGA_DE]->(p);
MATCH (j:Jugador {nombre: 'John Unitas'}), (p:Posicion {id: 'QB'})
MERGE (j)-[r:JUEGA_DE]->(p);
MATCH (j:Jugador {nombre: 'Raheem Mostert'}), (p:Posicion {id: 'RB'})
MERGE (j)-[r:JUEGA_DE]->(p);
MATCH (j:Jugador {nombre: 'Antonio Brown'}), (p:Posicion {id: 'WR'})
MERGE (j)-[r:JUEGA_DE]->(p);
MATCH (j:Jugador {nombre: 'Patrick Mahomes'}), (p:Posicion {id: 'QB'})
MERGE (j)-[r:JUEGA_DE]->(p);
MATCH (j:Jugador {nombre: 'Travis Kelce'}), (p:Posicion {id: 'TE'})
MERGE (j)-[r:JUEGA_DE]->(p);
MATCH (j:Jugador {nombre: 'Jason Kelce'}), (p:Posicion {id: 'C'})
MERGE (j)-[r:JUEGA_DE]->(p);
MATCH (j:Jugador {nombre: 'Justin Tucker'}), (p:Posicion {id: 'K'})
MERGE (j)-[r:JUEGA_DE]->(p);
MATCH (j:Jugador {nombre: 'AJ Dillon'}), (p:Posicion {id: 'RB'})
MERGE (j)-[r:JUEGA_DE]->(p);

MATCH (j:Jugador {nombre: 'Josh Allen'}), (e:Equipo {id: 'BUF'})
MERGE (j)-[r:PERTENECE_A {ingreso: 2018}]->(e);
MATCH (j:Jugador {nombre: 'Stefon Diggs'}), (e:Equipo {id: 'BUF'})
MERGE (j)-[r:PERTENECE_A {ingreso: 2020}]->(e);
MATCH (j:Jugador {nombre: 'John Unitas'}), (e:Equipo {id: 'LAC'})
MERGE (j)-[r:PERTENECE_A {ingreso: 1973}]->(e);
MATCH (j:Jugador {nombre: 'Raheem Mostert'}), (e:Equipo {id: 'MIA'})
MERGE (j)-[r:PERTENECE_A {ingreso: 2022}]->(e);
MATCH (j:Jugador {nombre: 'Antonio Brown'}), (e:Equipo {id: 'TB'})
MERGE (j)-[r:PERTENECE_A {ingreso: 2020}]->(e);
MATCH (j:Jugador {nombre: 'Patrick Mahomes'}), (e:Equipo {id: 'KC'})
MERGE (j)-[r:PERTENECE_A {ingreso: 2017}]->(e);
MATCH (j:Jugador {nombre: 'Travis Kelce'}), (e:Equipo {id: 'KC'})
MERGE (j)-[r:PERTENECE_A {ingreso: 2013}]->(e);
MATCH (j:Jugador {nombre: 'Jason Kelce'}), (e:Equipo {id: 'PHI'})
MERGE (j)-[r:PERTENECE_A {ingreso: 2011}]->(e);
MATCH (j:Jugador {nombre: 'Justin Tucker'}), (e:Equipo {id: 'BLT'})
MERGE (j)-[r:PERTENECE_A {ingreso: 2012}]->(e);
MATCH (j:Jugador {nombre: 'AJ Dillon'}), (e:Equipo {id: 'GB'})
MERGE (j)-[r:PERTENECE_A {ingreso: 2020}]->(e);

MATCH (j:Jugador {nombre: 'Stefon Diggs'}), (e:Equipo {id: 'MIN'})
MERGE (j)-[r:PERTENECIO_A {ingreso: 2015, retiro: 2019}]->(e);
MATCH (j:Jugador {nombre: 'John Unitas'}), (e:Equipo {id: 'PIT'})
MERGE (j)-[r:PERTENECIO_A {ingreso: 1955, retiro: 1955}]->(e);
MATCH (j:Jugador {nombre: 'John Unitas'}), (e:Equipo {id: 'IND'})
MERGE (j)-[r:PERTENECIO_A {ingreso: 1956, retiro: 1972}]->(e);
MATCH (j:Jugador {nombre: 'Raheem Mostert'}), (e:Equipo {id: 'SF'})
MERGE (j)-[r:PERTENECIO_A {ingreso: 2016, retiro: 2021}]->(e);
MATCH (j:Jugador {nombre: 'Raheem Mostert'}), (e:Equipo {id: 'CHI'})
MERGE (j)-[r:PERTENECIO_A {ingreso: 2016, retiro: 2016}]->(e);
MATCH (j:Jugador {nombre: 'Raheem Mostert'}), (e:Equipo {id: 'CLV'})
MERGE (j)-[r:PERTENECIO_A {ingreso: 2015, retiro: 2015}]->(e);
MATCH (j:Jugador {nombre: 'Raheem Mostert'}), (e:Equipo {id: 'BLT'})
MERGE (j)-[r:PERTENECIO_A {ingreso: 2015, retiro: 2015}]->(e);
MATCH (j:Jugador {nombre: 'Antonio Brown'}), (e:Equipo {id: 'PIT'})
MERGE (j)-[r:PERTENECIO_A {ingreso: 2010, retiro: 2018}]->(e);
MATCH (j:Jugador {nombre: 'Antonio Brown'}), (e:Equipo {id: 'LV'})
MERGE (j)-[r:PERTENECIO_A {ingreso: 2019, retiro: 2019}]->(e);
MATCH (j:Jugador {nombre: 'Antonio Brown'}), (e:Equipo {id: 'NE'})
MERGE (j)-[r:PERTENECIO_A {ingreso: 2019, retiro: 2019}]->(e);

MATCH (w:Equipo {id: 'KC'}), (l:Equipo {id: 'PHI'})
MERGE (w)-[r:GANO_A {temporada: 2022, superbowl: True}]->(l);
MATCH (w:Equipo {id: 'BUF'}), (l:Equipo {id: 'LAC'})
MERGE (w)-[r:GANO_A {temporada: 2022, superbowl: False}]->(l);
MATCH (w:Equipo {id: 'CHI'}), (l:Equipo {id: 'SF'})
MERGE (w)-[r:GANO_A {temporada: 2022, superbowl: False}]->(l);
MATCH (w:Equipo {id: 'PIT'}), (l:Equipo {id: 'CIN'})
MERGE (w)-[r:GANO_A {temporada: 2022, superbowl: False}]->(l);
MATCH (w:Equipo {id: 'MIN'}), (l:Equipo {id: 'GB'})
MERGE (w)-[r:GANO_A {temporada: 2022, superbowl: False}]->(l);
MATCH (w:Equipo {id: 'BLT'}), (l:Equipo {id: 'BUF'})
MERGE (w)-[r:GANO_A {temporada: 2018, superbowl: False}]->(l);
MATCH (w:Equipo {id: 'KC'}), (l:Equipo {id: 'SF'})
MERGE (w)-[r:GANO_A {temporada: 2019, superbowl: True}]->(l);
MATCH (w:Equipo {id: 'LAC'}), (l:Equipo {id: 'CIN'})
MERGE (w)-[r:GANO_A {temporada: 2021, superbowl: True}]->(l);
MATCH (w:Equipo {id: 'SEA'}), (l:Equipo {id: 'DEN'})
MERGE (w)-[r:GANO_A {temporada: 2013, superbowl: True}]->(l);
MATCH (w:Equipo {id: 'PHI'}), (l:Equipo {id: 'NE'})
MERGE (w)-[r:GANO_A {temporada: 2017, superbowl: True}]->(l);

MATCH (e:Equipo {id: 'BUF'}), (c:Conferencia {nombre: 'AFC'})
MERGE (e)-[r:PARTE_DE {division: 'Este'}]->(c);
MATCH (e:Equipo {id: 'IND'}), (c:Conferencia {nombre: 'AFC'})
MERGE (e)-[r:PARTE_DE {division: 'Sur'}]->(c);
MATCH (e:Equipo {id: 'MIA'}), (c:Conferencia {nombre: 'AFC'})
MERGE (e)-[r:PARTE_DE {division: 'Este'}]->(c);
MATCH (e:Equipo {id: 'TB'}), (c:Conferencia {nombre: 'NFC'})
MERGE (e)-[r:PARTE_DE {division: 'Sur'}]->(c);
MATCH (e:Equipo {id: 'PIT'}), (c:Conferencia {nombre: 'AFC'})
MERGE (e)-[r:PARTE_DE {division: 'Norte'}]->(c);
MATCH (e:Equipo {id: 'KC'}), (c:Conferencia {nombre: 'AFC'})
MERGE (e)-[r:PARTE_DE {division: 'Oeste'}]->(c);
MATCH (e:Equipo {id: 'PHI'}), (c:Conferencia {nombre: 'NFC'})
MERGE (e)-[r:PARTE_DE {division: 'Este'}]->(c);
MATCH (e:Equipo {id: 'BLT'}), (c:Conferencia {nombre: 'AFC'})
MERGE (e)-[r:PARTE_DE {division: 'Norte'}]->(c);
MATCH (e:Equipo {id: 'CIN'}), (c:Conferencia {nombre: 'AFC'})
MERGE (e)-[r:PARTE_DE {division: 'Norte'}]->(c);
MATCH (e:Equipo {id: 'CHI'}), (c:Conferencia {nombre: 'NFC'})
MERGE (e)-[r:PARTE_DE {division: 'Norte'}]->(c);
MATCH (e:Equipo {id: 'GB'}), (c:Conferencia {nombre: 'NFC'})
MERGE (e)-[r:PARTE_DE {division: 'Norte'}]->(c);
MATCH (e:Equipo {id: 'MIN'}), (c:Conferencia {nombre: 'NFC'})
MERGE (e)-[r:PARTE_DE {division: 'Norte'}]->(c);
MATCH (e:Equipo {id: 'LAC'}), (c:Conferencia {nombre: 'AFC'})
MERGE (e)-[r:PARTE_DE {division: 'Oeste'}]->(c);
MATCH (e:Equipo {id: 'SF'}), (c:Conferencia {nombre: 'NFC'})
MERGE (e)-[r:PARTE_DE {division: 'Oeste'}]->(c);
MATCH (e:Equipo {id: 'CLV'}), (c:Conferencia {nombre: 'AFC'})
MERGE (e)-[r:PARTE_DE {division: 'Norte'}]->(c);
MATCH (e:Equipo {id: 'LV'}), (c:Conferencia {nombre: 'AFC'})
MERGE (e)-[r:PARTE_DE {division: 'Oeste'}]->(c);
MATCH (e:Equipo {id: 'NE'}), (c:Conferencia {nombre: 'AFC'})
MERGE (e)-[r:PARTE_DE {division: 'Este'}]->(c);
MATCH (e:Equipo {id: 'DEN'}), (c:Conferencia {nombre: 'AFC'})
MERGE (e)-[r:PARTE_DE {division: 'Oeste'}]->(c);
MATCH (e:Equipo {id: 'SEA'}), (c:Conferencia {nombre: 'NFC'})
MERGE (e)-[r:PARTE_DE {division: 'Oeste'}]->(c);

MATCH (s:Estado {id: 'NY'}), (e:Equipo {id: 'BUF'})
MERGE (s)-[r:CASA_DE {municipalidad: 'Búfalo'}]->(e);
MATCH (s:Estado {id: 'IN'}), (e:Equipo {id: 'IND'})
MERGE (s)-[r:CASA_DE {municipalidad: 'Indianápolis'}]->(e);
MATCH (s:Estado {id: 'FL'}), (e:Equipo {id: 'MIA'})
MERGE (s)-[r:CASA_DE {municipalidad: 'Miami'}]->(e);
MATCH (s:Estado {id: 'FL'}), (e:Equipo {id: 'TB'})
MERGE (s)-[r:CASA_DE {municipalidad: 'Tampa Bay'}]->(e);
MATCH (s:Estado {id: 'PA'}), (e:Equipo {id: 'PIT'})
MERGE (s)-[r:CASA_DE {municipalidad: 'Pittsburgh'}]->(e);
MATCH (s:Estado {id: 'MO'}), (e:Equipo {id: 'KC'})
MERGE (s)-[r:CASA_DE {municipalidad: 'Kansas City'}]->(e);
MATCH (s:Estado {id: 'NY'}), (e:Equipo {id: 'PHI'})
MERGE (s)-[r:CASA_DE {municipalidad: 'Filadelfia'}]->(e);
MATCH (s:Estado {id: 'MD'}), (e:Equipo {id: 'BLT'})
MERGE (s)-[r:CASA_DE {municipalidad: 'Baltimore'}]->(e);
MATCH (s:Estado {id: 'OH'}), (e:Equipo {id: 'CIN'})
MERGE (s)-[r:CASA_DE {municipalidad: 'Cincinnati'}]->(e);
MATCH (s:Estado {id: 'IL'}), (e:Equipo {id: 'CHI'})
MERGE (s)-[r:CASA_DE {municipalidad: 'Chicago'}]->(e);
MATCH (s:Estado {id: 'WI'}), (e:Equipo {id: 'GB'})
MERGE (s)-[r:CASA_DE {municipalidad: 'Green Bay'}]->(e);
MATCH (s:Estado {id: 'MN'}), (e:Equipo {id: 'MIN'})
MERGE (s)-[r:CASA_DE {municipalidad: 'Minesota'}]->(e);
MATCH (s:Estado {id: 'CA'}), (e:Equipo {id: 'LAC'})
MERGE (s)-[r:CASA_DE {municipalidad: 'Los Ángeles'}]->(e);
MATCH (s:Estado {id: 'CA'}), (e:Equipo {id: 'SF'})
MERGE (s)-[r:CASA_DE {municipalidad: 'San Francisco'}]->(e);
MATCH (s:Estado {id: 'OH'}), (e:Equipo {id: 'CLV'})
MERGE (s)-[r:CASA_DE {municipalidad: 'Cleveland'}]->(e);
MATCH (s:Estado {id: 'NV'}), (e:Equipo {id: 'LV'})
MERGE (s)-[r:CASA_DE {municipalidad: 'Las Vegas'}]->(e);
MATCH (s:Estado {id: 'MA'}), (e:Equipo {id: 'NE'})
MERGE (s)-[r:CASA_DE {municipalidad: 'Foxborough'}]->(e);
MATCH (s:Estado {id: 'CO'}), (e:Equipo {id: 'DEN'})
MERGE (s)-[r:CASA_DE {municipalidad: 'Denver'}]->(e);
MATCH (s:Estado {id: 'WA'}), (e:Equipo {id: 'SEA'})
MERGE (s)-[r:CASA_DE {municipalidad: 'Seattle'}]->(e);

// Visualización del resultado final
CALL db.schema.visualization;

// Jugadores
MATCH (j:Jugador) RETURN j;
MATCH (j:jugador)-[r]->(n) RETURN j, r, n;

// Equipos
MATCH (e:Equipo) return e;
MATCH (e:Equipo)-[r]-(n) RETURN e, r, n;

// Todos los nodos
MATCH (n)-[r]-(m) RETURN n, r, m;
