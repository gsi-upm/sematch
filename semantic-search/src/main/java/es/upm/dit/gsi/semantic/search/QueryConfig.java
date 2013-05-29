package es.upm.dit.gsi.semantic.search;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class QueryConfig {
	
	private Map<String,String> queryMap = null;
	private Map<String,String[]> cacheMap = null;
	
	public QueryConfig(){
		queryMap = new HashMap<String,String>();
		cacheMap = new HashMap<String,String[]>();
	}

	public Map<String,String> getQuery(){
		return this.queryMap;
	}

	public Set<String> getQueryFileds() {
		return queryMap.keySet();
	}

	public void setQuery(String key,String value) {
		this.queryMap.put(key, value);
	}

	//TODO:add fieldCache not find exception
	public String[] getFieldCache(String key) {
		return cacheMap.get(key);
	}

	public void setCache(String field, String[] cache) {
		this.cacheMap.put(field, cache);
	}

}
