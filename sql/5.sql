SELECT GovernmentForm, SUM(SurfaceArea) AS SumSurfaseArea
FROM Country
GROUP BY GovernmentForm 
ORDER BY SumSurfaseArea DESC 
LIMIT 1;
