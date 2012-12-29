package es.upm.dit.gsi.semantic.similarity.compute;

import com.hp.hpl.jena.rdf.model.Literal;
import com.hp.hpl.jena.rdf.model.RDFNode;

import es.upm.dit.gsi.semantic.similarity.SimilarityCompute;

public class NumericSimilarityCompute implements SimilarityCompute {

	private double deviation;
	private boolean downward;

	public boolean isDownward() {
		return downward;
	}

	public void setDownward(boolean downward) {
		this.downward = downward;
	}

	public double getDeviation() {
		return deviation;
	}

	public void setDeviation(double deviation) {
		this.deviation = deviation;
	}

	@Override
	public double computeSimilarity(RDFNode query, RDFNode resource) {
		Literal q = (Literal) query;
		Literal r = (Literal) resource;
		return numericSimilarity(q.getDouble(), r.getDouble());
	}

	private double numericSimilarity(double value_1, double value_2) {

		switch (Double.compare(value_1, value_2)) {

		// v1 = v2
		case 0:
			return 1;
			// v1 > v2
		case 1:
			if (isDownward()) {
				if ((value_1 - value_2) > value_1 * deviation) {
					return 0;
				} else {
					return (1 - ((value_1 - value_2) / (value_1 * deviation)));
				}

			} else {
				return 1;
			}
			// v1 < v2
		case -1:
			if (isDownward()) {
				return 1;
			} else {
				if ((value_2 - value_1) > value_1 * deviation) {
					return 0;
				} else {
					return (1 - ((value_2 - value_1) / (value_1 * deviation)));
				}
			}
		}

		return 0;
	}

}
