package es.upm.dit.gsi.semantic.similarity;

import com.hp.hpl.jena.rdf.model.Resource;

import es.upm.dit.gsi.semantic.similarity.taxonomy.Taxonomy;

import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;

import org.apache.log4j.Logger;

public class MatchEngine {
	
	private Logger logger = Logger.getLogger(this.getClass());
	
	private SimilarityService similarityService;
	private SemanticGraph queryGraph;
	private SemanticGraph resourceGraph;
	private Map<String,Map<String,Double>> result;
	
 
	
	public MatchEngine(){
		result = new HashMap<String,Map<String,Double>>();
	}
	
	public void init(){
		logger.info("initiation...");
		queryGraph.getModelByConstruct();
		resourceGraph.getModelByConstruct();
	}
	
	public void execute(){
		logger.info("Executing...");
		for(Resource query : getQueryGraph().getResourceList()){
			
			if(!result.containsKey(Taxonomy.parseURI(query.toString()))){
				Map<String,Double> resourceMap = new HashMap<String,Double>();
				result.put(Taxonomy.parseURI(query.toString()), resourceMap);
			}
			
			for(Resource resource : getResourceGraph().getResourceList()){
				compute(query,resource);
			}
		}
	}
	
	public void compute(Resource query, Resource resource) {
		double similarity = similarityService.getSimilarity(query, resource);
		result.get(Taxonomy.parseURI(query.toString())).
		put(Taxonomy.parseURI(resource.toString()), new Double(similarity));
	}
	
	public void print(){
		
		for(String query : result.keySet()){
			logger.info("Query: "+query);
			SimilarityComparator comparator =  new SimilarityComparator(result.get(query));
		    TreeMap<String,Double> sorted = new TreeMap<String,Double>(comparator);
		    sorted.putAll(result.get(query));
		    System.out.println(sorted);
		}
	}
	
	public SemanticGraph getQueryGraph() {
		return queryGraph;
	}

	public void setQueryGraph(SemanticGraph queryGraph) {
		this.queryGraph = queryGraph;
	}

	public SemanticGraph getResourceGraph() {
		return resourceGraph;
	}

	public void setResourceGraph(SemanticGraph resourceGraph) {
		this.resourceGraph = resourceGraph;
	}

	public SimilarityService getSimilarityService() {
		return similarityService;
	}

	public void setSimilarityService(SimilarityService similarityService) {
		this.similarityService = similarityService;
	}
	
	class SimilarityComparator implements Comparator<String> {

	    Map<String, Double> base;
	    public SimilarityComparator(Map<String, Double> base) {
	        this.base = base;
	    }

	    // Descending order 
	    public int compare(String a, String b) {
	        if (base.get(a) >= base.get(b)) {
	            return -1;
	        } else {
	            return 1;
	        } 
	    }
	}

}
