package es.upm.dit.gsi.semantic.similarity;

import com.hp.hpl.jena.rdf.model.Resource;

import java.util.HashMap;
import java.util.Map;

import org.apache.log4j.Logger;

public class Engine {
	
	private Logger logger = Logger.getLogger(this.getClass());
	
	private SimilarityService similarityService;
	private SemanticGraph queryGraph;
	private SemanticGraph resourceGraph;
	private Map<String,Map<String,Double>> result;
 
	
	public Engine(){
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
			
			if(!result.containsKey(query.toString())){
				Map<String,Double> resourceMap = new HashMap<String,Double>();
				result.put(query.toString(), resourceMap);
			}
			
			for(Resource resource : getResourceGraph().getResourceList()){
				compute(query,resource);
			}
		}
	}
	
	public void print(){
		for(String query : result.keySet()){
			logger.info("Query: "+query);
			for(String resource : result.get(query).keySet()){
				logger.info("Resource: "+resource);
				logger.info("Similarity: "+result.get(query).get(resource).doubleValue());
			}
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

	public void compute(Resource query, Resource resource) {
		double similarity = similarityService.getSimilarity(query, resource);
		result.get(query.toString()).put(resource.toString(), new Double(similarity));
	}
	
	public SimilarityService getSimilarityService() {
		return similarityService;
	}

	public void setSimilarityService(SimilarityService similarityService) {
		this.similarityService = similarityService;
	}

}
