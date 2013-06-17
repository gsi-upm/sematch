package es.upm.dit.gsi.semantic.search;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import org.apache.lucene.index.IndexReader;
import org.apache.lucene.search.FieldCache;
import org.apache.lucene.search.function.CustomScoreProvider;

import es.upm.dit.gsi.semantic.similarity.SimilarityService;

class SemanticScoreProvider extends CustomScoreProvider{
	
	private QueryConfig config;
	private SimilarityService simService;
	private Map<String,String[]> fieldCache = null;

	public SemanticScoreProvider(IndexReader reader, QueryConfig config, SimilarityService simService) {
		super(reader);
		this.config = config;
		this.simService = simService;
		initFieldCache(reader);
	}
	
	private void initFieldCache(IndexReader reader){
		fieldCache = new HashMap<String,String[]>();
		try {
			for(String filed : config.getQueryFileds()){
				fieldCache.put(filed, FieldCache.DEFAULT.getStrings(reader,filed));
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	@Override
	public float customScore(int doc, float subQueryScore, float valSrcScore) throws IOException {
		
		Map<String,String> resource = new HashMap<String,String>();
		Map<String,String> query = config.getQuery();
		
		for(String field : config.getQueryFileds()){
			String fieldValue = fieldCache.get(field)[doc];
			resource.put(field, fieldValue);
		}
		
		return simService.getSimilarity(query, resource);
		
	}
	
}
