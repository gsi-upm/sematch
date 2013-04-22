package es.upm.dit.gsi.semantic.similarity.measure;

import java.util.List;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.rdf.model.Resource;
import es.upm.dit.gsi.semantic.similarity.Similarity;

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
	public double getSimilarity(Resource query, Resource resource) {
		
		double similarity = 0;
		double childSim = 0;
		for (Similarity sim : simCluster) {
			childSim = sim.getSimilarity(query, resource);
			similarity = similarity + childSim ;
		}
		logger.info(label + " Weight: " + weight+ "	Sim: " + similarity);
		return similarity*getWeight();
	}

}
