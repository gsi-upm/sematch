from sematch.semantic.analysis import create_lsi
from sematch.semantic.analysis import create_lsi_index
from sematch.semantic.analysis import LONG_TFIDF_CORPUS
from sematch.semantic.analysis import LONG_LSI_MODEL
from sematch.semantic.analysis import LONG_DICT
from sematch.semantic.analysis import LONG_LSI_SHARD
from sematch.semantic.analysis import LONG_LSI_INDEX

# import logging
# logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.DEBUG)
# logging.root.level = logging.DEBUG
#
# create_lsi(LONG_DICT,LONG_TFIDF_CORPUS,LONG_LSI_MODEL)
# create_lsi_index(LONG_TFIDF_CORPUS,LONG_LSI_MODEL,LONG_LSI_SHARD,LONG_LSI_INDEX)

#
# from sematch.semantic.relatedness import EntityRelatedness
#
# rel = EntityRelatedness()
# print rel.relatedness_type_synsets('http://dbpedia.org/resource/Apple_Inc.','http://dbpedia.org/resource/Steve_Jobs')
# print rel.relatedness_type_synsets('http://dbpedia.org/resource/Apple_Inc.','http://dbpedia.org/resource/NeXT')
