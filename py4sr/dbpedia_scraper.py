from SPARQLWrapper import SPARQLWrapper, SPARQLExceptions, JSON
 
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)

def get_european_countries(): 
    sparql.setQuery("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
   
SELECT ?country WHERE {
?country rdf:type yago:EuropeanCountries .
?country rdf:type dbpedia-owl:Country
}
""")
    results = sparql.query().convert()
    for country in results["results"]["bindings"]:
        country_uri = country["country"]["value"]
        print country_uri

def get_european_capitals(): 
    sparql.setQuery("""
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX : <http://dbpedia.org/resource/>
    PREFIX dbpedia2: <http://dbpedia.org/property/>
    PREFIX dbpedia: <http://dbpedia.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT * WHERE {
    ?subject rdf:type <http://dbpedia.org/class/yago/CapitalsInEurope>.
    ?subject rdfs:label ?label.
    ?subject rdfs:comment ?abstract.
    FILTER (lang(?label) = "en" && lang(?abstract) = "en")
    } 

""")
    results = sparql.query().convert()
    for city in results["results"]["bindings"]:
        print city

def get_city_info(uri): 
    sparql.setQuery("""
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX : <http://dbpedia.org/resource/>
    PREFIX dbpedia2: <http://dbpedia.org/property/>
    PREFIX dbpedia: <http://dbpedia.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>


    SELECT ?property ?hasValue ?isValueOf
    WHERE {
      { <"""+uri+"""> ?property ?hasValue }
        UNION
          { ?isValueOf ?property <"""+uri+"""> }
          }
""")
    results = sparql.query().convert()
    results = results["results"]["bindings"]
    city = {}
    for result in results:


get_city_info("http://dbpedia.org/resource/Amsterdam")
