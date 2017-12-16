SELECT Country.Name, IFNULL(Sum(City.Population >= 1000000), 0) AS MillionCity 
FROM Country
JOIN City ON City.CountryCode = Country.Code
GROUP BY Country.Name
ORDER BY MillionCity DESC, Country.Name;
