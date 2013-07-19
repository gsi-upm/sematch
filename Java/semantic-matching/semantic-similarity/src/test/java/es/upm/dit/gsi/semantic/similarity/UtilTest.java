package es.upm.dit.gsi.semantic.similarity;


import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import org.junit.Ignore;
import org.junit.Test;

public class UtilTest {

	
	@Ignore
	public void testJsonMap() {
		
		Map<String,Object> root = new HashMap<String,Object>();
		ArrayList<Object> child = new ArrayList<Object>();
		
		root.put("name", "root");
		root.put("children", child);
		
		Map<String,Object> child1 = new HashMap<String,Object>();
		Map<String,Object> child2 = new HashMap<String,Object>();
		
		child.add(child1);
		child.add(child2);
		
		child1.put("name", "child1");
		child2.put("name", "child2");
		
		Map<String,Object> child11 = new HashMap<String,Object>();
		Map<String,Object> child12 = new HashMap<String,Object>();
		
		ArrayList<Object> children = new ArrayList<Object>();
		child1.put("children", children);
		children.add(child11);
		children.add(child12);
		
		child11.put("name", "child1");
		child12.put("name", "child2");
		
		
		JSONObject json = JSONObject.fromObject(root);
		System.out.println(json);
		
	}
	
	@Ignore
	public void testJsonArray(){
		JSONObject object1 = new JSONObject();
		object1.element("value", "1");
		JSONObject object2 = new JSONObject();
		object2.element("value", "2");
		JSONArray array = new JSONArray();
		array.add(object1);
		array.add(object2);
		System.out.println(array);
	}
	
	@Test
	public void testSparql(){
		String query = SparqlClient.getSparql("query.sparql");
		String sparqlUri = "http://demos.gsi.dit.upm.es/lmf/sparql/select?query=";
		try {
			query = URLEncoder.encode(query, "UTF-8");
		} catch (UnsupportedEncodingException e1) {
			// TODO Auto-generated catch block
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
		JSONObject json = JSONObject.fromObject(result);
		JSONArray array = json.getJSONObject("results").getJSONArray("bindings");
		for (int i = 0; i < array.size(); i++) {
			JSONObject people = array.getJSONObject(i);

			System.out.println(people.toString());
			
		}
		
	}


}
