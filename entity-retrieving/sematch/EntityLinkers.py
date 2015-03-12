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


