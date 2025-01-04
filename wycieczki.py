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


class KosztyOrganizacji(Base):
    __tablename__ = 'koszty_organizacji'
    id_płatności = Column(Integer, primary_key=True, autoincrement=True)
    id_wycieczki = Column(Integer, ForeignKey('rodzaje.id_wycieczki'))
    nazwa_kosztu = Column(String)
    koszt = Column(DECIMAL)


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




w1 = Rodzaje(
    nazwa_wycieczki = 'Spacer po dachach Wrocławia',
    opis = 'Wyobraź sobie nocną wycieczkę po dachach budynków na Starym Mieście. Z pomocą lin i uprzęży wspinasz się na szczyty gotyckich kościołów i modernistycznych wieżowców, oglądając Wrocław z perspektywy ptaka. Na koniec na najwyższym punkcie miasta czeka niespodzianka, tajemniczy koncert „z góry”.',
    max_liczba_uczestników = random.randint(35,40),
    min_liczba_uczestników = 30,
    koszt_udzialu = 400,
    koszt_organizacji = 8600,
    kontakt_do_bliskich = True
)
w2 = Rodzaje(
nazwa_wycieczki='Symulacja inwazji smoków',
opis='Cały Ostrów Tumski zostaje zamieniony w arenę walki z mitycznymi smokami. '
        'Wyposażony w zestaw wirtualnej rzeczywistości i fantazyjny sprzęt bojowy '
        'przemierzasz ulice, walcząc z wielkimi bestiami, które niszczą mosty i wspinają się na kościoły. '
        'Czy uda Ci się uratować miasto?',
max_liczba_uczestników=random.randint(35, 40),
min_liczba_uczestników=30,
koszt_udzialu=500,
koszt_organizacji=10000,
kontakt_do_bliskich=True
)

koszty_w1 = [
    KosztyOrganizacji(nazwa_kosztu='Sprzęt wspinaczkowy', koszt=3000),
    KosztyOrganizacji(nazwa_kosztu='Ubezpieczenie uczestników', koszt=1000),
    KosztyOrganizacji(nazwa_kosztu='Organizacja koncertu', koszt=4000),
    KosztyOrganizacji(nazwa_kosztu='Transport i logistyka', koszt=600),
]

koszty_w2 = [
    KosztyOrganizacji(nazwa_kosztu='Wynajem sprzętu VR', koszt=5000),
    KosztyOrganizacji(nazwa_kosztu='Przygotowanie areny i efektów specjalnych', koszt=3500),
    KosztyOrganizacji(nazwa_kosztu='Ubezpieczenie uczestników', koszt=1500),
]

for x in koszty_w1:
    x.id_wycieczki = 1
for x in koszty_w2:
    x.id_wycieczki = 2




w3 = Rodzaje(
nazwa_wycieczki='Skok na bungee z Mostu Grunwaldzkiego',
opis='Poczuj prawdziwą dawkę adrenaliny, skacząc na bungee z Mostu Grunwaldzkiego. '
        'Z wysokości mostu wznosisz się nad Odrą, czując przypływ emocji, które tylko skok na bungee może zapewnić.',
max_liczba_uczestników=random.randint(35, 40),
min_liczba_uczestników=30,
koszt_udzialu=300,
koszt_organizacji=5500,
kontakt_do_bliskich=True
)

koszty_w3 = [
    KosztyOrganizacji(nazwa_kosztu='Sprzęt do skoków na bungee', koszt=2500),
    KosztyOrganizacji(nazwa_kosztu='Ubezpieczenie uczestników', koszt=800),
    KosztyOrganizacji(nazwa_kosztu='Transport i logistyka', koszt=500),
    KosztyOrganizacji(nazwa_kosztu='Przygotowanie mostu i zabezpieczenia', koszt=1700),
]

for x in koszty_w3:
    x.id_wycieczki = 3

w4 = Rodzaje(
nazwa_wycieczki='Lot motoparalotnią nad Wrocławiem',
opis='Unikalna okazja, aby zobaczyć Wrocław z powietrza podczas lotu motoparalotnią. '
        'Wznosisz się ponad miasto, podziwiając panoramę, a nasz instruktor dba o Twoje bezpieczeństwo i komfort podczas lotu.',
max_liczba_uczestników=random.randint(35, 40),
min_liczba_uczestników=30,
koszt_udzialu=325,
koszt_organizacji=5500,
kontakt_do_bliskich=True
)

koszty_w4 = [
    KosztyOrganizacji(nazwa_kosztu='Wynajem motoparalotni', koszt=3000),
    KosztyOrganizacji(nazwa_kosztu='Obsługa lotu', koszt=1000),
    KosztyOrganizacji(nazwa_kosztu='Paliwo i logistyka', koszt=800),
    KosztyOrganizacji(nazwa_kosztu='Ubezpieczenie uczestników', koszt=500) ,
    KosztyOrganizacji(nazwa_kosztu='Zabezpieczenie sprzętu', koszt=1200),
]

for x in koszty_w4:
    x.id_wycieczki = 4

w5 = Rodzaje(
nazwa_wycieczki='Podwodna ekspedycja w Odrze',
opis='Eksploracja dna Odry w specjalnej łodzi podwodnej. Odkryj tajemnice zatopionych wraków, mostów '
        'i tajemnicze skarby, a także poznaj historię Wrocławia z perspektywy rzeki.',
max_liczba_uczestników=random.randint(10, 15),
min_liczba_uczestników=10,
koszt_udzialu=1560,
koszt_organizacji=12000,
kontakt_do_bliskich=True
)
koszty_w5 = [
    KosztyOrganizacji(nazwa_kosztu='Wynajem łodzi podwodnej', koszt=5000),
    KosztyOrganizacji(nazwa_kosztu='Dodatokwy operator', koszt=2500),
    KosztyOrganizacji(nazwa_kosztu='Sprzęt nurkowy i bezpieczeństwo', koszt=1500),
    KosztyOrganizacji(nazwa_kosztu='Transport uczestników i sprzętu', koszt=1000),
    KosztyOrganizacji(nazwa_kosztu='Ubezpieczenie uczestników', koszt=1000),
]
for x in koszty_w5:
    x.id_wycieczki = 5

w6 = Rodzaje(
nazwa_wycieczki='Tyrolka z Mostu Zwierzynieckiego',
opis='Poczuj dreszczyk emocji, zjeżdżając na tyrolce z Mostu Zwierzynieckiego. '
        'Podziwiaj panoramę Wrocławia z niecodziennej perspektywy, z wysokości mostu, i przeżyj niezapomnianą przygodę.',
max_liczba_uczestników=random.randint(35, 40),
min_liczba_uczestników=30,
koszt_udzialu=150,
koszt_organizacji=3500,
kontakt_do_bliskich=True
)

koszty_w6 = [
    KosztyOrganizacji(nazwa_kosztu='Wynajem sprzętu tyrolki', koszt=2000),
    KosztyOrganizacji(nazwa_kosztu='Bezpieczeństwo i zabezpieczenia', koszt=800),
    KosztyOrganizacji(nazwa_kosztu='Transport i logistyka', koszt=700),
]

for x in koszty_w6:
    x.id_wycieczki = 6



Session = sessionmaker(bind=engine)
session = Session()

session.add(w1)
session.add(w2)
session.add(w3)
session.add(w4)
session.add(w5)
session.add(w6)

session.commit() 

for x in koszty_w1:
    session.add(x)
for x in koszty_w2:
    session.add(x)
for x in koszty_w3:
    session.add(x)
for x in koszty_w4:
    session.add(x)
for x in koszty_w5:
    session.add(x)
for x in koszty_w6:
    session.add(x)

session.commit() 

session.close()
engine.dispose()
