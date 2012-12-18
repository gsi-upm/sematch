package es.upm.dit.gsi.semantic.similarity;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import es.upm.dit.gsi.semantic.similarity.SemanticSimilarity.SimilarityMethod;

public class Engine {

	// The concepts in a query
	private Map<String, String> queryConcepts = null;

	// The concepts of resources
	private Map<String, String> resourceConcepts = null;

	// initial the concepts
	public void loadConcepts() {

		queryConcepts = new HashMap<String, String>();
		resourceConcepts = new HashMap<String, String>();

	}

	//assign the concepts
	public void loadConcepts(Map<String, String> query,
			Map<String, String> resource) {
		this.queryConcepts = query;
		this.resourceConcepts = resource;
	}
	
	//calculate the similarity between query and resource
	public List<Double> computeSimilarity(SimilarityMethod method){
		
	
		return null;
	}

}
