WITH WycieczkiKlienta AS (
	SELECT
		klienci.id_klienta,
		zrealizowane.id_wycieczki,
		zrealizowane.data_wyjazdu,
		ROW_NUMBER() OVER (PARTITION BY klienci.id_klienta, zrealizowane.id_wycieczki ORDER BY zrealizowane.data_wyjazdu) AS numer_wycieczki,
		LEAD(zrealizowane.data_wyjazdu) OVER (PARTITION BY klienci.id_klienta ORDER BY zrealizowane.data_wyjazdu) AS data_następnej_wycieczki
	FROM
		klienci
	LEFT JOIN
		transakcje_klienci ON klienci.id_klienta = transakcje_klienci.id_klienta
	LEFT JOIN
		zrealizowane ON zrealizowane.id_eventu = transakcje_klienci.id_eventu
),

PonowneWycieczki AS (
	SELECT
		id_wycieczki,
		id_klienta
	FROM
		WycieczkiKlienta
	WHERE
		numer_wycieczki > 1
)

SELECT
	rodzaje.id_wycieczki,
	rodzaje.nazwa_wycieczki,
	COALESCE(COUNT(PonowneWycieczki.id_klienta), 0) AS liczba_ponownego_uczestnictwa
FROM
	rodzaje
LEFT JOIN
	PonowneWycieczki ON rodzaje.id_wycieczki = PonowneWycieczki.id_wycieczki
GROUP BY
	rodzaje.id_wycieczki
ORDER BY
	liczba_ponownego_uczestnictwa DESC;