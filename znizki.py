from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, Date, DECIMAL, ForeignKey, MetaData, Table
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from faker import Faker
import random
from datetime import datetime

engine = create_engine("mysql+pymysql://team09:te%40mzaoq@giniewicz.it:3306/team09")
metadata = MetaData()
Base = declarative_base()


class Znizka(Base):
    __tablename__ = 'zniżki'

    id_zniżki = Column(Integer, primary_key=True, autoincrement=True)
    nazwa_zniżki = Column(String)
    procent = Column(Integer)

znizki = [
    Znizka(id_zniżki=1, nazwa_zniżki="ulgowa", procent=10),
    Znizka(id_zniżki=2, nazwa_zniżki="partnerska", procent=5),
    Znizka(id_zniżki=3, nazwa_zniżki="rodzinna", procent=15)
]

Session = sessionmaker(bind=engine)
session = Session()

for znizka in znizki:
    session.add(znizka)

session.commit()

# Zamknięcie sesji
session.close()
engine.dispose()