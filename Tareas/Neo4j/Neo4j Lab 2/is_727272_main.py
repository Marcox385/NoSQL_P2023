#!/usr/bin/env python3
# Modified main.py base by IS727272 - Cordero Hernández, Marco Ricardo
import os, time

from neo4j import GraphDatabase
from neo4j.exceptions import ClientError, ConstraintError

class NFLStats(object):

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.transactions = {
            'DELETE_ALL': 'MATCH (n) DETACH DELETE n',
            'CONFERENCIAS': 'CREATE (c:Conferencia {nombre: $name})',
            'POSICIONES': 'CREATE (p:Posicion {id: $id, nombre: $name, tipo: $type})',
            'EQUIPOS': ['CREATE (e:Equipo {id: $id, nombre: $name, campeonatos: toInteger($chmp)})',
                       'MATCH (e:Equipo {id: $id}), (c:Conferencia {nombre: $conf_id}) MERGE (e)-[r:PARTE_DE {division: $div}]->(c)'],
            'JUGADORES': ['CREATE (j:Jugador {nombre: $name, nacimiento: date($bd), estatura: toFloat($height), peso: toFloat($weight), numero: toInteger($number)})',
                         'MATCH (j:Jugador {nombre: $name}), (p:Posicion {id: $pos_id}) MERGE (j)-[r:JUEGA_DE]->(p)',
                         'MATCH (j:Jugador {nombre: $name}), (e:Equipo {id: $team_id}) MERGE (j)-[r:PERTENECE_A {ingreso: toInteger($in_yr)}]->(e)'],
            'EQUIPOS_PASADOS': 'MATCH (j:Jugador {nombre: $name}), (e:Equipo {id: $team_id}) MERGE (j)-[r:PERTENECIO_A {ingreso: toInteger($in_yr), retiro: toInteger($out_yr)}]->(e)',
            'PARTIDOS': 'MATCH (w:Equipo {id: $winner}), (l:Equipo {id: $loser}) MERGE (w)-[r:GANO_A {temporada: toInteger($tmp_year), superbowl: toBoolean(toInteger($spbwl))}]->(l)',
            'ESTADOS': 'CREATE (s:Estado {id: $id, nombre: $name})',
            'CASAS': 'MATCH (s:Estado {id: $state_id}), (e:Equipo {id: $team_id}) MERGE (s)-[r:CASA_DE {municipalidad: $munc}]->(e)'
        }

        with self.driver.session() as session: # Constraint creation as transactions
            session.execute_write(self._create_constraints)

    def close(self):
        self.driver.close()

    # Modified for own constraints and transaction oriented operation
    def _create_constraints(self, tx):
        # Ensure constraint deletion (ommited as it throws an exception)
        '''tx.run('DROP CONSTRAINT nombreJugador IF EXISTS')
        tx.run('DROP CONSTRAINT posID IF EXISTS')
        tx.run('DROP CONSTRAINT equipoID IF EXISTS')
        tx.run('DROP CONSTRAINT nombreConferencia IF EXISTS')
        tx.run('DROP CONSTRAINT estadoINIT IF EXISTS')'''

        # Create constraints
        tx.run('CREATE CONSTRAINT nombreJugador IF NOT EXISTS FOR (j:Jugador) REQUIRE j.nombre IS UNIQUE')
        tx.run('CREATE CONSTRAINT posID IF NOT EXISTS FOR (p:Posicion) REQUIRE p.id IS UNIQUE')
        tx.run('CREATE CONSTRAINT equipoID IF NOT EXISTS FOR (e:Equipo) REQUIRE e.id IS UNIQUE')
        tx.run('CREATE CONSTRAINT nombreConferencia IF NOT EXISTS FOR (c:Conferencia) REQUIRE c.nombre IS UNIQUE')
        tx.run('CREATE CONSTRAINT estadoINIT IF NOT EXISTS FOR (s:Estado) REQUIRE s.id IS UNIQUE')

    def _generic_write_tx(self, exec_str, **kwargs):
        def inner_tx(tx):
            tx.run(exec_str, **kwargs)
        
        with self.driver.session() as session:
            try:
                session.execute_write(inner_tx)
            except (ClientError, ConstraintError) as e:
                print(f'Error in transaction: {exec_str}\nParameters -> {kwargs}\nFull trace -> {e}')
                exit()

    def init(self, source):
        start = time.time() # Starting time of operations
        self._generic_write_tx(self.transactions['DELETE_ALL']) # Uncomment for initial data deletion
        with open(source, newline='') as f:
            contents = f.readlines()
            segment_type = ''
            curr_headers = []

            for line in contents:
                line = line.rstrip('\n')

                if (line.startswith('-')): # Start of new data segment
                    segment_type = line.strip('- ')
                    continue
                elif (not line): # End of data segment
                    segment_type = ''
                    curr_headers = []

                if (segment_type): # Data segment parsing
                    vals = line.split('|')

                    if (not curr_headers): # Get data segment headers
                        curr_headers = vals
                        continue

                    vals = {k:v for k,v in zip(curr_headers,vals)}
                    
                    if (segment_type in self.transactions.keys()):
                        tx = self.transactions[segment_type]
                        if (type(tx) is list):
                            for ind_tx in tx:
                                self._generic_write_tx(ind_tx, **vals)
                        else:
                            self._generic_write_tx(self.transactions[segment_type], **vals)
                    else:
                        raise ValueError('Invalid node type. Incomplete operations made.')
            else:
                print(f'All operations completed successfully in {time.time() - start:.3f} seconds.')

if __name__ == "__main__":
    # Read connection env variables
    neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
    neo4j_password = os.getenv('NEO4J_PASSWORD', 'neo4j_nosql')

    nfl = NFLStats(neo4j_uri, neo4j_user, neo4j_password)
    nfl.init("data/nfl.txt")

    nfl.close()
