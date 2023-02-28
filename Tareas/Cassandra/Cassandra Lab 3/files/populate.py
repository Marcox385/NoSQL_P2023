#!/usr/bin/env python3
# IS727272 - Cordero Hernández, Marco Ricardo
import datetime
import random
import uuid

import time_uuid

CQL_FILE = '727272_data.cql'

USERS = [
    ('mike', 'Michael Jones'),
    ('stacy', 'Stacy Malibu'),
    ('john', 'John Doe'),
    ('marie', 'Marie Condo'),
    ('tom', 'Tomas Train')
]

INSTRUMENTS = [
    'ETSY', 'PINS', 'SE', 'SHOP', 'SQ', 'MELI', 'ISRG', 'DIS', 'BRK.A', 'AMZN',
    'VOO', 'VEA', 'VGT', 'VIG', 'MBB', 'QQQ', 'SPY', 'BSV', 'BND', 'MUB',
    'VSMPX', 'VFIAX', 'FXAIX', 'VTSAX', 'SPAXX', 'VMFXX', 'FDRXX', 'FGXX'
]

def cql_stmt_generator(accounts_num=10, positions_by_account=100, trades_by_account=1000):
    acc_stmt = "INSERT INTO accounts_by_user (username, account_number, cash_balance, name) VALUES ('{}', '{}', {}, '{}');"
    pos_stmt = "INSERT INTO positions_by_account(account, symbol, quantity) VALUES ('{}', '{}', {});"
    tad_stmt = "INSERT INTO trades_by_a_d (account, trade_id, type, symbol, shares, price, amount) VALUES('{}', {}, '{}', '{}', {}, {}, {});"
    tatd_stmt = "INSERT INTO trades_by_a_td (account, trade_id, type, symbol, shares, price, amount) VALUES('{}', {}, '{}', '{}', {}, {}, {});"
    tastd_stmt = "INSERT INTO trades_by_a_std (account, trade_id, type, symbol, shares, price, amount) VALUES('{}', {}, '{}', '{}', {}, {}, {});"
    tasd_stmt = "INSERT INTO trades_by_a_sd (account, trade_id, type, symbol, shares, price, amount) VALUES('{}', {}, '{}', '{}', {}, {}, {});"
    accounts = []
    with open(CQL_FILE, "w") as fd:
        # Generate accounts by user
        for i in range(accounts_num):
            user = random.choice(USERS)
            account_number = str(uuid.uuid4())
            accounts.append(account_number)
            cash_balance = random.uniform(0.1, 100000.0)
            fd.write(acc_stmt.format(user[0], account_number, cash_balance, user[1]))
            fd.write('\n')
        fd.write('\n\n')

        # Genetate possitions by account
        acc_sym = {}
        for i in range(positions_by_account):
            while True:
                acc = random.choice(accounts)
                sym = random.choice(INSTRUMENTS)
                if acc+'_'+sym not in acc_sym:
                    acc_sym[acc+'_'+sym] = True
                    quantity = random.randint(1, 500)
                    fd.write(pos_stmt.format(acc, sym, quantity))
                    fd.write('\n')
                    break
        fd.write('\n\n')

        for i in range(trades_by_account):
            trade_id = random_date(datetime.datetime(2013, 1, 1), datetime.datetime(2022, 8, 31))
            acc = random.choice(accounts)
            sym = random.choice(INSTRUMENTS)
            trade_type = random.choice(['buy', 'sell'])
            shares = random.randint(1, 5000)
            price = random.uniform(0.1, 100000.0)
            amount = shares * price
            fd.write(tad_stmt.format(acc, trade_id, trade_type, sym, shares, price, amount))
            fd.write('\n')
            fd.write(tatd_stmt.format(acc, trade_id, trade_type, sym, shares, price, amount))
            fd.write('\n')
            fd.write(tastd_stmt.format(acc, trade_id, trade_type, sym, shares, price, amount))
            fd.write('\n')
            fd.write(tasd_stmt.format(acc, trade_id, trade_type, sym, shares, price, amount))
            fd.write('\n')

def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    rand_date = start_date + datetime.timedelta(days=random_number_of_days)
    return time_uuid.TimeUUID.with_timestamp(time_uuid.mkutime(rand_date))

def main():
    cql_stmt_generator()

if __name__ == "__main__":
    main()