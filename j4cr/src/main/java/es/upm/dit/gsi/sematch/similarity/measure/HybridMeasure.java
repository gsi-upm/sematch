package es.upm.dit.gsi.sematch.similarity.measure;

import es.upm.dit.gsi.sematch.similarity.Similarity;
import es.upm.dit.gsi.sematch.similarity.SimilarityConfig;

public class HybridMeasure extends SimilarityMeasure {
	
	private Similarity concept;
	private Similarity property;
	
	@Override
	public double getSimilarity(SimilarityConfig config) {
		
		double similarity = 0;
		double simConcept = concept.getSimilarity(config);
		double simProperty = property.getSimilarity(config);
		
		similarity = simConcept + simProperty;
		
		return similarity*getWeight();
	}
	
	public Similarity getConcept() {
		return concept;
	}

	public void setConcept(Similarity concept) {
		this.concept = concept;
	}

	public Similarity getProperty() {
		return property;
	}

	public void setProperty(Similarity property) {
		this.property = property;
	}
	
}
