SELECT 
  CONCAT(LPAD(MONTH(data_wyjazdu), 2, '0'), '-', YEAR(data_wyjazdu)) AS data_realizacji,
  SUM(liczba_uczestników) AS liczba_klientów
FROM 
  zrealizowane 
GROUP BY 
  YEAR(data_wyjazdu), MONTH(data_wyjazdu)
ORDER BY 
  YEAR(data_wyjazdu), MONTH(data_wyjazdu) ASC;
