package es.upm.dit.gsi.semantic.similarity.compute;

import java.net.URI;
import java.net.URISyntaxException;
import com.hp.hpl.jena.rdf.model.Model;

import es.upm.dit.gsi.semantic.similarity.type.SimilarityMethod;

public class TaxonomySimilarityCompute {

	private int maxDepth = 5;
	private SimilarityMethod methodType;
	private Model taxonomy;
	
	public int getMaxDepth() {
		return maxDepth;
	}

	public void setMaxDepth(int maxDepth) {
		this.maxDepth = maxDepth;
	}

	public SimilarityMethod getMethodType() {
		return methodType;
	}

	public void setMethodType(SimilarityMethod methodType) {
		this.methodType = methodType;
	}

	public Model getTaxonomy() {
		return taxonomy;
	}

	public void setTaxonomy(Model taxonomy) {
		this.taxonomy = taxonomy;
	}


	public double computeSimilarity(Object query, Object resource) {

		int depth_1 = getDepth((String) query);
		int depth_2 = getDepth((String) resource);
		int depth_c = getCommonDepth((String) query, (String) resource);

		return computeConceptSimilarity(depth_1, depth_2, depth_c);
	}

	public double computeConceptSimilarity(int depth_1, int depth_2, int depth_common) {

		double similarity = 0;

		switch (methodType) {
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
		case GSI:
			similarity = simGSI(depth_1, depth_2, depth_common);
			break;
		}
		return similarity;
	}

	// Our proposed method based on commonality and differences without combine
	// property similarity
	private double simGSI(int depth_1, int depth_2, int depth_common) {

		int distance1 = depth_1 - depth_common;
		int distance2 = depth_2 - depth_common;
		int path = distance1 + distance2;

		double commonality = Math.log(depth_common);

		double difference = 0;

		if (path != 0)
			difference = Math.log(path);

		double similarity = commonality / (difference + commonality);

		return similarity;

	}

	// milestone methods
	private double simCGM(int depth_1, int depth_2, int depth_common) {

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
	private double simWuAndPalmer(int depth_1, int depth_2, int depth_common) {

		int Na = depth_1 - depth_common;
		int Nb = depth_2 - depth_common;

		double Nc = 2.0 * depth_common;
		double fraction_down = Na + Nb + Nc;

		double sim = Nc / fraction_down;

		return sim;
	}

	// Rada & Resnik
	private double simRada(int depth_1, int depth_2, int depth_common) {

		int distance1 = depth_1 - depth_common;
		int distance2 = depth_2 - depth_common;
		int path = distance1 + distance2;
		double distance = path / (2.0 * maxDepth);
		double sim = 1 - distance;

		return sim;
	}

	// Leacock & Chodorow
	// TODO:The similarity value is not located between 0 and 1. Need to be
	private double simLeacockandChodorow(int depth_1, int depth_2,
			int depth_common) {

		int distance1 = depth_1 - depth_common;
		int distance2 = depth_2 - depth_common;
		int path = distance1 + distance2;

		double sim = -Math.log(path / (2.0 * maxDepth));
		return sim;

	}

	// Li
	private double simLi(int depth_1, int depth_2, int depth_common) {

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

	// return the depth of the least common ancestor of two concepts
	public int getCommonDepth(String URI_1, String URI_2) {

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
	public int getDepth(String uri) {
		return parseURI(uri).length();
	}

	// extract the fragment of a URI
	public String parseURI(String nURI) {
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
