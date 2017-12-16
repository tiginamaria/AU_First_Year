SELECT City.Name FROM
City JOIN (Country JOIN Capital
ON Capital.CountryCode = Country.Code)
ON City.Id = Capital.CityId AND Country.Name = "Malaysia";
