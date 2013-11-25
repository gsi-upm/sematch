package es.upm.dit.gsi.sematch.search;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.List;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.store.Directory;

/**
 * This class is used for indexing the documents. The documents should be
 * json documents. Each line is a json object. The user need to explicitly define the
 * attribute that need to be indexed. This class will index those field correspondingly.
 * first call the setIndexConfig to pass the index config.
 * Then call the startIndexing to start creating the index.
 * @author gzhu
 *
 */

public class Indexing {
	
	private Indexer indexer;
	private IndexConfig indexConfig = null;

	public Indexing(IndexConfig indexConfig){
		this.indexConfig = indexConfig;
		indexer = new Indexer();
	}
	
	public void index_from_json_file(){
		
		FileReader file = null;
		String line = "";
		JSONObject json = null;
		BufferedReader reader = null;
		try {
			InputStream in = getClass().getResourceAsStream(indexConfig.getJsonFile());
			reader = new BufferedReader(new InputStreamReader(in));
			while ((line = reader.readLine()) != null) {
				json = JSONObject.fromObject(line);
				Document doc = new Document();
				for(String field : indexConfig.getFields()){
					String value = "";
					if(json.get(field) != null){
						value = json.get(field).toString();
					}
					doc.add(new Field(field, value, Field.Store.YES, Field.Index.NOT_ANALYZED_NO_NORMS));
				}
				indexer.indexDocument(doc);
			}
		} catch (FileNotFoundException e) {
			throw new RuntimeException("File not found");
		} catch (IOException e) {
			throw new RuntimeException("IO Error occured");
		} finally {
			if (file != null) {
				try {
					file.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
		indexer.closeIndexWriter();
	}
	
	//get data from the lmf endpoint
	public JSONObject sparqlRequest(String query){
		
		String sparqlUri = "http://demos.gsi.dit.upm.es/lmf/sparql/select?query=";
		try {
			query = URLEncoder.encode(query, "UTF-8");
		} catch (UnsupportedEncodingException e1) {
			e1.printStackTrace();
		}
		query = sparqlUri + query + "&output=json";
		URL url;
		HttpURLConnection conn;
		BufferedReader rd;
		String line;
		String result = "";
		try {
			url = new URL(query);
			conn = (HttpURLConnection) url.openConnection();
			conn.setRequestMethod("GET");
			rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
			while ((line = rd.readLine()) != null) {
				result += line;
			}
			rd.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
		return JSONObject.fromObject(result);
	}
	
	public List<String> getResourcesUrl(){
		List<String> resources = new ArrayList<String>();
		String query = readSparql("/resources.sparql");
		JSONObject json = sparqlRequest(query);
		JSONArray array = json.getJSONObject("results").getJSONArray("bindings");
		for (int i = 0; i < array.size(); i++) {
			JSONObject people = array.getJSONObject(i);
			String res = people.getJSONObject("people").get("value").toString();
			resources.add(res);	
		}
		return resources;
	}
	
	public String getSkills(String url){
		String query = readSparql("/skills.sparql");
		String skillQuery = query.replace("Resource", url);
		JSONObject json = sparqlRequest(skillQuery);
		JSONArray array = json.getJSONObject("results").getJSONArray("bindings");
		JSONArray skillArray = new JSONArray();
		for (int i = 0; i < array.size(); i++) {
			JSONObject skill = array.getJSONObject(i);
			JSONObject skillObject = new JSONObject();
			skillObject.put("skill", skill.getJSONObject("skillname").get("value").toString());
			skillObject.put("level", skill.getJSONObject("skilllevel").get("value").toString());
			skillArray.add(skillObject);
		}
		return skillArray.toString();
	}
	
	//index the data from lmf
	public void createIndexFromLMF(){
		
		indexer = new Indexer();
		
		for(String res: getResourcesUrl()){
			Document doc = new Document();
			doc.add(new Field("uri", res, Field.Store.YES, 
					Field.Index.NOT_ANALYZED_NO_NORMS));
			doc.add(new Field("skill", getSkills(res), Field.Store.YES, 
					Field.Index.NOT_ANALYZED_NO_NORMS));
			indexer.indexDocument(doc);
		}
		
		indexer.closeIndexWriter();
		
	}
	
	private String readSparql(String fileName){
		FileReader file = null;
		String line = "";
		BufferedReader reader = null;
		StringBuffer buffer = new StringBuffer();
		try {
			InputStream in = getClass().getResourceAsStream(fileName);
			reader = new BufferedReader(new InputStreamReader(in));
			while ((line = reader.readLine()) != null) {
				buffer.append(line);
				buffer.append("\n");
			}
		} catch (FileNotFoundException e) {
			throw new RuntimeException("File not found");
		} catch (IOException e) {
			throw new RuntimeException("IO Error occured");
		} finally {
			if (file != null) {
				try {
					file.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
		return buffer.toString();
	}
	
	public void close(){
		indexer.closeDirectory();
	}
	
	public Directory getIndexDirecotry(){
		return indexer.getDirectory();
	}
	
	public IndexConfig getIndexConfig() {
		return indexConfig;
	}

	public void setIndexConfig(IndexConfig indexConfig) {
		this.indexConfig = indexConfig;
	}

	
}
