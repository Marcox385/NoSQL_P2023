// Creación de constraints
CREATE CONSTRAINT airline_constraint IF NOT EXISTS FOR (al:Airline) REQUIRE al.name IS UNIQUE
CREATE CONSTRAINT airport_constraint IF NOT EXISTS FOR (ap:Airport) REQUIRE ap.id IS UNIQUE

// Limpieza inicial de la base
MATCH (n) DETACH DELETE n

// Creación de nodo tipo aerolínea
CREATE (al:Airline {name: $name})

// Creación de nodo tipo aeropuerto
CREATE (ar:Airport {id: $id})

// Creación de relación de tipo viaje entre aeropuertos
MATCH (org:Airport {id: $id_from}), (dest:Airport {id: $id_to}) 
MERGE (org)-[:TRAVEL {date: date($date), connection: $connection, wait: $wait}]->(dest)

// Búsqueda de resultados para predicción
MATCH (org:Airport)-[t:TRAVEL]->(dest:Airport) WHERE t.connection = "True"
[AND date >= date($date)]
[AND date <= date($date)]
RETURN org.id as ORIGIN, COUNT(dest) AS CONNECTIONS, avg(t.wait) AS WAIT_AVG
ORDER BY [WAIT_AVG, CONNECTIONS | CONNECTIONS, WAIT_AVG] DESC
[LIMIT N]

//* --- GDS --- *// 
// Page Rank
CALL gds.graph.project(
  'mod2_page_rank',
  'Airport',
  'TRAVEL',
  {
    relationshipProperties: 'wait'
  }
)

CALL gds.pageRank.stream('myGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).id AS name, score
ORDER BY score DESC, name ASC

// Closeness Centrality
CALL gds.graph.project('mod2_centrality', 'Airport', 'TRAVEL')

CALL gds.beta.closeness.stream('mod2_centrality')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).id AS id, score
ORDER BY score DESC
