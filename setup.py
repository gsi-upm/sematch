from setuptools import setup
import io

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    with io.open(filename, 'r') as f:
        lineiter = list(line.strip() for line in f)
    return [line for line in lineiter if line and not line.startswith("#")]

install_reqs = parse_requirements("requirements.txt")
test_reqs = parse_requirements("test-requirements.txt")

setup(name = 'sematch',
      packages=['sematch','sematch.semantic'],
      version = '1.0.5',
      description = 'Semantic similarity framework for knowledge graphs',
      long_description = open('README.md').read(),
      author = 'Ganggao Zhu',
      author_email = 'gzhu@dit.upm.es',
      license='Apache 2.0',
      url = 'https://github.com/gsi-upm/sematch',
      keywords = ['semantic similarity', 'taxonomy', 'knowledge graph', 
      'semantic analysis', 'knowledge base', 'WordNet', 'DBpedia','YAGO', 'ontology'],
      include_package_data=True,
      package_data = {'models':['models/dbpedia_2015-04.owl',
                                'models/dbpedia_type_ic.txt',
                                'models/type-linkings.txt',
                                'models/yago_type_ic.txt',
                                'models/FoxStoplist.txt',
                                'models/SmartStoplist.txt'],
                      'dataset/aspect':['dataset/aspect/data.txt'],
                      'dataset/wordsim':['dataset/wordsim/noun_mc.txt',
                                         'dataset/wordsim/noun_rg.txt',
                                         'dataset/wordsim/noun_simlex.txt',
                                         'dataset/wordsim/noun_ws353-sim.txt',
                                         'dataset/wordsim/noun_ws353.txt',
                                         'dataset/wordsim/rg65_EN-ES.txt',
                                         'dataset/wordsim/rg65_spanish.txt',
                                         'dataset/wordsim/graph_mc.txt',
                                         'dataset/wordsim/graph_rg.txt',
                                         'dataset/wordsim/graph_simlex.txt',
                                         'dataset/wordsim/graph_ws353-sim.txt',
                                         'dataset/wordsim/graph_ws353.txt',
                                         'dataset/wordsim/type_mc.txt',
                                         'dataset/wordsim/type_rg.txt',
                                         'dataset/wordsim/type_simlex.txt',
                                         'dataset/wordsim/type_ws353-sim.txt',
                                         'dataset/wordsim/type_ws353.txt',],
                      'dataset/wordsim/results':['dataset/wordsim/results/noun_simlex-wpath.txt'],
                      },
      classifiers = ['Development Status :: 5 - Production/Stable',
                     'Intended Audience :: Science/Research',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3.8',
                     'Topic :: Software Development :: Libraries'],
      install_requires=install_reqs,
      tests_require=test_reqs,
      )
