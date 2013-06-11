package es.upm.dit.gsi.semantic.matching;

import java.util.HashMap;

import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;

import com.hp.hpl.jena.rdf.model.Property;
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
	
	public void initIndex(){
		
		indexer = new Indexer();
		indexer.getIndexWriter();
		repository.getModelFromLocal();
		repository.getModel().write(System.out);
		indexer.getIndexWriter();
		
		HashMap<String,Property> propertyMap = new HashMap<String,Property>();
		
		for(String field : config.getFieldMap().keySet()){
			Property p = repository.getModel().getProperty(config.getFieldURI(field));
			propertyMap.put(field, p);
		}
		
		for(Resource res : repository.getResList()){
			
			Document doc = new Document();
			doc.add(new Field("resURI", res.getURI(), Field.Store.YES, 
					Field.Index.NOT_ANALYZED_NO_NORMS));
			doc.add(new Field("category","it",Field.Store.YES,
					Field.Index.NOT_ANALYZED_NO_NORMS));
			
			for(String field : propertyMap.keySet()){
				Property property = propertyMap.get(field);
				String object = res.getProperty(property).getObject().toString();
				doc.add(new Field(field,object, Field.Store.YES,
						Field.Index.NOT_ANALYZED_NO_NORMS));
			}
			indexer.indexDocument(doc);	
		}
		
		indexer.closeIndexWriter();
	}
	
	public Repository getRepository() {
		return repository;
	}

	public void setRepository(Repository repository) {
		this.repository = repository;
	}
	
	public IndexConfig getConfig() {
		return config;
	}

	public void setConfig(IndexConfig config) {
		this.config = config;
	}
	
	public Indexer getIndexer() {
		return indexer;
	}

	public void setIndexer(Indexer indexer) {
		this.indexer = indexer;
	}

}
