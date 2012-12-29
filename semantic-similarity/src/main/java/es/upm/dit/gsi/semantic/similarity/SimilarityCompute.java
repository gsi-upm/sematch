package es.upm.dit.gsi.semantic.similarity;

import com.hp.hpl.jena.rdf.model.RDFNode;

public interface SimilarityCompute {
	public double computeSimilarity(RDFNode query, RDFNode resource);
}
