package es.upm.dit.gsi.semantic.search;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class QueryConfig {
	
	private int resultSize;
	private ArrayList<String> fields = null;
	private Map<String,String> query = null;
	
	public QueryConfig(){
		fields = new ArrayList<String>();
	}

	public Map<String,String> getQuery(){
		return this.query;
	}

	public List<String> getQueryFileds() {
		return fields;
	}
	
	public void addField(String field){
		fields.add(field);
	}

	public void setQuery(Map<String,String> query) {
		this.query = query;
	}
	
	public int getResultSize() {
		return resultSize;
	}

	public void setResultSize(int resultSize) {
		this.resultSize = resultSize;
	}


}
