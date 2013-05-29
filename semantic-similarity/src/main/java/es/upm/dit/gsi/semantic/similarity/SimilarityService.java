package es.upm.dit.gsi.semantic.similarity;

import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;

public class SimilarityService {

	public Logger logger = Logger.getLogger(this.getClass());
	
	private List<Similarity> simMeasures;

	private SimilarityConfig config;
	
	public SimilarityService(){
		config = new SimilarityConfig();
	}

	public float getSimilarity(Map<String,String> query, Map<String,String> resource){
		config.setQuery(query);
		config.setResource(resource);
		Double sim = getSimilarity(config);
		return sim.floatValue();
	}
	
	public double getSimilarity(SimilarityConfig config) {
		double similarity = 0;
		for (Similarity sim : simMeasures) {
			double childSim = sim.getSimilarity(config);
			similarity = similarity + childSim ;
		}
		return similarity;
	}
	
	public List<Similarity> getSimMeasures() {
		return simMeasures;
	}

	public void setSimMeasures(List<Similarity> simMeasures) {
		this.simMeasures = simMeasures;
	}

}
