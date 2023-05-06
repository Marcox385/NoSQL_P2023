// IS727272 - Ejercicio 3

// Dado el siguiente modelo que representa el seguimiento de películas vistas por miembors de una plataforma tipo Netflix
// (Family)<-[BELONGS_TO]-(User)
// (User)-[WATCHED]->(Movie)
// (User)-[USES]->(IpAddress)
// (Movie)-[HAS]->(Genre)

// Genera nodos que representen el uso de Netflix de 2 familias
// Agrega al menos una propiedad a cada tipo de nodo y relación, excluye propiedades para la relación HAS entre Movie y Genre
// Familia 1
CREATE (f:Family {
    name: 'Cordero Hernández',
    members: 3
});

CREATE (u:User {
    username: 'Marcox385'
});

CREATE (ip:IpAddress {
    address: '182.12.214.4'
});

CREATE (m:Movie {
    title: 'Nosotros los nobles'
});

CREATE (g:Genre {
    name: 'Comedy'
});

// Familia 2
CREATE (f:Family {
    name: 'Familia Real',
    members: 4
});

CREATE (u:User {
    username: 'LARS'
});

CREATE (ip:IpAddress {
    address: '1.24.37.89'
});

CREATE (m:Movie {
    title: 'Just go with it'
});

CREATE (g:Genre {
    name: 'Documentary'
});

MATCH (u:User {username: 'Marcox385'}), (f:Familiy {name: 'Cordero Hernández'})
MERGE (u)-[:BELONGS_TO {since:date('2022-01-01')}]->(f);

MATCH (u:User {username: 'LARS'}), (f:Familiy {name: 'Romero Solis'})
MERGE (u)-[:BELONGS_TO {since:date('2018-04-28')}]->(f);

MATCH (u:User {username: 'Marcox385'}), (ip:IpAddress {address: '182.12.214.4'})
MERGE (u)-[:USES {mask: 14}]->(ip);

MATCH (u:User {username: 'LARS'}), (ip:IpAddress {address: '1.24.37.89'})
MERGE (u)-[:USES {mask: 24}]->(ip);

MATCH (u:User {username: 'Marcox385'}), (m:Movie {title: 'Nosotros los nobles'})
MERGE (u)-[:WATCHED {rating: 5.0}]->(m);

MATCH (u:User {username: 'LARS'}), (m:Movie {title: 'Just go with it'})
MERGE (u)-[:WATCHED {rating: 3.8}]->(m);

MATCH (m:Movie {title: 'Nosotros los nobles'}), (g:Genre {name: 'Comedy'})
MERGE (m)-[:HAS]->(g);

MATCH (m:Movie {title: 'Just go with it'}), (g:Genre {name: 'Documentary'})
MERGE (m)-[:HAS]->(g);

// Agrega 2 constraints
CREATE CONSTRAINT username IF NOT EXISTS
FOR (u:Username)
REQUIRE u.username IS UNIQUE;

CREATE CONSTRAINT members_qty IF NOT EXISTS
FOR (f:Family)
REQUIRE f.members IS NOT NULL;

// Agrega un índice del tipo RANGE
CREATE RANGE INDEX ip_addr_idx IF NOT EXISTS
FOR (ip:IpAddress)
ON (ip.address);

// Agrega un índice del tipo TEXT
CREATE TEXT INDEX movie_title_idx IF NOT EXISTS
FOR (m:Movie)
ON (m.title);
