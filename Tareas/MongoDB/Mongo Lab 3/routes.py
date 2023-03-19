#!/usr/bin/env python3
# IS727272 - Cordero Hernández, Marco Ricardo
import re

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from model import Book, BookUpdate

router = APIRouter()

@router.post("/", response_description="Post a new book", status_code=status.HTTP_201_CREATED, response_model=Book)
def create_book(request: Request, book: Book = Body(...)):
    book = jsonable_encoder(book)
    new_book = request.app.database["books"].insert_one(book)
    created_book = request.app.database["books"].find_one(
        {"_id": new_book.inserted_id}
    )

    return created_book

@router.get("/", response_description="Get all books", response_model=List[Book])
def list_books(request: Request, rating: float = 0, num_pages: str = '', ratings_count: str = '', title: str = '', limit: int = 10, skip: int = 0):
    search_params = {}

    allowed_operators = ('eq', 'gt', 'gte', 'lt', 'lte', 'ne')
    locals_vals = zip(list(locals().keys())[2:-4], list(locals().values())[2:-4])

    for k, v in locals_vals:
        param_re = re.search(r'(\d+)(.*)', v)

        if (param_re):
            if (not param_re.group(2)):
                search_params[k] = float(param_re.group(1))
            else:
                if (param_re.group(2) not in allowed_operators):
                    print(f'**** Operator "{param_re.group(2)}" not allowed')
                else:
                    search_params[k] = {f'${param_re.group(2)}': float(param_re.group(1))}
        elif (v):
            search_params[k] = {'$regex': v}
    
    print(search_params)
    
    books = list(request.app.database["books"]
                 .find(search_params)
                 .skip(skip)
                 .limit(limit))
    return books

@router.get("/{id}", response_description="Get a single book by id", response_model=Book)
def find_book(id: str, request: Request):
    if (book := request.app.database["books"].find_one({"_id": id})) is not None:
        return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

@router.put("/{id}", response_description="Update a book by id", response_model=Book)
def update_book(id: str, request: Request, book: BookUpdate = Body(...)):
    request.app.database["books"].update_one({"_id": id}, {"$set": jsonable_encoder(book)})
    updated_book = request.app.database["books"].find_one(
        {"_id": id}
    )

    return updated_book

@router.delete("/{id}", response_description="Delete a book")
def delete_book(id: str, request: Request, response: Response):
    if (request.app.database["books"].delete_one({"_id": id})) is not None:
        print(f'Successfully deleted book with id {id}')
        return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} couldn't get deleted (not found)")