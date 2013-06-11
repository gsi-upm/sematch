package es.upm.dit.gsi.semantic.search;

import java.util.Map;

public class IndexConfig {

	private String localFile;
	private String remoteUrl;
	private String query;
	private Map<String,String> fieldMap;
	
	public IndexConfig(){}

	public Map<String, String> getFieldMap() {
		return fieldMap;
	}

	public void setFieldMap(Map<String, String> fieldMap) {
		this.fieldMap = fieldMap;
	}
	
	public String getFieldURI(String field){
		return this.fieldMap.get(field);
	}
	
	public String getLocalFile() {
		return localFile;
	}

	public void setLocalFile(String localFile) {
		this.localFile = localFile;
	}

	public String getRemoteUrl() {
		return remoteUrl;
	}

	public void setRemoteUrl(String remoteUrl) {
		this.remoteUrl = remoteUrl;
	}

	public String getQuery() {
		return query;
	}

	public void setQuery(String query) {
		this.query = query;
	}

}
