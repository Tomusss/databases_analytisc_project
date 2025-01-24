SELECT
	CASE
		WHEN klienci.wiek BETWEEN 0 AND 20 THEN '0-20'
		WHEN klienci.wiek BETWEEN 21 AND 30 THEN '21-30'
		WHEN klienci.wiek BETWEEN 31 AND 40 THEN '31-40'
		WHEN klienci.wiek BETWEEN 41 AND 50 THEN '41-50'
		WHEN klienci.wiek BETWEEN 51 AND 60 THEN '51-60'
		WHEN klienci.wiek BETWEEN 61 AND 70 THEN '61-70'
		WHEN klienci.wiek BETWEEN 71 AND 80 THEN '71-80'
		WHEN klienci.wiek > 80 THEN 'starsi'
	END AS przedział_wiekowy,
	COUNT(DISTINCT transakcje_klienci.id_klienta) AS liczba_klientów
FROM
	klienci
JOIN
	transakcje_klienci
ON
	klienci.id_klienta = transakcje_klienci.id_klienta
GROUP BY
	przedział_wiekowy
ORDER BY 
	liczba_klientów DESC;