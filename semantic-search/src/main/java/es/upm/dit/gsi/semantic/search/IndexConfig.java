package es.upm.dit.gsi.semantic.search;

import java.util.List;
import java.util.Map;

public class IndexConfig {

	private String type = null;
	private String localFile = null;
	private String remoteUrl = null;
	private String query = null;
	private List<String> fields = null;
	private Map<String,String> fieldMap = null;
	
	public IndexConfig(){}
	
	public List<String> getFields() {
		return fields;
	}

	public void setFields(List<String> fields) {
		this.fields = fields;
	}

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
	public String getType() {
		return type;
	}

	public void setType(String type) {
		this.type = type;
	}

}
