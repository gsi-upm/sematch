from sematch.utility import FileIO
from sematch.semantic.similarity import TextSimilarity

sts = TextSimilarity()

class Dataset:

    def __init__(self):
        self.sts2016headline = FileIO.filename('eval/sts/sts2016/STS2016.input.headlines.txt')
        self.sts2015headline = FileIO.filename('eval/sts/sts2015/STS.input.headlines.txt')
        self.sts2015images = FileIO.filename('eval/sts/sts2015/STS.input.images.txt')

    def load_dataset(self, name):
        with open(name, 'r') as f:
            data = [line.strip() for line in f]
        corpus = []
        for d in data:
            item = d.split('\t')
            corpus.append((item[0], item[1]))
        return corpus

dataset = Dataset()

# corpus_image = dataset.load_dataset(dataset.sts2015images)
# print len(corpus_image)

def evaluate(method_name, corpus_name, output_name):
    corpus = dataset.load_dataset(corpus_name)
    print 'dataset size: ', len(corpus)
    result = [sts.text_similarity(t1,t2, method_name) for t1, t2 in corpus]
    result = map(lambda x:"%.3f" % round(x,3), result)
    FileIO.save_list_file(output_name, result)

evaluate('lin', dataset.sts2016headline, 'eval/sts/sts2016/SYSTEM_OUT.headlines-lin.txt')

#evaluate('pathjcn', dataset.sts2015images, 'eval/sts/sts2015/SYSTEM_OUT.images-pathjcn.txt')
