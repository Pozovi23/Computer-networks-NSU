from fastapi import FastAPI, Query

from database import read_from_database, write_to_database

app = FastAPI()


def app_interaction():
    @app.get("/get_url")
    async def get_url(url: str = Query(...)):
        write_to_database(url)
        return "wrote successfully"

    @app.get("/read_database")
    async def read_database():
        response = read_from_database()
        return response


def main():
    app_interaction()


main()
