#!/usr/bin/env python3
''' Modelo 3: Modelo que determine picos en afluencia de pasajeros
en los aeropuertos para valorar la opción de introducir descuentos
o distintas estrategias comerciales '''
import argparse, os, sys
from datetime import datetime

from pymongo import MongoClient

class TravelPredictor(object):
    ''' Modelo 3 '''
    def __init__(self, uri:str, target_db:str):
        self._client = MongoClient(uri)
        self.db = self._client[target_db]

        months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
                  'Agosto', 'Septiembre','Octubre', 'Noviembre', 'Diciembre']
        self._months = {i:m for i, m in enumerate(months, 1)}
    
    def __enter__(self):
        ''' Context manager helper '''
        return self

    def _cleanup(self, collections:list):
        ''' Database cleanup '''
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
                    'connection': True if curr_data['to'] == 'True' else False,
                    'date': date,
                    'reason': curr_data['reason'],
                    'stay': curr_data['stay']
                })

                op_count += 1
                print(f"Progreso: {op_count/len(lines):.0%}", end='\r')
        sys.stdout.write("\033[K")
        print('Finalizado')

    def _show_airports(self):
        ''' Return all airports in the database '''
        return [a['id'] for a in self.db['airport'].aggregate([{'$project': {'_id':0, 'id':'$id'}}])]

    def _show_airlines(self):
        ''' Return all airlines in the database '''
        return [a['name'] for a in self.db['airline'].find({}, {'_id':0})]
    
    def _choice_menu(self, choices:list, dec_msg:str = '', prev_msg:str = ''):
        ''' Menu display helper '''
        try:
            dec = input(f'\n{dec_msg} [S/n]: ').upper()
        except KeyboardInterrupt:
            print('\nSelección abortada')
            return None
        
        if (not(not dec or dec in ('S', 'Y'))):
            return None

        selection = ''
        choices = {str(i):elem for i, elem in enumerate(choices, 1)}

        while (not selection):
            print(prev_msg)
            for i, elem in choices.items():
                print(f'{i} - {elem}')
            
            try:
                selection = input('Selección: ')
            except KeyboardInterrupt:
                print('\nSelección abortada')
                return None

            if (selection not in choices.values()):
                if (selection in choices.keys()):
                    selection = choices[selection]
                else:
                    print('Selección incorrecta. Intenta de nuevo.\n')
                    selection = ''

        return selection

    def promotions(self, start = None, end = None):
        ''' Predict promotions based on parameters '''
        def query(airport, airline, start, end):
            ''' Actual query to be applied against database '''
            match_dict = {
                '$match':
                    {
                        'connection': {'$ne': 'true'},
                        'stay': {'$in': ['Hotel','Short-term homestay']},
                        'reason': {'$in': ['On vacation/Pleasure','Back Home']}
                    }
            }

            group_dict = {
                '$group':
                    {
                        '_id': {'$month': '$date'}, 
                        'qty': {'$sum': 1} 
                    }
            }

            project_dict = {
                '$project':
                    {
                        '_id': 0,
                        'month': '$_id',
                        'qty': '$qty',
                    }
            }

            sort_dict = {
                '$sort': {'qty': -1}
            }

            if (airport):
                match_dict['$match']['from'] = airport
            
            if (airline):
                match_dict['$match']['airline'] = airline
            
            if (start):
                match_dict['$match']['date'] = {'$gte': datetime(start, 1, 1)}
            
            if (end):
                if ('date' in match_dict['$match'].keys()):
                    match_dict['$match']['date']['$lt'] = datetime(end, 1, 1)
                else:
                    match_dict['$match']['date'] = {'$lt': datetime(end, 1, 1)}

            return list(self.db['travel'].aggregate([
                match_dict, group_dict, project_dict, sort_dict
            ]))

        def top_month(*args):
            ''' Get month with most occurrence in given lists '''
            dict_holder = {}
            res_month = ''
            max_holder = 0

            for months in args:
                for month in months:
                    if (month not in dict_holder.keys()):
                        dict_holder[month] = 0
                    
                    dict_holder[month] += 1

                    if (dict_holder[month] > max_holder):
                        res_month = month
                        max_holder = dict_holder[month]
            
            return res_month

        res_str = '\nMostrando posibles ofertas\n\tParámetros:'

        if (start):
            try:
                start = int(start)
                res_str += f'\n\t\t- Desde {start}'
            except ValueError:
                print(f'Parámetro de búsqueda incorrecto ({start=}). Revisa tus entradas.')
                exit(1)
        
        if (end):
            try:
                end = int(end)
                res_str += f'\n\t\t- Hasta {end}'
            except ValueError:
                print(f'Parámetro de búsqueda incorrecto ({end=}). Revisa tus entradas.')
                exit(1)

        airports = self._show_airports()
        airport = self._choice_menu(airports,
                '¿Deseas un aeropuerto en específico',
                'Selecciona un aeropuerto para realizar la predicción')
        
        airline = self._choice_menu(self._show_airlines(),
                '¿Deseas una aerolínea específica?',
                'Selecciona una aerolínea')
    
        if (airline):
            res_str += f'\n\t\t- Aerolínea "{airline}"'
        
        if (airport):
            query_res = query(airport, airline, start, end)

            if (not query_res):
                print('No hay recomendaciones disponibles para el conjunto de parámetros actual.')
                return
            
            res_str += f'\n\t\t- Aeropuerto "{airport}"'
            top = [self._months[r['month']] for r in query_res[:3]]
            bottom = [self._months[r['month']] for r in query_res[-3:]]
            
            print(res_str + '\n\nResultados:')
            print('\tPosibilidad de introducción de paquetes grupales o similar\n\t->', ', '.join(top))    
            print('\n\tPosibilidad de descuentos por baja demanda\n\t->', ', '.join(bottom))

            if (not top == bottom):
                print(f'\nMes con mejor posibilidad de introducción de promociones: {top_month(top, bottom)}')
        else:
            if (res_str.endswith('Parámetros:')): res_str = res_str.rstrip('Parámetros:')
            print(res_str + '\n\nResultados:', end='')
            holder = []

            for airport_i in airports:
                print(f'\nAeropuerto "{airport_i}"')

                res = query(airport_i, airline, start, end)
                
                if (not res):
                    print('\tSin recomendaciones posibles')
                    continue

                top = [self._months[r['month']] for r in res[:3]]
                bottom = [self._months[r['month']] for r in res[-3:]]
                holder.append(top)
                holder.append(bottom)

                print('\tPosibilidad de introducción de paquetes grupales o similar\n\t->', ', '.join(top))
                print('\n\tPosibilidad de descuentos por baja demanda\n\t->', ', '.join(bottom))
            
            print(f'\nMes con mejor posibilidad de introducción de promociones: {top_month(*holder)}')

    def close(self):
        ''' Close database connection '''
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
