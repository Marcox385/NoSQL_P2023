#!/usr/bin/env python3
# IS727272 - Cordero Hernández, Marco Ricardo
import logging
from datetime import datetime

# Set logger
log = logging.getLogger()


CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS {}
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {} }}
"""

CREATE_USERS_TABLE = """
    CREATE TABLE IF NOT EXISTS accounts_by_user (
        username TEXT,
        account_number TEXT,
        cash_balance DECIMAL,
        name TEXT STATIC,
        PRIMARY KEY ((username),account_number)
    )
"""

CREATE_POSITIONS_BY_ACCOUNT_TABLE = """
    CREATE TABLE IF NOT EXISTS positions_by_account (
        account TEXT,
        symbol TEXT,
        quantity DECIMAL,
        PRIMARY KEY ((account),symbol)
    )
"""

CREATE_TRADES_BY_ACCOUNT_DATE_TABLE = """
    CREATE TABLE IF NOT EXISTS trades_by_a_d (
        account TEXT,
        trade_id TIMEUUID,
        type TEXT,
        symbol TEXT,
        shares DECIMAL,
        price DECIMAL,
        amount DECIMAL,
        PRIMARY KEY ((account), trade_id)
    ) WITH CLUSTERING ORDER BY (trade_id DESC)
"""

CREATE_TRADES_BY_ACCOUNT_TRADE_DATE_TABLE = """
    CREATE TABLE IF NOT EXISTS trades_by_a_td (
        account TEXT,
        trade_id TIMEUUID,
        type TEXT,
        symbol TEXT,
        shares DECIMAL,
        price DECIMAL,
        amount DECIMAL,
        PRIMARY KEY ((account), type, trade_id)
    ) WITH CLUSTERING ORDER BY (type DESC, trade_id DESC)
"""

CREATE_TRADES_BY_ACCOUNT_SYMBOL_TRADE_DATE_TABLE = """
    CREATE TABLE IF NOT EXISTS trades_by_a_std (
        account TEXT,
        trade_id TIMEUUID,
        type TEXT,
        symbol TEXT,
        shares DECIMAL,
        price DECIMAL,
        amount DECIMAL,
        PRIMARY KEY ((account), symbol, type, trade_id)
    ) WITH CLUSTERING ORDER BY (symbol DESC, type DESC, trade_id DESC)
"""

CREATE_TRADES_BY_ACCOUNT_SYMBOL_DATE_TABLE = """
    CREATE TABLE IF NOT EXISTS trades_by_a_sd (
        account TEXT,
        trade_id TIMEUUID,
        type TEXT,
        symbol TEXT,
        shares DECIMAL,
        price DECIMAL,
        amount DECIMAL,
        PRIMARY KEY ((account), symbol, trade_id)
    ) WITH CLUSTERING ORDER BY (symbol DESC, trade_id DESC)
"""

SELECT_USER_ACCOUNTS = """
    SELECT username, account_number, name, cash_balance
    FROM accounts_by_user
    WHERE username = ?
"""

SELECT_ACCOUNT_POSITIONS = """
    SELECT symbol, quantity
    FROM positions_by_account
    WHERE account = ?
"""

SELECT_TRADES = """
    SELECT toDate(trade_id) as date, amount, price, shares, symbol, type
    FROM trades_by_a_d
    WHERE account = ?
"""

SELECT_TRADES_DATE_RANGE = """
    SELECT toDate(trade_id) as date, amount, price, shares, symbol, type
    FROM trades_by_a_d
    WHERE account = ?
    AND trade_id >= minTimeuuid(?)
    AND trade_id <= maxTimeuuid(?)
"""

SELECT_TRADES_TYPE = """
    SELECT toDate(trade_id) as date, amount, price, shares, symbol, type
    FROM trades_by_a_d
    WHERE account = ?
    AND type = ? ALLOW FILTERING
"""

SELECT_TRADES_SYMBOL = """
    SELECT toDate(trade_id) as date, amount, price, shares, symbol, type
    FROM trades_by_a_d
    WHERE account = ?
    AND symbol = ? ALLOW FILTERING
"""

def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Creating keyspace: {keyspace} with replication factor {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))

def create_schema(session):
    log.info("Creating model schema")
    session.execute(CREATE_USERS_TABLE)
    session.execute(CREATE_POSITIONS_BY_ACCOUNT_TABLE)
    session.execute(CREATE_TRADES_BY_ACCOUNT_DATE_TABLE)
    session.execute(CREATE_TRADES_BY_ACCOUNT_TRADE_DATE_TABLE)
    session.execute(CREATE_TRADES_BY_ACCOUNT_SYMBOL_TRADE_DATE_TABLE)
    session.execute(CREATE_TRADES_BY_ACCOUNT_SYMBOL_DATE_TABLE)

def get_user_accounts(session, username): # Option 1
    log.info(f"Retrieving {username} accounts")
    stmt = session.prepare(SELECT_USER_ACCOUNTS)
    rows = session.execute(stmt, [username])

    for row in rows:
        print(f"\n=== Account: {row.account_number} ===")
        print(f"\tCash Balance: {row.cash_balance}")
    print('\n')

def get_account_positions(session, account): # Option 2
    log.info(f"Retrieving positions from account {account}")
    stmt = session.prepare(SELECT_ACCOUNT_POSITIONS)
    rows = session.execute(stmt, [account])

    print(f"=== Showing position for account {account} ===")
    for row in rows:
        print(f"\tSymbol {row.symbol} -- Quantity: ${row.quantity}")
    print('\n')

def get_trade_history(session, account, date_range=None, t_type=None, symbol=None):
    log.info(f"Retrieving trade history from account {account} || " +
             f"Date range: start = {date_range[0]}, end = {date_range[1]} " if date_range else ' ' +
             f"Type: {t_type} " if t_type else ' ' +
             f"Symbol: {symbol} " if symbol else ' ')
    
    stmt = None
    rows = None

    if (not date_range and not t_type and not symbol):
        stmt = session.prepare(SELECT_TRADES)
        rows = session.execute(stmt, [account])
    elif (date_range and len(date_range) == 2):
        stmt = session.prepare(SELECT_TRADES_DATE_RANGE)
        s = datetime.strptime(date_range[0], '%Y-%m-%d')
        e = datetime.strptime(date_range[1], '%Y-%m-%d')
        rows = session.execute(stmt, [account, s, e])
    elif (t_type):
        stmt = session.prepare(SELECT_TRADES_TYPE)
        rows = session.execute(stmt, [account, t_type])
    elif (symbol):
        stmt = session.prepare(SELECT_TRADES_SYMBOL)
        rows = session.execute(stmt, [account, symbol])
    else:
        print('Invalid arguments. Try again.')
        return

    print(f"=== Showing trade history for account {account} ===")
    for row in rows:
        print(f"\tDate: {row.date}; amount: {row.amount}; price: {row.price}; shares: {row.shares}; symbol: {row.symbol}; type: {row.type}")
    print('\n')