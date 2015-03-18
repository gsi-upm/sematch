from Utility import FileIO
import spotlight

class DBpediaSpotlight:

    def __init__(self):
        self.uri = 'http://spotlight.dbpedia.org/rest/annotate'
        self.confidence = 0.3
        self.support = 20

    def annotate(self, query):
        annotations = spotlight.annotate(self.uri,query,confidence=self.confidence, support=self.support)
        annotations = [a['URI'] for a in annotations]
        return annotations


class SynsetLinker:

    def __init__(self):
        self.links = FileIO.read_json_file("sematch/db/type-linkings.txt")
        self.links = {data['offset']:data for data in self.links}

    def offset(self, synset):
        return str(synset.offset + 100000000)

    def link_append(self, typeLinks, lst):
        if typeLinks.get('dbpedia'):
            lst.append(typeLinks['dbpedia'])

        if typeLinks.get('yago_dbpedia'):
            lst.append(typeLinks['yago_dbpedia'])

    def type_linking(self, synsets):
        links = []
        for s in synsets:
            if self.links.get(self.offset(s)):
                self.link_append(self.links.get(self.offset(s)), links)
        return links