package es.upm.dit.gsi.sematch.similarity;

public interface Similarity {
	
	public String getLabel();

	public double getWeight(); 
	
	public double getSimilarity(SimilarityConfig config);
	
}
