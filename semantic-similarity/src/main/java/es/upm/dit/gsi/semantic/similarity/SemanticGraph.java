package es.upm.dit.gsi.semantic.similarity;

import java.io.File;
import java.util.List;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.query.Query;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.query.ResultSet;

public class SemanticGraph{
	
	private Logger logger = Logger.getLogger(this.getClass());

	private Model model;
	private String modelFile;
	private String constructQuery;
	private String resourceQuery;
	private String resourceName;
	private List<Resource> resourceList;
	
	public Query getQuery(String queryFile){
		File file = new File(queryFile);
		return SparqlClient.getQueryFromFile(file);
	}
	
	public Model getModelFromLocal() {
		setModel(SemanticRepository.readFromXML(modelFile));
		return model;
	}
	
	public Model getModelFromRemote(){
		return model;
	}
	
	public Model getModelByConstruct(){
		setModel(SemanticRepository.readFromXML(modelFile));
		setModel(SparqlClient.executeConstructQuery(getQuery(constructQuery), model));
		return model;
	}
	
	public Model getModel(){
		return model;
	}

	public void setModel(Model model) {
		this.model = model;
	}
	

	public List<Resource> getResourceList() {
		ResultSet rset = SparqlClient.executeSelectQuery(getQuery(resourceQuery),getModel());
		setResourceList(SparqlClient.asResourceList(rset, resourceName));
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
