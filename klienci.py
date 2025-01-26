from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, Date, DECIMAL, ForeignKey, Table, Null
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from faker import Faker
import random
from datetime import datetime

engine = create_engine("mysql+pymysql://team09:te%40mzaoq@giniewicz.it:3306/team09")

Base = declarative_base()

class Klient(Base):
    __tablename__ = 'klienci'
    id_klienta = Column(Integer, primary_key=True, autoincrement=True)
    imię = Column(String)
    nazwisko = Column(String)
    numer_telefonu = Column(String)
    mail = Column(String)
    adres = Column(String)
    numer_1 = Column(String)
    numer_2 = Column(String)
    miasto = Column(String)
    kod_pocztowy = Column(String)
    id_zniżki = Column(Integer)
    wiek = Column(Integer)


class ZrealizowanaWycieczka(Base):
    __tablename__ = 'zrealizowane'

    id_eventu = Column(Integer, primary_key=True)
    id_wycieczki = Column(Integer, ForeignKey('rodzaje.id_wycieczki'))
    data_wyjazdu = Column(Date)
    liczba_uczestników = Column(Integer) 
    id_pracownika = Column(Integer, ForeignKey('pracownicy.id_pracownika'))



faker = Faker('pl_PL')
k=[]


liczba_ucz = 0
Session = sessionmaker(bind=engine)
session = Session()

wyjazdy = session.query(ZrealizowanaWycieczka).all()
for x in wyjazdy:
    liczba_ucz+=x.liczba_uczestników
print(liczba_ucz)

nowi = int(liczba_ucz*0.7)
for x in range(nowi):
    klient = Klient(
        imię=faker.first_name(),
        nazwisko=faker.last_name(),
        numer_telefonu=faker.phone_number(),
        mail=faker.email(domain='poczta.pl'),
        adres=f"{faker.street_address()} {faker.building_number()}",
        numer_1=faker.phone_number(),
        numer_2=faker.phone_number(),
        miasto=faker.city(),
        kod_pocztowy=faker.postcode(),
        wiek=random.randint(18, 70) 
        )
    if random.randint(0,9) <= 2:
            klient.id_zniżki = random.randint(1,3)

    session.add(klient)
session.commit()

session.close()
engine.dispose()