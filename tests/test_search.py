

def test_entity_search():
    from sematch.search import EntitySearch
    queries = ["who produce film starring Natalie Portman",
               "give me all soccer club in Spain",
               'Neil Gaiman novels',
               'Paul Auster novels',
               'State capitals of the United States of America',
               'Novels that won the Booker Prize',
               'Films directed by Akira Kurosawa',
               'Airports in Germany',
               'Universities in Catalunya',
               'Give me all professional skateboarders from Sweden',
               'Give me all cars that are produced in Germany',
               'Give me all movies directed by Francis Ford Coppola',
               'Give me all companies in Munich',
               'Give me a list of all lakes in Denmark',
               'Give me all Argentine films',
               'Give me the capitals of all countries in Africa',
               'Give me all presidents of the United States',
               'Give me all actors starring in Batman Begins',
               'Which actors were born in Germany?',
               'Give me all films produced by Hal Roach',
               'Give me all books written by Danielle Steel',
               'Give me all movies with Tom Cruise']
    searcher = EntitySearch()
    for q in queries:
        assert searcher.search(q) is not None

