WITH SezonWycieczek AS (
	SELECT
		zrealizowane.id_wycieczki,
		zrealizowane.data_wyjazdu,
		EXTRACT(MONTH FROM zrealizowane.data_wyjazdu) AS miesiąc,
		CASE
			WHEN EXTRACT(MONTH FROM zrealizowane.data_wyjazdu) IN (12, 1, 2) THEN 'Zima'
			WHEN EXTRACT(MONTH FROM zrealizowane.data_wyjazdu) IN (3, 4, 5) THEN 'Wiosna'
			WHEN EXTRACT(MONTH FROM zrealizowane.data_wyjazdu) IN (6, 7, 8) THEN 'Lato'
			WHEN EXTRACT(MONTH FROM zrealizowane.data_wyjazdu) IN (9, 10, 11) THEN 'Jesień'
		END AS pora_roku,
		zrealizowane.liczba_uczestników AS liczba_uczestników
	FROM
		zrealizowane
	JOIN
		transakcje_klienci ON zrealizowane.id_eventu = transakcje_klienci.id_eventu
	GROUP BY
		zrealizowane.id_wycieczki,
		zrealizowane.data_wyjazdu
)
SELECT
	pora_roku,
	FLOOR(AVG(liczba_uczestników)) AS średnia_liczba_uczestników
FROM
	SezonWycieczek
GROUP BY
	pora_roku
ORDER BY
	średnia_liczba_uczestników DESC;