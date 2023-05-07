#!/usr/bin/env python3
''' Modelo 2: Modelo que recomienda en qué aeropuertos es
recomendable abrir servicios de alimentos/bebidas '''
import os, time, argparse

from neo4j import GraphDatabase
from graphdatascience import GraphDataScience
from neo4j.exceptions import ClientError, ConstraintError

class TravelPredictor(object):

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self._create_constraints()

        self.transactions = {
            'DELETE_ALL': 'MATCH (n) DETACH DELETE n',
            'Airline': 'CREATE (al:Airline {name: $name})',
            'Airport': 'CREATE (ar:Airport {id: $id})',
            'Travel': '''MATCH (org:Airport {id: $id_from}), (dest:Airport {id: $id_to}) '''
                      '''MERGE (org)-[:TRAVEL {date: date($date), connection: $connection, wait: $wait}]->(dest)'''
        }

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

        # Reset database contents
        self._generic_write_tx(self.transactions['DELETE_ALL'])

        with open(source, newline='') as csv:
            headers = csv.readline().rstrip('\r\n').split(',')
            curr_data = {}

            for line in csv.readlines():
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

    def search_range(self, start='', end=''):
        def inner_tx(tx, start, end):
            start_date = ''
            end_date = ''

            if (start):
                start_date = list(map(lambda x: x.lstrip('0'), start.split('-')))
                start_date = '{' + f'year: {start_date[2]}, month: {start_date[1]}, day: {start_date[0]}' + '}'
                start_date = f' AND t.date >= date({start_date})'
            
            if (end):
                end_date = end.split('-')
                end_date = '{' + f'year: {end_date[2]}, month: {end_date[1]}, day: {end_date[0]}' + '}'
                end_date = f' AND t.date <= date({end_date})'

            result = tx.run('MATCH (org:Airport)-[t:TRAVEL]->(dest:Airport) WHERE t.connection = "True"'
                + start_date + end_date + ' RETURN org.id as ORIGIN, COUNT(dest) AS CONNECTIONS, avg(t.wait) AS WAIT_AVG'
                + ' ORDER BY WAIT_AVG, CONNECTIONS DESC')
            return [record.values() for record in result]
        
        with self.driver.session() as session:
            results = session.execute_read(inner_tx, start, end)
            
            print('The most suitable airports to open more establishments are the following')
            for i, r in enumerate(results[:5], 1):
                print(f'{i} - Airport ID: {r[0]}\n\t- Connections: {r[1]}\n\t- Waiting time average per connection: {r[2]:.2f} minutes\n')

    def close(self):
        ''' Close Neo4j instance '''
        self.driver.close()
    
    def __exit__(self):
        ''' Object cleanup '''
        self.close()

if __name__ == "__main__":
    neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
    neo4j_password = os.getenv('NEO4J_PASSWORD', 'neo4j_nosql')

    parser = argparse.ArgumentParser()

    actions = ['fill', 'predict']
    parser.add_argument('action', choices=actions,
            help='Available application actions')
    parser.add_argument('-f', '--file',
            help='Dataset for database filling (csv format)', default=None)
    parser.add_argument('-s', '--start',
            help='Starting date in format (dd-mm-yyy)', default=None)
    parser.add_argument('-e', '--end',
            help='Ending date in format (dd-mm-yyy)', default=None)

    args = parser.parse_args()
    tp = TravelPredictor(neo4j_uri, neo4j_user, neo4j_password)

    if args.action == 'fill':
        if (args.start or args.end):
            print('Invalid arguments combination.')
            exit(1)

        if (not args.file):
            print('Filling file not provided. Try again.')
            exit(1)
        
        if ('.csv' not in args.file):
            print('Incorrect file format')
            exit(1)

        tp.fill(args.file)
    elif args.action == 'predict':
        tp.search_range(start=args.start,end=args.end)
