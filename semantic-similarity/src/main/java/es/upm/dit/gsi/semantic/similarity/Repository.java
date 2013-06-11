package es.upm.dit.gsi.semantic.similarity;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;

import net.sf.json.JSONObject;

import com.hp.hpl.jena.query.Query;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.util.FileManager;

public class Repository {

	private Model model;

	// local rdf file name
	private String fileName;

	// remote sparql service url
	private String remoteUrl;

	// construct sparql query file
	private String consQueryFile;

	// resource sparql query file
	private String resQueryFile;

	// rdf resource name
	private String resName;

	// resource url list
	private List<Resource> resList = null;

	public Model getModel() {
		return model;
	}

	public void setModel(Model model) {
		this.model = model;
	}
	
	public Model getModelFromTriple(){
		setModel(readFromTriple(fileName));
		return getModel();
	}

	// read model from local file
	public Model getModelFromLocal() {
		setModel(readFromXML(fileName));
		return getModel();
	}

	// TODO:read model from remote server
	public Model getModelFromRemote() {

		File queryFile = new File(this.getConsQueryFile());
		SparqlClient client = SparqlClient.getSparqlClient();
		Query query = client.getQueryFromFile(queryFile);
		Model constructModel = client.executeConstructQuery(query, getModel());
		setModel(constructModel);
		return getModel();

	}

	public List<Resource> getResList() {
		if (resList == null) {
			SparqlClient client = SparqlClient.getSparqlClient();
			File queryFile = new File(this.getResQueryFile());
			Query query = client.getQueryFromFile(queryFile);
			ResultSet rset = client.executeSelectQuery(query, getModel());
			setResList(client.asResourceList(rset, resName));
		}
		return resList;
	}

	// writing the RDF model to XML file
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
	
	public static Model readFromTriple(String fileName){
		Model model = ModelFactory.createDefaultModel();
		InputStream in = FileManager.get().open(fileName);
		if (in == null) {
			throw new IllegalArgumentException("File: " + fileName
					+ " not found");
		}
		
		model.read(in, null, "N-TRIPLE");
		return model;
	}

	// reading the RDF model from the XML file
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

	public static Model readFromXML(InputStream in) {
		Model model = ModelFactory.createDefaultModel();
		model.read(in, "");
		return model;
	}

	// writing the json to the file for generating taxonomy graph
	public static void writeJSON(String fileName, JSONObject json) {

		writeTextFile(fileName,json.toString());

	}

	// read json from the file
	public static JSONObject readJSON(String fileName) {
		String jsonString = readTextFile(fileName);
		return JSONObject.fromObject(jsonString);
	}
	
	//read from text file
	public static String readTextFile(String fileName) {
		
		FileReader file = null;
		String line = "";
		BufferedReader reader = null;
		StringBuffer buffer = new StringBuffer();
		try {
			file = new FileReader(fileName);
			reader = new BufferedReader(file);
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

	//write to text file
	public static void writeTextFile(String fileName, String str) {
		BufferedWriter writer = null;
		try {
			writer = new BufferedWriter(new FileWriter(fileName));
			writer.write(str);
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			if (writer != null) {
				try {
					writer.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}

	}
	
	public void setResList(List<Resource> resourceList) {
		this.resList = resourceList;
	}

	public String getModelFile() {
		return fileName;
	}

	public void setModelFile(String modelFile) {
		this.fileName = modelFile;
	}

	public String getFileName() {
		return fileName;
	}

	public void setFileName(String fileName) {
		this.fileName = fileName;
	}

	public String getRemoteUrl() {
		return remoteUrl;
	}

	public void setRemoteUrl(String remoteUrl) {
		this.remoteUrl = remoteUrl;
	}

	public String getConsQueryFile() {
		return consQueryFile;
	}

	public void setConsQueryFile(String consQueryFile) {
		this.consQueryFile = consQueryFile;
	}

	public String getResQueryFile() {
		return resQueryFile;
	}

	public void setResQueryFile(String resQueryFile) {
		this.resQueryFile = resQueryFile;
	}

	public String getResName() {
		return resName;
	}

	public void setResName(String resName) {
		this.resName = resName;
	}

}
