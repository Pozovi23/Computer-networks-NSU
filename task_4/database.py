import json

from sqlalchemy import Column, String, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Tool(Base):
    __tablename__ = "tools"

    name = Column(String(50), primary_key=True)
    amount_of_reviews = Column(String(50), unique=False, nullable=True)
    description = Column(String(50), unique=False, nullable=True)
    voltage = Column(String(50), unique=False, nullable=True)
    weight = Column(String(50), unique=False, nullable=True)
    max_torque = Column(String(50), unique=False, nullable=True)


def write_to_database(tools_and_its_features_list):
    database_url = "postgresql://postgres:12345rcpc@127.0.0.1/networks"
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    for tool_data in tools_and_its_features_list:
        if len(tool_data.keys()) == 0:
            continue

        insert_query = text(
            """INSERT INTO tools (name, description, amount_of_reviews, voltage, weight, max_torque)
            VALUES (:name, :description, :amount_of_reviews, :voltage, :weight, :max_torque)
            ON CONFLICT (name) DO NOTHING"""
        )

        session.execute(
            insert_query,
            {
                "name": tool_data.get("name"),
                "description": tool_data.get("description"),
                "amount_of_reviews": tool_data.get("amount_of_reviews"),
                "voltage": tool_data.get("Напряжение аккумулятора"),
                "weight": tool_data.get("Вес нетто"),
                "max_torque": tool_data.get("Max крутящий момент "),
            },
        )

    session.commit()
    session.close()


def read_from_database():
    database_url = "postgresql://postgres:12345rcpc@127.0.0.1/networks"

    engine = create_engine(database_url)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    tools = session.query(Tool).all()
    tools_list = []
    for tool in tools:
        tools_list.append(
            {
                "name": tool.name,
                "description": tool.description,
                "amount_of_reviews": tool.amount_of_reviews,
                "voltage": tool.voltage,
                "weight": tool.weight,
                "max_torque": tool.max_torque,
            }
        )

    session.close()
    with open("tools_data.json", "w", encoding="utf-8") as json_file:
        json.dump(tools_list, json_file, ensure_ascii=False, indent=4)

    return json.dumps(tools_list, ensure_ascii=False)
