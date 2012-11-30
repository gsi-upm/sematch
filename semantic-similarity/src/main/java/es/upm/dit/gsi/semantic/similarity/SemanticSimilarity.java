package es.upm.dit.gsi.semantic.similarity;

public class SemanticSimilarity {

	public static double simGanggao(int depth_1, int depth_2, int depth_common) {

		// information content values
		double ic_1 = Math.exp(-depth_1);
		double ic_2 = Math.exp(-depth_2);
		double ic_common = Math.exp(-depth_common);

		double distance_1_c = ic_common - ic_1;
		double distance_2_c = ic_common - ic_2;
		double distance_1_2 = distance_1_c + distance_2_c;

		return 1 - distance_1_2;
	}

}
