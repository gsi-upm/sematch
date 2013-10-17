package es.upm.dit.gsi.semantic.similarity.measure;

import org.apache.log4j.Logger;

import es.upm.dit.gsi.semantic.similarity.SimilarityConfig;
import es.upm.dit.gsi.semantic.similarity.compute.SimCompute;

public class AtomicMeasure extends SimilarityMeasure {

	private Logger logger = Logger.getLogger(this.getClass());

	protected SimCompute simCompute;

	@Override
	public double getSimilarity(SimilarityConfig config) {

		String query = config.getQuery(label).toString();
		String resource = config.getResource(label).toString();
		double similarity = simCompute.compute(query, resource);
		//logger.info(query+"\n"+resource);
		//logger.info(label + " Weight: " + weight+ "	Sim: " + similarity);
		return similarity*getWeight();
	}
	
	public SimCompute getSimCompute() {
		return simCompute;
	}

	public void setSimCompute(SimCompute simCompute) {
		this.simCompute = simCompute;
	}

}
