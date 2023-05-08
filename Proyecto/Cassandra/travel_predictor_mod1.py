CREATE_KEYSPACE = """
    CREATE KEYSPACE IF NOT EXISTS {}
    WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {} }}
"""

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
Página 19 de 32
stay TEXT,
transit TEXT,
connection BOOLEAN,
wait INT,
PRIMARY KEY((flight_month, passenger_id), flight_year)
)

def create_schema(session):
    log.info("Creating model schema")
    session.execute(CREATE_PASSENGERS_TABLE)

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
    Página 20 de 32
    travel_reason,
    stay,
    transit,
    connection,
    wait) VALUES(
    uuid(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

def get_most_popular_travel_months(session, months_qty):
    log.info(f"Retrieving the {months_qty} most popular months for travel")
    stmt = session.prepare(SELECT_POPULAR_MONTHS)
    rows = session.execute(stmt)
