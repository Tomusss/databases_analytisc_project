from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, Date, DECIMAL, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from faker import Faker
import random
from datetime import datetime, timedelta

engine = create_engine("mysql+pymysql://team09:te%40mzaoq@giniewicz.it:3306/team09")

Base = declarative_base()

class Klienci(Base):
    __tablename__ = 'klienci'
    id_klienta = Column(Integer, primary_key=True, autoincrement=True)
    imię = Column(String)
    nazwisko = Column(String)
    numer_telefonu = Column(String)
    mail = Column(String)
    adres = Column(String)
    numer_1 = Column(String)
    numer_2 = Column(String)


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


class TransakcjeKlienci(Base):
    __tablename__ = 'transakcje_klienci'
    id_transakcji = Column(Integer, primary_key=True, autoincrement=True)
    id_klienta = Column(Integer, ForeignKey('klienci.id_klienta'), nullable=False)
    id_wyjazdu = Column(Integer, ForeignKey('transakcje_firma.id_wyjazdu'))
    koszt_udziału = Column(DECIMAL)
    rodzaj_płatności = Column(String)
    czy_zapłacono = Column(Boolean, default=False)
    data_płatności = Column(Date)


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

liczba_ucz = 0
Session = sessionmaker(bind=engine)
session = Session()

platnosci = ['przelew','karta', 'gotowka','blik']
wyjazdy = session.query(Zrealizowane).all()
rodzaje = session.query(Rodzaje).all()
id_wyjazdow = [wyjazd.id_wyjazdu for wyjazd in wyjazdy] 
uczestnicy_wyj = []

for x in wyjazdy:
    liczba_ucz+=x.liczba_uczestników
nowi = int(liczba_ucz*0.7)

"""for wyjazd in session.query(Zrealizowane).all():
        rodzaj_wycieczki = session.query(Rodzaje).filter(Rodzaje.id_wycieczki == wyjazd.id_wycieczki).first()
        if rodzaj_wycieczki:
            koszt_zorganizowania = rodzaj_wycieczki.koszt_organizacji
            data_płatności = faker.date_between(start_date=wyjazd.data_wyjazdu - timedelta(days=30), end_date=wyjazd.data_wyjazdu + timedelta(days=7))
            rodzaj_płatności = random.choice(platnosci)
            transakcja_firma = TransakcjeFirma(
                koszt_zorganizowania=koszt_zorganizowania,
                czy_zrealizowany=True,
                data_płatności=data_płatności,
                rodzaj_płatności=rodzaj_płatności
            )
            
            session.add(transakcja_firma)"""

for x in range(nowi): 
    wyjazd = random.choice(wyjazdy)
    przypisani_klienci = session.query(TransakcjeKlienci).filter_by(id_wyjazdu=wyjazd.id_wyjazdu).count()
    
    if przypisani_klienci < wyjazd.liczba_uczestników:
        klient = random.choice(session.query(Klienci).all())
        
        istniejąca_transakcja = session.query(TransakcjeKlienci).filter_by(
            id_klienta=klient.id_klienta,
            id_wyjazdu=wyjazd.id_wyjazdu
        ).first()
        
        if not istniejąca_transakcja:
            transakcja = TransakcjeKlienci(
                id_klienta=klient.id_klienta,
                id_wyjazdu=wyjazd.id_wyjazdu,
                koszt_udziału=wyjazd.wycieczka.koszt_udzialu,
                rodzaj_płatności=random.choice(platnosci),
                czy_zapłacono=True,
                data_płatności=faker.date_between(
                    start_date=datetime(2023, 5, 1),
                    end_date=wyjazd.data_wyjazdu
                )
            )
            session.add(transakcja)


for wyjazdd in wyjazdy:
    przypisani_klienci = session.query(TransakcjeKlienci).filter_by(id_wyjazdu=wyjazdd.id_wyjazdu).all()

    while len(przypisani_klienci) < wyjazdd.liczba_uczestników:
        klient = random.choice(session.query(Klienci).all())
        data_max = wyjazdd.data_wyjazdu

        transakcja = TransakcjeKlienci(
            id_klienta=klient.id_klienta,
            id_wyjazdu=wyjazdd.id_wyjazdu,
            koszt_udziału=rodzaje[wyjazdd.id_wycieczki - 1].koszt_udzialu,
            rodzaj_płatności=random.choice(platnosci),
            czy_zapłacono=True,
            data_płatności=faker.date_between(start_date=datetime(2023, 5, 1), end_date=data_max)
        )

        session.add(transakcja)

        przypisani_klienci.append(transakcja)

session.commit()








session.close()
engine.dispose()