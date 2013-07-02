package es.upm.dit.gsi.semantic.service.matching;



import java.util.List;
import java.util.Map;

import org.apache.lucene.search.MatchAllDocsQuery;
import org.apache.lucene.search.Query;
import org.apache.lucene.store.Directory;

import es.upm.dit.gsi.semantic.search.IndexConfig;
import es.upm.dit.gsi.semantic.search.QueryConfig;
import es.upm.dit.gsi.semantic.search.Searcher;
import es.upm.dit.gsi.semantic.search.SemanticQuery;
import es.upm.dit.gsi.semantic.similarity.SimilarityService;

public class Searching {
	
	private QueryConfig queryConfig = null;
	private IndexConfig indexConfig = null;
	private SimilarityService simService = null;
	private Searcher searcher = null;
	private SemanticQuery query = null;

	public Searching(Directory directory){
		searcher = new Searcher(directory);
		//sub query must not be null
		Query q = new MatchAllDocsQuery();
		query = new SemanticQuery(q);
	}
	
	public List<Map<String,String>> search(Map<String,String> queryData){
		
		queryConfig.setQuery(queryData);
		query.setQueryConfig(queryConfig);
		query.setSimService(simService);
		return searcher.search(query,indexConfig);
	}

	public void setQueryConfig(QueryConfig queryConfig) {
		this.queryConfig = queryConfig;
		this.searcher.setResultSize(queryConfig.getResultSize());
	}

	public void setSimService(SimilarityService simService) {
		this.simService = simService;
	}
	
	public void setIndexConfig(IndexConfig indexConfig) {
		this.indexConfig = indexConfig;
	}
	
	public void close(){
		searcher.close();
	}

}
