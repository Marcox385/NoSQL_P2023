import logging
import os
import csv
from cassandra.cluster import Cluster

import model

# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('flight_predictor.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars releated to Cassandra App
CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', 'localhost')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'flight_predictor')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')


def print_menu():
    mm_options = {
        1: "Show most travel popular months",
        2: "Load dataset",
        3: "Exit"
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])

def load_dataset(session, dataset_path):
    with open(dataset_path, "r") as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if row != [] and row[0] != "airline":
                tmp = row
                try:
                    # Integer conversion
                    tmp[3] = int(tmp[3])
                    tmp[4] = int(tmp[4])
                    tmp[5] = int(tmp[5])
                    tmp[6] = int(tmp[6])
                    tmp[-1] = int(tmp[-1])
                    tmp[-2] = bool(tmp[-2])
                except Exception as e:
                    pass
                else:
                    print(tmp)
                    model.insert_passenger(session, tmp)


def main():
    log.info("Connecting to Cluster")
    cluster = Cluster(CLUSTER_IPS.split(','))
    session = cluster.connect()

    model.create_keyspace(session, KEYSPACE, REPLICATION_FACTOR)
    session.set_keyspace(KEYSPACE)

    model.create_schema(session)


    while(True):
        print_menu()
        option = int(input('Enter your choice: '))
        if option == 1:
            month_qty = int(input('How many months: '))
            model.get_most_popular_travel_months(session, month_qty)
        if option == 2:
            dataset_path = input("Enter the full path to the dataset file: ")
            load_dataset(session, dataset_path)
        if option == 3:
            exit(0)


if __name__ == '__main__':
    main()
