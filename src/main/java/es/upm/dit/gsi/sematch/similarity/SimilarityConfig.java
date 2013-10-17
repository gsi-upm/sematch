package es.upm.dit.gsi.sematch.similarity;

import java.util.Map;

public class SimilarityConfig {
	
	private Map<String,Object> query = null;
	private Map<String,Object> resource = null;
	
	public SimilarityConfig(){}
	
	public Object getQuery(String label){
		return this.query.get(label);
	}
	
	public Object getResource(String label){
		return this.resource.get(label);
	}
	
	public Map<String, Object> getQuery() {
		return query;
	}

	public void setQuery(Map<String, Object> query) {
		this.query = query;
	}

	public Map<String, Object> getResource() {
		return resource;
	}

	public void setResource(Map<String, Object> resource) {
		this.resource = resource;
	}
}
