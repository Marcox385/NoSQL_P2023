#!/usr/bin/env python3
# IS727272 - Cordero Hernández, Marco Ricardo
import argparse
import logging
import os, sys
import requests
import json

# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('books.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to API connection
BOOKS_API_URL = os.getenv("BOOKS_API_URL", "http://localhost:8000")

def print_book(book):
    for k in book.keys():
        print(f"{k}: {book[k]}")
    print("="*50)

def list_books(rating):
    suffix = "/book"
    endpoint = BOOKS_API_URL + suffix
    params = {
        "rating": rating
    }
    response = requests.get(endpoint, params=params) if rating else requests.get(endpoint)
    if response.ok:
        json_resp = response.json()
        for book in json_resp:
            print_book(book)
    else:
        print(f"Error: {response}")

def get_book_by_id(id):
    suffix = f"/book/{id}"
    endpoint = BOOKS_API_URL + suffix
    response = requests.get(endpoint)
    if response.ok:
        json_resp = response.json()
        print_book(json_resp)
    else:
        print(f"Error: {response}")

def update_book(id, json_file): # Done
    data = {}

    with (open(json_file, 'r')) as f:
        data = json.loads(''.join(f.readlines()))

    suffix = f"/book/{id}"
    endpoint = BOOKS_API_URL + suffix
    response = requests.put(endpoint, json = data)
    if response.ok:
        print(f'Successfully updated book with id {id}')
        print_book(response.json())
    else:
        print(f"Error: {response}")

def delete_book(id): # Done
    suffix = f"/book/{id}"
    endpoint = BOOKS_API_URL + suffix
    response = requests.delete(endpoint)
    if response.ok:
        print(f'Successfully deleted book with id {id}')
    else:
        print(f"Error: {response}")

def main():
    log.info(f"Welcome to books catalog. App requests to: {BOOKS_API_URL}")

    parser = argparse.ArgumentParser()

    list_of_actions = ["search", "get", "update", "delete"]
    parser.add_argument("action", choices=list_of_actions,
            help="Action to be user for the books library")
    parser.add_argument("-i", "--id",
            help="Provide a book ID which related to the book action", default=None)
    parser.add_argument("-r", "--rating",
            help="Search parameter to look for books with average rating equal or above the param (0 to 5)", default=None)
    parser.add_argument("-j", "--json",
            help="JSON file parameter for book updating", default=None)

    args = parser.parse_args()

    if args.id and not args.action in ["get", "update", "delete"]:
        log.error(f"Can't use arg id with action {args.action}")
        sys.exit(1)

    if args.rating and args.action != "search":
        log.error(f"Rating arg can only be used with search action")
        sys.exit(1)
    
    if args.json and args.action != 'update':
        log.error(f'JSON file can only be passed when updating a book')
        sys.exit(1)

    if args.action == "search":
        list_books(args.rating)
    elif args.action == "get" and args.id:
        get_book_by_id(args.id)
    elif args.action == "update":
        update_book(args.id, args.json)
    elif args.action == "delete":
        delete_book(args.id)

if __name__ == "__main__":
    main()