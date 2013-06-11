package es.upm.dit.gsi.semantic.matching;

import org.apache.lucene.index.Term;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.TermQuery;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import es.upm.dit.gsi.semantic.search.QueryConfig;
import es.upm.dit.gsi.semantic.search.Searcher;
import es.upm.dit.gsi.semantic.search.SemanticQuery;
import es.upm.dit.gsi.semantic.similarity.SimilarityService;

public class Matching {
	
	private Configuration config;
	private Indexing indexing;
	private Searching searching;
	private ApplicationContext simContext;
	private SimilarityService simService;
	Searcher searcher = new Searcher();
	
	public Matching(){
		
	}
	
	public void initializing(){
		
		config = new Configuration();
		indexing = new Indexing();
		indexing.setConfig(config.getIndexConfig());
		simContext = new ClassPathXmlApplicationContext(
				config.getSimConfig());
		simService = simContext.getBean(config.getSimBean(),
				SimilarityService.class);
		
		indexing.initIndex();

		
	}
	
	public void search(){
		Term t = new Term("category", "it");
		Query q = new TermQuery(t);
		QueryConfig queryConfig = new QueryConfig();
		queryConfig.setQuery("skill", "Java");
		queryConfig.setQuery("level", "Expert");
		
		SemanticQuery query = new SemanticQuery(q,queryConfig,simService);
		searcher.getIndexSearcher(indexing.getIndexer().getDirectory());
		searcher.search(query);
		
	}
	
	public void finalization(){
		searcher.closeSemanticSearcher();
		indexing.getIndexer().closeDirectory();
	}
}
