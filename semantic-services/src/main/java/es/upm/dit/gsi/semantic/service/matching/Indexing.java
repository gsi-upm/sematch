package es.upm.dit.gsi.semantic.service.matching;

import java.util.HashMap;

import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.store.Directory;


import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.ResIterator;
import com.hp.hpl.jena.rdf.model.Resource;

import es.upm.dit.gsi.semantic.search.IndexConfig;
import es.upm.dit.gsi.semantic.search.Indexer;
import es.upm.dit.gsi.semantic.similarity.Repository;



public class Indexing {
	
	private Indexer indexer;
	private IndexConfig config;
	private Repository repository;

	public Indexing(){
	}
	
	public void initRepository(){
		repository = new Repository();
		if(config.getType().equalsIgnoreCase("local")){
			repository.setFileName(config.getLocalFile());
			repository.getModelRDF();
		}else{
			//TODO:load from remote data center.
		}
	}
	
	//create a ram index from the model.
	public void createIndex(){
		
		initRepository();
		indexer = new Indexer();
		indexer.getIndexWriter();
		
		HashMap<String,Property> properties = new HashMap<String,Property>();
		
		for(String field : config.getFields()){
			Property p = repository.getModel().getProperty(config.getFieldURI(field));
			properties.put(field, p);
		}

		Property property = properties.get(config.getFields().get(0));
		ResIterator iterator = repository.getModel().listResourcesWithProperty(property);
		
		while(iterator.hasNext()){
			
			Resource res = iterator.nextResource();
			Document doc = new Document();
			doc.add(new Field("uri", res.getURI(), Field.Store.YES, 
					Field.Index.NOT_ANALYZED_NO_NORMS));
			doc.add(new Field("category","it",Field.Store.YES,
					Field.Index.NOT_ANALYZED_NO_NORMS));
			
			for(String field : properties.keySet()){
				String object = res.getProperty(properties.get(field)).getObject().toString();
				doc.add(new Field(field, object, Field.Store.YES, Field.Index.NOT_ANALYZED_NO_NORMS));
			}
			
			indexer.indexDocument(doc);
		}
		
		indexer.closeIndexWriter();
	}
	
	public void close(){
		indexer.closeDirectory();
	}
	
	public Directory getIndexDirecotry(){
		return indexer.getDirectory();
	}
	
	public IndexConfig getConfig() {
		return config;
	}

	public void setConfig(IndexConfig config) {
		this.config = config;
	}

}
