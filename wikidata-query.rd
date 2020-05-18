# Notable people from Strasbourg
#defaultView:Table
SELECT  
        ?fullname
        (GROUP_CONCAT(DISTINCT ?occupationLabel; separator=", ") AS ?occupations)
        ?photo
        ?article
        (year(?dob) AS ?birthyear) 
WHERE 
{
        # studied in Unistra Strasbourg      
        ?person wdt:P69 wd:Q157575.
        ?person wdt:P106 ?occupation.
        ?person wdt:P18 ?image .
        ?person wdt:P569 ?dob .
        ?article schema:about ?person ; 
                 schema:isPartOf <https://en.wikipedia.org/> ; 
                 schema:name ?fullname .
        ?person rdfs:label ?fullname filter (lang(?fullname) = "en") .
        
        SERVICE wikibase:label {
          bd:serviceParam wikibase:language "en" . 
          ?occupation rdfs:label ?occupationLabel .
          ?image rdfs:label ?photo .
        }
}

GROUP BY ?fullname ?photo ?article ?dob ?birthyear
LIMIT 100