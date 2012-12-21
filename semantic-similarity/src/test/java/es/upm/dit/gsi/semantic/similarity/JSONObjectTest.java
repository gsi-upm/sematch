package es.upm.dit.gsi.semantic.similarity;



import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;


import net.sf.json.JSONArray;
import net.sf.json.JSONObject;


import org.junit.Test;
import org.junit.Ignore;

public class JSONObjectTest {

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

}
