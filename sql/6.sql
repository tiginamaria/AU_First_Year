SELECT City.Name, City.Population AS CityPopulation, Country.Population AS CountryPopulation 
FROM City, Country
WHERE Country.Population > 0 AND City.CountryCode = Country.Code 
ORDER BY (CityPopulation / CountryPopulation) DESC, City.Name DESC LIMIT 20;
