package es.upm.dit.gsi.sematch.search;

import org.apache.lucene.index.IndexReader;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.function.CustomScoreProvider;
import org.apache.lucene.search.function.CustomScoreQuery;

import es.upm.dit.gsi.sematch.similarity.SimilarityService;

public class SemanticQuery extends CustomScoreQuery {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	
	private QueryConfig queryConfig = null;
	
	private SimilarityService simService = null;
	
	public SemanticQuery(){
		super(null);
	}
	
	public SemanticQuery(Query subQuery) {
		super(subQuery);
	}

	@Override
	public CustomScoreProvider getCustomScoreProvider(IndexReader reader) {
		return new SemanticScoreProvider(reader,queryConfig,simService);
	}

	public void setSimService(SimilarityService simService) {
		this.simService = simService;
	}

	public void setQueryConfig(QueryConfig queryConfig) {
		this.queryConfig = queryConfig;
	}
	
	public QueryConfig getQueryConfig() {
		return queryConfig;
	}


}
