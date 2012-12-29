package es.upm.dit.gsi.semantic.similarity;

import com.hp.hpl.jena.rdf.model.Resource;

public interface Similarity {
	
	public void printResult();
	
	public String getLabel();

	public double getWeight(); 
	
	public double getSimilarity(Resource query, Resource resource);
	
	
}
