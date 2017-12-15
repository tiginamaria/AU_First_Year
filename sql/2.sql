SELECT Name, (SELECT MAX(Rate) FROM LiteracyRate) AS MaxRate FROM Country, LiteracyRate
WHERE Code = CountryCode AND Rate = MaxRate;

