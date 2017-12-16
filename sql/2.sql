SELECT Name, Rate AS MaxRate
FROM Country
JOIN LiteracyRate ON Country.Code = LiteracyRate.CountryCode
GROUP BY CountryCode
HAVING MAX(Year) = Year
ORDER BY MaxRate DESC
LIMIT 1;

