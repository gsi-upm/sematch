from Utility import FileIO

class SynsetLinker:

    def __init__(self):
        self.links = FileIO.read_json_file("type-linkings.txt")
        self.links = {data['offset']:data for data in self.links}

    def offset(self, synset):
        return str(synset.offset + 100000000)

    def link_append(self, typeLinks, lst):
        print typeLinks
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