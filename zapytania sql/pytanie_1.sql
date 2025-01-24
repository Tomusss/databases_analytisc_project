SELECT 
   zrealizowane.id_wycieczki, 
   rodzaje.nazwa_wycieczki,
   SUM(transakcje_klienci.koszt_udziału) AS dochód_z_wycieczki,
   rodzaje.koszt_organizacji * COUNT(DISTINCT zrealizowane.id_eventu) AS koszt_organizacji_wycieczki,
   SUM(transakcje_klienci.koszt_udziału) - rodzaje.koszt_organizacji * COUNT(DISTINCT zrealizowane.id_eventu) AS łączny_zysk_z_wycieczki
FROM 
   transakcje_klienci 
JOIN 
   zrealizowane ON transakcje_klienci.id_eventu = zrealizowane.id_eventu
JOIN 
   transakcje_firma ON transakcje_firma.id_eventu = zrealizowane.id_eventu
JOIN 
	rodzaje ON rodzaje.id_wycieczki = zrealizowane.id_wycieczki
GROUP BY 
	zrealizowane.id_wycieczki, rodzaje.koszt_organizacji
ORDER BY
	łączny_zysk_z_wycieczki DESC;
