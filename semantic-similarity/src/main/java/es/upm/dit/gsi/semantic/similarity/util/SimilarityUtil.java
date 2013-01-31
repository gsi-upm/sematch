package es.upm.dit.gsi.semantic.similarity.util;

import java.text.DecimalFormat;
import java.util.List;

import org.apache.log4j.Logger;

import com.hp.hpl.jena.rdf.model.Resource;
import es.upm.dit.gsi.semantic.similarity.Similarity;

public class SimilarityUtil {
	
	private static Logger logger = Logger.getLogger(SimilarityUtil.class);

	private static final DecimalFormat simFormat = new DecimalFormat("0.0000");

	public static String format(double similarity) {
		return simFormat.format(similarity);
	}

	public static double getSimilarity(Resource query, Resource resource,
			List<Similarity> list) {
		double similarity = 0;
		for (Similarity sim : list) {
			double childSim = sim.getSimilarity(query, resource);
			similarity = similarity + childSim ;
			logger.info(similarity);
		}
		return similarity;
	}

	
	public static double simGSI(int depth_1, int depth_2, int depth_common, double propertySim) {
		
		double similarity = 0;

		double description = propertySim+depth_1+depth_2;
		logger.info("description: "+description);
			
		double commonality = 2.0*depth_common;
			similarity = commonality / description;
		
		return similarity;

	}

	// milestone methods
	public static double simCGM(int depth_1, int depth_2, int depth_common) {

		// information content values
		
		double ic_1 = 1/Math.pow(2, depth_1);
		double ic_2 = 1/Math.pow(2, depth_2);
		double ic_common = 1/Math.pow(2, depth_common);

		double distance_1_c = ic_common - ic_1;
		double distance_2_c = ic_common - ic_2;
		
		double distance = 0;
		
		//if the resource is subclass of the query, the distance is 0
		if(depth_1 != depth_common)
			distance = distance_1_c + distance_2_c;

		return 1 - distance;
	}

	// Wu & Palm methods
	public static double simWuAndPalmer(int depth_1, int depth_2, int depth_common) {

		double common = 2.0 * depth_common;
		double fraction = depth_1 + depth_2;

		double sim = common/fraction ;

		return sim;
	}

	// Rada & Resnik
	public static double simRada(int depth_1, int depth_2, int depth_common, int maxDepth) {

		int distance1 = depth_1 - depth_common;
		int distance2 = depth_2 - depth_common;
		int path = distance1 + distance2;
		double distance = path / (2.0 * maxDepth);
		double sim = 1 - distance;

		return sim;
	}

	// Leacock & Chodorow
	// TODO:The similarity value is not located between 0 and 1. Need to be
	public static double simLeacockandChodorow(int depth_1, int depth_2,
			int depth_common, int maxDepth) {

		int distance1 = depth_1 - depth_common;
		int distance2 = depth_2 - depth_common;
		int path = distance1 + distance2;

		double sim = -Math.log(path / (2.0 * maxDepth));
		return sim;

	}

	// Li
	public static double simLi(int depth_1, int depth_2, int depth_common) {

		int distance1 = depth_1 - depth_common;
		int distance2 = depth_2 - depth_common;
		int path = distance1 + distance2;
		// System.out.println(depth_1+":"+depth_2+":"+depth_common);
		// System.out.println(path);
		double simpath = Math.exp(-path);
		// System.out.println(simpath);
		double simdepth_up = (Math.exp(depth_common) - Math.exp(-depth_common));
		double simdepth_down = (Math.exp(depth_common) + Math
				.exp(-depth_common));

		double simdepth = simdepth_up * simdepth_down;
		// System.out.println(simdepth);
		double result = simpath * simdepth;
		// System.out.println(result);
		return result;
	}

	


}
