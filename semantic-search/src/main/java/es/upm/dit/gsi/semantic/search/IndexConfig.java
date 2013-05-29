package es.upm.dit.gsi.semantic.search;

import java.util.Map;

public class IndexConfig {
	
	private Map<String,String> fieldMap = null;

	public Map<String, String> getFieldMap() {
		return fieldMap;
	}

	public void setFieldMap(Map<String, String> fieldMap) {
		this.fieldMap = fieldMap;
	}
	
	public String getFieldURI(String field){
		return this.fieldMap.get(field);
	}
	
}
