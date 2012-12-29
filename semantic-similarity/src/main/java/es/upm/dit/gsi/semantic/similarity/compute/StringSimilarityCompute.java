package es.upm.dit.gsi.semantic.similarity.compute;

import com.hp.hpl.jena.rdf.model.RDFNode;

import es.upm.dit.gsi.semantic.similarity.SimilarityCompute;

public class StringSimilarityCompute implements SimilarityCompute {

	private boolean caseSensitive;

	public boolean isCaseSensitive() {
		return caseSensitive;
	}

	public void setCaseSensitive(boolean caseSensitive) {
		this.caseSensitive = caseSensitive;
	}

	@Override
	public double computeSimilarity(RDFNode query, RDFNode resource) {
		return stringSimilarity(query.toString(), resource.toString());
	}

	private double stringSimilarity(String query, String resource) {

		int similarity;

		if (!isCaseSensitive()) {
			similarity = query.compareToIgnoreCase(resource);
		} else {
			similarity = query.compareTo(resource);
		}

		if (similarity == 0) {
			return 1.0;
		} else {
			return 0;
		}
	}

}
