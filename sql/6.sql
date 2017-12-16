SELECT City.Name, City.Population AS CityPopulation, Country.Population AS CountryPopulation 
FROM City
JOIN Country ON Country.Population > 0 AND City.CountryCode = Country.Code 
ORDER BY CAST(CityPopulation AS FLOAT) / CAST (CountryPopulation AS FLOAT) DESC, City.Name DESC 
LIMIT 20;
