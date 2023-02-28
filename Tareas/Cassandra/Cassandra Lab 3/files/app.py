#!/usr/bin/env python3
# IS727272 - Cordero Hernández, Marco Ricardo
import logging
import os
import random

from cassandra.cluster import Cluster

import model

# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('investments.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars releated to Cassandra App
CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', '172.17.0.2')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'investments')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')


def print_menu():
    mm_options = {
        1: "Show accounts",
        2: "Show positions",
        3: "Show trade history",
        4: "Change username",
        5: "Exit",
    }
    
    for key in mm_options.keys():
        print(key, '--', mm_options[key])

def print_trade_history_menu():
    thm_options = {
        1: "All",
        2: "Date Range",
        3: "Transaction Type (Buy/Sell)",
        4: "Instrument Symbol",
    }
    for key in thm_options.keys():
        print('\t', key, '--', thm_options[key])

def set_username():
    username = input('**** Enter username: ')
    log.info(f"Username set to {username}")
    return username

def get_instrument_value(instrument):
    instr_mock_sum = sum(bytearray(instrument, encoding='utf-8'))
    return random.uniform(1.0, instr_mock_sum)

def main():
    log.info("Connecting to Cluster")
    cluster = Cluster(CLUSTER_IPS.split(','))
    session = cluster.connect()

    model.create_keyspace(session, KEYSPACE, REPLICATION_FACTOR)
    session.set_keyspace(KEYSPACE)

    model.create_schema(session)

    username = set_username()

    while(True):
        print_menu()
        option = int(input('Enter your choice: '))

        if (option not in range(1, 6)):
            print('Invalid option. Try again.')
            continue

        if option == 1:
            model.get_user_accounts(session, username)
        elif option == 2:
            account = input('Enter desired account: ')
            model.get_account_positions(session, account)
        elif option == 3:
            account = input('Enter desired account: ')

            tv_option = None
            while (True):
                print_trade_history_menu()
                tv_option = int(input('Enter your trade view choice: '))

                if (tv_option not in range(1, 5)):
                    print('Invalid option. Try again.')
                else: break
            
            if (tv_option == 1):
                model.get_trade_history(session, account)
            elif (tv_option == 2):
                s = input('Enter start date (yyyy-mm-dd): ')
                e = input('Enter end date (yyyy-mm-dd): ')
                model.get_trade_history(session, account, date_range=(s, e))
            elif (tv_option == 3):
                t_type = input("Enter trade type (buy/sell): ")
                model.get_trade_history(session, account, t_type=t_type)
            elif (tv_option == 4):
                symbol = input('Enter desired symbol: ')
                model.get_trade_history(session, account, symbol=symbol)
        elif option == 4:
            username = set_username()
        elif option == 5:
            exit(0)


if __name__ == '__main__':
    main()
