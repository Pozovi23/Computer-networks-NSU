import json

from sqlalchemy import Column, String, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class URL(Base):
    __tablename__ = "urls"
    url = Column(String(50), primary_key=True)


def write_to_database(url):
    database_url = "postgresql://postgres:12345rcpc@database:5432/urls"
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    insert_query = text(
        """INSERT INTO urls (url)
        VALUES (:url)
        ON CONFLICT (url) DO NOTHING"""
    )

    session.execute(
        insert_query,
        {
            "url": url,
        },
    )

    session.commit()
    session.close()


def read_from_database():
    database_url = "postgresql://postgres:12345rcpc@database:5432/urls"

    engine = create_engine(database_url)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    urls_session = session.query(URL).all()
    urls = []

    for url in urls_session:
        urls.append(url.url)

    session.close()
    return json.dumps(urls, ensure_ascii=False)
