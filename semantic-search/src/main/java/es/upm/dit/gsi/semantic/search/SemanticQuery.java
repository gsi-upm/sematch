package es.upm.dit.gsi.semantic.search;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import org.apache.lucene.index.IndexReader;
import org.apache.lucene.search.FieldCache;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.function.CustomScoreProvider;
import org.apache.lucene.search.function.CustomScoreQuery;

import es.upm.dit.gsi.semantic.similarity.SimilarityService;

public class SemanticQuery extends CustomScoreQuery {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	
	private QueryConfig config = null;
	private SimilarityService simService = null;

	public SemanticQuery(Query subQuery, QueryConfig config, SimilarityService simService) {
		super(subQuery);
		this.config = config;
		this.simService = simService;
	}
	
	private class SemanticScoreProvider extends CustomScoreProvider{
		
		private QueryConfig config;
		private SimilarityService simService;

		public SemanticScoreProvider(IndexReader reader, QueryConfig config, SimilarityService simService) {
			super(reader);
			this.config = config;
			this.simService = simService;
			initFieldCache(reader);
		}
		
		private void initFieldCache(IndexReader reader){
			
			try {
				for(String filed : config.getQueryFileds()){
						config.setCache(filed, 
								FieldCache.DEFAULT.getStrings(reader,filed));
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		
		@Override
		public float customScore(int doc, float subQueryScore,
	            float valSrcScore) throws IOException {
			
			Map<String,String> resource = new HashMap<String,String>();
			Map<String,String> query = config.getQuery();
			
			for(String field : config.getQueryFileds()){
				String fieldValue = config.getFieldCache(field)[doc];
				resource.put(field, fieldValue);
			}
			
			return simService.getSimilarity(query, resource);
			
		}
	}


	@Override
	public CustomScoreProvider getCustomScoreProvider(IndexReader reader) {
		return new SemanticScoreProvider(reader,config,simService);
	}

}
