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

class Pracownik(Base):
    __tablename__ = 'pracownicy'

    id_pracownika = Column(Integer, primary_key=True)
    imię = Column(String)
    nazwisko = Column(String)
    działy = Column(String)
    data_zatrudnienia = Column(Date)
    aktywny = Column(Integer)
    pensja = Column(DECIMAL)


class Rodzaj(Base):
    __tablename__ = 'rodzaje'

    id_wycieczki = Column(Integer, primary_key=True)
    nazwa_wycieczki = Column(String)
    opis = Column(String)
    max_liczba_uczestników = Column(Integer)
    min_liczba_uczestników = Column(Integer)
    koszt_udziału = Column(DECIMAL)
    koszt_organizacji = Column(DECIMAL)
    kontakt_do_bliskich = Column(Integer)


class ZrealizowanaWycieczka(Base):
    __tablename__ = 'zrealizowane'

    id_eventu = Column(Integer, primary_key=True)
    id_wycieczki = Column(Integer, ForeignKey('rodzaje.id_wycieczki'))
    data_wyjazdu = Column(Date)
    liczba_uczestników = Column(Integer)
    id_pracownika = Column(Integer, ForeignKey('pracownicy.id_pracownika'))

    wycieczka = relationship("Rodzaj")
    pracownik = relationship("Pracownik")


faker = Faker('pl_PL')
k=[]

dzialy = ['it','marketing','ksiegowosc','obsluga_klienta','obsluga_wycieczek']
place ={ 'it':(6000,10000), 'marketing':(5000,7000),'ksiegowosc':(5000,7000),'obsluga_klienta':(4300,5500),'obsluga_wycieczek':(4300,6000)}
obsluga = []


Session = sessionmaker(bind=engine)
session = Session()

for x in range(7):
    dzial = random.choice(dzialy)
    if dzial != 'obsluga_wycieczek':
        dzialy.remove(dzial)
    else:
        obsluga.append(x)

    min_pensja, max_pensja = place[dzial]

    pracownik = Pracownik(
        imię = faker.first_name(),
        nazwisko = faker.last_name(),
        działy = dzial,
        data_zatrudnienia = faker.date_between(start_date=datetime(2023, 5, 1), end_date=datetime(2023, 12, 1)),
        aktywny = random.choice([0,1,1,1,1,1]),
        pensja = random.randint(min_pensja, max_pensja)
    )
    
    session.add(pracownik)

wycieczki = session.query(Rodzaj).all()
p = session.query(Pracownik).all()
z=[]
for x in range(30):
    o = []
    id = random.randint(1,6)
    data = faker.date_between(start_date=datetime(2023, 5, 1), end_date=datetime(2024, 12, 31))
    for pracownik in p:
            if pracownik.data_zatrudnienia <= data and pracownik.działy == 'obsluga_wycieczek' :
                o.append(pracownik.id_pracownika)
                #print(x.data_zatrudnienia)
    print(o)
    if len(o) > 0:
        realizacja = ZrealizowanaWycieczka(
            id_wycieczki = id,
            data_wyjazdu = data,
            liczba_uczestników = random.randint(wycieczki[id-1].min_liczba_uczestników,wycieczki[id-1].max_liczba_uczestników), 
            id_pracownika = random.choice(o)
        )

        z.append(realizacja)


for prac in p:
    session.add(prac)

for realizacja in z:
    session.add(realizacja)

session.commit() 

session.close()
engine.dispose()