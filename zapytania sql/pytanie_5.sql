SELECT 
   pracownicy.id_pracownika,
   pracownicy.imię,
   pracownicy.nazwisko,
   COUNT(zrealizowane.id_eventu) AS liczba_wycieczek,
   SUM(zrealizowane.liczba_uczestników) AS liczba_uczestników
FROM 
   zrealizowane
JOIN 
   pracownicy ON zrealizowane.id_pracownika = pracownicy.id_pracownika
GROUP BY 
   pracownicy.id_pracownika, pracownicy.nazwisko
ORDER BY 
   liczba_wycieczek DESC, liczba_uczestników DESC;