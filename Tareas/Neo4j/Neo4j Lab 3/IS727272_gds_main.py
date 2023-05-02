#!/usr/bin/env python3
# IS727272 - Cordero Hernández, Marco Ricardo
from neo4j import GraphDatabase
from neo4j.exceptions import ClientError
from graphdatascience import GraphDataScience

URI = 'bolt://localhost:7687'
AUTH = ('neo4j', "iteso@123")
driver = GraphDatabase.driver(URI, auth=AUTH)

with driver as drv:
    drv.verify_connectivity()

with driver.session() as session:
    gds = GraphDataScience(URI, auth=AUTH)

    # Borrado inicial de proyecto y datos previos
    gds.run_cypher('''
        MATCH (n)
        DETACH DELETE n
    ''')

    try:
        gds.run_cypher('''
            CALL gds.graph.drop('lab3_demo_py')
            YIELD graphName
        ''')
    except ClientError:
        pass

    # Creación de nodos
    gds.run_cypher(
    """
        CREATE (a:Station {name: 'Kings Cross',         latitude: 51.5308,  longitude: -0.1238}),
               (b:Station {name: 'Euston',              latitude: 51.5282,  longitude: -0.1337}),
               (c:Station {name: 'Camden Town',         latitude: 51.5392,  longitude: -0.1426}),
               (d:Station {name: 'Mornington Crescent', latitude: 51.5342,  longitude: -0.1387}),
               (e:Station {name: 'Kentish Town',        latitude: 51.5507,  longitude: -0.1402}),
               (f:Station {name: 'Tlaquepaque',         latitude: 20.64091, longitude: -103.29327}),
               (a)-[:CONNECTION {distance: 0.7}]->(b),
               (b)-[:CONNECTION {distance: 1.3}]->(c),
               (b)-[:CONNECTION {distance: 0.7}]->(d),
               (d)-[:CONNECTION {distance: 0.6}]->(c),
               (c)-[:CONNECTION {distance: 1.3}]->(e),
               (f)-[:CONNECTION {distance: 0.9}]->(c),
               (c)-[:CONNECTION {distance: 0.9}]->(f),
               (d)-[:CONNECTION {distance: 0.8}]->(f)
    """
    )

    # Creación del proyecto
    G_stations, project_result = gds.graph.project(
        'lab3_demo_py',
        {'Station': {'properties': ['latitude', 'longitude']}},
        {'CONNECTION': {'properties': ['distance']}}
    )

    source_id = gds.find_node_id(['Station'], {'name': 'Kings Cross'})
    target_id = gds.find_node_id(['Station'], {'name': 'Tlaquepaque'})

    print(gds.shortestPath.astar.stream.estimate(
            G = G_stations,
            sourceNode = source_id,
            targetNode = target_id,
            latitudeProperty = 'latitude',
            longitudeProperty = 'longitude',
            relationshipWeightProperty = 'distance'
        )
    )

    print(gds.shortestPath.astar.stream(
            G = G_stations,
            sourceNode = source_id,
            targetNode = target_id,
            latitudeProperty = 'latitude',
            longitudeProperty = 'longitude',
            relationshipWeightProperty = 'distance'
        )
    )
    