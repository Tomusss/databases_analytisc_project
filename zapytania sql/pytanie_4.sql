SELECT 
   rodzaje.koszt_udzialu AS cena_wycieczki,
   SUM(zrealizowane.liczba_uczestników) AS liczba_uczestników,
   ROUND(SUM(zrealizowane.liczba_uczestników) * 100.0 / (SELECT SUM(liczba_uczestników) FROM zrealizowane), 2) AS procent_uczestników
FROM 
   zrealizowane
JOIN 
   rodzaje ON zrealizowane.id_wycieczki = rodzaje.id_wycieczki
GROUP BY 
   rodzaje.koszt_udzialu
ORDER BY 
   liczba_uczestników DESC;
