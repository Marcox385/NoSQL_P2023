#!/usr/bin/env python

"""
Generador de datos para proyecto de Bases de Datos No Relacionales
ITESO 
"""
import argparse
import csv
import datetime

from random import choice, randint, randrange


airlines = ["American Airlines", "Delta Airlines", "Alaska", "Aeromexico", "Volaris"]
airports = ["PDX", "GDL", "SJC", "LAX", "JFK"]
genders = ["male", "female", "unspecified", "undisclosed"]
reasons = ["On vacation/Pleasure", "Business/Work", "Back Home"]
stays = ["Hotel", "Short-term homestay", "Home", "Friend/Family"]
transits = ["Airport cab", "Car rental", "Mobility as a service", "Public Transportation", "Pickup", "Own car"]
connections = [True, False]


def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = randrange(days_between_dates)
    rand_date = start_date + datetime.timedelta(days=random_number_of_days)
    return rand_date


def generate_dataset(output_file, rows):
    with open(output_file, "w") as fd:
        fieldnames = ["airline", "from" ,"to", "day", "month", "year","age", "gender", "reason", "stay", "transit", "connection", "wait"]
        fp_dict = csv.DictWriter(fd, fieldnames=fieldnames)
        fp_dict.writeheader()
        for i in range(rows):
            from_airport = choice(airports)
            to_airport = choice(airports)
            while from_airport == to_airport:
                to_airport = choice(airports)
            date = random_date(datetime.datetime(2013, 1, 1), datetime.datetime(2023, 4, 25))
            reason = choice(reasons)
            stay = choice(stays)
            connection = choice(connections)
            wait = randint(30, 720)
            transit = choice(transits)
            if not connection:
               wait = 0
            else:
                transit = ""
            if reason == "Back Home":
                stay = "Home"
                connection = False
                wait = 0
                
            line = {
                "airline": choice(airlines),
                "from":  from_airport,
                "to":  to_airport,
                "day": date.day,
                "month": date.month,
                "year": date.year,
                "age": randint(1,90),
                "gender": choice(genders),
                "reason": reason,
                "stay": stay,
                "transit": transit,
                "connection": connection,
                "wait": wait,
            }
            fp_dict.writerow(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output",
            help="Specify the output filename of your csv, defaults to: flight_passengers.csv", default="flight_passengers.csv")
    parser.add_argument("-r", "--rows",
            help="Amount of random generated entries for the dataset, defaults to: 100", type=int, default=100)

    args = parser.parse_args()
    
    print(f"Generating {args.rows} for flight passenger dataset")
    generate_dataset(args.output, args.rows)
    print(f"Completed generating dataset in {args.output}")
