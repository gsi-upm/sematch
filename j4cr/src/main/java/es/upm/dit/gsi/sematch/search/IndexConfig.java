package es.upm.dit.gsi.sematch.search;

import java.util.ArrayList;

/**
 * It can have more configuration possibilities.
 * @author gzhu
 *
 */
public class IndexConfig {

	private ArrayList<String> fields = null;
	private String jsonFile = null;

	public String getJsonFile() {
		return jsonFile;
	}

	public void setJsonFile(String jsonFile) {
		this.jsonFile = jsonFile;
	}

	public IndexConfig(){
		fields = new ArrayList<String>();
	}
	
	public void addField(String field){
		this.fields.add(field);
	}
	
	public ArrayList<String> getFields() {
		return fields;
	}

	public void setFields(ArrayList<String> fields) {
		this.fields = fields;
	}
	
}
