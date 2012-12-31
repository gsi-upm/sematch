package es.upm.dit.gsi.semantic.similarity;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;

import net.sf.json.JSONObject;

import org.apache.commons.io.IOUtils;

import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;
import com.hp.hpl.jena.util.FileManager;

public class SemanticRepository {

	public static void writeToXML(Model model, String fileName) {

		File file = null;
		FileOutputStream out = null;
		try {
			file = new File(fileName);
			out = new FileOutputStream(file);
			if (!file.exists()) {
				file.createNewFile();
			}
			model.write(out);
			out.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public static Model readFromXML(String fileName) {
		Model model = ModelFactory.createDefaultModel();
		InputStream in = FileManager.get().open(fileName);
		if (in == null) {
			throw new IllegalArgumentException("File: " + fileName
					+ " not found");
		}
		
		model.read(in, "");
		return model;
	}
	
	public static Model readFromXML(InputStream in){
		Model model = ModelFactory.createDefaultModel();
		model.read(in, "");
		return model;
	}
	
	public static void writeJSON(String fileName, JSONObject json){
		 
		try {
			FileWriter file = new FileWriter(fileName);
			file.write(json.toString());
			file.flush();
			file.close();
	 
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public static JSONObject readJSON(String fileName){
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
