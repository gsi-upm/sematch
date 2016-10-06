
def test_name_sparql():
    from sematch.sparql import NameSPARQL
    name_linker = NameSPARQL()
    assert 'http://dbpedia.org/resource/Natalie_Portman' in name_linker.name2entities('Natalie Portman')
    assert 'http://dbpedia.org/resource/China' in name_linker.name2entities('China')
    assert 'http://dbpedia.org/resource/Spain' in name_linker.name2entities('Spain')
    assert 'http://dbpedia.org/resource/Brooklyn_Bridge' in name_linker.name2entities('Brooklyn Bridge')


def test_query_graph():
    from sematch.sparql import QueryGraph
    qg = QueryGraph()
    concepts = ['http://dbpedia.org/class/yago/Film106262567',
                'http://dbpedia.org/class/yago/Film103339296',
                'http://dbpedia.org/class/yago/Film103338648',
                'http://dbpedia.org/class/yago/Movie106613686',
                'http://dbpedia.org/class/yago/Film103338821']
    entity = 'http://dbpedia.org/resource/Hal_Roach'
    assert 'http://dbpedia.org/resource/Luke_Pipes_the_Pippins' in qg.type_entity_query(concepts,entity)

def test_entity_features():
    from sematch.sparql import EntityFeatures
    entity_f = EntityFeatures()
    yin_and_yang = entity_f.features('http://dbpedia.org/resource/Yin_and_yang')
    print yin_and_yang