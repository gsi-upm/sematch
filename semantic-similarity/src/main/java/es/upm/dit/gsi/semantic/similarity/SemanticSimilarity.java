package es.upm.dit.gsi.semantic.similarity;

import java.net.URI;
import java.net.URISyntaxException;
import java.text.DecimalFormat;

public class SemanticSimilarity {
	
	private static final DecimalFormat simFormat = new DecimalFormat("0.0000"); 

	public enum SimilarityMethod {
		CGM, WuAndPalm, Rada, LeacockAndChodorow, Li
	}

	private static int Max_Depth = 5;

	public static void setMaxDepth(int depth) {
		Max_Depth = depth;
	}

	public static int getMaxDepth() {
		return Max_Depth;
	}

	public static String computeSimilarity(SimilarityMethod method,
			String concept_1, String concept_2) {

		int depth_1 = getDepth(concept_1);
		int depth_2 = getDepth(concept_2);
		int depth_c = getCommonDepth(concept_1, concept_2);

		double similarity = computeConceptSimilarity(method, depth_1, depth_2,
				depth_c);
		//return similarity;
		return simFormat.format(similarity);
	}

	public static double computeConceptSimilarity(SimilarityMethod method,
			int depth_1, int depth_2, int depth_common) {

		double similarity = 0;

		switch (method) {
		case CGM:
			similarity = simCGM(depth_1, depth_2, depth_common);
			break;
		case WuAndPalm:
			similarity = simWuAndPalmer(depth_1, depth_2, depth_common);
			break;
		case Rada:
			similarity = simRada(depth_1, depth_2, depth_common);
			break;
		case LeacockAndChodorow:
			similarity = simLeacockandChodorow(depth_1, depth_2, depth_common);
			break;
		case Li:
			similarity = simLi(depth_1, depth_2, depth_common);
			break;
		}
		return similarity;
	}

	// milestone methods
	private static double simCGM(int depth_1, int depth_2, int depth_common) {

		// information content values
		double ic_1 = Math.exp(-depth_1);
		double ic_2 = Math.exp(-depth_2);
		double ic_common = Math.exp(-depth_common);

		double distance_1_c = ic_common - ic_1;
		double distance_2_c = ic_common - ic_2;
		double distance_1_2 = distance_1_c + distance_2_c;

		return 1 - distance_1_2;
	}

	// Wu & Palm methods
	private static double simWuAndPalmer(int depth_1, int depth_2,
			int depth_common) {

		int Na = depth_1 - depth_common;
		int Nb = depth_2 - depth_common;
		
		double Nc = 2.0*depth_common;
		double fraction_down = Na+Nb+Nc;
		
		double sim = Nc / fraction_down;

		return sim;
	}

	// Rada & Resnik
	private static double simRada(int depth_1, int depth_2,
			int depth_common) {

		int distance1 = depth_1 - depth_common;
		int distance2 = depth_2 - depth_common;
		int path = distance1 + distance2;
		double distance = path/(2.0*Max_Depth);
		double sim = 1 - distance;

		return sim;
	}

	// Leacock & Chodorow
	//TODO:The similarity value is not located between 0 and 1.
	private static double simLeacockandChodorow(int depth_1, int depth_2,
			int depth_common) {

		int distance1 = depth_1 - depth_common;
		int distance2 = depth_2 - depth_common;
		int path = distance1 + distance2;

		double sim = -Math.log(path / (2.0 * Max_Depth));
		return sim;

	}

	// Li
	private static double simLi(int depth_1, int depth_2, int depth_common) {

		int distance1 = depth_1 - depth_common;
		int distance2 = depth_2 - depth_common;
		int path = distance1 + distance2;
		//System.out.println(depth_1+":"+depth_2+":"+depth_common);
		//System.out.println(path);
		double simpath = Math.exp(-path);
		//System.out.println(simpath);
		double simdepth_up = (Math.exp(depth_common) - Math.exp(-depth_common));
		double simdepth_down = (Math.exp(depth_common) + Math
				.exp(-depth_common));
		
		double simdepth = simdepth_up * simdepth_down;
		//System.out.println(simdepth);
		double result = simpath * simdepth;
		//System.out.println(result);
		return result;
	}

	// return the depth of the least common ancestor of two concepts
	public static int getCommonDepth(String URI_1, String URI_2) {

		char[] concept_1 = parseURI(URI_1).toCharArray();
		char[] concept_2 = parseURI(URI_2).toCharArray();

		int depth_1 = concept_1.length;
		int depth_2 = concept_2.length;

		int common = 0;

		if (depth_1 >= depth_2) {
			for (int i = 0; i < depth_2; i++) {
				if (concept_1[i] != concept_2[i]) {
					common = i;
					return common;
				}
			}
			common = depth_2;
		} else {
			for (int i = 0; i < depth_1; i++) {
				if (concept_1[i] != concept_2[i]) {
					common = i;
					return common;
				}
			}
			common = depth_1;
		}

		return common;
	}

	// return the depth of a node in the taxonomy
	public static int getDepth(String uri) {
		return parseURI(uri).length();
	}

	// extract the fragment of a URI
	public static String parseURI(String nURI) {
		String fragment = null;
		try {
			URI uri = new URI(nURI);
			fragment = uri.getFragment();
		} catch (URISyntaxException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return fragment;
	}
	

}
