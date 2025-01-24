SELECT
	CASE
		WHEN klienci.id_zniżki IS NULL THEN 'brak zniżki'
		ELSE 'ze zniżką'
	END AS typ_klienta,
	COUNT(transakcje_klienci.id_klienta) AS liczba_transakcji,
	COUNT(DISTINCT transakcje_klienci.id_klienta) AS liczba_klientów,
	ROUND(COUNT(transakcje_klienci.id_klienta) * 1.0 / COUNT(DISTINCT transakcje_klienci.id_klienta),2) AS średnia_transakcji_na_klienta
FROM
	transakcje_klienci
JOIN
	klienci
ON transakcje_klienci.id_klienta = klienci.id_klienta
LEFT JOIN
	zniżki ON zniżki.id_zniżki = klienci.id_zniżki
GROUP BY
	CASE
		WHEN klienci.id_zniżki IS NULL THEN 'brak zniżki'
		ELSE 'ze zniżką'
	END
ORDER BY 
	średnia_transakcji_na_klienta DESC;