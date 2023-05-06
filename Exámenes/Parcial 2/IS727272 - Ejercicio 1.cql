// IS727272 - Ejercicio 1

// Sentencias iniciales
CREATE (PussInBoots:Movie {title:'Puss in Boots: The Last Wish', released:2022, tagline:"All that I need, are the boots!"});
CREATE (AntonioB:Person {name:'Antonio Banderas', born:1960});
CREATE (SalmaH:Person {name:'Salma Hayek', born:1966});
CREATE (JoelC:Person {name:'Joel Crawford', born:1975});

// Genera la relación DIRECTED entre la Persona Joel Crawford y la película PussInBoots.
MATCH (p:Person {name:'Joel Crawford'}), (m:Movie {title:'Puss in Boots: The Last Wish'})
MERGE (p)-[:DIRECTED]->(m);

// Genera la relación de ACTED_IN entre la persona Antonio Banderas y la película Puss In Boots,
// la relación debe tener la propiedad role con valor de "Puss in Boots".
MATCH (p:Person {name:'Antonio Banderas'}), (m:Movie {title:'Puss in Boots: The Last Wish'})
MERGE (p)-[:ACTED_IN {role:'Puss in Boots'}]->(m);

// Genera la relación de ACTED_IN entre la persona Salma Hayek y la película Puss In Boots,
// la relación debe tener la propiedad role con valor de "Kitty Softpaws".
MATCH (p:Person {name:'Salma Hayek'}), (m:Movie {title:'Puss in Boots: The Last Wish'})
MERGE (p)-[:ACTED_IN {role:'Kitty Softpaws'}]->(m);
