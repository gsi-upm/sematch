package es.upm.dit.gsi.semantic.similarity.measure;

import java.util.List;

import org.apache.log4j.Logger;

import es.upm.dit.gsi.semantic.similarity.Similarity;
import es.upm.dit.gsi.semantic.similarity.SimilarityConfig;

public class ClusterMeasure extends SimilarityMeasure {

	public Logger logger = Logger.getLogger(this.getClass());

	private List<Similarity> simCluster;

	public List<Similarity> getSimCluster() {
		return simCluster;
	}

	public void setSimCluster(List<Similarity> simCluster) {
		this.simCluster = simCluster;
	}

	@Override
	public double getSimilarity(SimilarityConfig config) {
		
		double similarity = 0;
		double childSim = 0;
		
		for (Similarity sim : simCluster) {
			childSim = sim.getSimilarity(config);
			similarity = similarity + childSim ;
		}
		//logger.info(label + " Weight: " + weight+ "	Sim: " + similarity);
		return similarity*getWeight();
	}

}
