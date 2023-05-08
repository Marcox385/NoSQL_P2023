#!/usr/bin/env python3
''' Modelo 2: Modelo que recomienda en qué aeropuertos es
recomendable abrir servicios de alimentos/bebidas '''
import argparse, os, sys

from neo4j import GraphDatabase
from graphdatascience import GraphDataScience
from neo4j.exceptions import ClientError, ConstraintError

class TravelPredictor(object):

    def __init__(self, uri, user, password):
        self._uri = uri
        self._AUTH = (user, password)
        self.driver = GraphDatabase.driver(self._uri, auth=self._AUTH)
        self._create_constraints()

        self.transactions = {
            'DELETE_ALL': 'MATCH (n) DETACH DELETE n',
            'Airline': 'CREATE (al:Airline {name: $name})',
            'Airport': 'CREATE (ar:Airport {id: $id})',
            'Travel': '''MATCH (org:Airport {id: $id_from}), (dest:Airport {id: $id_to}) '''
                      '''MERGE (org)-[:TRAVEL {date: date($date), connection: $connection, wait: $wait}]->(dest)'''
        }
    
    def __enter__(self):
        return self

    def _create_constraints(self):
        ''' Create constraints'''
        def inner_tx(tx):
            tx.run('CREATE CONSTRAINT airline_constraint IF NOT EXISTS FOR (al:Airline) REQUIRE al.name IS UNIQUE')
            tx.run('CREATE CONSTRAINT airport_constraint IF NOT EXISTS FOR (ap:Airport) REQUIRE ap.id IS UNIQUE')
        
        with self.driver.session() as session:
            session.execute_write(inner_tx)

    def _generic_write_tx(self, exec_str, **kwargs):
        def inner_tx(tx):
            tx.run(exec_str, **kwargs)
        
        with self.driver.session() as session:
            try:
                session.execute_write(inner_tx)
            except (ClientError, ConstraintError) as e:
                print(f'Error in transaction: {exec_str}\nParameters -> {kwargs}\nFull trace -> {e}')
                exit(1)

    def fill(self, source):
        ''' Populate database given input dataset '''
        airlines = set()
        airports = set()
        op_count = 1

        # Reset database contents
        self._generic_write_tx(self.transactions['DELETE_ALL'])

        with open(source, newline='') as csv:
            headers = csv.readline().rstrip('\r\n').split(',')
            curr_data = {}
            lines = csv.readlines()

            for line in lines:
                curr_data = {k:v for k, v in zip(headers, line.rstrip('\r\n').split(','))}

                if (curr_data['airline'] not in airlines):
                    self._generic_write_tx(self.transactions['Airline'], name=curr_data['airline'])
                    airlines.add(curr_data['airline'])
                
                if (curr_data['from'] not in airports):
                    self._generic_write_tx(self.transactions['Airport'], id=curr_data['from'])
                    airports.add(curr_data['from'])

                if (curr_data['to'] not in airports):
                    self._generic_write_tx(self.transactions['Airport'], id=curr_data['to'])
                    airports.add(curr_data['to'])

                date = '-'.join([curr_data['year'], curr_data['month'], curr_data['day']])

                self._generic_write_tx(self.transactions['Travel'], id_from=curr_data['from'],
                    id_to=curr_data['to'], date=date, connection=curr_data['connection'],wait=int(curr_data['wait']))
            
                op_count += 1
                print(f"Progreso: {op_count/len(lines):.0%}", end='\r')
        sys.stdout.write("\033[K")
        print('Finalizado')

    def search_range(self, top:int=5, reverse:bool=False, start:str='', end:str=''):
        '''
            Search nodes between a start and end date to predict viability
            of new stores in airports
        '''
        def inner_tx(tx, limit, order, start_date, end_date):
            limit = f' LIMIT {limit}' if limit else ''
            order = ' ORDER BY ' +  ('WAIT_AVG, CONNECTIONS' if not order else 'CONNECTIONS, WAIT_AVG') + ' DESC'

            result = tx.run('MATCH (org:Airport)-[t:TRAVEL]->(dest:Airport) WHERE t.connection = "True"'
                + start_date + end_date + ' RETURN org.id as ORIGIN, COUNT(dest) AS CONNECTIONS, avg(t.wait) AS WAIT_AVG'
                + order + limit)
            return [record.values() for record in result]
        
        with self.driver.session() as session:
            start_date = ''
            end_date = ''

            if (start):
                if ('/' in start): start = start.replace('/', '-')
                start_date = list(map(lambda x: x.lstrip('0'), start.split('-')))
                start_date = '{' + f'year: {start_date[2]}, month: {start_date[1]}, day: {start_date[0]}' + '}'
                start_date = f' AND t.date >= date({start_date})'
                start = f'desde {start} '
            
            if (end):
                if ('/' in end): end = end.replace('/', '-')
                end_date = list(map(lambda x: x.lstrip('0'), end.split('-')))
                end_date = '{' + f'year: {end_date[2]}, month: {end_date[1]}, day: {end_date[0]}' + '}'
                end_date = f' AND t.date <= date({end_date})'
                end = f'hasta {end} '
            
            try:
                top = int(top)

                if (top <= 0):
                    raise ValueError
            except ValueError:
                top = 5

            try:
                reverse = bool(reverse)
            except ValueError:
                reverse = False

            results = session.execute_read(inner_tx, top, reverse, start_date, end_date)
            
            print(f'El top {top} de aeropuertos con posibilidad de apertura de establecimientos '
                + (start if start else '') + (end if end else '') + 'son los siguientes')
            for i, r in enumerate(results, 1):
                print(f'{i} - ID de Aeropuerto: {r[0]}\n\t- Conexiones: {r[1]}\n\t- Promedio de tiempo de espera por conexión: {r[2]:.2f} minutes\n')

    def stats(self, links:bool=False, centrality:bool=False):
        ''' Call GDS Algorithm for node inspection '''
        with self.driver.session() as session:
            gds = GraphDataScience(self._uri, auth=self._AUTH)

            try:
                gds.run_cypher("CALL gds.graph.drop('mod2_page_rank')")
                gds.run_cypher("CALL gds.graph.drop('mod2_centrality')")
            except ClientError:
                pass

            if (links):
                G_mod2_pr, _ = gds.graph.project(
                    'mod2_page_rank',
                    'Airport',
                    {'TRAVEL': {'properties': ['wait']}}
                )

                pr_results = gds.pageRank.stream(G = G_mod2_pr)
                print('-- PAGE RANK --')
                for node_id, score in zip(pr_results.nodeId, pr_results.score):
                    print(f'Aeropuerto: {gds.util.asNode(node_id)._properties["id"]} - Puntuación: {score}')

            if (links and centrality): print()

            if (centrality):
                G_mod2_cent, _ = gds.graph.project(
                    'mod2_centrality',
                    'Airport',
                    'TRAVEL'
                )

                pr_results = gds.beta.closeness.stream(G = G_mod2_cent)
                print('-- CENTRALITY --')
                for node_id, score in zip(pr_results.nodeId, pr_results.score):
                    print(f'Aeropuerto: {gds.util.asNode(node_id)._properties["id"]} - Puntuación: {score}')

    def close(self):
        ''' Close Neo4j instance '''
        self.driver.close()
    
    def __exit__(self, exc_type, exc_value, traceback):
        ''' Object cleanup '''
        self.close()

if __name__ == "__main__":
    neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
    neo4j_password = os.getenv('NEO4J_PASSWORD', 'neo4j_nosql')

    parser = argparse.ArgumentParser()

    actions = ['fill', 'predict', 'stats']
    parser.add_argument('action', choices=actions,
            help='Acciones disponibles')
    parser.add_argument('-f', '--file',
            help='Set de datos para el llenado de la base (formato csv)', default=None)
    parser.add_argument('-t', '--top',
            help='Limitar resultados a la cota superior [top]', default=5)
    parser.add_argument('-r', '--reverse',
            help='Invertir factores de ordenamiento (Waiting avg, Connection amount)', default=False)
    parser.add_argument('-s', '--start',
            help='Fecha inicio en el formato (dd-mm-aaaa)', default=None)
    parser.add_argument('-e', '--end',
            help='Fecha final en el formato (dd-mm-aaaa)', default=None)
    parser.add_argument('-l', '--links',
            help='Ejecutar algoritmo Page Rank para vínculos entre aeropuertos', default=False)
    parser.add_argument('-c', '--centrality',
            help='Ejecutar algoritmo Closeness Centrality para inspección de nodos', default=False)

    args = parser.parse_args()

    with TravelPredictor(neo4j_uri, neo4j_user, neo4j_password) as tp:
        if args.action == 'fill':
            if (not args.file):
                print('Archivo de entrada faltante. Intenta de nuevo.')
                exit(1)
        
            if (not args.file.endswith('.csv')):
                print('Formato de archivo incorrecto.')
                exit(1)

            tp.fill(args.file)
        elif args.action == 'predict':
            tp.search_range(top=args.top, reverse=args.reverse, start=args.start,end=args.end)
        elif args.action == 'stats':
            tp.stats(args.links, args.centrality)
