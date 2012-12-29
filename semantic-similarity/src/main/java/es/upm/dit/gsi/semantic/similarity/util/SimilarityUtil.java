package es.upm.dit.gsi.semantic.similarity.util;

import java.text.DecimalFormat;
import java.util.List;

import com.hp.hpl.jena.rdf.model.Resource;
import es.upm.dit.gsi.semantic.similarity.Similarity;

public class SimilarityUtil {

	private static final DecimalFormat simFormat = new DecimalFormat("0.0000");

	public static String format(double similarity) {
		return simFormat.format(similarity);
	}

	public static double getSimilarity(Resource query, Resource resource,
			List<Similarity> list) {
		double similarity = 0;
		for (Similarity sim : list) {
			similarity += sim.getSimilarity(query, resource) * sim.getWeight();
		}
		return similarity;
	}

	public static void printResult(List<Similarity> list) {
		for(Similarity sim : list){
			sim.printResult();
		}
	}

}
