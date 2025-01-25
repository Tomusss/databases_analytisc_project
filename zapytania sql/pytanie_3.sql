WITH WycieczkiKlienta AS (
	SELECT
		klienci.id_klienta,
		zrealizowane.id_wycieczki,
		zrealizowane.data_wyjazdu,
		ROW_NUMBER() OVER (PARTITION BY klienci.id_klienta ORDER BY zrealizowane.data_wyjazdu) AS numer_wycieczki,
		LEAD(zrealizowane.data_wyjazdu) OVER (PARTITION BY klienci.id_klienta ORDER BY zrealizowane.data_wyjazdu) AS data_następnej_wycieczki
	FROM
		klienci
	LEFT JOIN
		transakcje_klienci ON klienci.id_klienta = transakcje_klienci.id_klienta
	LEFT JOIN
		zrealizowane ON zrealizowane.id_eventu = transakcje_klienci.id_eventu
)

SELECT 
	WycieczkiKlienta.id_wycieczki,
	rodzaje.nazwa_wycieczki,
	COUNT(CASE WHEN data_następnej_wycieczki IS NOT NULL THEN 1 END) AS liczba_powrotów_po_tej_wycieczce,
	COUNT(CASE WHEN data_następnej_wycieczki IS NULL THEN 1 END) AS liczba_braku_powrotu_po_tej_wycieczce,
	COUNT(WycieczkiKlienta.id_klienta) AS liczba_uczestników,
	ROUND(100.00 * COUNT(CASE WHEN data_następnej_wycieczki IS NOT NULL THEN 1 END) / COUNT(WycieczkiKlienta.id_klienta), 2) AS procent_powrotów,
	ROUND(100.00 * COUNT(CASE WHEN data_następnej_wycieczki IS NULL THEN 1 END) / COUNT(WycieczkiKlienta.id_klienta), 2) AS procent_braku_powrotu
FROM
	WycieczkiKlienta
LEFT JOIN
	rodzaje ON rodzaje.id_wycieczki = WycieczkiKlienta.id_wycieczki
WHERE
	WycieczkiKlienta.id_wycieczki IS NOT NULL
GROUP BY
	WycieczkiKlienta.id_wycieczki, rodzaje.nazwa_wycieczki
ORDER BY
	procent_powrotów DESC;