from parser import parser

from database import read_from_database
from fastapi import FastAPI, Query

app = FastAPI()


def app_interaction():
    @app.get("/parser")
    async def parse_page(number_of_page: int = Query(...)):
        parser(number_of_page)
        return "parsed successfully"

    @app.get("/read_database")
    async def read_database():
        response = read_from_database()
        return response


def main():
    app_interaction()


main()
