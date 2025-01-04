from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, Date, DECIMAL, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from faker import Faker
import random
from datetime import datetime

engine = create_engine("mysql+pymysql://team09:te%40mzaoq@giniewicz.it:3306/team09")

Base = declarative_base()

class Klienci(Base):
    __tablename__ = 'klienci'
    id_klienta = Column(Integer, primary_key=True, autoincrement=True)
    imię = Column(String)
    nazwisko = Column(String)
    numer_telefonu = Column(Integer)
    mail = Column(String)
    adres = Column(String)
    numer_1 = Column(Integer)
    numer_2 = Column(Integer)


class KosztyOrganizacji(Base):
    __tablename__ = 'koszty_organizacji'
    id_płatności = Column(Integer, primary_key=True, autoincrement=True)
    id_wycieczki = Column(Integer, ForeignKey('rodzaje.id_wycieczki'))
    nazwa_kosztu = Column(String)
    koszt = Column(DECIMAL)


class Pracownicy(Base):
    __tablename__ = 'pracownicy'
    id_pracownika = Column(Integer, primary_key=True, autoincrement=True)
    imię = Column(String)
    nazwisko = Column(String)
    data_zatrudnienia = Column(Date)
    aktywny = Column(Boolean)
    działy = Column(String)

    zrealizowane = relationship("Zrealizowane", back_populates="pracownik")

class Rodzaje(Base):
    __tablename__ = 'rodzaje'
    id_wycieczki = Column(Integer, primary_key=True, autoincrement=True)
    nazwa_wycieczki = Column(String)
    opis = Column(String)
    max_liczba_uczestników = Column(Integer)
    min_liczba_uczestników = Column(Integer)
    koszt_udzialu = Column(DECIMAL)
    koszt_organizacji = Column(DECIMAL)
    kontakt_do_bliskich = Column(Boolean)

    zrealizowane = relationship("Zrealizowane", back_populates="wycieczka")



class TransakcjeFirma(Base):
    __tablename__ = 'transakcje_firma'
    id_wyjazdu = Column(Integer, primary_key=True, autoincrement=True)
    koszt_zorganizowania = Column(DECIMAL)
    czy_zrealizowany = Column(Boolean)
    data_płatności = Column(Date)
    rodzaj_płatności = Column(String)
    id_pracownika = Column(Integer, ForeignKey('pracownicy.id_pracownika'))


class TransakcjeKlienci(Base):
    __tablename__ = 'transakcje_klienci'
    id_transakcji = Column(Integer, primary_key=True, autoincrement=True)
    id_klienta = Column(Integer, ForeignKey('klienci.id_klienta'), nullable=False)
    id_wyjazdu = Column(Integer, ForeignKey('transakcje_firma.id_wyjazdu'))
    koszt_udziału = Column(DECIMAL)
    rodzaj_płatności = Column(String)
    czy_zapłacono = Column(Boolean, default=False)


class Zrealizowane(Base):
    __tablename__ = 'zrealizowane'
    id_wyjazdu = Column(Integer,  primary_key=True, autoincrement=True)
    id_wycieczki = Column(Integer, ForeignKey('rodzaje.id_wycieczki'))
    data_wyjazdu = Column(Date)
    liczba_uczestników = Column(Integer)
    id_pracownika = Column(Integer, ForeignKey('pracownicy.id_pracownika'))

    wycieczka = relationship("Rodzaje", back_populates="zrealizowane")
    pracownik = relationship("Pracownicy", back_populates="zrealizowane")



faker = Faker('pl_PL')
k=[]
p=[]
dzialy = ['it','marketing','ksiegowosc','obsluga_klienta','obsluga_wycieczek']
place ={ 'it':(6000,10000), 'marketing':(5000,7000),'ksiegowosc':(5000,7000),'obsluga_klienta':(4300,5500),'obsluga_wycieczek':(4300,6000)}
obsluga = []

idp = 1 
for x in range(7):
    dzial = random.choice(dzialy)
    if dzial != 'obsluga_wycieczek':
        dzialy.remove(dzial)
    else:
        obsluga.append(x)

    pracownik = Pracownicy(
        id_pracownika = idp,
        imię = faker.first_name(),
        nazwisko = faker.last_name(),
        działy = dzial,
        data_zatrudnienia = faker.date_between(start_date=datetime(2023, 5, 1), end_date=datetime(2024, 5, 1)),
        aktywny = random.choice([0,1,1,1,1,1]),
    )
    
    p.append(pracownik)
    idp+=1

w1 = Rodzaje(
    nazwa_wycieczki='Spacer po dachach Wrocławia',
    opis='Wyobraź sobie nocną wycieczkę po dachach budynków na Starym Mieście. Z pomocą lin i uprzęży wspinasz się na szczyty gotyckich kościołów i modernistycznych wieżowców, oglądając Wrocław z perspektywy ptaka. Na koniec na najwyższym punkcie miasta czeka niespodzianka, tajemniczy koncert „z góry”.',
    max_liczba_uczestników=random.randint(35, 40),
    min_liczba_uczestników=30,
    koszt_udzialu=400,
    koszt_organizacji=8600,
    kontakt_do_bliskich=True
)

w2 = Rodzaje(
    nazwa_wycieczki='Symulacja inwazji smoków',
    opis='Cały Ostrów Tumski zostaje zamieniony w arenę walki z mitycznymi smokami. Wyposażony w zestaw wirtualnej rzeczywistości i fantazyjny sprzęt bojowy przemierzasz ulice, walcząc z wielkimi bestiami, które niszczą mosty i wspinają się na kościoły. Czy uda Ci się uratować miasto?',
    max_liczba_uczestników=random.randint(35, 40),
    min_liczba_uczestników=30,
    koszt_udzialu=500,
    koszt_organizacji=10000,
    kontakt_do_bliskich=True
)

w3 = Rodzaje(
    nazwa_wycieczki='Skok na bungee z Mostu Grunwaldzkiego',
    opis='Poczuj prawdziwą dawkę adrenaliny, skacząc na bungee z Mostu Grunwaldzkiego. Z wysokości mostu wznosisz się nad Odrą, czując przypływ emocji, które tylko skok na bungee może zapewnić.',
    max_liczba_uczestników=random.randint(35, 40),
    min_liczba_uczestników=30,
    koszt_udzialu=300,
    koszt_organizacji=5500,
    kontakt_do_bliskich=True
)

w4 = Rodzaje(
    nazwa_wycieczki='Lot motoparalotnią nad Wrocławiem',
    opis='Unikalna okazja, aby zobaczyć Wrocław z powietrza podczas lotu motoparalotnią. Wznosisz się ponad miasto, podziwiając panoramę, a nasz instruktor dba o Twoje bezpieczeństwo i komfort podczas lotu.',
    max_liczba_uczestników=random.randint(35, 40),
    min_liczba_uczestników=30,
    koszt_udzialu=325,
    koszt_organizacji=5500,
    kontakt_do_bliskich=True
)

w5 = Rodzaje(
    nazwa_wycieczki='Podwodna ekspedycja w Odrze',
    opis='Eksploracja dna Odry w specjalnej łodzi podwodnej. Odkryj tajemnice zatopionych wraków, mostów i tajemnicze skarby, a także poznaj historię Wrocławia z perspektywy rzeki.',
    max_liczba_uczestników=random.randint(10, 15),
    min_liczba_uczestników=10,
    koszt_udzialu=1560,
    koszt_organizacji=12000,
    kontakt_do_bliskich=True
)

w6 = Rodzaje(
    nazwa_wycieczki='Tyrolka z Mostu Zwierzynieckiego',
    opis='Poczuj dreszczyk emocji, zjeżdżając na tyrolce z Mostu Zwierzynieckiego. Podziwiaj panoramę Wrocławia z niecodziennej perspektywy, z wysokości mostu, i przeżyj niezapomnianą przygodę.',
    max_liczba_uczestników=random.randint(35, 40),
    min_liczba_uczestników=30,
    koszt_udzialu=150,
    koszt_organizacji=3500,
    kontakt_do_bliskich=True
)
z=[]
wycieczki = [w1, w2, w3, w4, w5, w6]
for x in range(30):
    o = []
    id = random.randint(1,6)
    data = faker.date_between(start_date=datetime(2023, 5, 1), end_date=datetime(2024, 12, 31))
    #print(data)
    for x in p:
            if x.data_zatrudnienia > data:
                o.append(x.id_pracownika)
                #print(x.data_zatrudnienia)
    print(o)
    if len(o) > 0:
        realizacja = Zrealizowane(
            id_wycieczki = id,
            data_wyjazdu = data,
            liczba_uczestników = random.randint(wycieczki[id-1].min_liczba_uczestników,wycieczki[id-1].max_liczba_uczestników), 
            id_pracownika = random.choice(o)
        )

        z.append(realizacja)

Session = sessionmaker(bind=engine)
session = Session()

for prac in p:
    session.add(prac)

for realizacja in z:
    session.add(realizacja)

session.commit() 

session.close()
engine.dispose()