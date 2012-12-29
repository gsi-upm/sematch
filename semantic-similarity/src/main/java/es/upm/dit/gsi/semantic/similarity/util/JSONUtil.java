package es.upm.dit.gsi.semantic.similarity.util;

import net.sf.json.*;

import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.FileReader;
import java.io.IOException;

import org.apache.commons.io.IOUtils;

public class JSONUtil {
	
	
	public static void write(String fileName, JSONObject json){
		 
		try {
			FileWriter file = new FileWriter(fileName);
			file.write(json.toString());
			file.flush();
			file.close();
	 
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public static JSONObject read(String fileName){
		JSONObject jsonObject = null;
		try {
	 
			FileReader reader = new FileReader(fileName);
			String jsonString = IOUtils.toString(reader);
			jsonObject = JSONObject.fromObject(jsonString);
			reader.close();
	 
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} 
		return jsonObject;
	}
	
	
	
}
