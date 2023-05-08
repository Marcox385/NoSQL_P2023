import logging

# Set logger
log = logging.getLogger()

# CREATE queries

CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS {}
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {} }}
"""

CREATE_PASSENGERS_TABLE = """
    CREATE TABLE IF NOT EXISTS passengers (
        passenger_id UUID,
        airline TEXT,
        airport_from TEXT,
        airport_to TEXT,
        flight_day INT,
        flight_month INT,
        flight_year INT,
        age INT,
        gender TEXT,
        travel_reason TEXT,
        stay TEXT,
        transit TEXT,
        connection BOOLEAN,
        wait INT,
        PRIMARY KEY((flight_month, passenger_id), flight_year)
    )
"""

# INSERT queries

INSERT_PASSENGER = """
    INSERT INTO passengers(
        passenger_id,
        airline,
        airport_from,
        airport_to,
        flight_day,
        flight_month,
        flight_year,
        age,
        gender,
        travel_reason,
        stay,
        transit,
        connection,
        wait) VALUES(
            uuid(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

# SELECT queries

SELECT_POPULAR_MONTHS = """
    SELECT *
    FROM passengers
"""

def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Creating keyspace: {keyspace} with replication factor {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))


def create_schema(session):
    log.info("Creating model schema")
    session.execute(CREATE_PASSENGERS_TABLE)


def get_most_popular_travel_months(session, months_qty):
    log.info(f"Retrieving the {months_qty} most popular months for travel")
    stmt = session.prepare(SELECT_POPULAR_MONTHS)
    rows = session.execute(stmt)
    res = {1: 0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}
    for row in rows:
        res[row.flight_month] += 1
    c = 0
    print("")
    print(f"Retrieving the {months_qty} most popular months for travel")
    for k, v in sorted(res.items(), key=lambda x:x[1], reverse=True):
        if c >= months_qty:
            break
        else:
            c += 1

        print(f"=== Month: {k} ===")
        print(f"- Total passengers: {v}")
    print("")

def insert_passenger(session, args):
    log.info("Inserting passenger")
    print(args)
    stmt = session.prepare(INSERT_PASSENGER)
    session.execute(stmt, args)
    