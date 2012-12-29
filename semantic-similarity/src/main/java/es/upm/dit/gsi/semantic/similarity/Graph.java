package es.upm.dit.gsi.semantic.similarity;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.List;

import org.apache.log4j.Logger;
import org.springframework.beans.factory.InitializingBean;

import com.hp.hpl.jena.query.Query;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;
import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.util.FileManager;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.query.ResultSet;

public class Graph implements InitializingBean{
	
	private Logger logger = Logger.getLogger(this.getClass());

	private String modelFile;
	private String constructQuery;
	private String resourceQuery;
	private String resourceName;
	private Model model;
	private List<Resource> resourceList;
	
	public Query getQuery(String queryFile){
		File file = new File(queryFile);
		return SparqlClient.getQueryFromFile(file);
	}
	
	public Property getProperty(String uri){
		return model.getProperty(uri);
	}
	
	public void writeAsXML(Model model, String fileName){
		
		File file = null;
		FileOutputStream out = null;
		try {
			file = new File(fileName);
			out = new FileOutputStream(file);
			if(!file.exists()){
				file.createNewFile();
			}
			model.write(out);
			out.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
	}
	
	public Model readFromXML(String fileName) {
		Model model = ModelFactory.createDefaultModel();
		InputStream in = FileManager.get().open(fileName);
		if (in == null) {
			throw new IllegalArgumentException("File: " + fileName
					+ " not found");
		}
		
		model.read(in, "");
		return model;
	}
	
	public Model readFromXML(InputStream in){
		Model model = ModelFactory.createDefaultModel();
		model.read(in, "");
		return model;
	}

	@Override
	public void afterPropertiesSet() throws Exception {
		logger.info("Initializing graph...");
		Model originalModel = readFromXML(modelFile);
		setModel(SparqlClient.executeConstructQuery(getQuery(constructQuery), originalModel));
		ResultSet rset = SparqlClient.executeSelectQuery(getQuery(resourceQuery),getModel());
		setResourceList(SparqlClient.asResourceList(rset, resourceName));
	}
	
	public Model getModel() {
		return model;
	}

	public void setModel(Model model) {
		this.model = model;
	}
	

	public List<Resource> getResourceList() {
		return resourceList;
	}

	public void setResourceList(List<Resource> resourceList) {
		this.resourceList = resourceList;
	}

	public String getResourceName() {
		return resourceName;
	}

	public void setResourceName(String resourceName) {
		this.resourceName = resourceName;
	}

	public String getModelFile() {
		return modelFile;
	}

	public void setModelFile(String modelFile) {
		this.modelFile = modelFile;
	}
	
	public String getConstructQuery() {
		return constructQuery;
	}

	public void setConstructQuery(String constructQuery) {
		this.constructQuery = constructQuery;
	}

	public String getResourceQuery() {
		return resourceQuery;
	}

	public void setResourceQuery(String resourceQuery) {
		this.resourceQuery = resourceQuery;
	}


}
