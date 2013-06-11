package es.upm.dit.gsi.semantic.service;

import static org.junit.Assert.*;

import org.apache.lucene.index.Term;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.TermQuery;
import org.junit.Ignore;
import org.junit.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import es.upm.dit.gsi.semantic.matching.Indexing;
import es.upm.dit.gsi.semantic.search.SemanticQuery;
import es.upm.dit.gsi.semantic.search.QueryConfig;
import es.upm.dit.gsi.semantic.search.Searcher;
import es.upm.dit.gsi.semantic.similarity.SimilarityService;


public class SpringBeanTest {

	@Test
	public void testIndex(){
		
		ApplicationContext context = new ClassPathXmlApplicationContext(
				"similarity-config.xml");
		
		Indexing indexing = context.getBean("indexing", Indexing.class);
		SimilarityService simService = context.getBean("simService",SimilarityService.class);
		indexing.initIndex();

		Term t = new Term("category", "it");
		Query q = new TermQuery(t);
		QueryConfig config = new QueryConfig();
		config.setQuery("skill", "Java");
		config.setQuery("level", "Expert");
		
		SemanticQuery query = new SemanticQuery(q,config,simService);
		
		Searcher searcher = new Searcher();
		searcher.getIndexSearcher(indexing.getIndexer().getDirectory());
		searcher.search(query);
		searcher.closeSemanticSearcher();
		indexing.getIndexer().closeDirectory();

	}

}
