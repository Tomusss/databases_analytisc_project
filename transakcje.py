from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, Date, DECIMAL, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from faker import Faker
import random
from datetime import datetime, timedelta
from decimal import Decimal

engine = create_engine("mysql+pymysql://team09:te%40mzaoq@giniewicz.it:3306/team09")

Base = declarative_base()

class Znizka(Base):
    __tablename__ = 'zniżki'
    id_zniżki = Column(Integer, primary_key=True)
    nazwa_zniżki = Column(String)
    procent = Column(Integer)

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
     
class Rodzaj(Base):
    __tablename__ = "rodzaje"

    id_wycieczki = Column(Integer, primary_key=True, autoincrement=True)
    nazwa_wycieczki = Column(String, nullable=False)
    opis = Column(String, nullable=True)
    max_liczba_uczestników = Column(Integer, nullable=False)
    min_liczba_uczestników = Column(Integer, nullable=False)
    koszt_udziału = Column(DECIMAL, nullable=False)  
    koszt_organizacji = Column(DECIMAL, nullable=False)
    kontakt_do_bliskich = Column(Boolean, nullable=False)



class TransakcjeFirma(Base):    
    __tablename__ = 'transakcje_firma'
    id_transakcji= Column(Integer, primary_key=True, autoincrement=True)
    id_eventu = Column(Integer)
    czy_zrealizowany = Column(Boolean)
    data_płatności = Column(Date)


class TransakcjeKlienci(Base):
    __tablename__ = 'transakcje_klienci'
    id_transakcji = Column(Integer, primary_key=True, autoincrement=True)
    id_klienta = Column(Integer, ForeignKey('klienci.id_klienta'), nullable=False)
    id_eventu = Column(Integer, ForeignKey('zrealizowane.id_eventu'))
    koszt_udziału = Column(DECIMAL)
    rodzaj_płatności = Column(String)
    czy_zapłacono = Column(Boolean, default=False)
    data_płatności = Column(Date)


class ZrealizowanaWycieczka(Base):
    __tablename__ = 'zrealizowane'

    id_eventu = Column(Integer, primary_key=True)
    id_wycieczki = Column(Integer, ForeignKey('rodzaje.id_wycieczki'))
    data_wyjazdu = Column(Date)
    liczba_uczestników = Column(Integer)
    id_pracownika = Column(Integer, ForeignKey('pracownicy.id_pracownika'))

    wycieczka = relationship("Rodzaj")


faker = Faker('pl_PL')

liczba_ucz = 0
Session = sessionmaker(bind=engine)
session = Session()

platnosci = ['przelew','karta', 'gotowka','blik']
wyjazdy = session.query(ZrealizowanaWycieczka).all()
rodzaje = session.query(Rodzaj).all()
id_wyjazdow = [wyjazd.id_eventu for wyjazd in wyjazdy] 
uczestnicy_wyj = []

for x in wyjazdy:
    liczba_ucz+=x.liczba_uczestników
nowi = int(liczba_ucz*0.7)

for wyjazd in session.query(ZrealizowanaWycieczka).order_by(ZrealizowanaWycieczka.data_wyjazdu).all():
        data_płatnosci = faker.date_between(start_date=wyjazd.data_wyjazdu - timedelta(days=30), end_date=wyjazd.data_wyjazdu + timedelta(days=7))
        transakcja_firma = TransakcjeFirma(
            id_eventu = wyjazd.id_eventu,
            czy_zrealizowany=True,
            data_płatności=data_płatnosci,
        )
            
        session.add(transakcja_firma)

for x in range(nowi): 
    wyjazd = random.choice(wyjazdy)
    przypisani_klienci = session.query(TransakcjeKlienci).filter_by(id_eventu=wyjazd.id_eventu).count()
    
    if przypisani_klienci < wyjazd.liczba_uczestników:
        klient = random.choice(session.query(Klient).all())
        
        istniejąca_transakcja = session.query(TransakcjeKlienci).filter_by(
            id_klienta=klient.id_klienta,
            id_eventu=wyjazd.id_eventu
        ).first()
        
        if not istniejąca_transakcja:
            znizka = session.query(Znizka).filter_by(id_zniżki=klient.id_zniżki).first()

            transakcja = TransakcjeKlienci(
                id_klienta=klient.id_klienta,
                id_eventu=wyjazd.id_eventu,
                koszt_udziału = wyjazd.wycieczka.koszt_udziału * Decimal((1 - (znizka.procent / 100) if znizka else 1)),
                rodzaj_płatności=random.choice(platnosci),
                czy_zapłacono=True,
                data_płatności=faker.date_between(
                    start_date=datetime(2023, 5, 1),
                    end_date=wyjazd.data_wyjazdu
                )
            )
            session.add(transakcja)


for wyjazdd in wyjazdy:
    przypisani_klienci = session.query(TransakcjeKlienci).filter_by(id_eventu=wyjazdd.id_eventu).all()

    while len(przypisani_klienci) < wyjazdd.liczba_uczestników:
        klient = random.choice(session.query(Klient).all())
        data_max = wyjazdd.data_wyjazdu
        znizka = session.query(Znizka).filter_by(id_zniżki=klient.id_zniżki).first()


        transakcja = TransakcjeKlienci(
            id_klienta=klient.id_klienta,
            id_eventu=wyjazdd.id_eventu,
            koszt_udziału=wyjazdd.wycieczka.koszt_udziału*Decimal((1 - (znizka.procent / 100) if znizka else 1)),
            rodzaj_płatności=random.choice(platnosci),
            czy_zapłacono=True,
            data_płatności=faker.date_between(start_date=datetime(2023, 5, 1), end_date=data_max)
        )

        session.add(transakcja)

        przypisani_klienci.append(transakcja)

session.commit()








session.close()
engine.dispose()