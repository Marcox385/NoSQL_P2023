#!/usr/bin/env python3
''' Modelo 3: Modelo que determine picos en afluencia de pasajeros
en los aeropuertos para valorar la opción de introducir descuentos
o distintas estrategias comerciales '''
import argparse, os, sys
from datetime import datetime

from pymongo import MongoClient

class TravelPredictor(object):
    def __init__(self, uri:str, target_db:str):
        self._client = MongoClient(uri)
        self.db = self._client[target_db]
    
    def __enter__(self):
        ''' Context manager helper '''
        return self

    def _cleanup(self, collections:list):
        for collection in collections:
            self.db[collection].delete_many({})

    def fill(self, source:str):
        ''' Populate database given input dataset '''
        airlines = set()
        airports = set()
        op_count = 1

        collections = ['airline', 'airport', 'travel']

        # Reset database contents
        self._cleanup(collections)

        with open(source, newline='') as csv:
            headers = csv.readline().rstrip('\r\n').split(',')
            curr_data = {}
            lines = csv.readlines()

            for line in lines:
                curr_data = {k:v for k, v in zip(headers, line.rstrip('\r\n').split(','))}
            
                if (curr_data['airline'] not in airlines):
                    # Airline insertion
                    self.db['airline'].insert_one({'name': curr_data['airline']})
                    airlines.add(curr_data['airline'])
                
                if (curr_data['from'] not in airports):
                    # Airport insertion
                    self.db['airport'].insert_one({'id': curr_data['from']})
                    airports.add(curr_data['from'])

                if (curr_data['to'] not in airports):
                    # Airport insertion
                    self.db['airport'].insert_one({'id': curr_data['to']})
                    airports.add(curr_data['to'])

                date = datetime(year=int(curr_data['year']),
                                month=int(curr_data['month']),
                                day=int(curr_data['day']))

                # Travel insertion
                self.db['travel'].insert_one({
                    'airline': curr_data['airline'],
                    'from': curr_data['from'],
                    'to': curr_data['to'],
                    'date': date,
                    'reason': curr_data['reason'],
                    'stay': curr_data['stay']
                })

                op_count += 1
                print(f"Progreso: {op_count/len(lines):.0%}", end='\r')
        sys.stdout.write("\033[K")
        print('Finalizado')

    def _show_airports(self):
        return [a['id'] for a in self.db['airport'].aggregate([{'$project': {'_id':0, 'id':'$id'}}])]

    def _show_airlines(self):
        return [a['name'] for a in self.db['airline'].find({}, {'_id':0})]
    
    def _choice_menu(self, choices:list, prev_msg:str = ''):
        selection = ''
        choices = {str(i):elem for i, elem in enumerate(choices, 1)}

        while (not selection):
            print(prev_msg)
            for i, elem in choices.items():
                print(f'{i} - {elem}')
            selection = input('Selección: ')

            if (selection not in choices.values()):
                if (selection in choices.keys()):
                    selection = choices[selection]
                else:
                    print('Selección incorrecta. Intenta de nuevo.\n')
                    selection = ''

        return selection

    def promotions(self, start = None, end = None):
        if (start):
            try:
                start = int(start)
            except ValueError:
                print(f'Parámetro de búsqueda incorrecto ({start=}). Revisa tus entradas.')
                exit(1)
        
        if (end):
            try:
                end = int(end)
            except ValueError:
                print(f'Parámetro de búsqueda incorrecto ({end=}). Revisa tus entradas.')
                exit(1)

        airport = self._choice_menu(self._show_airports(),
                'Selecciona un aeropuerto para realizar la predicción')
        
        dec = input('\n¿Deseas una aerolínea específica? [S/n]: ').upper()
        if (not dec or dec in ('S', 'Y')):
            airline = self._choice_menu(self._show_airlines(),
                    'Selecciona una aerolínea')
        else: dec = None

    def close(self):
        self._client.close()
    
    def __exit__(self, exc_type, exc_value, traceback):
        ''' Object cleanup '''
        self.close()

if __name__ == '__main__':
    mdb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
    db_name = os.getenv('MONGODB_DB_NAME', 'proj_mod3')

    parser = argparse.ArgumentParser()

    actions = ['fill', 'predict']
    parser.add_argument('action', choices=actions,
            help='Acciones disponibles')
    parser.add_argument('-f', '--file',
            help='Set de datos para el llenado de la base (formato csv)', default=None)
    parser.add_argument('-s', '--start',
            help='Año de inicio para rango de búsqueda', default=None)
    parser.add_argument('-e', '--end',
            help='Año de término para rango de búsqueda', default=None)

    args = parser.parse_args()

    with TravelPredictor(mdb_uri, db_name) as db:
        if args.action == 'fill':
            if (not args.file):
                print('Archivo de entrada faltante. Intenta de nuevo.')
                exit(1)
        
            if (not args.file.endswith('.csv')):
                print('Formato de archivo incorrecto.')
                exit(1)

            db.fill(args.file)
        elif args.action == 'predict':
            db.promotions(start=args.start, end=args.end)
