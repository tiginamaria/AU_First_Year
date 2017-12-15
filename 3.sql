SELECT City.Name FROM City, Capital, Country 
WHERE City.Id = Capital.CityId AND City.CountryCode = Country.Code AND Country.Name LIKE "Malaysia";
