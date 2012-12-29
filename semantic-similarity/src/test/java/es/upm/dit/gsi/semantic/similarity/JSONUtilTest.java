package es.upm.dit.gsi.semantic.similarity;


import java.util.Iterator;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import org.junit.Ignore;
import org.junit.Test;

import es.upm.dit.gsi.semantic.similarity.util.JSONUtil;

public class JSONUtilTest {

	@Ignore
	public void testWrite() {
		JSONObject obj = new JSONObject();
		obj.put("name", "Information Technology");
		JSONArray list = new JSONArray();
		list.add("Software");
		list.add("Hardware");
		list.add("WebService");
		obj.put("children", list);
		JSONUtil.write("result/test.json",obj);
	}
	
	@Ignore
	public void testRead() {
		JSONObject object = JSONUtil.read("result/test.json");
		String name = (String) object.get("name");
		System.out.println(name);
		// loop array
		JSONArray children = (JSONArray) object.get("children");
		Iterator<String> iterator = children.iterator();
		while (iterator.hasNext()) {
			System.out.println(iterator.next());
		}
		
	}

}
