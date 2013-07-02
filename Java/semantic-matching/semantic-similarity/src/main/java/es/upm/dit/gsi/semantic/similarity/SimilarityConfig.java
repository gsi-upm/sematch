package es.upm.dit.gsi.semantic.similarity;

import java.util.Map;

public class SimilarityConfig {
	
	private Map<String,String> query = null;
	private Map<String,String> resource = null;
	
	public SimilarityConfig(){}
	
	public String getQuery(String label){
		return this.query.get(label);
	}
	
	public String getResource(String label){
		return this.resource.get(label);
	}
	
	public Map<String, String> getQuery() {
		return query;
	}

	public void setQuery(Map<String, String> query) {
		this.query = query;
	}

	public Map<String, String> getResource() {
		return resource;
	}

	public void setResource(Map<String, String> resource) {
		this.resource = resource;
	}
}
