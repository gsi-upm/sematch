package es.upm.dit.gsi.semantic.search;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class QueryConfig {
	
	private int resultSize;
	private ArrayList<String> fields = null;
	private Map<String,Object> query = null;
	
	public QueryConfig(){
		fields = new ArrayList<String>();
	}

	public Map<String,Object> getQuery(){
		return this.query;
	}

	public List<String> getFileds() {
		return fields;
	}
	
	public void addField(String field){
		fields.add(field);
	}

	public void setQuery(Map<String,Object> query) {
		this.query = query;
	}
	
	public int getResultSize() {
		return resultSize;
	}

	public void setResultSize(int resultSize) {
		this.resultSize = resultSize;
	}


}
