SELECT Country.Name, IFNULL(SUM(City.Population > 1000000), 0) AS MillionCity FROM Country, City
WHERE City.CountryCode = Country.Code
GROUP BY CountryCode
ORDER BY MillionCity DESC;
