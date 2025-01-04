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


liczba_ucz = 0
Session = sessionmaker(bind=engine)
session = Session()

wyjazdy = session.query(Zrealizowane).all()

for x in wyjazdy:
    liczba_ucz+=x.liczba_uczestników
print(liczba_ucz)

"""nowi = int(liczba_ucz*0.7)
for x in range(nowi):
    klient = Klienci(
                imię=faker.first_name(),
                nazwisko=faker.last_name(),
                numer_telefonu=faker.phone_number(),
                mail=faker.email(domain='poczta.pl'),
                adres=faker.address(),
                numer_1=faker.phone_number(),
                numer_2=faker.phone_number()
            )
    session.add(klient)
session.commit()"""

session.close()
engine.dispose()