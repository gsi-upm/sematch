package es.upm.dit.gsi.sematch.similarity.compute;

public class StringSimCompute implements SimCompute {

	private boolean caseSensitive = false;

	@Override
	public double compute(String query, String resource) {
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

	public boolean isCaseSensitive() {
		return caseSensitive;
	}

	public void setCaseSensitive(boolean caseSensitive) {
		this.caseSensitive = caseSensitive;
	}

}
